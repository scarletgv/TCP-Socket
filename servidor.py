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

MAX_CLIENTES    = 10
MSG_TAMANHO_MAX = 100
total = 0

# Leitura da porta a ser atribuida ao servidor
if len(sys.argv) < 2:
    print("python servidor.py [PORTA]")
porta = int(sys.argv[1])

# Criacao do socket
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Timeout
tempo = struct.pack('LL', 15, 0)
ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, tempo)

# Abertura passiva
endereco = ("", porta)
ssocket.bind(endereco)
ssocket.listen(MAX_CLIENTES)

while True:
    print("Esperando por novo cliente...")

    csocket, cliente = ssocket.accept()
    print("Conectado a {}".format(cliente))
    
    # Comunicacao
    while True:
        msg_bytes = csocket.recv(5) # Recebe a mensagem do cliente
        
        if not msg_bytes:
            print("Falha ao receber uma mensagem")
            break
        
        msg = struct.unpack('=cI', msg_bytes) # Unpack a mensagem em um char e um inteiro
         
        # Definindo a operação
        if msg[0] == b'1':
            total = total + msg[1]
        else:
            total = total - msg[1]
        
        # Complemento
        if total < 0:
            total = 1000000 - total
        
        # Módulo
        if total >= 1000000:
            total = total%1000000
        
        msg = struct.pack('=i', total)
        nbytes = csocket.send(msg)

    # Finalizacao
    csocket.close()

ssocket.close()