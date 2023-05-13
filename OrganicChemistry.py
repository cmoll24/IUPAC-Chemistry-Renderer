import turtle

#Organic Chemistry
import re

prefixes = ['meth','eth','prop','but','pent','hex','hept','oct','non','dec','undec','dodec'] 
greekL = ['di','tri','tetra'] + prefixes[4:]
suffixes = ['e','ol','al','one','oique']

def valid(molecule):
    #BEHOLD MY MONSTROSITY
    Npre = '(' + '|'.join(prefixes) + ')'
    Gpre = '(' + '|'.join(greekL) + ')'
    suf = '(' + '|'.join(suffixes) + ')'
    ind = re.fullmatch(
        r'((([0-9],?)+)-'+Gpre+'?'+Npre+'yl(-?))*'+Npre+'an'+'(-([0-9]+)-)?'+suf,
        molecule)

    if ind == None:
        return False
    return True

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

#------------------- PROGRAMME -------------------

while True:
    molecule = input("Insert molecule name: ")

    if valid(molecule):
        break
    else:
        print("Please provide valid molecule.\n")

#RAMMIFICATION
rammify = []
tempM = molecule

for i in range(tempM.count('yl')):
    ind = tempM.find('-')
    numb = getList(',', tempM[:ind])
    
    size = ind + 1
    
    greek = getElt(greekL, tempM[size:])
    
    repeat = 1
    if greek:
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
wn.bgcolor("#90EE90")
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
