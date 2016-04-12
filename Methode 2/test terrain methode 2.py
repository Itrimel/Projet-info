# -*- coding: utf-8 -*-
from sympy import N
from random import gauss
import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit o� enregistrer
import numpy as np #Module pour l'organisation des coordonn�es pour l'affichage
import os #Module pour rennomer le fichier � la fin
from mayavi import mlab #Module pour g�n�rer le dessin
class Point:

    def __init__(self, xP=0, yP=0, zP=0): #valeurs par d�faut : (0,0,0)
        self.xP=xP
        self.yP=yP
        self.zP=zP
    
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
        
    def __eq__(self,other):
        if N(self.xP,7)==N(other.xP,7) and N(self.yP,7)==N(other.yP,7) and N(self.zP,7)==N(other.zP,7):
            return True
        else:
            return False
    
    def __ne__(self,other):
        return not self==other

def creation_image(liste,save="True",chemin="ask"):
	'''Cr�� le dessin, � partir d'une liste de points.
	La variable save g�re si l'image est enregistr�e (Par d�faut,oui), � l'emplacement "chemin". Par d�faut,l'emplacement est demand� � l'utilisateur'''
	X=[]#Initialisation des 3 listes contenant les coordonn�es des sommets des triangles
	Y=[]
	Z=[]
        tri=[]
	pos=0
	for triangle in liste:
		print(pos)
		for k in range(1,len(triangle)): #Cr�ation de la liste des triangles : on s'int�resse ici aux triangles entre la ligne k-1 et k
			nb_a=(k-1)*k/2 #Position globale du premier point de la ligne k-1
			nb_b=nb_a+k #Position globale du premier point de la ligne k
			for i in range(k-1):
				tri+=[(pos+nb_a,pos+nb_b,pos+nb_b+1),(pos+nb_a,pos+nb_a+1,pos+nb_b+1)] #On ajoute 2 triangles
				nb_a+=1 #On passe aux points prochains
				nb_b+=1
			tri+=[(pos+nb_a,pos+nb_b,pos+nb_b+1)] #On ajoute le dernier triangle
		for ligne in triangle:
			for point in ligne: #On ajoute les coordonn�es des points une � une aux diff�rentes listes
				pos+=1
				X=X+[point.xP]
				Y=Y+[point.yP]
				Z=Z+[point.zP]
	X=np.array(X)#Les listes sont converties en un format reconnu par mlab
	Y=np.array(Y)
	Z=np.array(Z)
	fig=mlab.triangular_mesh(X,Y,Z,tri) #La figure est dessin�e
	if save: #Instructions pour la sauvegarde du fichier
		if chemin=="ask": #Instructions pour demander � l'utilisateur l'emplacement du fichier
			root = Tkinter.Tk()
			root.withdraw()
			chemin = tkFileDialog.asksaveasfilename(parent=root,initialdir="/",defaultextension="vrml",initialfile="image", title="Selectionnez le dossier d'enregistrement")
		mlab.savefig(chemin)#Le fichier est enregistr�
		#Bloc pour modifier l'extension du fichier, et faire en sorte de ne pas effacer un autre fichier image. L'extension doit �tre modifi�e, car, pour Blender, les fichiers VRML ont une extension en .wrl
		nom, ext = os.path.splitext(chemin) #Le nom et l'extension du fichier sont s�par�s
		i=0# Le fichier est nomm� par d�faut image. Pour ne pas effacer d'autres fichiers, on rajoute _i � la fin du nom, o� i est un nombre. i est incr�ment� jusqu'� ce que l'emplacement soit disponible
		nom=nom+"_"
		while os.path.isfile(nom+str(i)+".wrl"):#Instrction testant si le fichier existe, et renvoyant true si c'est le cas
			i+=1
		nom=nom+str(i)
		os.rename(chemin, nom + ".wrl")#Instruction permettant de renommer le fichier "chemin" en nom +".wrl", qui est le m�me nom, � l'extension et un nombre � la fin pr�s
		#Fin du bloc

def modif_rang_ajout(liste,pos,i):
    '''Cette proc�dure permet d'ajouter des points � des lignes d�j� existantes'''
    ligne=liste[pos]#On stocke la ligne sur laquelle on travaille    
    ligne2=[ligne[0]]#On cr�e une nouvelle ligne qui contiendra les modifications : elle contient de base le premier point qui ne bougera pas
    long=len(ligne)
    for k in range(long-1):
        point=(ligne[k]+ligne[k+1])/2.0 #Les points � ajouter sont les milieux des segments
        point = point + Point(0,0,gauss(0,0.25**i)) #D�place le point verticalement
        ligne2=ligne2+[point,ligne[k+1]]#On ajoute un point cr�e, puis un point existant, qui ne bouge pas
    return [ligne2]

