# -*- coding: utf-8 -*-
#Nécessite Pyhton 2 avec le module mayavi installé
from random import * #Utilisé pour le calcul de la distance, à l'aide d'un générateur gaussien
import numpy as np
import os #Module pour rennomer le fichier à la fin
from mayavi import mlab #Module pour générer le dessin
import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit où enregistrer
class Point:
    def __init__(self, xP=0, yP=0, zP=0): #valeurs par défaut : (0,0,0)
        self.xP=xP
        self.yP=yP
        self.zP=zP
        self.numpy=np.array([self.xP,self.yP,self.zP])
class Triangle:
    def __init__(self, A=Point(0,0,0), B=Point(1,1,0), C=Point(2,-1,0)): 
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


def milieu_triangle (T) :
    '''Retourne sous forme d'un ponit le centre du triangle donné en argument'''
    C=Point(0,0,0) #somme des sommets du triangle
    C=Point((T.point1.xP+T.point2.xP+T.point3.xP)/3,(T.point1.yP+T.point2.yP+T.point3.yP)/3,(T.point1.zP+T.point2.zP+T.point3.zP)/3)#C devient le centre du triangle
    return(C)

    
def Normale(T, distance,centre):
    '''Retourne trois triangles issus du triangle T dont le centre a été déplacé de la distance distance.
       L'argument centrepermet de déterminer l'intérieur de la structure'''
    M=milieu_triangle(T).numpy#Expression des données dans un format permettant de faire des calculs plus facilement
    p1=T.point1.numpy
    p2=T.point2.numpy
    p3=T.point3.numpy
    centre=centre.numpy
    u=p1-p2#On calcule les deux vecteurs
    v=p1-p3
    #Voilà fifi le produit vectoriel
    w=np.cross(u,v)
    norme=np.linalg.norm(w) #Norme de w 
    w=w/norme #w est maintenant normé   
    a=centre-M #Vecteur allant du centre du triangle au point centre, qui est à l'interieur de la structure    
    if np.dot(w,a)>0: #On fait le produit scalaire des 2 vecteurs. Si le produit scalaire est positif, cela signifie que les 2 vecteurs sont environ du même sens, donc que w pointe vers l'interieur
        w=-1*w #On prend l'opposé de w, qui pointe alors vers l'exterieur
    p4=M+distance*w# point sur la normale   
    p4=Point(p4[0],p4[1],p4[2])
    return(p4)
    
def creation_triangle(T,distance,centre):
    C=Normale(T,distance,centre)
    T1=Triangle(T.point1,T.point2,C)
    T2=Triangle(T.point1,T.point3,C)
    T3=Triangle(T.point2,T.point3,C)
    return[T1,T2,T3] #retourner les triangles dans une liste pour être compatible avec la boucle principale

def creation_image(liste,save="True",chemin="ask"):
	'''Créé le dessin, à partir de la liste entréé. 
	La variable save gère si l'image est enregistrée (Par défaut,oui), à l'emplacement "chemin". Par défaut,l'emplacement est demandé à l'utilisateur'''
	X=[]#Initialisation des 3 listes contenant les coordonnées des sommets des triangles
	Y=[]
	Z=[]
	tri=[(3*i,3*i+1,3*i+2) for i in range(len(liste))]#Liste contenant les triplets correspondant aux sommets de chaque triangle. Par exemple, pour le premier triangle, on a (0,1,2), les 3 premiers points de la liste
	for triangle in liste:
		for point in triangle: #On ajoute les coordonnées des points une à une aux différentes listes
			X=X+[point[0]]
			Y=Y+[point[1]]
			Z=Z+[point[2]]
	X=np.array(X)#Les listes sont converties en un format reconnu par mlab
	Y=np.array(Y)
	Z=np.array(Z)
	fig=mlab.triangular_mesh(X,Y,Z,tri) #La figure est dessinée
	if save: #Instructions pour la sauvegarde du fichier
		if chemin=="ask": #Instructions pour demander à l'utilisateur l'emplacement du fichier
			root = Tkinter.Tk()
			root.withdraw()
			chemin = tkFileDialog.asksaveasfilename(parent=root,initialdir="/",defaultextension="vrml",initialfile="image", title="Selectionnez le dossier d'enregistrement")
		mlab.savefig(chemin)#Le fichier est enregistré
		#Bloc pour modifier l'extension du fichier, et faire en sorte de ne pas effacer un autre fichier image. L'extension doit être modifiée, car, pour Blender, les fichiers VRML ont une extension en .wrl
		nom, ext = os.path.splitext(chemin) #Le nom et l'extension du fichier sont séparés
		i=0# Le fichier est nommé par défaut image. Pour ne pas effacer d'autres fichiers, on rajoute _i à la fin du nom, où i est un nombre. i est incrémenté jusqu'à ce que l'emplacement soit disponible
		nom=nom+"_"
		while os.path.isfile(nom+str(i)+".wrl"):#Instrction testant si le fichier existe, et renvoyant true si c'est le cas
			i+=1
		nom=nom+str(i)
		os.rename(chemin, nom + ".wrl")#Instruction permettant de renommer le fichier "chemin2" en nom +".wrl", qui est le même nom, à l'extension et un nombre à la fin près
		#Fin du bloc

triangle_0=Triangle(Point(0,0,0),Point(1,0,0),Point(0,1,0))
distance = abs(gauss(1,0.2))
liste=creation_triangle(triangle_0,distance,Point(0,0,-1))
centre_1=milieu_triangle(liste[0])
centre_2=milieu_triangle(liste[1])
centre_3=milieu_triangle(liste[2])
centre=milieu_triangle(Triangle(centre_1,centre_2,centre_3))
for i in range(6):
 	  for j in range(len(liste)):
	     distance = abs(gauss(4**(-i-1),0.2**(i+1)))#Donne un nombre aléatoire selon une répartition gaussienne. A voir pour les paramètres ( le premier est la valeur moyenne, le second l’écart type)
 	     liste=liste+creation_triangle(liste.pop(0),distance,centre)#Enlève un triangle à la liste pour ajouter les trois triangles qui en sont issus

for i in range(len(liste)):#On transforme chaque élément de la liste, pour que le module d'affichage 3d puisse en faire qqchose
	   triangle=liste[i]
 	  liste[i]=[(triangle.point1.xP,triangle.point1.yP,triangle.point1.zP),(triangle.point2.xP,triangle.point2.yP,triangle.point2.zP),(triangle.point3.xP,triangle.point3.yP,triangle.point3.zP)]
creation_image(liste)

