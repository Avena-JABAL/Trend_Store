# Trend Store

Projeto colaborativo desenvolvido com Django.

## Requisitos

- Python 3.12 ou superior
- Git

## Configuração local

Clone o repositório e entre na pasta do projeto:

```powershell
git clone <URL_DO_REPOSITORIO>
cd Trend_Store
```

Crie e ative um ambiente virtual:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

No macOS ou Linux, use `python3 -m venv .venv` e `source .venv/bin/activate`.

Instale as dependências e crie sua configuração local:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

No macOS ou Linux, substitua o último comando por `cp .env.example .env`.
Cada pessoa deve manter seu próprio `.env`; ele não deve ser enviado ao Git.

## Executar

```powershell
python manage.py migrate
python manage.py runserver
```

A aplicação fica disponível em http://127.0.0.1:8000/. Para criar um usuário
administrador local, execute `python manage.py createsuperuser`.

## Trabalho em equipe

- Crie uma branch para cada tarefa e abra um pull request para integrar mudanças.
- Não envie `.env`, `.venv/` nem o banco local `db.sqlite3` ao repositório.
- Ao adicionar uma dependência, atualize `requirements.txt` e informe a equipe.
- Ao alterar modelos, inclua as migrações geradas (`python manage.py makemigrations`)
  no mesmo pull request.

## Estrutura

```text
config/          Configurações e pontos de entrada do Django
manage.py        Utilitário de administração do Django
requirements.txt Dependências Python do projeto
```
