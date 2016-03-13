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
    
    def __add__(self,other): #Additionner 2 points : p+q
        return Point(self.xP+other.xP,self.yP+other.yP,self.zP+other.zP)
    
    def __mul__(self,n):#Multiplier un point par un nombre : p*2
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __rmul__(self,n):#Multiplier un point par un nombre : 2*p
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __truediv__(self,n):#Diviser un point par un nombre
        return Point(self.xP/n,self.yP/n,self.zP/n)
    
    def __xor__(self,other):# Produit vectoriel : p^q
        L1=[self.xP,self.yP,self.zP]  
        L2=[other.xP,other.yP,other.zP]
        return Point(L1[1]*L2[2]-L1[2]*L2[1],L1[2]*L2[0]-L1[0]*L2[2],L1[0]*L2[1]-L1[1]*L2[0])
    
    def __and__(self,other):#Produit scalaire : p & q
        L1=[self.xP,self.yP,self.zP]  
        L2=[other.xP,other.yP,other.zP]
        return L1[0]*L2[0]+L1[1]*L2[1]+L1[2]*L2[2]
        
    def setAbs(self,x): #changement d'abscisse
        self.xP=x
        
    def setOrd(self,y): #changement d'ordonnée
        self.yP=y
        
    def setAlt(self,z): #changement d'ordonnée)        
        self.zP=z
        
    def setCoord(self,x,y,z): #changement de coordonnées
        self.xP=x
        self.yP=y
        self.zP=z
        
    def dist(self,andPkt): #distance d'un point à un autre : andPkt pour "andere Punkt"
        return(pow((self.xP - andPkt.xP)**2+(self.yP - andPkt.yP)**2+(self.zP - andPkt.zP)**2,1/2)) #j'utilise pow vu que sqrt déconne
        
        #VOIR : Classe Point.py pour les modifs

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

    
class Tetraedre:
    """ Définit un tétraèdre à partir d'un point et d'un triangle. Utilisation : T = Tetraedre(D=Point(x4,y4,z4), T=Triangle(A=Point(x1,y1,z1), B=Point(x2,y2,z2), C=Point(x3,y3,z3)))
     Commandes : elles s'utilisent toutes comme T.commande() avec éventuellement des arguments, sauf str
     - str, pour afficher le tétraèdre (str(T)), rend : [(x1,y1,z1),(x2,y2,z2),(x3,y3,z3),(x4,y4,z4)]
     - setCoord1, setAbs1, setOrd1, setAlt1, idem que pour Point et Triangle
     - setCoord2, setAbs2, setOrd2, setAlt2
     - setCoord3, setAbs3, setOrd3, setAlt3
     - setCoord4, setAbs4, setOrd4, setAlt4
     - setCoordAll pour faire tout d'un coup
     - Face0, Face1, Face2, Face3 qui permettent de définir le triangle formé par chaque face, utilisation : U=T.Face0() (Ne pas oublier les parenthèses !!)
     Pour les dernières, en tapant F0=Triangle(T.point1,T.point2,T.point3) ça fonctionne aussi.
    """
    def __init__(self, D=Point(0,0,1), T=Triangle(A=Point(0,0,0), B=Point(1,1,0), C=Point(2,-1,0))): #sans le triangle?
    #def __init__(self, D=Point(0,0,1), A=Point(0,0,0), B=Point(1,1,0), C=Point(2,-1,0)): #ça marche!
        self.point1=T.point1 #T.A marche pas?
        self.point2=T.point2
        self.point3=T.point3
        self.point4=D
        self.absPoint1=T.point1.xP #bien penser à prendre les bons objets ! A,B,C n'existent "pas" en tant que tels, ils font partie de T, faut aller les chercher là
        self.absPoint2=T.point2.xP
        self.absPoint3=T.point3.xP
        self.absPoint4=D.xP
        self.ordPoint1=T.point1.yP
        self.ordPoint2=T.point2.yP
        self.ordPoint3=T.point3.yP
        self.ordPoint4=D.yP
        self.altPoint1=T.point1.zP
        self.altPoint2=T.point2.zP
        self.altPoint3=T.point3.zP
        self.altPoint4=D.zP
        self.__d1=self.point1.dist(self.point2)
        self.__d2=self.point2.dist(self.point3)
        self.__d3=self.point3.dist(self.point1)
        self.__d4=self.point4.dist(self.point1)
        self.__d5=self.point4.dist(self.point2)
        self.__d6=self.point4.dist(self.point3)
        
    def __str__(self):
        return("["+str(self.point1) + "," + str(self.point2) + "," + str(self.point3) + "," + str(self.point4)+"]")
    
    def Face0(self): #face de base à partir du triangle de base #marche pas. mais à la patte ça fonctionne !
        return(Triangle(self.point1,self.point2,self.point3))
    def Face1(self):
        return(Triangle(Point(self.point1.xP,self.point1.yP,self.point1.zP),Point(self.point2.xP,self.point2.yP,self.point2.zP),Point(self.point4.xP,self.point4.yP,self.point4.zP)))
    def Face2(self):
        return(Triangle(Point(self.point1.xP,self.point1.yP,self.point1.zP),Point(self.point3.xP,self.point3.yP,self.point3.zP),Point(self.point4.xP,self.point4.yP,self.point4.zP)))
    def Face3(self):
        return(Triangle(Point(self.point2.xP,self.point2.yP,self.point2.zP),Point(self.point3.xP,self.point3.yP,self.point3.zP),Point(self.point4.xP,self.point4.yP,self.point4.zP)))    

