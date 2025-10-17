from dotenv import load_dotenv
load_dotenv()

import redis
import hashlib
import os

class RedisAuth:
    def __init__(self):
        """Inicializa a conexão com Redis"""
        # Configuração do Redis
        # Para Redis local use: host='localhost', port=6379
        # Para Redis Cloud/Upstash use a URL fornecida
        
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_password = os.getenv('REDIS_PASSWORD', None)
        
        try:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            
            # Testar conexão
            self.redis_client.ping()
            print("✅ Conectado ao Redis com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao conectar ao Redis: {e}")
            raise
    
    def _hash_password(self, password):
        """
        Gera hash SHA256 da senha
        
        Args:
            password (str): Senha em texto plano
            
        Returns:
            str: Hash da senha
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password):
        """
        Registra um novo usuário no Redis
        
        Args:
            username (str): Nome de usuário
            password (str): Senha do usuário
            
        Returns:
            bool: True se registrado com sucesso, False se usuário já existe
        """
        try:
            # Verificar se usuário já existe
            if self.redis_client.exists(f"user:{username}"):
                print(f"⚠️ Usuário '{username}' já existe")
                return False
            
            # Hash da senha
            password_hash = self._hash_password(password)
            
            # Salvar no Redis com chave "user:username"
            self.redis_client.set(f"user:{username}", password_hash)
            print(f"✅ Usuário '{username}' registrado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao registrar usuário: {e}")
            return False
    
    def authenticate(self, username, password):
        """
        Autentica um usuário
        
        Args:
            username (str): Nome de usuário
            password (str): Senha do usuário
            
        Returns:
            bool: True se autenticado, False caso contrário
        """
        try:
            # Buscar hash da senha armazenado
            stored_hash = self.redis_client.get(f"user:{username}")
            
            if not stored_hash:
                print(f"⚠️ Usuário '{username}' não encontrado")
                return False
            
            # Comparar hash da senha fornecida com o armazenado
            password_hash = self._hash_password(password)
            
            if password_hash == stored_hash:
                print(f"✅ Usuário '{username}' autenticado com sucesso!")
                return True
            else:
                print(f"❌ Senha incorreta para usuário '{username}'")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao autenticar usuário: {e}")
            return False
    
    def delete_user(self, username):
        """
        Remove um usuário do Redis
        
        Args:
            username (str): Nome de usuário
            
        Returns:
            bool: True se removido, False caso contrário
        """
        try:
            result = self.redis_client.delete(f"user:{username}")
            
            if result > 0:
                print(f"✅ Usuário '{username}' removido com sucesso!")
                return True
            else:
                print(f"⚠️ Usuário '{username}' não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao remover usuário: {e}")
            return False
    
    def user_exists(self, username):
        """
        Verifica se um usuário existe
        
        Args:
            username (str): Nome de usuário
            
        Returns:
            bool: True se existe, False caso contrário
        """
        try:
            return self.redis_client.exists(f"user:{username}") > 0
        except Exception as e:
            print(f"❌ Erro ao verificar usuário: {e}")
            return False
    
    def list_users(self):
        """
        Lista todos os usuários cadastrados
        
        Returns:
            list: Lista de usernames
        """
        try:
            # Buscar todas as chaves que começam com "user:"
            keys = self.redis_client.keys("user:*")
            # Extrair usernames removendo o prefixo "user:"
            usernames = [key.replace("user:", "") for key in keys]
            print(f"✅ {len(usernames)} usuário(s) encontrado(s)")
            return usernames
        except Exception as e:
            print(f"❌ Erro ao listar usuários: {e}")
            return []
    
    def close_connection(self):
        """Fecha a conexão com Redis"""
        try:
            self.redis_client.close()
            print("✅ Conexão com Redis fechada")
        except Exception as e:
            print(f"❌ Erro ao fechar conexão: {e}")
    
    def __del__(self):
        """Destrutor para garantir que a conexão seja fechada"""
        try:
            self.close_connection()
        except:
            pass