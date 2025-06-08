#!/bin/bash
set -e

echo "--- Ativando ambiente virtual ---"
source venv/bin/activate

echo "--- Executando o projeto (main.py) ---"

python3 main.py
python3 app.py
# A desativação acontecerá automaticamente quando o script terminar
echo "--- Aplicação finalizada. Desativando o ambiente virtual. ---"
deactivate
