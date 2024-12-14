import tkinter as tk
from tkinter import  messagebox, PhotoImage
import os
from os.path import normcase, normpath, isfile, isdir, abspath, exists
import subprocess
import platform
from PIL import Image, ImageTk
from sys import argv

def pesquisa(texto, array):
    encontrados= []
    texto= texto.lower()
    for i in array:
        c= i.split(' ')
        c= ' '.join(c[1:])# 'c:/pasta'
        nome= os.path.basename(i)# 'pasta'
        if texto in nome:
            encontrados.append(i)
    return encontrados

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


user= os.path.expanduser('~')
ds= os.listdrives()
drives= []
for d in ds:
    d= d.lower()
    d= d.replace('\\', '')
    drives.append(d)
cwd=    'rel'
viewft= 'rel'
favs= [normcase('C:/'), user.lower()]

a, l= 900, 700#largura e altura
root= tk.Tk()

root.title('Gerenciador de arquivos pY')
root.geometry(f'{a}x{l}')
root['bg']= 'silver'#para as bordas serem da cor silver
#variaveis para manipulacao de arquivos e pastas
abertos= []
tarquivos= []
tpastas= []
exts= []

def getabertos():
    tarquivos.clear()
    tpastas.clear()
    exts.clear()
    for i in abertos:
        i= i.split(' ')
        if i[0]== '[diretorio]':
            tpastas.append(i)
        else:
            tarquivos.append(i)
            nome= os.path.basename(' '.join(i[1:]))
            ext= os.path.splitext(nome)
            for i in range(1):
                if not ext[1]== '':
                    exts.append(ext[1])
                else:
                    exts.append(ext[0])
getabertos()
#criacao da GUI

#header, onde tera o menu e o sea, para pesquisa
header= tk.Frame(root, bd= 0)
header.grid(row= 0, column= 0, columnspan= 2, sticky= 'ew')
header['bg']= 'silver'
header['height']= 43

#menu
menu= tk.Frame(header, bd= 0)
menu.pack_propagate(False)
menu['height']= 18
menu['bg']= 'darkgrey'
menu.pack(side= tk.TOP, fill= tk.X)

#botao para criar pastas
newbA= tk.Button(menu, text= 'criar pasta', bd= 0)
newbA.pack(padx= 0.5, pady= 0.5, side= tk.LEFT)

#botao para criar arquivos
newbB= tk.Button(menu, text= 'criar arquivo', bd= 0)
newbB.pack(padx= 0.5, pady= 0.5, side= tk.LEFT)

#botao para deletar pastas
newbC= tk.Button(menu, text= 'deletar pasta', bd= 0)
newbC.pack(padx= 0.5, pady= 0.5, side= tk.LEFT)

#botao para deletar arquivos
newbD= tk.Button(menu, text= 'deletar arquivo', bd= 0)
newbD.pack(padx= 0.5, pady= 0.5, side= tk.LEFT)

# Cria o frame que ocupa a linha 0 e as duas colunas
sea= tk.Frame(header, bd= 0)
sea.pack_propagate(False)
sea['height']= 25
sea.pack(pady= (0, 0.5), side= tk.BOTTOM, fill= tk.X)
#input de pesquisa
inp= tk.Entry(sea)
inp.pack(side= tk.LEFT, fill= tk.BOTH, expand= True)


def clear(event):
    inp.delete(0, tk.END)

btn= tk.Button(sea, text= 'limpar', bd= 0)
btn.bind('<Button-1>', clear)
btn.pack(side= tk.RIGHT)







# Cria o frame que ocupa a linha 1 e a coluna 0
aside = tk.Frame(root, width=175)
aside.grid(padx= (0, 0.5), pady= 0, row=1, column=0, sticky="nsew")
#scroll do aside
scrollA= tk.Scrollbar(aside, orient= tk.VERTICAL)
scrollA.pack(side= tk.RIGHT, fill= tk.Y)

