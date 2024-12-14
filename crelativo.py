import os
from os.path import normcase, basename

def rel(path, drives):
    if path and drives:
        discos= []#tratamento das chars
        unidade= False
        root= False
        ok= False
        final= ''

        for d in drives:
            d= d.replace(os.sep, '')
            discos.append(d)
        path= path.lower()
        path= path.split(os.sep)
        list(path)

        if path[0] in discos:
            unidade= True
        if path[-1]== '':
            path.pop()

        filho= ''
        pai= ''
        #verificando se path e raiz, 'c:/' ou 'c:'
        if len(path) == 1 and path[0] in discos:
            root= True
            ok= False
            pai= discos[0]
            final= f'{pai}/'
        elif len(path) >= 1:
            #verificando se o diretorio pai e disco e se o ultimo nao e disco
            if len(path) == 2  and (not path[1] in discos):
                root= False
                ok= True
                filho= path[1]
                pai= path[0]
                final= f'{pai}/{filho}'
            #verificando o nao tem disco
            elif len(path) >= 3 and (not path[1] in discos):
                root= False
                ok= True
                filho= path[-1]
                pai= path[-2]
                final= f'../{pai}/{filho}'
        return final
    else:
        return 'Voce deve passar o caminho e as unidades de dicos'
