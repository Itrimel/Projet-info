from random import *
import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit où enregistrer
import numpy as np #Module pour l'organisation des coordonnées pour l'affichage
import os #Module pour rennomer le fichier à la fin
from mayavi import mlab #Module pour générer le dessin
class Point:

    def __init__(self, xP=0, yP=0, zP=0): #valeurs par défaut : (0,0,0)
        self.xP=xP
        self.yP=yP
        self.zP=zP
        self.numpy=np.array([self.xP,self.yP,self.zP])
    
    def __add__(self,other):
        return Point(self.xP+other.xP,self.yP+other.yP,self.zP+other.zP)
    
    def __mul__(self,n):
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __rmul__(self,n):
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __truediv__(self,n):
        return Point(self.xP/n,self.yP/n,self.zP/n)

    def __div__(self,n):
        return Point(self.xP/n,self.yP/n,self.zP/n)
    
    def __sub__(self,other):
        return self+other*(-1)
    
    def __xor__(self,other):# Produit vectoriel : p^q
        L1=[self.xP,self.yP,self.zP]  
        L2=[other.xP,other.yP,other.zP]
        return Point(L1[1]*L2[2]-L1[2]*L2[1],L1[2]*L2[0]-L1[0]*L2[2],L1[0]*L2[1]-L1[1]*L2[0])
    
    def __and__(self,other):#Produit scalaire : p & q
        L1=[self.xP,self.yP,self.zP]  
        L2=[other.xP,other.yP,other.zP]
        return L1[0]*L2[0]+L1[1]*L2[1]+L1[2]*L2[2]
    
    def __str__(self): #affichage
        return(str((self.xP,self.yP,self.zP)))

def modif_rang_ajout(liste,pos,i):
    ligne=liste[pos]
    ligne2=[ligne[0]]      
    long=len(ligne)
    for k in range(long-1):
        point=(ligne[k]+ligne[k+1])/2.0
        point = point + Point(0,0,gauss(0.5**(i-1),0.3**i)) #Déplace le point verticalement
        ligne2=ligne2+[point,ligne[k+1]]
    return [ligne2]

def modif_rang_creation(liste,pos,i):
    ligne_a=liste[pos-1]
    ligne_b=liste[pos]
    ligne_nouv=[(ligne_a[0]+ligne_b[0])/2.0]
    pos_a=0
    pos_b=1
    for k in range(pos-1):
        point1=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point1 = point1 + Point(0,0,gauss(0.3**(i-1),0.25**i)) #Déplace le point verticalement
        pos_a+=1
        point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point2 = point2 + Point(0,0,gauss(0.3**(i-1),0.25**i)) #Déplace le point verticalement
        pos_b+=1
        ligne_nouv=ligne_nouv+[point1,point2]
    ligne_nouv=ligne_nouv+[(ligne_a[-1]+ligne_b[-1])/2.0]
    return [ligne_nouv]

def creation_image(liste,save="True",chemin2="ask"):
	'''Créé le dessin, à partir d'un document texte placé à l'emplacement "chemin1". Par défaut, cet emplacement sera demandé à l'utilisateur.
	La variable save gère si l'image est enregistrée (Par défaut,oui), à l'emplacement "chemin2". Par défaut,l'emplacement est demandé à l'utilisateur'''
	X=[]#Initialisation des 3 listes contenant les coordonnées des sommets des triangles
	Y=[]
	Z=[]
        tri=[]
	for k in range(1,len(liste)):
		nb_a=(k-1)*k/2
		nb_b=nb_a+k
		for i in range(k-1):
			tri+=[(nb_a,nb_b,nb_b+1),(nb_a,nb_a+1,nb_b+1)]
			nb_a+=1
			nb_b+=1
		tri+=[(nb_a,nb_b,nb_b+1)]                  
	for ligne in liste:
		for point in ligne: #On ajoute les coordonnées des points une à une aux différentes listes
			X=X+[point.xP]
			Y=Y+[point.yP]
			Z=Z+[point.zP]
	X=np.array(X)#Les listes sont converties en un format reconnu par mlab
	Y=np.array(Y)
	Z=np.array(Z)
	fig=mlab.triangular_mesh(X,Y,Z,tri) #La figure est dessinée
	if save: #Instructions pour la sauvegarde du fichier
		if chemin2=="ask": #Instructions pour demander à l'utilisateur l'emplacement du fichier
			root = Tkinter.Tk()
			root.withdraw()
			chemin2 = tkFileDialog.asksaveasfilename(parent=root,initialdir="/",defaultextension="vrml",initialfile="image", title="Selectionnez le dossier d'enregistrement")
		mlab.savefig(chemin2)#Le fichier est enregistré
		#Bloc pour modifier l'extension du fichier, et faire en sorte de ne pas effacer un autre fichier image. L'extension doit être modifiée, car, pour Blender, les fichiers VRML ont une extension en .wrl
		nom, ext = os.path.splitext(chemin2) #Le nom et l'extension du fichier sont séparés
		i=0# Le fichier est nommé par défaut image. Pour ne pas effacer d'autres fichiers, on rajoute _i à la fin du nom, où i est un nombre. i est incrémenté jusqu'à ce que l'emplacement soit disponible
		nom=nom+"_"
		while os.path.isfile(nom+str(i)+".wrl"):#Instrction testant si le fichier existe, et renvoyant true si c'est le cas
			i+=1
		nom=nom+str(i)
		os.rename(chemin2, nom + ".wrl")#Instruction permettant de renommer le fichier "chemin2" en nom +".wrl", qui est le même nom, à l'extension et un nombre à la fin près
		#Fin du bloc

def proc(k):
    liste=[[Point(0,0,0)],[Point(-0.5,1,0),Point(0.5,1,0)]]
    for i in range(k):
        liste2=[liste[0]]
        for pos in range(1,len(liste)-1):
            liste2 = liste2 + modif_rang_creation(liste,pos,i) + modif_rang_ajout(liste,pos,i)
        liste2 = liste2 + modif_rang_creation(liste,len(liste)-1,i) + modif_rang_ajout(liste,len(liste)-1,10**3)
	liste=liste2
    creation_image(liste)


