from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

class MongoDBManager:
    def __init__(self):
        """Inicializa a conexão com MongoDB Atlas"""
        # URL de conexão do MongoDB Atlas
        # Substitua pela sua URL do MongoDB Atlas
        self.connection_string = os.getenv(
            'MONGODB_URI',
            'mongodb+srv://<usuario>:<senha>@cluster.mongodb.net/?retryWrites=true&w=majority'
        )
        
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client['gerenciador_senhas']
            self.collection = self.collection = self.db['senhas']
            
            # Testar conexão
            self.client.server_info()
            print("✅ Conectado ao MongoDB Atlas com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao conectar ao MongoDB: {e}")
            raise
    
    def create_password(self, usuario, nome, senha):
        """
        CREATE - Insere uma nova senha no banco
        
        Args:
            usuario (str): Nome do usuário dono da senha
            nome (str): Nome/serviço da senha
            senha (str): Senha criptografada
            
        Returns:
            str: ID do documento inserido ou None em caso de erro
        """
        try:
            documento = {
                'usuario': usuario,
                'nome': nome,
                'senha': senha,
                'data_criacao': datetime.now(),
                'data_atualizacao': datetime.now()
            }
            
            resultado = self.collection.insert_one(documento)
            print(f"✅ Senha cadastrada com ID: {resultado.inserted_id}")
            return str(resultado.inserted_id)
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar senha: {e}")
            return None
    
    def list_passwords(self, usuario):
        """
        READ - Lista todas as senhas de um usuário
        
        Args:
            usuario (str): Nome do usuário
            
        Returns:
            list: Lista de documentos (senhas)
        """
        try:
            senhas = list(self.collection.find({'usuario': usuario}))
            
            # Converter ObjectId para string para exibição
            for senha in senhas:
                senha['_id'] = str(senha['_id'])
            
            print(f"✅ {len(senhas)} senha(s) encontrada(s) para o usuário {usuario}")
            return senhas
            
        except Exception as e:
            print(f"❌ Erro ao listar senhas: {e}")
            return []
    
    def get_password_by_id(self, password_id):
        """
        READ - Busca uma senha específica por ID
        
        Args:
            password_id (str): ID da senha
            
        Returns:
            dict: Documento da senha ou None
        """
        try:
            senha = self.collection.find_one({'_id': ObjectId(password_id)})
            
            if senha:
                senha['_id'] = str(senha['_id'])
                print(f"✅ Senha encontrada: {senha['nome']}")
                return senha
            else:
                print(f"⚠️ Senha com ID {password_id} não encontrada")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao buscar senha: {e}")
            return None
    
    def update_password(self, password_id, novo_nome, nova_senha):
        """
        UPDATE - Atualiza uma senha existente
        
        Args:
            password_id (str): ID da senha a ser atualizada
            novo_nome (str): Novo nome/serviço
            nova_senha (str): Nova senha criptografada
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        try:
            resultado = self.collection.update_one(
                {'_id': ObjectId(password_id)},
                {
                    '$set': {
                        'nome': novo_nome,
                        'senha': nova_senha,
                        'data_atualizacao': datetime.now()
                    }
                }
            )
            
            if resultado.modified_count > 0:
                print(f"✅ Senha atualizada com sucesso!")
                return True
            else:
                print(f"⚠️ Nenhuma senha foi modificada (ID pode não existir)")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao atualizar senha: {e}")
            return False
    
    def delete_password(self, password_id):
        """
        DELETE - Remove uma senha do banco
        
        Args:
            password_id (str): ID da senha a ser removida
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        try:
            resultado = self.collection.delete_one({'_id': ObjectId(password_id)})
            
            if resultado.deleted_count > 0:
                print(f"✅ Senha excluída com sucesso!")
                return True
            else:
                print(f"⚠️ Nenhuma senha foi excluída (ID pode não existir)")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao excluir senha: {e}")
            return False
    
    def close_connection(self):
        """Fecha a conexão com o MongoDB"""
        try:
            self.client.close()
            print("✅ Conexão com MongoDB fechada")
        except Exception as e:
            print(f"❌ Erro ao fechar conexão: {e}")
    
    def __del__(self):
        """Destrutor para garantir que a conexão seja fechada"""
        self.close_connection()