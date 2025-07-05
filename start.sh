#!/bin/bash

# Inicia os dois bots em paralelo
python main.py &
python mensageiro_free.py

# Espera os processos terminarem (evita saída imediata)
wait