listboxA= tk.Listbox(aside, highlightthickness= 0, bd= 0)
listboxA.pack(fill= tk.BOTH, expand= True)
listboxA.config(yscrollcommand= scrollA.set)
scrollA.config(command= listboxA.yview)




# Cria o frame que ocupa a linha 1 e a coluna 1
main = tk.Frame(root, bg= 'silver')
main.grid(row=1, column=1, sticky="nsew")

#metodos de impressao
mtm= tk.Frame(main, height= 15)
mtm.pack_propagate(False)
mtm.pack(pady= (0, 0.5), side= tk.TOP, fill= tk.X)

#botao para imprimir os nomes dos itens
btnA= tk.Button(mtm, text= 'Apenas nomes', bd= 0, bg= 'gainsboro')
btnA.pack(padx= (0.5, 0), pady= 0.5, side= tk.LEFT)

#botao paraimprimir os caminhos absolutos dos itens
btnB= tk.Button(mtm, text= 'Apenas absolutos', bd= 0, bg= 'gainsboro')
btnB.pack(padx= (0.5, 0), pady= 0.5, side= tk.LEFT)

#botao para imprimir os caminhos relativos dos itens
btnC= tk.Button(mtm, text= 'Apenas relativos', bd= 0, bg= 'gainsboro')
btnC.pack(padx= (0.5, 0), pady= 0.5, side= tk.LEFT)

#input para pesquisa de itens
inpB= tk.Entry(mtm, relief= 'groove')
inpB['width']= 20
inpB.pack(padx= 2, side= tk.RIGHT)




#frame para estatistivas
estas= tk.Frame(main, height= 15)
estas.pack_propagate(False)
estas.pack(pady= (0.5, 0), side= tk.BOTTOM, fill= tk.X)

#label para total de itens
lbtotaldi= tk.Label(estas, text= '')
lbtotaldi.pack(side= tk.LEFT)

#label para total de pastas
lbtotaldp= tk.Label(estas, text= '')
lbtotaldp.pack(side= tk.LEFT)

#label para total de arquivos
lbtotalda= tk.Label(estas, text= '')
lbtotalda.pack(side= tk.LEFT)

#label para dois extensoes de arquivos
lbext= tk.Label(estas, text= '')
lbext.pack(side= tk.LEFT)



#scroll do main
scrollMV= tk.Scrollbar(main, orient= tk.VERTICAL)
scrollMV.pack(side= tk.RIGHT, fill= tk.Y)

# Criando a Scrollbar
scrollMH = tk.Scrollbar(main, orient=tk.HORIZONTAL)
scrollMH.pack(side=tk.BOTTOM, fill=tk.X)

#local onde o conteudo da pasta listada será imprimido
listboxM= tk.Listbox(main, highlightthickness= 0,  bd= 0)
listboxM.pack(fill= tk.BOTH, expand= True)
listboxM.config(yscrollcommand= scrollMV.set)
scrollMV.config(command= listboxM.yview)
listboxM.config(xscrollcommand=scrollMH.set)
scrollMH.config(command= listboxM.xview)



# Cria o frame que ocupa a linha 2 e as duas colunas
infos= tk.Frame(root)
infos.pack_propagate(False)
infos['height']= 20
infos.grid(padx= 0.5, pady= 0.5, row=2, column=0, columnspan=2, sticky="ew")
#label que nos informa a pasta de trabalho
labelcwd= tk.Label(infos)
labelcwd.pack(side= tk.LEFT)


def at():
    getabertos()
    lbtotaldi['text']= f'Total de itens: {len(abertos)}'
    lbtotaldp['text']= f'Total de pastas: {len(tpastas)}'
    lbtotalda['text']= f'Total de arquivos: {len(tarquivos)}'
    match len(exts):
        case a if a >= 2:
            lbext['text']= f'Extensões: {exts[-2]}, {exts[-1]}'
        case a if a== 1:
            lbext['text']= f'Extensões: {exts[-1]}'
        case a if a== 0:
            lbext['text']= f'Extensões: ...'

