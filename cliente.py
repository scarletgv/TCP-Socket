#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
UFMG - ICEx - DCC - Redes de Computadores - 2019/1
Aluna: Scarlet Gianasi Viana
Matrícula: 2016006891

Versão utilizada: Python 3.6.7

'''

import socket
import sys
import struct

# Recebe o IP e a porta como argumentos
enderecoIP = sys.argv[1]
porta = int(sys.argv[2])

# Criação do socket
csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Timeout após 15 segundos
tempo = struct.pack('ll', 15, 0)
csocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, tempo)

# Conexão
endServidor = (enderecoIP, porta)
csocket.connect(endServidor)

# Comunicação
for msgRaw in sys.stdin:
    
    # Definindo o operador
    if msgRaw[0] == '+':   # Adição
        operador = b'1'
        
    elif msgRaw[0] == '-': # Subtração
        operador = b'0'
        
    # Qualquer coisa além fecha a conexão
    else:
        csocket.shutdown(socket.SHUT_RDWR)
        csocket.close()
        break
    
    operando = int(msgRaw.split(' ')[1])
   
    # Empacotando o operando e operador em 5 bytes e enviando para o servidor
    operacao = struct.pack('!ci', operador, operando)        
    msg = csocket.send(operacao)
    
    # Recebe a string com 6 bytes com o resultado da operação do servidor
    msgServidor = csocket.recv(6)
         
    if not msg:
        print("Falha ao receber a mensagem do servidor.")
        break
    
    # Impressão do resultado na tela
    print(msgServidor.decode("ascii"))

csocket.close()
