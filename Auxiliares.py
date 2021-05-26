
def ReadTemp(a,b):
    with open(a, 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
    temp1=last_line
    f.close()
    with open(b, 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
    temp2=last_line
    f.close()
    return temp1, temp2

def ReadPres(a):
    with open(a, 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
    pres=last_line
    f.close()
    return pres

def Medidas(a,b,c):
    
    t1, t2 = ReadTemp(a, b)
    p1 = ReadPres(c)

    t1=t1.split('+')
    t2=t2.split('+')
    p1=p1.split(',')

    time1 = t1[0]
    time2 = t2[0]
    time3 = p1[0]
    
    valores=[t1,t2,p1]
    
    d1 = "\nDiodo 1: " + str(t1[1]) + "K"
    d2 = "\nDiodo 2: " + str(t1[2]) + "K"
    d3 = "\nDiodo 3: " + str(t1[3]) + "K"
    d4 = "\nDiodo 4: " + str(t1[4]) + "K"
    c5 = "\nCernox 5: " + str(t1[5]) + "K"
    c6 = "\nCernox 6: " + str(t1[6]) + " K"
    ca = "\nCernox A: " + str(t2[1]) + "K" 
    cb = "\nCernox B: " + str(t2[2]) + " K"
    pf = "\nMKS Sensor: " + str(p1[1]) + " Torr"

    return d1, d2, d3, d4, c5, c6, ca, cb, pf , time1, time2, time3, valores