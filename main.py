import csv
import sys
import matplotlib.pyplot as plt
import numpy as np


sys.setrecursionlimit(10000)

class No:
    def __init__(self, id, titulo, ano, idade, netflix, hulu, primeVideos, disney, genero, lingua, tempo):
        self.esquerda = None  
        self.direita = None
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.idade = idade
        self.netflix = netflix
        self.hulu = hulu
        self.primeVideos = primeVideos
        self.disney = disney
        self.genero = genero
        self.lingua = lingua
        self.tempo = tempo



def dadosFinal (str, arv, qnt, ordem):
    tema = (stringToArray(filtroAux([],str,arv))) #obtem todos os valores das celulas (genero/lingua)
    dadosTema = []
    for i in range(len(tema)):
        dadosTema.append(tema[i]) #coloca o nome da lingua
        dadosTema.append(filtro1(arv,str,tema[i],0)) #junto com a quantidade que foi encontrada de cada lingua/genero

    dadosTemaFinal = Convert(dadosTema) #transforma em dicionario e remove os repetidos
    dadosTemaFinal = dict(sorted(dadosTemaFinal.items(), key=lambda item: item[1], reverse=ordem)) #deixa em ordem crescente ou decrescente dependendo da variável booleana de entrada da função "ordem"
    dadosTemaFinal.pop('') #remove a quantidade de linhas que é quardado na chave ''
    aux = {}
    if qnt != 0:
        for l in range(qnt):
            aux.update({list(dadosTemaFinal.items())[l][0]: list(dadosTemaFinal.items())[l][1]}) #cria um novo dicionario e define quantos primeiros valores vão ser inseridos, baseando na variavel inteira de entrada "qnt"
        return aux
    return dadosTemaFinal

def Convert(arry): #converte a array em dict (facilitar o plot dos graficos)
    dicio = {arry[i]: arry[i + 1] for i in range(0, len(arry), 2)}
    return dicio


# Metodo de Insercao
def insere(no,  id, title, ano, idade, netflix, hulu, primeVideos, disney, genero, lingua, tempo):
    if no is None:
        no = No( id, title, ano, idade, netflix, hulu, primeVideos, disney, genero, lingua, tempo)
    else:
        if id < no.id:
            no.esquerda = insere(no.esquerda, id, title,ano, idade, netflix, hulu, primeVideos, disney, genero, lingua, tempo)
        else:
            no.direita = insere(no.direita,  id, title,ano, idade, netflix, hulu, primeVideos, disney, genero, lingua, tempo)
    return no





def stringToArray (arry): # transforma os valores do csv que contem mais de um valor em uma string (linguas e generos, onde pode existir mais de um valor em uma célula)
    for i in range(len(arry)): #percorre todo o array 
        arry[i] = arry[i].split(",") #divide o que for divisível
    aux = []
    for i in range(len(arry)): #junta as arrays e subarrays
        aux += arry[i]
    return(aux)


def filtro1(no, criterio, valor, count):
    if no is None: #se não tem nó, não tem valor a ser contado
        return 0
    else: #nó existe
        if valor == getattr(no, criterio) or str(valor) in str(getattr(no, criterio)): #se o valor buscado for igual ou o valor buscado estiver dentro de onde for buscado
            return 1 + filtro1(no.esquerda, criterio, valor, count) + filtro1(no.direita, criterio, valor, count) #adiciona 1 ao contador e utiliza da recursão para avançar para proximo no à esquerda e direta 
        else:
            return 0 + filtro1(no.esquerda, criterio, valor, count) + filtro1(no.direita, criterio, valor, count) #não adiciona ao contador e utiliza da recursão para avançar para proximo no à esquerda e direta 




def filtro2(no, criterio, valor, criterio2, valor2, count):
    if no is None: #se não tem nó, não tem valor a ser contado
        return 0
    else: #nó existe
        if (valor == getattr(no, criterio) or str(valor) in str(getattr(no, criterio))) and (valor2 == getattr(no, criterio2) or str(valor2) in str(getattr(no, criterio2))): #utiliza a mesma lógica do filtro1, porém no filtro 2 utiliza 2 critérios
            return 1 + filtro2(no.esquerda, criterio, valor, criterio2, valor2, count) + filtro2(no.direita, criterio, valor, criterio2, valor2, count) #adiciona 1 ao contador e utiliza da recursão para avançar para proximo no à esquerda e direta 
        else:
            return 0 + filtro2(no.esquerda, criterio, valor, criterio2, valor2, count) + filtro2(no.direita, criterio, valor, criterio2, valor2, count) #não adiciona ao contador e utiliza da recursão para avançar para proximo no à esquerda e direta 


