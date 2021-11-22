import math
from constraint import *

def pomocnaF(vektor):
        suma=0
        lista=[]
        n=len(vektor)
        i=0
        while(i<n):
            
            if(vektor[i]==1):
                while(i<n and vektor[i]==1):
                    suma+=1
                    i+=1
                lista.append(suma)
            suma=0
            i+=1
        return lista


def dodajConstaint(problem : Problem, uslov, promenljive):
    def o1(*niz):
        return pomocnaF(niz) == uslov
    problem.addConstraint(o1, promenljive)
    



def ucitajPodatke(n):
    redovi = []
    kolone = []
    for i in range(n):
        linija = input().strip()
        if linija[0] == '[':
            linija = linija[1:-1]
        tokeni = [int(x.strip()) for x in linija.split(',')]
        redovi.append(tokeni)
    for i in range(n):
        linija = input().strip()
        if linija[0] == '[':
            linija = linija[1:-1]
        tokeni = [int(x.strip()) for x in linija.split(',')]
        kolone.append(tokeni)

    return redovi, kolone


def upisiNaPrvaIPoslednjaNRed(matrica, i, p, indMatrica):
    n = len(matrica[0])
    red = [1 for i in range(n)]
    red[:p] = [0 for i in range(p)]
    red[n-p:] = [0 for i in range(p)]
    matrica[i] = red
    indMatrica[i] = [x==1 for x in red]

def upisiNaPrvaIPoslednjaNKolona(matrica, i, p, indMatrica):
    n = len(matrica[0])
    for j in range(p,n-p,1):
        matrica[j][i] = 1
        indMatrica[j][i] = True

def upisiSigurne1(matrica, redovi, kolone, indMatrica):
    n = len(redovi)
    granica = math.floor(n/2)
    for i, red in enumerate(redovi):
        if len(red) > 1:
            continue
        el = red[0]
        if granica < el:
            upisiNaPrvaIPoslednjaNRed(matrica, i, n-el, indMatrica)
    for i, kolona in enumerate(kolone):
        if len(kolona) > 1:
            continue
        el = kolona[0]
        if granica < el:
            upisiNaPrvaIPoslednjaNKolona(matrica, i, n-el, indMatrica)

def iscrtajRed(matrica,red,i, indMatrica):
    novi = [1 for j in range(len(matrica[0]))]
    suma = 0
    for el in red[:-1]:
        suma += el
        novi[suma] = 0
        suma += 1
    matrica[i] = novi
    indMatrica[i] = [True for j in range(len(matrica[0]))]

def iscrtajKolonu(matrica,kolona,i,indMatrica):
    n = len(matrica[0])
    suma = 0
    for j in range(n):
        matrica[j][i] = 1
        indMatrica[j][i] = True
    for el in kolona[:-1]:
        suma += el
        matrica[suma][i] = 0
        suma += 1
    
def upisiSigurne2(matrica, redovi, kolone, indMatrica):
    n = len(redovi)
    for i,red in enumerate(redovi):
        if sum(red) + len(red) == n+1 and len(red) != 1:
            iscrtajRed(matrica, red, i, indMatrica)
    for i,kolona in enumerate(kolone):
        if sum(kolona) + len(kolona) == n+1 and len(kolona) != 1:
            iscrtajKolonu(matrica, kolona, i, indMatrica)

def iscrtajMapu(resenje, n):
    for i in range(n):
        for j in range(n):
            print(str(resenje[f'p{i}{j}']) + " ", end = "")
        print()

if __name__ == '__main__':
    n = int(input("unesite N\n"))
    redovi, kolone = ucitajPodatke(n)

    matrica = [[0 for i in range(n)] for i in range(n)]

    #inicijalizacija i domen 
    problem = Problem()
    for i in range(n):
        for j in range(n):
            problem.addVariable(f"p{i}{j}", [0,1])
    problem.addVariable('a', [1])
    problem.addVariable('b', [0])

    promenljivePoRedovima = []    
    promenljivePoKolonama = [] 
    for i in range(n):
        pomocna = [f'p{i}{j}' for j in range(n)]
        promenljivePoRedovima.append(pomocna)
        pomocna2 = [f'p{j}{i}' for j in range(n)]
        promenljivePoKolonama.append(pomocna2)

    indMatrica = [[False for i in range(n)] for i in range(n)]
    upisiSigurne1(matrica,redovi,kolone, indMatrica)
    upisiSigurne2(matrica,redovi,kolone, indMatrica)

    for i in range(n):
        for j in range(n):
            if indMatrica[i][j]:
                if matrica[i][j] == 0:
                    problem.addConstraint(lambda a, b: a == b, [f"p{i}{j}", 'b'])
                if matrica[i][j] == 1:
                    problem.addConstraint(lambda a, b: a == b, [f"p{i}{j}", 'a'])


    for i in range(n):
        uslov = redovi[i]
        dodajConstaint(problem, uslov, promenljivePoRedovima[i])
        
    for i in range(n):
        uslov = kolone[i]
        dodajConstaint(problem, uslov, promenljivePoKolonama[i])

    resenja = problem.getSolutions()
    for resenje in resenja:
        iscrtajMapu(resenje, n)

    