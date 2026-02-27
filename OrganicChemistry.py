#Organic Chemistry
import turtle
import re

prefixes = ['meth','eth','prop','but','pent','hex','hept','oct','non','dec','undec','dodec'] 
greekL = ['di','tri','tetra'] + [elt + 'a' for elt in prefixes[4:]]
suffixes = {'e':[],'ol':['OH'],'al':['O'],'one':['O'],'oique':['O','OH']}

GRID = 6
DEG = 360/GRID
SIZE = 50

def valid(molecule):
    #BEHOLD MY MONSTROSITY
    Npre = '(' + '|'.join(prefixes) + ')'
    Gpre = '(' + '|'.join(greekL) + ')'
    suf1 = '(' + '|'.join(list(suffixes)[::2]) + ')' #suffixes that don't need a positional argument
    suf2 = '(' + '|'.join(list(suffixes)[1::2]) + ')' #suffixes that need a positional argument
    
    nums = '(([0-9],?)+)-' #ex: 2,12,3,6
    rams = nums+Gpre+'?'+Npre+'yl' #ex: 2,2-dimethyl
    
    groups = nums+Gpre+'?'+suf2 #ex: -2,3-diol
    princ = Npre+'an('+suf1+'|(-'+groups+'))' #ex: propane, methanoique, butan-1,2-diol
    
    exp = r'(acide )?('+rams+'(-?))*'+princ #3-ethyl-2,2-dimethylhexan-4,5-diol]
    
    ind = re.fullmatch(exp,molecule)

    if ind == None:
        return False
    return True

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

def drawElt(elt, t):
    if type(elt) == str:
        t.write(elt, align="center", font=('Arial', 12, 'bold'))
    elif type(elt) == int:
        tempPos = t.pos()
        tempHead = t.heading()
        d = 1
        t.down()
        for i in range(elt-1):
            t.right(d*DEG)
            d = -d
            t.forward(SIZE)
        t.up()
        t.setpos(tempPos)
        t.seth(tempHead)
        t.down()

def drawMolecule(liste):
    wn = turtle.Screen()
    wn.bgcolor("#eeeee4")
    wn.title("PC Organic Chemistry")
    #<-code from https://stackoverflow.com/questions/44775445/python-turtle-window-on-top
    rootwindow = wn.getcanvas().winfo_toplevel()
    rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
    rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
    #->

    turt = turtle.Turtle()
    turt.pensize(2)
    turt.up()

    offset = -(len(liste)-1)*43
    turt.setx(offset/2)
    
    #DRAW FIRST LINK
    turt.down()
    if len(liste[0]) >= 1:
        drawElt(liste[0][0], turt)
        turt.seth(DEG/2)
        turt.forward(SIZE)
        
    if len(liste[0]) >= 2:
        turt.right(DEG*2)
        turt.backward(SIZE)
        drawElt(liste[0][1], turt)
        turt.forward(SIZE)
        turt.left(DEG)
    turt.up()
    turt.seth(DEG/2)
    
    #DRAW CHAIN
    for C in liste[1:-1]:
        turt.down()
        if turt.heading() < 180:
            turt.right(DEG)
        else:
            turt.left(DEG)
            
        if len(C) >= 0:
            turt.forward(SIZE)
        if len(C) == 1:
            turt.left(sign(turt.heading()) * 60)
            turt.forward(SIZE)
            drawElt(C[0], turt)
            turt.backward(SIZE)
            turt.right(sign(turt.heading()) * 60)
        if len(C) == 2:
            turt.left(sign(turt.heading()) * 90)
            turt.forward(SIZE)
            drawElt(C[0], turt)
            turt.backward(SIZE)
            turt.right(sign(turt.heading()) * 180)
            turt.forward(SIZE)
            drawElt(C[1], turt)
            turt.backward(SIZE)
            turt.right(sign(turt.heading()) * 150)
        turt.up()  
    
    #DRAW LAST
    if len(liste) > 1:
        turt.down()
        if turt.heading() < 180:
            turt.right(DEG)
        else:
            turt.left(DEG)
        
        if len(liste[-1]) == 0:
            turt.forward(SIZE)
        
        if len(liste[-1]) >= 1:
            drawElt(liste[-1][0], turt)
            turt.seth(DEG/2)
            turt.forward(SIZE)
            
        if len(liste[-1]) >= 2:
            turt.backward(SIZE)
            turt.right(DEG)
            turt.forward(SIZE)
            drawElt(liste[-1][-1], turt)
        turt.up()
    turt.hideturtle()
    turtle.done()

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

    print(rammify)

    #CHAINE PRINCIPAL

    print(tempM)

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

while True:
    molecule_name = input("Insert molecule name: ").lower()

    if valid(molecule_name):
        break
    else:
        print("Please provide valid molecule.\n")

tableau = parseMolecule(molecule_name)

print(tableau)

drawMolecule(tableau)
