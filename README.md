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
clinica_aba_versao_final/
│
├── app/
│   ├── models/              # Modelos do banco (Paciente, Evolução, Usuário)
│   ├── repository/          # Repositórios de dados
│   ├── routes/              # Rotas da aplicação
│   ├── services/            # Lógica de negócio
│   ├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/           # Páginas HTML (Jinja2)
│   ├── tests/               # Testes automatizados
│   └── utils/               # Funções auxiliares (auth, PDF, config)
│
├── app.py                   # Ponto de entrada principal do Flask
├── requirements.txt         # Dependências do projeto
├── .env                     # Variáveis de ambiente (configurações locais)
├── .gitignore               # Arquivos ignorados pelo Git
├── .coverage                # Relatório de cobertura de testes
├── README.md                # Documentação do projeto
└── venv/                    # Ambiente virtual (não versionado)
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