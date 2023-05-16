#Micro Python for Numworks
from turtle import *

prefixes = ['meth','eth','prop','but','pent','hex','hept','oct','non','dec','undec','dodec'] 
greekL = ['di','tri','tetra'] + [elt + 'a' for elt in prefixes[4:]]
suffixes = {'e':[],'ol':['OH'],'al':['O'],'one':['O'],'oique':['O','OH']}

GRID = 6
DEG = 360/GRID
SIZE = 20

def removeAcide(mol):
    if mol[:6] == 'acide ':
        if mol[-5:] == suffixes[4]:
            mol = mol[6:]
        else:
            print('ERROR not acide')
    
    return mol

def getElt(liste, mol):
    for elt in liste:
        if mol.find(elt) == 0:
            return elt
    return None

def getList(link, string):
    liste = []
    temp = ''
    for x in string:
        if x != link:
            temp += x
        else:
            liste.append(temp)
            temp = ''
    if temp != '':
        liste.append(temp)
    return liste

def getNumbs(string):
    ind = string.find('-')
    numb = getList(',', string[:ind])
    string = string[ind+1:]
    
    numb = [int(elt) for elt in numb]
    
    return numb, string

def getRepeat(string):
    greek = getElt(greekL, string)
    
    repeat = 1
    if greek:
        repeat = greekL.index(greek)+2
        string = string[len(greek):]
    
    return repeat, string

def sign(degrees):
    if degrees > 180:
        return -1
    else:
        return 1

def drawElt(elt):
    if type(elt) == str:
        write(elt)
    elif type(elt) == int:
        tempPos = position()
        tempHead = heading()
        d = 1
        pendown()
        for i in range(elt-1):
            right(d*DEG)
            d = -d
            forward(SIZE)
        penup()
        goto(tempPos)
        setheading(tempHead)
        pendown()

def drawMolecule(liste):
    reset()
    pensize(2)
    penup()

    offset = -(len(liste)-1)*SIZE
    goto(offset/2,5)
    
    #DRAW FIRST LINK
    pendown()
    if len(liste[0]) >= 1:
        drawElt(liste[0][0])
        setheading(DEG/2)
        forward(SIZE)
        
    if len(liste[0]) >= 2:
        right(DEG*2)
        backward(SIZE)
        drawElt(liste[0][1])
        forward(SIZE)
        left(DEG)
    penup()
    setheading(DEG/2)
    
    #DRAW CHAIN
    for C in liste[1:-1]:
        pendown()
        if heading() < 180:
            right(DEG)
        else:
            left(DEG)
            
        if len(C) >= 0:
            forward(SIZE)
        if len(C) == 1:
            left(sign(heading()) * 60)
            forward(SIZE)
            drawElt(C[0])
            backward(SIZE)
            right(sign(heading()) * 60)
        if len(C) == 2:
            left(sign(heading()) * 90)
            forward(SIZE)
            drawElt(C[0])
            backward(SIZE)
            right(sign(heading()) * 180)
            forward(SIZE)
            drawElt(C[1])
            backward(SIZE)
            right(sign(heading()) * 150)
        penup()
        
        
    #DRAW LAST LINK
    pendown()
    if heading() < 180:
        right(DEG)
    else:
        left(DEG)
    
    if len(liste[-1]) == 0:
        forward(SIZE)
    
    if len(liste[-1]) >= 1:
        drawElt(liste[-1][0])
        setheading(DEG/2)
        forward(SIZE)
        
    if len(liste[-1]) >= 2:
        backward(SIZE)
        right(DEG)
        forward(SIZE)
        drawElt(liste[-1][-1])
    penup()
    hideturtle()

def parseMolecule(mol):
    tempM = mol
    
    #RAMMIFICATION
    rammify = []

    for i in range(tempM.count('yl')):
        numb, tempM = getNumbs(tempM)
        repeat, tempM= getRepeat(tempM)
        
        if len(numb) != repeat:
            print("ERROR: {} doesn't match {}".format(len(numb),repeat))
        
        pre = getElt(prefixes, tempM)
        tempM = tempM[len(pre):]
        
        val = prefixes.index(pre)+1
        for i in range(repeat):
            rammify.append((numb[i],val))
        tempM = tempM[2:]
        
        if tempM[0] == '-':
            tempM = tempM[1:]

    #CHAINE PRINCIPAL

    pre = getElt(prefixes, tempM)
    tempM = tempM[len(pre) + 2:]

    numb = [1] #when the ending is suf1
    if tempM[0] == '-':
        numb, tempM = getNumbs(tempM[1:])
        repeat, tempM= getRepeat(tempM)
        if len(numb) != repeat:
            print("ERROR: {} doesn't match {}".format(len(numb),repeat))

    suf = getElt(suffixes, tempM)

    val = prefixes.index(pre)+1

    tableau = [[] for i in range(val)]
    for elt in rammify:
        tableau[elt[0]-1].append(elt[1])

    for i in numb:
        for atom in suffixes.get(suf):
            tableau[i-1].append(atom)
    
    return tableau


#------------------- PROGRAMME -------------------

def chem(size = 20):
    
    global GRID,DEG,SIZE
    
    GRID = 6
    DEG = 360/GRID
    SIZE = size
    
    molecule = input("Insert molecule name: ").lower()
    tableau = parseMolecule(molecule)
    print(tableau)

    drawMolecule(tableau)
