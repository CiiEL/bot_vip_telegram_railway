#!/bin/bash

echo "🔁 Iniciando bots..."

# Inicia o bot principal
python3 main.py &

# Inicia o bot do grupo free
python3 mensageiro_free.py &

# Espera ambos finalizarem (mantém o container vivo)
wait
