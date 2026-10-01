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

Execute a configuração automática no PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

O script cria `.venv`, instala as dependências de `requirements.txt` e copia
`.env.example` para `.env` apenas se o arquivo local ainda não existir. No macOS
ou Linux, as etapas ainda podem ser executadas manualmente:

```powershell
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
```

Se `.env` já existir, mantenha-o: ele não será sobrescrito e não deve ser enviado
ao Git.

## Executar

```powershell
python manage.py migrate
python manage.py runserver
```

A aplicação fica disponível em http://127.0.0.1:8000/. Para criar um usuário
administrador local, execute `python manage.py createsuperuser`.

## Trabalho em equipe

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
