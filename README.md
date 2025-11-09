# 🧩 Clínica ABA - Sistema de Gerenciamento

**Clínica ABA - Sistema de Gerenciamento** é um sistema web desenvolvido para gerenciar o acompanhamento de pacientes em clínicas especializadas em Análise do Comportamento Aplicada (ABA). O projeto foi criado como **MVP de TCC**, com foco em funcionalidades essenciais para cadastro, registro de evoluções, geração de relatórios e visualização de prontuários.

---

## 🎯 Objetivo do Projeto

O sistema tem como objetivo principal oferecer uma **plataforma simples, intuitiva e eficiente** para:

- Cadastro de pacientes, terapeutas e responsáveis  
- Registro de evoluções (timeline de atividades e observações)  
- Geração de relatórios automáticos em PDF com gráficos por domínio  
- Prontuário unificado por paciente  

Este MVP **atende os requisitos da pesquisa e valida a automação do registro de dados e relatórios**, sem funcionalidades complexas como agendamento ou mobile.

---

## 🛠️ Stack Tecnológica

**Backend:**  
- Python 3.11+  
- Flask (microframework web)  
- SQLAlchemy (ORM)  
- Flask-Login (autenticação)  
- Flask-Migrate (migrações do banco)  

**Banco de Dados:**  
- PostgreSQL (local)  

**Frontend:**  
- HTML + CSS + JS  
- Bootstrap 5 (estilização)  
- Chart.js (gráficos interativos)  
- Jinja2 (templates do Flask)  

**Relatórios:**  
- WeasyPrint (HTML → PDF)  
- matplotlib (gráficos opcionais no backend)  

---

## 📂 Estrutura do Projeto
```
clinica_aba/
├── app.py # Entrada principal do Flask
├── config.py # Configurações do Flask e do banco
├── models.py # Models SQLAlchemy (User, Patient, Evolution)
├── routes.py # Rotas/views do Flask
├── requirements.txt # Dependências Python
├── /templates/ # HTMLs renderizados com Jinja2
│ ├── base.html
│ ├── login.html
│ ├── pacientes.html
│ ├── evolucao.html
│ └── relatorio.html
└── /static/ # CSS, JS e imagens
├── /css/
├── /js/
└── /img/
```
---

## ⚡ Funcionalidades Principais

1. **Autenticação de usuários** (Admin, Profissional, Coordenador)  
2. **CRUD de pacientes**  
3. **Registro de evoluções** (com autor e timestamp automático)  
4. **Timeline de evoluções por paciente**  
5. **Geração de relatórios PDF com gráficos**  
6. **Prontuário centralizado e unificado**

---

## 🚀 Como Executar

1. Clonar o repositório:
```
git clone https://github.com/MatheusCosta001/clinica_aba
cd clinica_aba
```

Criar e ativar o ambiente virtual:
```
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

Instalar dependências:
```
pip install -r requirements.txt
```

Configurar banco PostgreSQL (local) e atualizar config.py com usuário, senha e database.

Rodar o projeto:
```
python app.py
```
