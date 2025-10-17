import streamlit as st
from database import MongoDBManager
from auth import RedisAuth
from cryptography.fernet import Fernet
import os

# Configuração da página
st.set_page_config(
    page_title="Gerenciador de Senhas",
    page_icon="🔐",
    layout="wide"
)

# Inicializar gerenciadores
@st.cache_resource
def init_managers():
    mongo = MongoDBManager()
    redis_auth = RedisAuth()
    return mongo, redis_auth

mongo_manager, redis_auth = init_managers()

# Função para criptografar senha
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

# Função para descriptografar senha
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

# Inicializar session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'encryption_key' not in st.session_state:
    st.session_state.encryption_key = None

# Página de Login
def login_page():
    st.title("🔐 Gerenciador de Senhas")
    st.subheader("Login")
    
    tab1, tab2 = st.tabs(["Entrar", "Registrar"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if username and password:
                    if redis_auth.authenticate(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        # Gerar chave de criptografia baseada no usuário
                        st.session_state.encryption_key = Fernet.generate_key()
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos!")
                else:
                    st.warning("Preencha todos os campos!")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Novo Usuário")
            new_password = st.text_input("Nova Senha", type="password")
            confirm_password = st.text_input("Confirmar Senha", type="password")
            register = st.form_submit_button("Registrar")
            
            if register:
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        if redis_auth.register(new_username, new_password):
                            st.success("Usuário registrado com sucesso! Faça login.")
                        else:
                            st.error("Usuário já existe!")
                    else:
                        st.error("As senhas não conferem!")
                else:
                    st.warning("Preencha todos os campos!")

# Página Principal
def main_page():
    st.title(f"🔐 Gerenciador de Senhas - Bem-vindo, {st.session_state.username}!")
    
    # Botão de Logout
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Sair"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.encryption_key = None
            st.rerun()
    
    # Menu de operações
    menu = st.sidebar.selectbox(
        "Menu",
        ["📋 Listar Senhas", "➕ Adicionar Senha", "✏️ Editar Senha", "🗑️ Excluir Senha"]
    )
    
    if menu == "📋 Listar Senhas":
        list_passwords()
    elif menu == "➕ Adicionar Senha":
        add_password()
    elif menu == "✏️ Editar Senha":
        edit_password()
    elif menu == "🗑️ Excluir Senha":
        delete_password()

# Listar todas as senhas
def list_passwords():
    st.header("📋 Minhas Senhas Armazenadas")
    
    passwords = mongo_manager.list_passwords(st.session_state.username)
    
    if passwords:
        st.info(f"Total de senhas armazenadas: {len(passwords)}")
        
        for idx, pwd in enumerate(passwords, 1):
            with st.expander(f"🔑 {pwd['nome']} (ID: {pwd['_id']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Nome:** {pwd['nome']}")
                    st.write(f"**Usuário:** {st.session_state.username}")
                with col2:
                    # Mostrar senha ofuscada com opção de revelar
                    if st.button(f"👁️ Mostrar Senha", key=f"show_{idx}"):
                        try:
                            decrypted = decrypt_password(pwd['senha'], st.session_state.encryption_key)
                            st.code(decrypted)
                        except:
                            st.code(pwd['senha'])
                    else:
                        st.code("••••••••")
    else:
        st.warning("Nenhuma senha cadastrada ainda.")

# Adicionar nova senha
def add_password():
    st.header("➕ Adicionar Nova Senha")
    
    with st.form("add_form"):
        nome = st.text_input("Nome/Serviço (ex: Gmail, Facebook)")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("💾 Salvar")
        
        if submit:
            if nome and senha:
                # Criptografar senha antes de salvar
                encrypted = encrypt_password(senha, st.session_state.encryption_key)
                
                result = mongo_manager.create_password(
                    st.session_state.username,
                    nome,
                    encrypted
                )
                
                if result:
                    st.success(f"✅ Senha para '{nome}' adicionada com sucesso!")
                    st.balloons()
                else:
                    st.error("Erro ao adicionar senha.")
            else:
                st.warning("⚠️ Preencha todos os campos!")

# Editar senha existente
def edit_password():
    st.header("✏️ Editar Senha")
    
    passwords = mongo_manager.list_passwords(st.session_state.username)
    
    if passwords:
        # Criar dicionário para seleção
        pwd_dict = {f"{pwd['nome']} (ID: {pwd['_id']})": pwd for pwd in passwords}
        
        selected = st.selectbox("Selecione a senha para editar:", list(pwd_dict.keys()))
        
        if selected:
            pwd = pwd_dict[selected]
            
            with st.form("edit_form"):
                novo_nome = st.text_input("Novo Nome/Serviço", value=pwd['nome'])
                nova_senha = st.text_input("Nova Senha", type="password")
                submit = st.form_submit_button("💾 Atualizar")
                
                if submit:
                    if novo_nome and nova_senha:
                        # Criptografar nova senha
                        encrypted = encrypt_password(nova_senha, st.session_state.encryption_key)
                        
                        result = mongo_manager.update_password(
                            pwd['_id'],
                            novo_nome,
                            encrypted
                        )
                        
                        if result:
                            st.success(f"✅ Senha atualizada com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar senha.")
                    else:
                        st.warning("⚠️ Preencha todos os campos!")
    else:
        st.info("Nenhuma senha cadastrada para editar.")

# Excluir senha
def delete_password():
    st.header("🗑️ Excluir Senha")
    
    passwords = mongo_manager.list_passwords(st.session_state.username)
    
    if passwords:
        pwd_dict = {f"{pwd['nome']} (ID: {pwd['_id']})": pwd for pwd in passwords}
        
        selected = st.selectbox("Selecione a senha para excluir:", list(pwd_dict.keys()))
        
        if selected:
            pwd = pwd_dict[selected]
            
            st.warning(f"⚠️ Tem certeza que deseja excluir a senha de '{pwd['nome']}'?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Sim, excluir", type="primary"):
                    result = mongo_manager.delete_password(pwd['_id'])
                    if result:
                        st.success("Senha excluída com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao excluir senha.")
            with col2:
                if st.button("❌ Cancelar"):
                    st.info("Operação cancelada.")
    else:
        st.info("Nenhuma senha cadastrada para excluir.")

# Controle de fluxo da aplicação
if st.session_state.logged_in:
    main_page()
else:
    login_page()