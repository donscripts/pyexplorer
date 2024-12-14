import os
from os.path import normcase, basename

def pesquisa(texto, array):
    encontrados= []
    texto= texto.lower()
    for i in array:
        c= i.split(' ')
        c= ' '.join(c[1:])# 'c:/pasta'
        nome= basename(i)# 'pasta'
        if texto in nome:
            encontrados.append(i)
    return encontrados
