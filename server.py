#!/usr/bin/env python3

import socket
import select
import sys

localHost     = "127.0.0.1"
localPort   = int(sys.argv[1])
bufferSize  = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((localHost, localPort))

TagsPorCliente= {}

def addTag(client, Tag):
    if(client not in TagsPorCliente):
        TagsPorCliente[client]=[Tag]
        conf = 'Tag \"' + str(Tag) + '\" adicionada'
        s.sendto(conf.encode('utf-8'), client)
        conf = "Add \"" + str(Tag) + "\" para cliente " + str(client)
        print(conf)
    else:
        if(Tag not in TagsPorCliente[client]):
            TagsPorCliente[client].append(Tag)
            conf = 'Tag ' + str(Tag) + ' adicionada'
            s.sendto(conf.encode('utf-8'), client)
            conf = "Add \"" + str(Tag) + "\" para cliente " + str(client)
            print(conf)


def delTag(client,Tag):
    if Tag not in TagsPorCliente[client]:
        s.sendto("Tag não existe".encode('utf-8'), client)
        return

    for i in TagsPorCliente[client]:
        if i == Tag:
            TagsPorCliente[client].remove(i)
            conf = 'Tag ' + str(Tag) + ' deletada'
            s.sendto(conf.encode('utf-8'), client)
            conf = "Deletando tag \"" + str(Tag) + "\" para cliente " + str(client)
            print(conf)

def rmvDup(listTags):
    output = []
    seen = set()
    for value in listTags:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def sendMsg(message, Tags,clientSource):
    Tags = rmvDup(Tags)
    for client in TagsPorCliente:
        for tagSearch in TagsPorCliente[client]:
            for Tag in Tags:
                if tagSearch == Tag and client != clientSource:
                    conf = "Mensagem \"" + str(message) + "\" enviada para cliente " + str(client)
                    print (conf)
                    s.sendto(message.encode('utf-8'), client)

def splitTags(message):
    MsgList = message.split()
    ListReturn = []
    for i in MsgList:
        if (i[0]=="#"):
            ListReturn.append(i[1:])

    return ListReturn




def checkTag(client, message):
    
    if message[0] == "+":
        addTag(client, message[1:])
    elif message[0] == "-":
        delTag(client, message[1:])
    else:
        print("Mensagem recebida: \"" + str(message) + "\"")
        split = splitTags(message)
        sendMsg(message,split,client)


    

# Loop principal de leitura de dados
while True:

    data, address = s.recvfrom(bufferSize)
    if data:
        data = data.decode('utf-8')
        checkTag(address, data)