#caminho absoluto da pasta de trabalho
def obcwd():
    global cwd
    labelcwd['text']= ''
    labelcwd['text']= f'[ {normcase(os.getcwd())} ]: => caminho absoluto'
    cwd= 'abs'

#caminho relativo da pasta de trabalho
def relcwd():
    global cwd
    labelcwd['text']= ''
    labelcwd['text']= f'[ {rel(os.getcwd(), drives)} ]: => caminho relativo'
    cwd= 'rel'

#nome da pasta de trabalho
def nomcwd():
    global cwd
    labelcwd['text']= ''
    c= os.getcwd()
    if not c.lower() == normcase('C:/'):
        labelcwd['text']= f'[ {normcase(os.path.basename(os.getcwd()))} ]: => nome do caminho'
    else:
        labelcwd['text']= f'[ {c.lower()} ]: => nome do caminho'
    cwd= 'nom'

def getcwdd():
    global cwd
    if cwd== 'abs':#para caminho absoluto da pasta de trabalho
        obcwd()
    elif cwd== 'rel':#para caminho relativo da pasta de trabalho
        relcwd()
    elif cwd== 'nom':#para apenas o nome da pasta de trabalho
        nomcwd()


btncwd= tk.Button(menu, text= 'cwd', command= obcwd, bd= 0)
btncwd.pack(padx= (10, 0.5), pady= 0.5, side= tk.LEFT)

btncwdrel= tk.Button(menu, text= 'cwdrel', command= relcwd, bd= 0)
btncwdrel.pack(padx= 0.5, pady= 0.5, side= tk.LEFT)

btncwdnom= tk.Button(menu, text= 'cwdnom', command= nomcwd, bd= 0)
btncwdnom.pack(padx= 0.5, pady= 0.5, side= tk.LEFT)

# Configura o peso das linhas e colunas para que elas se expandam
root.grid_rowconfigure(0, minsize= 20)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, minsize= 20)
root.grid_columnconfigure(0, minsize= 175)
root.grid_columnconfigure(1, weight=1)

def viewfget():
    global viewft
    listboxM.delete(0, tk.END)
    listboxM.insert(tk.END, '[diretorio]: ..')
    if viewft== 'abs':
        for item in abertos:
            item= item.split(' ')
            path= ' '.join(item[1:])
            tipo= item[0].replace('[', '').replace(']', '')
            if tipo== 'diretorio':
                listboxM.insert(tk.END, f'[diretorio]: {path}')
            else:
                listboxM.insert(tk.END, f'[arquivo]: {path}')
    elif viewft== 'rel':
        for item in abertos:
            item= item.split(' ')
            path= ' '.join(item[1:])
            tipo= item[0].replace('[', '').replace(']', '')
            if tipo== 'diretorio':
                listboxM.insert(tk.END, f'[diretorio]: {rel(path, drives)}')
            else:
                listboxM.insert(tk.END, f'[arquivo]: {rel(path, drives)}')
    elif viewft== 'nom':
        for item in abertos:
            item= item.split(' ')
            path= ' '.join(item[1:])
            tipo= item[0].replace('[', '').replace(']', '')
            if tipo== 'diretorio':
                listboxM.insert(tk.END, f'[diretorio]: {os.path.basename(path)}')
            else:
                listboxM.insert(tk.END, f'[arquivo]: {os.path.basename(path)}')
    at()

def viewabs():
    global viewft
    viewft= 'abs'
    viewfget()

def viewrel():
    global viewft
    viewft= 'rel'
    viewfget()

def viewnom():
    global viewft
    viewft= 'nom'
    viewfget()

btnA['command']= viewnom
btnB['command']= viewabs
btnC['command']= viewrel

