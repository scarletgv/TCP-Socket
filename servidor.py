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

# Recebe a porta como argumento
porta = int(sys.argv[1])

# Criação do socket
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexão
endereco = ("", porta)
ssocket.bind(endereco)
ssocket.listen(10)

# Inicialização do contador global
total = 0

while True:
    print("Esperando um cliente...")

    csocket, cliente = ssocket.accept()
    print("Conectado a {}".format(cliente))
    
    # Comunicação
    while True:
        # Recebe a mensagem do cliente
        msgCliente = csocket.recv(5)
        
        if not msgCliente:
            print("Falha ao receber a mensagem do cliente.")
            break
        
        # Desempacota os bytes recebidos do cliente
        msg = struct.unpack('!ci', msgCliente)
         
        # Definindo e executando a operação
        if msg[0] == b'1':         # Adicao
            total = total + msg[1]
        else:                      # Subtração
            total = total - msg[1]
        
        # Complemento
        if total < 0:
            total = 1000000 - total
        
        # Módulo
        if total >= 1000000:
            total = total%1000000
        
        resultado = str(total)
        
        # Empacotando o resultado para enviar ao cliente
        msgResult = struct.pack('!6s', resultado.encode('ascii'))
        msgServidor = csocket.send(msgResult)

    csocket.close()

ssocket.close()
