from random import *
from numpy import *

def milieu_triangle (Triangle(p1,p2,p3)) :
    C=Point(0,0,0) #somme des sommets du triangle
    C=Point((xp1+xp2+xp3)/3,(yp1+yp2+yp3)/3,(zp1+zp2+zp3)/3)#C devient le centre du triangle
    return (C)


def Normale(Triangle(p1,p2,p3), distance):
    u=array([xp1-px2),(yp1-yp2),(zp1-zp2)])#On calcule les deux vecteurs
    v=array([xp1-px3),(yp1-yp3),(zp1-zp3)])
    #Voilà fifi le produit vectoriel
    w=array([(yp1-yp2)*(zp1-zp3)-(zp1-zp3)*(yp1-yp3),(zp1-zp2)*(xp1-xp3)-(xp1-xp3)*(zp1-zp3),(xp1-xp2)*(yp1-yp3)-(yp1-yp3)*(xp1-xp3)])
    p4=milieu_triangle(Triangle(p1,p2,p3)+ w*distance#point sur la normale
    return(p4)
