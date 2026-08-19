# Mini Rede ABM

Uma mini rede social voltada para moradores de condomínio, desenvolvida como projeto de aprendizado prático de desenvolvimento web full-stack — do zero até um fluxo completo de API REST, autenticação, upload de arquivos e recuperação de senha por e-mail.

> Projeto construído com foco em fundamentos: sem ORM, sem frameworks de frontend, SQL puro e JavaScript vanilla — priorizando entendimento profundo de cada camada antes de introduzir abstrações.

---

## Funcionalidades

- **Autenticação completa**: cadastro, login, logout e recuperação de senha via e-mail (com token seguro e expiração)
- **Mural de posts** (client-rendered): criação, edição e remoção de posts sem recarregar a página, com atualização automática entre usuários
- **Categorização de posts**: Aviso, Compra e venda, Evento e Alerta — cada uma com identidade visual própria
- **Perfil de usuário**: edição de nome, e-mail e foto de perfil (upload real de imagem, com preview instantâneo)
- **Autorização por post**: cada morador só edita/apaga o próprio conteúdo
- **Interface responsiva**, com identidade visual própria inspirada no tema do bosque/floresta

## Stack técnica

| Camada | Tecnologia |
|---|---|
| Backend | Python + Flask (Blueprints) |
| Banco de dados | SQLite (SQL puro, sem ORM) |
| Frontend (server-rendered) | HTML + Jinja2 |
| Frontend (client-rendered) | JavaScript vanilla + Fetch API + manipulação de DOM |
| Estilo | CSS próprio |
| E-mail | SMTP (Gmail) via `smtplib` |
| Versionamento | Git + GitHub (fluxo de branch por feature + Pull Request) |

## Arquitetura

O projeto combina duas abordagens de renderização, deliberadamente:

- **Server-rendered** (Flask + Jinja2): usado em telas de baixa interatividade (cadastro)
- **Client-rendered** (API REST + JavaScript): usado no mural e no perfil, onde a interatividade em tempo real compensa a complexidade extra

O backend expõe uma API REST (`/api/*`) consumida pelo frontend via `fetch`, seguindo convenções REST (recurso na URL, ação no verbo HTTP).

## Estrutura do projeto

```
mini-rede-abm/
├── app.py                  # inicialização do Flask e registro dos blueprints
├── config.py
├── email_utils.py          # envio de e-mail (recuperação de senha)
├── models/
│   └── db.py                # conexão e schema do banco de dados
├── routes/
│   ├── auth.py               # login, cadastro, logout, recuperação de senha
│   ├── posts.py               # rota do mural
│   ├── perfil.py               # rota de perfil
│   └── api.py                   # endpoints REST (posts, login, perfil)
├── static/
│   ├── css/style.css
│   ├── js/                     # mural.js, perfil.js, login.js, common.js
│   └── uploads/perfil/           # fotos de perfil enviadas pelos usuários
└── templates/                    # arquivos HTML (Jinja2)
```

## Rodando localmente

### Pré-requisitos

- Python 3.9+
- Uma conta Gmail com [senha de app](https://myaccount.google.com/apppasswords) gerada (para o envio de e-mails)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/guilherme-dsm/mini-rede-abm.git
cd mini-rede-abm

# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
GMAIL_USUARIO=seuemail@gmail.com
GMAIL_SENHA_APP=suasenhadeappsemespacos
```

### Populando o banco com os dados iniciais

```bash
python3 seed_predios.py
```

### Rodando o servidor

```bash
python3 app.py
```

Acesse [http://127.0.0.1:5001](http://127.0.0.1:5001)

## Roadmap

- [x] Fase 0 — Fundamentos de internet e HTTP
- [x] Fase 1 — Mural server-rendered (Flask + Jinja2)
- [x] Fase 2 — API REST + mural client-rendered
- [x] Edição de perfil com upload de foto
- [x] Recuperação de senha via e-mail
- [x] Deploy em produção (migração para PostgreSQL)
- [ ] Integração com IA (categorização automática de posts)

## Sobre o projeto

Este projeto foi desenvolvido como parte de um processo de aprendizado autodidata em desenvolvimento web, com o objetivo de compreender profundamente cada camada de uma aplicação full-stack — desde o protocolo HTTP até deploy em produção — antes de recorrer a frameworks e abstrações de alto nível.

## Licença

Este é um projeto de estudo, sem fins comerciais.