def modif_rang_creation(liste,pos,i,cote_0,cote_2,nb_etapes):
    '''Cette proc�dure permet de cr�er une nouvelle ligne de points'''
    ligne_a=liste[pos-1] #On stocke les 2 lignes entre lesquelles sera ajout� la nouvelle ligne
    ligne_b=liste[pos]
    if cote_0:
        ligne_nouv=[cote_0[(2*pos-1)*(2**(nb_etapes-i-1))]]
    else:
        #On cr�e la nouvelle ligne avec le premier point, milieu du segment form� par les premiers points des 2 lignes pr�c�dentes. Ce point ne sera pas boug� afin d'avoir des bords r�alistes
        ligne_nouv=[(ligne_a[0]+ligne_b[0])/2.0 + Point(0,0,gauss(0,0.25**i))]
    #On cr�e les variables contenant les positions des points dont on veut obtenir le centre
    pos_a=0
    pos_b=1
    for k in range(pos-1):
        point1=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point1 = point1 + Point(0,0,gauss(0,0.25**i)) #D�place le point verticalement
        pos_a+=1 #On ajuste la position du point de la premi�re ligne afin d'obtenir le prochain point 
        point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point2 = point2 + Point(0,0,gauss(0,0.25**i)) #D�place le point verticalement
        pos_b+=1 #On ajuste la position du point de la deuxi�me ligne afin d'obtenir le prochain point lors du prochain passage dans la boucle
        ligne_nouv+=[point1,point2] #On ajoute les 2 points � la ligne
    if cote_2:
        ligne_nouv+=cote_2[(2*pos-1)*(2**(nb_etapes-i-1))]
    else:
        ligne_nouv+=[(ligne_a[-1]+ligne_b[-1])/2.0 + Point(0,0,gauss(0,0.25**i))]
    return [ligne_nouv]


def modif_triangle(triangle,cotes_deja_faits,nb_etapes):
    liste=[[triangle[0]],[triangle[1],triangle[2]]] 
    cote_0=cotes_deja_faits[0]
    cote_1=cotes_deja_faits[1]
    cote_2=cotes_deja_faits[2]
    if cote_0:
    	if not cote_0[0]==triangle[0]:
        	cote_0.reverse()
    if cote_1:	
	if not cote_1[0]==triangle[1]:
        	cote_1.reverse()
    if cote_2:
    	if not cote_2[0]==triangle[0]:
        	cote_2.reverse()
    #Le format utilis� est le suivant : une liste de listes de points, chaque liste correspondant � une ligne du triangle, donc contenant les points de cette ligne
    for i in range(nb_etapes):
        liste2=[liste[0]] 
        #Cette liste contiendra le triangle avec ses nouveaux points. On commence par mettre la premi�re ligne de 1 point, qui ne change jamais
        #La liste contenant le triangle pr�c�dant ne sera pas modifi�e 
        for pos in range(1,len(liste)-1):#On cr�e toutes les nouvelles lignes, sauf les 2 derni�res
            #Lors de l'ajout de nouveaux points, il se passe 2 choses : on cr�� de nouvelles lignes, et on ajoute des points aux lignes existantes, d'o� les 2 proc�dures
            liste2 = liste2 + modif_rang_creation(liste,pos,i,cote_0,cote_2,nb_etapes) + modif_rang_ajout(liste,pos,i)
        if cote_1:#Si le cote est deja fait, c'est �quivalent � True, si c'est False, le cot� est pas fait et on passe dans le bout else
            dernier_cote=cote_1[0]
            for k in range(2**(i+1)):
                dernier_cote=dernier_cote + [cote_1[k*(2**(nb_etapes-i-1))]]
            dernier_cote=[dernier_cote]
        else:
            dernier_cote = modif_rang_ajout(liste,len(liste)-1,i)
        liste2= liste2 + modif_rang_creation(liste,len(liste)-1,i,cote_0,cote_2,nb_etapes) + dernier_cote #On fait � part, car les points de la derni�re ligne peuvent ou ne peuvent pas �tre ajout�s al�atoirement
        liste=liste2 #La liste principale est modifi�e, car le nouveau triangle est totalement construit
    return liste


def main(triangles,cotes,nb_etapes):    
    etat_des_cotes=[False for i in range(len(cotes))]
    liste=[]
    for tri in triangles:
        cotes_du_tri=[cotes[tri[0]],cotes[tri[1]],cotes[tri[2]]]
        cotes_deja_faits=[etat_des_cotes[tri[0]],etat_des_cotes[tri[1]],etat_des_cotes[tri[2]]]
        if cotes_du_tri[1][0]==cotes[tri[0]][0] or cotes_du_tri[1][0]==cotes[tri[0]][1]:
            point_3=cotes_du_tri[1][1]
        else:
            point_3=cotes_du_tri[1][0]
        triangle=[cotes_du_tri[0][0],cotes_du_tri[0][1],point_3]
        triangle=modif_triangle(triangle,cotes_deja_faits,nb_etapes)       
        if not cotes_deja_faits[0]:
            cote_0=[]            
            for k in range(len(triangle)):
                cote_0+=[triangle[k][0]]
            etat_des_cotes[tri[0]]=cote_0
        if not cotes_deja_faits[2]:
            cote_2=[]            
            for k in range(len(triangle)):
                cote_2+=[triangle[k][-1]]
            etat_des_cotes[tri[2]]=cote_2
        if not cotes_deja_faits[1]:
            etat_des_cotes[tri[1]]=triangle[-1]                
        liste+=[triangle]
    creation_image(liste)

def main2():
	main([(0,1,2),(2,3,4),(4,5,6)],[(Point(0,0,0),Point(1,0,0)),(Point(1,0,0),Point(1,1,0)),(Point(0,0,0),Point(1,1,0)),(Point(1,1,0),Point(0,1,0)),(Point(0,0,0),Point(0,1,0)),(Point(0,0,0),Point(-1,1,0)),(Point(-1,1,0),Point(0,1,0))],5)