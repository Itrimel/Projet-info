# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 21:05:03 2016

@author: User
"""

class Point:
    from math import sqrt
    def __init__(self, xP=0, yP=0): #valeurs par défaut : (0,0)
        self.xP=xP
        self.yP=yP
        
    def __str__(self): #affichage
        return(str((self.xP,self.yP))) 
        
    def setAbs(self,x): #changement d'abscisse
        self.xP=x
        
    def setOrd(self,y): #changement d'ordonnée
        self.yP=y
        
    def setCoord(self,x,y): #changement de coordonnées
        self.xP=x
        self.yP=y
        
    def dist(self,andPkt): #distance d'un point à un autre : andPkt pour "andere Punkt"
        return(sqrt((self.xP - andPkt.xP)**2+(self.yP - andPkt.yP)**2))

def AireTri(A,B,C):
    from math import sqrt
    a=A.dist(B)
    b=B.dist(C)
    c=C.dist(A)
    s=(a+b+c)/2
    Aire=sqrt(s*(s-a)*(s-b)*(s-c))
    return(Aire)