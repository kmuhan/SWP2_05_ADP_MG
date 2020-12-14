def acesCalc(dicelist):
    ones = dicelist.count(1)
    n = ones * 1
    return n

def twosCalc(dicelist):
    twos = dicelist.count(2)
    n = twos * 2
    return n

def threesCalc(dicelist):
    threes = dicelist.count(3)
    n = threes * 3
    return n

def foursCalc(dicelist):
    fours = dicelist.count(4)
    n = fours * 4
    return n

def fivesCalc(dicelist):
    fives = dicelist.count(5)
    n = fives * 5
    return n

def sixesCalc(dicelist):
    sixes = dicelist.count(6)
    n = sixes * 6
    return n

def choiceCalc(dicelist):
    n = sum(dicelist)
    return n

def fourofakindCalc(dicelist):
    list1 = sorted(dicelist)
    list2 = []
    for num in range(1, 7):
        numCount = list1.count(num)
        list2.append(numCount)
    n = sum(dicelist)

    if 4 in list2 and 1 in list2:
        return n
    else:
        return 0

def fullhouseCalc(dicelist):
    list1 = sorted(dicelist)
    list2 = []
    for num in range(1, 7):
        numCount = list1.count(num)
        list2.append(numCount)

    if 2 in list2 and 3 in list2:
        return 25
    else:
        return 0

def littlestraightCalc(dicelist):
    list1=sorted(dicelist)
    list2=[]
    for i in list1:
        if i not in list2:
            list2.append(i)

    if list2[0:4] == [1,2,3,4] or list2[0:4] == [2,3,4,5] or list2[0:4] == [3,4,5,6]:
        return 30
    else:
        return 0

def bigstraightCalc(dicelist):
    list1 = sorted(dicelist)
    list2 = []
    for i in list1:
        if i not in list2:
            list2.append(i)

    if list2[0:5] == [1, 2, 3, 4,5] or list2[0:5] == [2, 3, 4, 5,6]:
        return 40
    else:
        return 0


def yachtCalc(dicelist):
    list1=(dicelist)
    list2 = []
    for i in list1:
        if i not in list2:
            list2.append(i)

    if len(list2)== 1:
        return 50
    else:
        return 0