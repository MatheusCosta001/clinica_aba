# 🧩 Clínica ABA - Sistema Web de Gerenciamento

**Clínica ABA** é um sistema web desenvolvido para **gerenciar o acompanhamento de pacientes** em clínicas especializadas em **Análise do Comportamento Aplicada (ABA)**.  
Este projeto foi criado como **MVP de TCC** do curso de **Sistemas de Informação**, com o objetivo de automatizar o registro, acompanhamento e geração de relatórios clínicos.

---

## 🎯 Objetivo do Projeto

O sistema tem como propósito oferecer uma **plataforma prática, organizada e intuitiva** para:

- 📋 Cadastrar pacientes, profissionais e coordenadores  
- 🧠 Registrar evoluções e observações dos atendimentos  
- 📈 Gerar relatórios automáticos em **PDF**, com gráficos e estatísticas  
- 🗂️ Manter um **prontuário digital unificado** para cada paciente  
- 🔒 Controlar acessos conforme o tipo de usuário (Admin, Profissional, Coordenador)


---

## 🧱 Arquitetura do Projeto

O sistema segue o padrão **MVC (Model-View-Controller)**, com camadas bem definidas:

- **Models:** definição das entidades e estrutura do banco  
- **Repository:** comunicação com o banco de dados  
- **Services:** regras de negócio e processamento dos dados  
- **Routes:** rotas e endpoints HTTP  
- **Utils:** funções auxiliares (autenticação, geração de PDFs, etc.) 

---

## 🛠️ Stack Tecnológica

**Backend**
- Python 3.11+  
- Flask (microframework web)  
- Flask SQLAlchemy (ORM)  
- Flask-Login (autenticação)  
- python-dotenv (configurações via `.env`)  
- ReportLab (geração de PDFs)

**Banco de Dados**
- PostgreSQL (ambiente local)

**Frontend**
- HTML5, CSS3 e JavaScript  
- Bootstrap 5  
- Chart.js (gráficos interativos)  
- Jinja2 (template engine do Flask)

**Testes**
- Pytest  
- Pytest-Flask  
- Coverage e Pytest-Cov (relatórios de cobertura)

---

## 📂 Estrutura de Pastas

```text
clinica_aba/main
│
├── app/
│   ├── models/              # Modelos ORM (Paciente, Evolução, Usuário, etc.)
│   ├── repository/          # Repositórios responsáveis pelo acesso ao banco
│   ├── routes/              # Rotas/blueprints da aplicação Flask
│   ├── services/            # Camada de negócio (regras, validações, lógica)
│   ├── utils/               # Funções auxiliares (auth, email, PDF, conversões)
│   ├── templates/           # Arquivos HTML (Jinja2)
│   └── static/              # CSS, JS, imagens, logos, ícones
│
├── migrations/              # Diretório padrão do Alembic
│   └── versions/            # Arquivos de migration gerados (altera tabelas/colunas)
│
├── scripts/                 # Scripts auxiliares (ex: add_lgpd_columns.py)
│
├── app.py                   # Arquivo principal que cria e inicia a aplicação
├── config.py                # Configurações (Desenvolvimento, Produção, Testes)
├── alembic.ini              # Configuração do Alembic (migrations)
│
├── .env.example             # Exemplo de variáveis de ambiente para outros devs
├── .env                     # Variáveis de ambiente reais (não versionadas)
├── .gitignore               # Arquivos/pastas ignorados pelo Git
├── requirements.txt         # Dependências do Python (Flask, SQLAlchemy, etc.)
└── README.md                # Documentação inicial do projeto

```
---

## 📊 Funcionalidades Principais

👥 Usuários	Cadastro, login e controle de acesso (Admin, Coordenador, Profissional)  
🧾 Pacientes	Cadastro, edição e visualização de prontuários  
🧠 Evoluções	Registro de atividades e progresso do paciente  
📄 Relatórios	Geração de relatórios em PDF com gráficos e informações detalhadas  
🔐 Autenticação	Sessões seguras com Flask-Login e utils de autenticação  
🧩 Testes	Testes automatizados para serviços e autenticação  

---

## 🚀 Como Executar

1. Clonar o repositório:
```
git clone https://github.com/MatheusCosta001/clinica_aba.git
cd clinica_aba
```

2. Criar e ativar o ambiente virtual:
```
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. Instalar dependências:
```
pip install -r requirements.txt
```
4. Configurar o arquivo .env:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://usuario:senha@localhost:5432/clinica_aba
SECRET_KEY=sua_chave_secreta_aqui
```
5. Executar o sistema
```
python app.py
```
Acesse em: http://localhost:5000

---

## ✉️ Configuração de E-mail (SMTP) — Gmail e Hotmail/Outlook

O sistema suporta envio de e-mails via servidor SMTP. Seguem exemplos de configuração para Gmail e Hotmail (Outlook). Coloque estas variáveis em seu arquivo `.env`.

Geral (variáveis usadas pelo `app/config.py`):
```
MAIL_SERVER=smtp.exemplo.com
MAIL_PORT=587
MAIL_USERNAME=seu_usuario
MAIL_PASSWORD=sua_senha
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_DEFAULT_SENDER=no-reply@clinica.local
```

Gmail (recomendado usar App Passwords se sua conta usa 2FA):
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=sua_app_password_aqui
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_DEFAULT_SENDER=seu_email@gmail.com
```

Observações para Gmail:
- Se sua conta tiver 2FA, gere uma App Password no painel Google e use-a em `MAIL_PASSWORD`.
- Se não usar 2FA, pode ser necessário ativar o acesso a apps menos seguros (não recomendado).

Hotmail / Outlook (Office365):
```
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USERNAME=seu_email@outlook.com
MAIL_PASSWORD=sua_senha
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_DEFAULT_SENDER=seu_email@outlook.com
```

Após configurar, reinicie a aplicação. O endpoint de recuperação de senha (`/esqueci_senha`) tentará enviar o link; em caso de falha por falta de configuração, o link será exibido no console do servidor para testes.

---

## 🧪 Executar Testes
Para rodar os testes com relatório de cobertura:
```
pytest --cov=app

```
Gerar relatório HTML:
```
pytest --cov=app --cov-report=html
```
O relatório será salvo em htmlcov/index.html.

---

## 👨‍💻 Autores

Matheus Costa & Mariana de Freitas
💡 Projeto desenvolvido como MVP de TCC — Curso de Sistemas de Informação.
📂 GitHub: github.com/MatheusCosta001
📂 GitHub: github.com/marif28

---

## 🧾 Licença

Este projeto é de uso acadêmico e livre para fins educacionais.