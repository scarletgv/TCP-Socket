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

MSG_TAMANHO_MAX = 100

# Leitura da porta a ser atribuida ao servidor
if len(sys.argv) < 3:
    print("python cliente.py [ENDERECO] [PORTA]")
enderecoIP = sys.argv[1]
porta      = int(sys.argv[2])

# Criacao do socket
csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexao (abertura ativa)
endServidor = (enderecoIP, porta)
csocket.connect(endServidor)
# Timeout
tempo = struct.pack('LL', 15, 0)
csocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, tempo)

# Comunicacao
while True:
    msgRaw = input("Operação: ") #Input do cliente
    
    if msgRaw[0] == '+': # Definindo a operacao
        op = b'1'
    elif msgRaw[0] == '-':
        op = b'0'
    else: 
        csocket.shutdown(socket.SHUT_RDWR)
        csocket.close()
        break
   
    msg = struct.pack('=cI', op, int(msgRaw.split(' ')[1]))
        
    nbytes = csocket.send(msg)
    
    msg = csocket.recv(5)
        
    msgUnp = struct.unpack('=i', msg)
        
    if not msg:
        print("Falha ao receber uma mensagem")
        break
    print("Resultado: "+ str(msgUnp[0]))


csocket.close()