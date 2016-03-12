class Point:
    """ Définit un point avec trois coordonnées (x,y,z). Utilisation : A=Point(x,y,z) 
     Commandes : elles s'utilisent toutes comme A.commande() avec éventuellement des arguments, sauf str 
     - str , pour afficher le point (str(A)), rend : (x,y,z)
     - setAbs (changement d'abscisse) 
     - setOrd (changement d'ordonnée) 
     - setAlt (changement d'altitude) 
     - setCoord (changement des 3 coordonnées) 
     - dist (distance entre deux points) """
    def __init__(self, xP=0, yP=0, zP=0): #valeurs par défaut : (0,0,0)
        self.xP=xP
        self.yP=yP
        self.zP=zP
        
    def __str__(self): #affichage
        return(str((self.xP,self.yP,self.zP))) 
        
class Triangle:
    """ Définit un triangle à partir de trois points (classe Point). Utilisation : T=Triangle(A=Point(x1,y1,z1),B=Point(x2,y2,z2),C=Point(x3,y3,z3))
     Commandes : elles s'utilisent toutes comme T.commande() avec éventuellement des arguments, sauf str 
     - str, pour afficher le triangle (str(T)), rend : [(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)]
     - setCoord1, setAbs1, setOrd1, setAlt1, idem que pour Point
     - setCoord2, setAbs2, setOrd2, setAlt2 
     - setCoord3, setAbs3, setOrd3, setAlt3
     - getPer pour avoir le périmètre
     - Milieux pour avoir les trois milieux sous forme de liste ([0] : 1-2, [1] : 2-3, [2] : 3-1)
    """
    def __init__(self, A=Point(0,0,0), B=Point(1,1,0), C=Point(2,-1,0)): #test sans noms : NON
        self.point1=A
        self.point2=B
        self.point3=C
        self.absPoint1=A.xP
        self.absPoint2=B.xP
        self.absPoint3=C.xP
        self.ordPoint1=A.yP
        self.ordPoint2=B.yP
        self.ordPoint3=C.yP
        self.altPoint1=A.zP
        self.altPoint2=B.zP
        self.altPoint3=C.zP
        self.__d1=self.point1.dist(self.point2)
        self.__d2=self.point2.dist(self.point3)
        self.__d3=self.point3.dist(self.point1)
        
    def __str__(self):
        return("["+str(self.point1) + "," + str(self.point2) + "," + str(self.point3)+"]")
        
    def Milieux(self): #ça retourne les milieux des côtés.)
        M1=Point((self.point1.xP+self.point2.xP)/2,(self.point1.yP+self.point2.yP)/2,(self.point1.zP+self.point2.zP)/2))
        M2=Point((self.point2.xP+self.point3.xP)/2,(self.point2.yP+self.point3.yP)/2,(self.point2.zP+self.point3.zP)/2))
        M3=Point((self.point3.xP+self.point1.xP)/2,(self.point3.yP+self.point1.yP)/2,(self.point3.zP+self.point1.zP)/2))
        return([M1,M2,M3])

def milieu_triangle (T) :
    C=Point(0,0,0) #somme des sommets du triangle
    C=Point((T.point1.xP+T.point2.xP+T.point3.xP)/3,(T.point1.yP+T.point2.yP+T.point3.yP)/3,(T.point1.zP+T.point2.zP+T.point3.zP)/3)#C devient le centre du triangle
    return(C)

from numpy import *
from math import *
from random import *

def NormaleN(T,distance): #mit numpy
    M=milieu_triangle(T).numpy#Expression des données dans un format permettant de faire des calculs plus facilement
    L=T.Milieux()
    M0=L[0].numpy #points milieux
    M1=L[1].numpy
    M2=L[2].numpy
    p1=T.point1.numpy
    p2=T.point2.numpy
    p3=T.point3.numpy
    u=p1-p2#On calcule les deux vecteurs
    v=p1-p3
    #Voilà fifi le produit vectoriel
    w=np.cross(u,v)
    norme=np.linalg.norm(w)#Norme de w
    w=w/norme#w est maintenant normé
    p4=M+distance*w#point sur la normale
    M3=M0+distance*random()*w #on bouge les milieux
    M4=M1+distance*random()*w
    M5=M2+distance*random()*w
    p4=Point(p4[0],p4[1],p4[2])
    M3=Point(M3[0],M3[1],M3[2])
    M4=Point(M4[0],M4[1],M4[2])
    M5=Point(M5[0],M5[1],M5[2])
    return([p4,M3,M4,M5])
    
def Normale(T,distance): #sans Numpy
    M=milieu_triangle(T)
    L=T.Milieux()
    M0=L[0] #points milieux
    M1=L[1]
    M2=L[2]
    p1=T.point1
    p2=T.point2
    p3=T.point3
    u=array([(p1.xP-p2.xP),(p1.yP-p2.yP),(p1.zP-p2.zP)])#On calcule les deux vecteurs
    v=array([(p1.xP-p3.xP),(p1.yP-p3.yP),(p1.zP-p3.zP)])
    #Voilà fifi le produit vectoriel
    w=array([(u[1])*(v[2])-(u[2])*(v[1]),(u[2])*(v[0])-(u[0])*(v[2]),(u[0])*(v[1])-(u[1])*(v[0])])
    n=pow(w[0]**2+w[1]**2+w[2]**2,1/2) #norme de w
    #w=[w[0]/n,w[1]/n,w[2]/n] #pour les listes classiques
    w=w/n #avec array, ça marche
    p4=Point(M.xP + w[0]*distance, M.yP + w[1]*distance, M.zP + w[2]*distance)
    k=random()
    M3=Point(M0.xP + w[0]*distance*k, M0.yP + w[1]*distance*k, M0.zP + w[2]*distance*k)
    M4=Point(M1.xP + w[0]*distance*k, M1.yP + w[1]*distance*k, M1.zP + w[2]*distance*k)
    M5=Point(M2.xP + w[0]*distance*k, M2.yP + w[1]*distance*k, M2.zP + w[2]*distance*k)#point sur la normale
    return([p4,M3,M4,M5])    

def DeuxiemeRound(T,distance):
    C1=Normale(T,distance)[0]
    M3=Normale(T,distance)[1]
    M4=Normale(T,distance)[2]
    M5=Normale(T,distance)[3]
    T1=Triangle(T.point1,M3,C1) #création des 6 nouveaux triangles
    T2=Triangle(T.point2,M3,C1) #→ prendre les éléments T.point1 et T.point2 pour la suite !
    T3=Triangle(T.point2,M4,C1)
    T4=Triangle(T.point3,M4,C1)
    T5=Triangle(T.point3,M5,C1)
    T6=Triangle(T.point1,M5,C1)
    return([T1,T2,T3,T4,T5,T6])
    
