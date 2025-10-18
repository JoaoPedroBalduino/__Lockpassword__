# 🔐 Gerenciador de Senhas - MongoDB + Redis + Streamlit

Sistema completo de gerenciamento de senhas desenvolvido em Python com interface web usando Streamlit, autenticação via Redis e armazenamento no MongoDB Atlas.


## 🎥 Vídeo Explicativo

Assista ao vídeo no YouTube explicando o projeto:  
[![Miniatura do Vídeo](<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/121f092a-70b5-4398-b950-932c01f617ab" />
)](https://www.youtube.com/watch?v=KGwS9bf6dFI&t=95s)


## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Operações CRUD](#operações-crud)
- [Segurança](#segurança)
- [Vídeo Demonstrativo](#vídeo-demonstrativo)
- [Autor](#autor)

## 📖 Sobre o Projeto

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de **Banco de Dados Avançados** do curso de Engenharia de Software. O objetivo é demonstrar a integração entre linguagens de programação e bancos de dados NoSQL (MongoDB) e in-memory (Redis).

## ✨ Funcionalidades

### Sistema de Autenticação (Redis)
- ✅ Registro de novos usuários
- ✅ Login com validação de credenciais
- ✅ Senha com hash SHA256
- ✅ Sessão persistente

### Gerenciamento de Senhas (MongoDB)
- ✅ **CREATE**: Adicionar novas senhas
- ✅ **READ**: Listar todas as senhas do usuário
- ✅ **UPDATE**: Editar senhas existentes
- ✅ **DELETE**: Excluir senhas

### Segurança
- 🔒 Criptografia de senhas com Fernet (symmetric encryption)
- 🔒 Hash de senhas de autenticação com SHA256
- 🔒 Senhas não são exibidas por padrão (ofuscadas)

### Interface
- 🎨 Interface web moderna e intuitiva com Streamlit
- 📱 Layout responsivo
- 🎭 Ícones e emojis para melhor UX
- 🎉 Feedback visual para ações do usuário

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework para interface web
- **MongoDB Atlas** - Banco de dados NoSQL em nuvem
- **Redis** - Banco de dados in-memory para autenticação
- **PyMongo** - Driver Python para MongoDB
- **Redis-py** - Cliente Python para Redis
- **Cryptography** - Biblioteca para criptografia

## 📦 Pré-requisitos

Antes de começar, você precisa ter instalado:

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Conta no MongoDB Atlas (gratuita)
- Redis instalado localmente OU conta no Redis Cloud (gratuita)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/gerenciador-senhas-mongodb.git
cd gerenciador-senhas-mongodb
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. MongoDB Atlas

1. Acesse [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crie uma conta gratuita (se não tiver)
3. Crie um novo cluster
4. Configure o acesso à rede (IP Address: 0.0.0.0/0 para permitir de qualquer lugar)
5. Crie um usuário do banco de dados
6. Obtenha a string de conexão (Connection String)

### 2. Redis

**Opção A: Redis Local**
```bash
# Windows (usando Chocolatey)
choco install redis-64

# Linux (Ubuntu/Debian)
sudo apt-get install redis-server
sudo service redis-server start

# Mac (usando Homebrew)
brew install redis
brew services start redis
```

**Opção B: Redis Cloud**
1. Acesse [Redis Cloud](https://redis.com/try-free/)
2. Crie uma conta gratuita
3. Crie um banco de dados
4. Obtenha o host, porta e senha

### 3. Arquivo de Configuração

Crie um arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/?retryWrites=true&w=majority

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

## ▶️ Como Executar

### 1. Certifique-se de que o Redis está rodando

```bash
# Testar conexão com Redis
redis-cli ping
# Deve retornar: PONG
```

### 2. Execute a aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
gerenciador-senhas-mongodb/
│
├── app.py                 # Aplicação principal (Interface Streamlit)
├── database.py            # Gerenciador MongoDB (CRUD)
├── auth.py                # Autenticação Redis
├── requirements.txt       # Dependências do projeto
├── .env.example          # Exemplo de variáveis de ambiente
├── .env                  # Suas configurações (não commitado)
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

## 🔄
