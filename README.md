# pyexplorer
Um gerenciador de arquivos simples

Os scripts *main.py*/*min.py* digamos que sejam os mesmos os arquivos pois, o *main.py* ele importa os arquivos *crelativo.py* e *pesquisa.py* já o
*min.py*, já vem com essas funções embutidas, por isso ele é um pouco maior.

# Funcionalidades:
1. criar/deletar arquivos
2. criar/deletar pastas vazias
3. após a confirmação, deletar pastas com conteúdo
4. executar arquivos executaveis e com possibilidade de inserir argumentos para o executavel


# *crelativo.py*:
ele serve para criar uma string que seria no caso, o caminho relativo, ele verifica se o caminho contém 
uma unidade de disco, 'c:', entao, ele transforma a string em um array onde, se, o array, é maior que 1, não 
é root, 'c:', se for, é root, se é igual a 2, retorna 'c:/users' por exemplo, se é maior ou igual a 3, retorna 
'../<pasta pai>/<pasta filho>', exemplo:
'C:/Users/Teste' => '../Users/Teste'

# *pesquisa.py*:
serve para a pesquisa de arquivos na pasta aberta, essa função é utilizada no input de pesquisa da janela

# módulos usados:
1. os
2. sys
3. tkinter
4. PIL
5. subprocess
6. platform

o platform é usado para identificação do SO e, logo em seguida, usamos o subprocess para executar o comando 
apropriado para execução de executaveis para cada SO