def filtroAux(arry, criterio, no):
    if no is None: #se não tiver nó, não tem dado a ser adicionado
        return
    else: #o nó existe
        if getattr(no, criterio) not in arry: #se o valor ainda não for catalogado
            arry += [getattr(no, criterio)] #cataloga o valor
            filtroAux(arry,criterio,no.esquerda) #tenta catalogar o no à esquerda
            filtroAux(arry,criterio,no.direita) #tenta catalogar o no à direita
            return arry #retorna o array preenchido
        else: #o valor já foi catalogado
            filtroAux(arry,criterio,no.esquerda) #tenta catalogar o no à esquerda
            filtroAux(arry,criterio,no.direita) #tenta catalogar o no à direita
            return arry #retorna o array preenchido

def dadosMedia (dic):  
    listaChaves = list(dic.keys())
    listaValores = list(dic.values())
    aux = 0
    for i in range(len(listaChaves)):
        for l in range(int(listaValores[i])):
            aux += int(listaChaves[i])
    soma = 0
    for k in range(len(listaValores)):
        soma += int(listaValores[k])
    print("Aux: ", aux)
    print("Soma: ", soma)
    return (aux/soma)

no = No(0, '', '', '','','','','','','', '')

raiz = None



with open('tv_shows.csv', 'r', encoding="utf8") as csvfile:
  reader = csv.DictReader(csvfile, delimiter = ';')
  for linha in reader:
    id = int(linha['ID'])
    title = linha['Title']
    ano = linha['Year']
    idade = linha['Age']
    netflix = int(linha['Netflix'])
    hulu = int(linha['Hulu'])
    primeVideos = int(linha['Prime Video'])
    disney = int(linha['Disney+'])
    genero = linha['Genres']
    lingua= linha['Language']
    tempo = linha['Runtime']


    raiz = insere(no, id, title, ano, idade, netflix, hulu, primeVideos, disney, genero, lingua, tempo)


streamingPrint = ["Netflix:","Hulu:","Disney+:","Prime Video:"]
streaming = ["netflix", "hulu", "disney", "primeVideos"]

print("Streaming com mais filmes em 2020")
for i in range(len(streaming)):
    print(streamingPrint[i], filtro2(no,streaming[i],1,"ano","2020",0))

print("Streaming com mais filmes livres")
for i in range(len(streaming)):
    print(streamingPrint[i], filtro2(no,streaming[i],1,"idade","all",0))

print("Top 10 linguas com mais filmes")
print(dadosFinal("lingua",no, 10, True),"\n")


dadosGeneroFinal = dadosFinal("genero",no,15,True) #Recebe dados da função dadosFinal e seta para os 15 gêneros com mais filmes em ordem decrescente
plt.subplot(211) #Cria um subplot para o gráfico 1
plt.bar(*zip(*dadosGeneroFinal.items()), color = ["#ffd060","#ea593d","#44572a","#292411"]) #Recebe dados de gênero e quantidade de filmes da função dadosGeneroFinal, gera um gráfico de barras com esses dados e seta a cor de cada barra 
plt.xticks(rotation=75) #Rotaciona as legendas do gráfico 1 para 75º
plt.title("Quantidade de Filmes x Gênero") #Cria um titulo para o gráfico 1

dadosLinguasFinal = dadosFinal("lingua",no, 15, True) #Recebe dados da função dadosFinal e seta para os 15 línguas com mais filmes em ordem decrescente
plt.subplot(212) #Cria um subplot para o gráfico 2 
plt.bar(*zip(*dadosLinguasFinal.items()), color = ["#ffaa5f", "#ffe658","#311400","#7c7673"]) #Recebe dados de Línguas e quantidade de filmes da função dadosLinguasFinal, gera um gráfico de barras com esses dados e seta a cor de cada barra
plt.xticks(rotation=75) #Rotaciona as legendas do gráfico 2 para 75º
plt.title("Quantidade de Filmes x Línguas") #Cria um titulo para o gráfico 1
plt.tight_layout() #Redimensiona o layout dos sub plots
plt.show() # Imprime os gráficos