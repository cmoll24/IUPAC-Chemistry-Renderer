#Organic Chemistry
import turtle
import re

prefixes = ['meth','eth','prop','but','pent','hex','hept','oct','non','dec','undec','dodec'] 
greekL = ['di','tri','tetra'] + prefixes[4:]
suffixes = ['e','ol','al','one','oique']

def valid(molecule):
    #BEHOLD MY MONSTROSITY
    Npre = '(' + '|'.join(prefixes) + ')'
    Gpre = '(' + '|'.join(greekL) + ')'
    suf1 = '(' + '|'.join(suffixes[::2]) + ')' #suffixes that don't need a positional argument
    suf2 = '(' + '|'.join(suffixes[1::2]) + ')' #suffixes that need a positional argument
    
    nums = '(([0-9],?)+)-' #ex: 2,12,3,6
    rams = nums+Gpre+'?'+Npre+'yl' #ex: 2,2-dimethyl
    
    groups = nums+Gpre+'?'+suf2 #ex: -2,3-diol
    princ = Npre+'an('+suf1+'|(-'+groups+'))' #ex: propane, methanoique, butan-1,2-diol
    
    exp = r'(acide )?('+rams+'(-?))*'+princ #3-ethyl-2,2-dimethylhexan-4,5-diol
    
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


def drawMolecule(liste):
    wn = turtle.Screen()
    wn.bgcolor("#eeeee4")
    wn.title("PC Organic Chemistry")
    #<-code from https://stackoverflow.com/questions/44775445/python-turtle-window-on-top
    rootwindow = wn.getcanvas().winfo_toplevel()
    rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
    rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
    #->
    
    grid = 6
    deg = 360/grid
    size = 50

    turt = turtle.Turtle()
    turt.pensize(2)
    turt.up()

    offset = -(len(liste)-1)*43
    turt.setx(offset/2)
    
    #DRAW FIRST LINK
    turt.down()
    print(liste[0],len(liste[0]))
    if len(liste[0]) == 1:
        turt.write(liste[0][0], align="center")
        turt.seth(deg/2)
        turt.forward(size)
        
    elif len(liste[0]) == 2:
        turt.write(liste[0][0], align="center")
        turt.seth(deg/2)
        turt.forward(size)
        turt.right(deg)
        turt.backward(size)
        turt.write(liste[0][1], align="center")
        turt.forward(size)
    turt.up()
    turt.seth(deg/2)
    
    #DRAW CHAIN
    for C in liste[0:]:
        print(C,len(C))
        
        turt.down()
        if turt.heading() < 180:
            turt.right(deg)
        else:
            turt.left(deg)
        turt.forward(size)
        turt.up()
    
    turt.hideturtle()
    turtle.done()
    

#------------------- PROGRAMME -------------------

drawMolecule(
    [['O','OH'],[],[]]
    )

while True:
    molecule = input("Insert molecule name: ")

    if valid(molecule):
        break
    else:
        print("Please provide valid molecule.\n")

#----------------- ANALYSING MOLECULE -----------------
        
tempM = removeAcide(molecule)

#RAMMIFICATION
rammify = []

for i in range(tempM.count('yl')):
    ind = tempM.find('-')
    numb = getList(',', tempM[:ind])
    
    size = ind + 1
    
    greek = getElt(greekL, tempM[size:])
    
    repeat = 1
    if greek and tempM[size+len(greek):size+len(greek)+2] != 'yl':
        repeat = greekL.index(greek)+2
        size += len(greek)
    
    if len(numb) != repeat:
        print("ERROR")
    
    pre = getElt(prefixes, tempM[size:])
    
    if not pre:
        break
    
    size += len(pre)
    
    if tempM[size:size+2] != 'yl':
        break
    
    val = prefixes.index(pre)+1
    for i in range(repeat):
        rammify.append((int(numb[i]),val))
    tempM = tempM[size+2:]
    
    if tempM[0] == '-':
        tempM = tempM[1:]

print(rammify)

#CHAINE PRINCIPAL

pre = getElt(prefixes, tempM)
tempM = tempM[len(pre) + 2:]

if tempM[0] == '-':
    tempM = tempM[1:]

pos = 1
ind = tempM.find('-')
if ind > 0:
    pos = int(tempM[:ind])

suf = getElt(suffixes, tempM[ind+1:])

val = prefixes.index(pre)+1
group = suffixes.index(suf)
princ = (val,pos,group)
print(princ)


wn = turtle.Screen()
wn.bgcolor("#eeeee4")
wn.title("PC Organic Chemistry")
#<-code from https://stackoverflow.com/questions/44775445/python-turtle-window-on-top
rootwindow = wn.getcanvas().winfo_toplevel()
rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
#->

grid = 6
deg = 360/grid
size = 50

turt = turtle.Turtle()
turt.pensize(2)
turt.up()

offset = -(princ[0]-1)*43
turt.setx(offset/2)
turt.seth(deg/2)

Cpos = []

direct = 1
turt.down()
for i in range(princ[0]-1):
    Cpos.append((turt.pos(),direct))
    turt.right(direct * deg)
    turt.forward(size)
    direct = -direct
Cpos.append((turt.pos(),direct))
turt.up()

for ram in rammify:
    C = Cpos[ram[0]-1]
    turt.setpos(C[0])
    turt.setheading(C[1] * 90)
    
    turt.down()
    direct = 1
    for i in range(ram[1]):
        turt.forward(size)
        turt.right(direct * deg)
        direct = -direct
    turt.up()
        
turt.hideturtle()
turtle.done()
