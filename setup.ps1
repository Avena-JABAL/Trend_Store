$ErrorActionPreference = 'Stop'

$projectRoot = $PSScriptRoot
$venvPath = Join-Path $projectRoot '.venv'
$pythonPath = Join-Path $venvPath 'Scripts\python.exe'

if (-not (Test-Path $pythonPath)) {
    Write-Host 'Criando o ambiente virtual...'
    & py -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw 'Não foi possível criar o ambiente virtual. Verifique a instalação do Python.'
    }
}

Write-Host 'Atualizando o pip e instalando as dependências...'
& $pythonPath -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw 'Não foi possível atualizar o pip.'
}

& $pythonPath -m pip install -r (Join-Path $projectRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) {
    throw 'Não foi possível instalar as dependências de requirements.txt.'
}

$envPath = Join-Path $projectRoot '.env'
if (-not (Test-Path $envPath)) {
    Copy-Item (Join-Path $projectRoot '.env.example') $envPath
    Write-Host 'Arquivo .env criado a partir de .env.example.'
} else {
    Write-Host 'Arquivo .env já existe; mantendo a configuração local.'
}

Write-Host 'Configuração concluída. Execute as migrações com .venv\Scripts\python.exe manage.py migrate.'