def info(titulo, texto):
    janela= tk.Toplevel()
    janela.title(titulo)
    janela.geometry('300x200')

    text= tk.Text(janela)
    text.pack(fill= tk.BOTH)

    for i in texto:
        text.insert(tk.END, f'[item]: {i}')

    janela.mainloop()
def popup(titulo, conteudo):
    messagebox.showinfo(titulo, conteudo)

def deletarpasta(dir_path):
    # Verifica se o diretório existe
    if os.path.exists(dir_path):
        # Lista todos os itens no diretório
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            # Se for um diretório, chama recursivamente a função
            if os.path.isdir(item_path):
                deletarpasta(item_path)
            else:
                # Se for um arquivo, remove o arquivo
                os.remove(item_path)
                print(f'{item_path} foi removido')
        # Depois de remover todos os arquivos e subdiretórios, remove o próprio diretório
        os.rmdir(dir_path)
        print(f'{dir_path} foi removido')
    else:
        print(f"O diretório {dir_path} não existe.")

def viewfolder():
    if len(abertos) > 0:
        getcwdd()
        viewfget()
    else:#se a pasta for vazia
        popup('Pasta', 'A pasta está vazia')

def viewimg(path):
    janela= tk.Toplevel()
    janela.title(path)
    janela.geometry('500x500')

    img= Image.open(normcase(path))
    img= img.resize((700, 600))
    foto= ImageTk.PhotoImage(img)

    label= tk.Label(janela, image= foto)
    label.pack(fill= tk.BOTH, expand= True)

    janela.mainloop()

def openfolder(c):
    try:
        abertos.clear()
        p= os.scandir(c)
        for item in p:
            if item.is_dir():
                abertos.append(f'[diretorio] {abspath(item)}')
                tpastas.append(abspath(item))
            else:
                abertos.append(f'[arquivo] {abspath(item)}')
                tarquivos.append(abspath(item))
        if len(abertos) > 0:
            os.chdir(c)
        else: print('A pasta esta vazia, nao foi adicionada a pasta de trabalho')

        viewfolder()
        inp.delete(0, tk.END)
        inp.insert(0,  normcase(os.getcwd()))
    except Exception as e:
        popup('Erro', e)

