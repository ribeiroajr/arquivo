#!/bin/bash
# deploy.sh — atualiza o S-ARQ a partir do repositório Git
#
# Uso: ./deploy.sh
# Requer: git, python3 (venv ativado ou no PATH), systemctl (para reiniciar o serviço)
#
# Variáveis de ambiente opcionais:
#   SERVICE_NAME  nome do serviço systemd do Gunicorn (padrão: gunicorn)
#   VENV_PATH     caminho para o virtualenv            (padrão: ./venv)

set -e  # interrompe em qualquer erro

SERVICE_NAME="${SERVICE_NAME:-gunicorn}"
VENV_PATH="${VENV_PATH:-./venv}"
PYTHON="$VENV_PATH/bin/python"

echo "==> [1/5] Atualizando código..."
git pull origin main

echo "==> [2/5] Instalando dependências..."
"$VENV_PATH/bin/pip" install -q -r requirements.txt

echo "==> [3/5] Aplicando migrations..."
"$PYTHON" manage.py migrate --noinput

echo "==> [4/5] Coletando arquivos estáticos..."
"$PYTHON" manage.py collectstatic --noinput --clear

echo "==> [5/5] Reiniciando serviço $SERVICE_NAME..."
if systemctl is-active --quiet "$SERVICE_NAME"; then
    sudo systemctl restart "$SERVICE_NAME"
    echo "    Serviço reiniciado."
else
    echo "    AVISO: serviço '$SERVICE_NAME' não está ativo — reinicie manualmente."
fi

echo ""
echo "Deploy concluído."