#criacao de arquivos e pastas
def manap(tipo, modo):
    if tipo and modo:
        janela= tk.Toplevel()
        w, h = 360, 140
        x= ((700 - h) // 2) + root.winfo_x()
        y= ((900 - w) // 2) + root.winfo_y()
        janela.geometry(f'{w}x{h}+{x}+{y}')
        janela.resizable(False, False)

        def fazer():
            nome= input.get()
            cam= inputc.get()
            c= cam + os.sep + nome
            res= messagebox.askquestion('Confirmação', 'Você tem certeza?')
            if res== 'yes':
                if modo== 'criar':
                    if not os.path.exists(c):
                        print(f'{c} foi criado')
                        if tipo== 'pasta':
                            os.mkdir(c)
                            openfolder(cam)
                            janela.destroy()
                            inp.focus_set()
                        else:
                            arquivo= open(c, 'w')
                            openfolder(cam)
                            janela.destroy()
                            inp.focus_set()
                    else:
                        popup('Erro', f'{c} ja existe')
                        print(f'{c} nao foi criado')
                        janela.destroy()
                        inp.focus_set()
                else:
                    if os.path.exists(c):
                        if tipo== 'pasta':
                            deletarpasta(c)
                            openfolder(cam)
                            janela.destroy()
                            inp.focus_set()
                        else:
                            os.remove(c)
                            openfolder(cam)
                            janela.destroy()
                            inp.focus_set()
                    else:
                        popup('Erro', 'O item nao existe')
                        janela.destroy()
                        inp.focus_set()
            else:
                janela.destroy()
                inp.focus_set()

        def enter(event):
            fazer()

        header= tk.Frame(janela, bg= 'silver', width= 320, height= 25)
        header.pack_propagate(False)
        header.pack(padx= 0, pady= (55, 0), side= tk.TOP)

        inputc= tk.Entry(header, width= 30, bd= 0)
        inputc.pack(padx= (0.5, 0), pady= 0.5, side= tk.LEFT, fill= tk.Y)
        inputc.insert(0, os.getcwd())

        #esse vai capitar o nome da pasta
        input= tk.Entry(header, width= 15, bd= 0)
        input.pack(padx= (0.5, 0.5), pady= 0.5, side= tk.LEFT, fill= tk.Y)

        btn= tk.Button(header, text= 'criar', command= fazer, width= 5, height= 15, bd= 0)
        btn.pack(padx= 0.5, pady= 0.5, side= tk.RIGHT)
        input.bind('<Return>', enter)
        input.focus_set()
        janela.title(f'{modo} [Arquivo~Pasta]')
        janela.mainloop()

newbA['command']= lambda: manap('pasta', 'criar')
newbB['command']= lambda: manap('arquivo', 'criar')
newbC['command']= lambda: manap('pasta', 'deletar')
newbD['command']= lambda: manap('arquivo', 'deletar')

def execexe(path):
    c= os.path.basename(path)
    res= messagebox.askquestion('Confirmação', 'Você quer executa-lo?')
    if res== 'yes':
        #janela para capitar possiveis argumentos para o executavel
        janela= tk.Toplevel()
        w, h = 260, 140
        x= ((700 - h) // 2) + root.winfo_x()
        y= ((900 - w) // 2) + root.winfo_y()
        janela.geometry(f'{w}x{h}+{x}+{y}')
        janela.resizable(False, False)

        def fazer():
            te= input.get()
            janela.destroy()
            if not te== '':
                if platform.system() == "Linux":
                    subprocess.run(["gnome-terminal", "--", c, te], shell= True)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", "-a", "Terminal", c, te], shell= True)
                elif platform.system() == 'Windows':
                    subprocess.run(["start", "cmd", "/k", c, te], shell= True)
            else:
                if platform.system() == "Linux":
                    subprocess.run(["gnome-terminal", "--", c], shell= True)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", "-a", "Terminal", c], shell= True)
                elif platform.system() == 'Windows':
                    subprocess.run(["start", "cmd", "/k", c], shell= True)
        def enter(event):
            fazer()

        header= tk.Frame(janela, bg= 'silver', width= 124, height= 25)
        header.pack_propagate(False)
        header.pack(padx= 0, pady= (55, 0), side= tk.TOP)

        #esse vai capitar o nome da pasta
        input= tk.Entry(header, bd= 0)
        input.pack(padx= (0.5, 0.5), pady= 0.5, side= tk.LEFT, fill= tk.Y)

        input.bind('<Return>', enter)
        input.focus_set()
        janela.title(f'Argumentos para executar')
        janela.mainloop()
    else: pass
def view(c):
    if isdir(c):
        openfolder(c)
    else:
        ext= os.path.splitext(c)
        imagens= ['.jpg', '.png', '.svg', '.ico', '.gif']
        e= ['.exe', '.com', '.COM', '.EXE']
        match ext[1]:
            case a if a in imagens:
                viewimg(c)
            case a if not a in e and not a in imagens:
                openfile(abspath((os.path.basename(c))))
            case a if a in e:
                execexe(c)
            case _:
                popup('Erro', f'[ {c} ] , sem suporte para o arquivo')

def openfile(path):
    if path and (exists(path) and isfile(path)):
        try:
            if os.path.isabs(path):
                pass
            else: path= os.path.abspath(path)
            janela= tk.Toplevel()
            janela.title(f'Arquivo [ {path} ]')
            janela.geometry('500x550')

            frame= tk.Frame(janela, bg= 'silver')
            frame.pack_propagate(False)
            frame.pack(fill= tk.BOTH, expand= True)

            # Cria um Scrollbar
            scrollbar = tk.Scrollbar(frame, orient= tk.VERTICAL)
            scrollbar.pack(side= tk.RIGHT, fill= tk.Y)

            # Cria um Scrollbar
            scrollbarB = tk.Scrollbar(frame, orient= tk.HORIZONTAL)
            scrollbarB.pack(side= tk.BOTTOM, fill= tk.X)

            ftext= tk.Frame(frame, bg= 'green')
            ftext.pack(fill= tk.BOTH, expand= True)

            text= tk.Text(ftext, wrap= 'none')
            text.pack(fill= tk.BOTH, expand= True)
            # Configuração da tag de realce
            text.tag_configure('keyword', foreground='red')

            scrollbar['command']= text.yview
            scrollbarB['command']= text.xview
            text['yscrollcommand']= scrollbar.set
            text['xscrollcommand']= scrollbarB.set

            f= open(path, 'r')
            data= f.read()
            f.close()
            text.insert(tk.END, data)

            def salvar():
                data= text.get('1.0', tk.END)
                f= open(path, 'w')
                f.write(data)
                popup('Salvo', 'Alteração feita com sucesso.')

            text.bind('<Control-s>', lambda event: salvar())
            janela.mainloop()
        except PermissionError:
            janela.destroy()
            popup('Erro', f'Acesso negado a {path}')
        except Exception as e:
            janela.destroy()
            popup('Erro', e)

def openm(event):
    i= listboxM.curselection()
    if len(i) > 0:
        item= listboxM.get(i[0]).split(' ')
        c= ' '.join(item[1:])
        match c:
            case a if not a== '..':
                view(a)
            case a if not os.getcwd() == drives[0] or not os.getcwd() == drives[1]:
                os.chdir('..')
                openfolder('.')
            case _:
                popup('Pasta', 'Você está na raiz, {os.getcwd()}')

def opena(event):
    i= listboxA.curselection()
    if len(i) > 0:
        item = str(listboxA.get(i[0]))
        openfolder(item)

#capitacao de eventos dos itens das listas
listboxA.bind('<<ListboxSelect>>', opena)#caso de click
listboxA.bind('<Return>', opena)#caso da tecla enter

listboxM.bind('<<ListboxSelect>>', openm)#caso de click
listboxM.bind('<Return>', openm)#caso da tecla enter

def ipp(event):
    c= inp.get()
    if not c == '':
        cos= c.split(' ')
        if not cos[0]== 'cd':
            ct= normcase(' '.join(cos[:]))
            view(ct)
        else:
            view(normcase(' '.join(cos[1:])))
    else:
        popup('Ei!', 'Informe um caminho...')

inp.bind('<Return>', ipp)

def verseb(text):
    global abertos
    text= text.lower()
    #funcao
    encontrados= []
    for i in abertos:
        c= i.split(' ')
        c= ' '.join(c[1:]).lower()
        nome= os.path.basename(i).lower()
        if text in nome:
            encontrados.append(i)

    if len(encontrados) > 0:
        listboxM.delete(0, tk.END)
        listboxM.insert(tk.END, '[diretorio] ..')
        for i in encontrados:
            listboxM.insert(tk.END, i)

def pesquisa(event):
    global abertos
    c= inpB.get()
    verseb(c)

inpB.bind('<Return>', pesquisa)

#verificando se foi passado uma pasta no argv
if argv and len(argv) > 1:
    c= ' '.join(argv[1:])
    erro1= isdir(c)
    erro2= os.path.exists(c)
    if erro2 and erro1:
        os.chdir(normcase(c))
        openfolder(normcase(os.getcwd()))
    else:
        popup('Ocorreu um erro', f'Erro na abertura do argumento, Existe: {erro2}, É uma pasta: {erro1}')
        os.chdir(user)
        openfolder(normcase(user))
else:
    os.chdir(user)
    openfolder(normcase(user))

getcwdd()
inp.focus_set()

#percorrer cada favorito
for item in favs:
    listboxA.insert(tk.END, item)
at()

#loop principal
root.mainloop()
