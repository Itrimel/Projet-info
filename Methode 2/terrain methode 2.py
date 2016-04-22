# -*- coding: utf-8 -*-
from sympy import N #Pour faire les arrondis lors des tests d'égalité. Nécessite donc l'installation de sympy
from random import gauss #Pour faire les déplacement aléatoires
import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit où enregistrer
import numpy as np #Module pour l'organisation des coordonnées pour l'affichage
import os #Module pour rennomer le fichier à la fin
from mayavi import mlab #Module pour générer le dessin
class Point:#Fonctionne comme un vecteur
    def __init__(self, xP=0, yP=0, zP=0): #valeurs par défaut : (0,0,0)
        self.xP=xP
        self.yP=yP
        self.zP=zP
    
    def __add__(self,other):#Addition de 2 points/vecteurs
        return Point(self.xP+other.xP,self.yP+other.yP,self.zP+other.zP)
    
    def __mul__(self,n):#Multiplication d'un point/vecteur par un scalaire
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __rmul__(self,n):#Multiplication d'un point/vecteur par un scalaire
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __truediv__(self,n):#Division d'un point/vecteur par un scalaire
        return Point(self.xP/n,self.yP/n,self.zP/n)

    def __div__(self,n):#Division d'un point/vecteur par un scalaire pour Python 2
        return Point(self.xP/n,self.yP/n,self.zP/n)
    
    def __sub__(self,other):#Soustraction de 2 points/vecteurs
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
        
    def __eq__(self,other):#Teste si Point A == Point B .Retourne un booléen
        if N(self.xP,7)==N(other.xP,7) and N(self.yP,7)==N(other.yP,7) and N(self.zP,7)==N(other.zP,7):
            return True
        else:
            return False
    
    def __ne__(self,other):#Teste si Point A != Point B .Retourne un booléen
        return not self==other

    def dist(self,other): #distance d'un point à un autre
        return ((self.xP - other.xP)**2+(self.yP - other.yP)**2+(self.zP-other.zP)**2)**0.5
        

def aire_tri(A,B,C):
    a=A.dist(B)
    b=B.dist(C)
    c=C.dist(A)
    s=(a+b+c)/2
    Aire=(s*(s-a)*(s-b)*(s-c))**0.5
    return(Aire)

def creation_image(liste,save="True",chemin="ask"):
	'''Créé le dessin, à partir d'une liste de points.
	La variable save gère si l'image est enregistrée (Par défaut,oui), à l'emplacement "chemin". Par défaut,l'emplacement est demandé à l'utilisateur'''
	X=[]#Initialisation des 3 listes contenant les coordonnées des sommets des triangles
	Y=[]
	Z=[]
        tri=[]#Liste contenant les triplets de points des sommets des triangles
	#La procédure d'origine permet de créer les sous triangles à partir de la taille de la liste pour un triangle, pour le premier sommet du triangle comptant comme le point 0
	#Vu qu'on a ici plusieurs triangles, la variable pos va compter le nombre de points présents avant le premier sommet afin de ne pas avoir les mêmes sous triangles qui se répetent
	pos=0
	for triangle in liste:#Pour chaque triangle d'origine, on fait la méthode
		for k in range(1,len(triangle)): #Création de la liste des sous triangles : on s'intéresse ici aux sous triangles entre la ligne k-1 et k
			nb_a=(k-1)*k/2 #Position globale du premier point de la ligne k-1
			nb_b=nb_a+k #Position globale du premier point de la ligne k
			for i in range(k-1):
				tri+=[(pos+nb_a,pos+nb_b,pos+nb_b+1),(pos+nb_a,pos+nb_a+1,pos+nb_b+1)] #On ajoute 2 triangles. On ajoute la variable pos afin de prendre en compte le décalage crée par les autres triangles principaux crées avant
				nb_a+=1 #On passe aux points prochains
				nb_b+=1
			tri+=[(pos+nb_a,pos+nb_b,pos+nb_b+1)] #On ajoute le dernier sous triangle. Toujours la même chose pour pos
		for ligne in triangle:
			for point in ligne: #On ajoute les coordonnées des points une à une aux différentes listes
				pos+=1#On incrémente pos pour chaque point, afin de bien décaler les prochain sous triangles crées
				X=X+[point.xP]
				Y=Y+[point.yP]
				Z=Z+[point.zP]
	X=np.array(X)#Les listes sont converties en un format reconnu par mlab
	Y=np.array(Y)
	Z=np.array(Z)
	fig=mlab.triangular_mesh(X,Y,Z,tri,colormap="gist_earth") #La figure est dessinée, avec de bonnes couleurs
	while 1:
        	if save: #Instructions pour la sauvegarde du fichier
			if chemin=="ask": #Instructions pour demander à l'utilisateur l'emplacement du fichier
				root = Tkinter.Tk()
				root.withdraw()
				chemin = tkFileDialog.asksaveasfilename(parent=root,initialdir="/",defaultextension="vrml",initialfile="image", title="Selectionnez le dossier d'enregistrement")
				if chemin=='':#Petite sécurité pour moins d'erreur
					break
			mlab.savefig(chemin)#Le fichier est enregistré
			#Bloc pour modifier l'extension du fichier, et faire en sorte de ne pas effacer un autre fichier image. L'extension doit être modifiée, car, pour Blender, les fichiers VRML ont une extension en .wrl
			nom, ext = os.path.splitext(chemin) #Le nom et l'extension du fichier sont séparés
			i=0# Le fichier est nommé par défaut image. Pour ne pas effacer d'autres fichiers, on rajoute _i à la fin du nom, où i est un nombre. i est incrémenté jusqu'à ce que l'emplacement soit disponible
			nom=nom+"_"
			while os.path.isfile(nom+str(i)+".wrl"):#Instrction testant si le fichier existe, et renvoyant true si c'est le cas
				i+=1
			nom=nom+str(i)
			os.rename(chemin, nom + ".wrl")#Instruction permettant de renommer le fichier "chemin" en nom +".wrl", qui est le même nom, à l'extension et un nombre à la fin près
			#Fin du bloc
		break


def modif_rang_ajout(liste,pos,i,sigma):
    '''Cette procédure permet d'ajouter des points à des lignes déjà existantes'''
    ligne=liste[pos]#On stocke la ligne sur laquelle on travaille    
    ligne2=[ligne[0]]#On crée une nouvelle ligne qui contiendra les modifications : elle contient de base le premier point qui ne bougera pas
    long=len(ligne)
    for k in range(long-1):
        point=(ligne[k]+ligne[k+1])/2.0 #Les points à ajouter sont les milieux des segments
        point = point + Point(0,0,gauss(0,sigma*0.4**i)) #Déplace le point verticalement
        ligne2=ligne2+[point,ligne[k+1]]#On ajoute un point crée, puis un point existant, qui ne bouge pas
    return [ligne2]

def modif_rang_creation(liste,pos,i,cote_0,cote_2,nb_etapes,sigma):
    '''Cette procédure permet de créer une nouvelle ligne de points'''
    ligne_a=liste[pos-1] #On stocke les 2 lignes entre lesquelles sera ajouté la nouvelle ligne
    ligne_b=liste[pos]
    if cote_0:#Si ce coté a été déja fait, cote_0 est une liste et la boucle if sera activée. Si il n'a pas été fait, cote_0 contien False, le la boucle else sera activée
        ligne_nouv=[cote_0[(2*pos-1)*(2**(nb_etapes-i-1))]]#On crée la nouvelle ligne avec le bon point. Il faut me croire sur parole pour la position du point da la liste ;)
    else:
        #On crée la nouvelle ligne avec le premier point, milieu du segment formé par les premiers points des 2 lignes précédentes, pouis le point est bougé
        ligne_nouv=[(ligne_a[0]+ligne_b[0])/2.0 + Point(0,0,gauss(0,sigma*0.4**i))]
    #On crée les variables contenant les positions des points dont on veut obtenir le centre
    pos_a=0
    pos_b=1
    for k in range(pos-1):
        point1=(ligne_a[pos_a]+ligne_b[pos_b])/2.0 # Milieu du segment
        point1 = point1 + Point(0,0,gauss(0,sigma*0.4**i)) #Déplace le point verticalement
        pos_a+=1 #On ajuste la position du point de la première ligne afin d'obtenir le prochain point 
        point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point2 = point2 + Point(0,0,gauss(0,sigma*0.4**i)) #Déplace le point verticalement
        pos_b+=1 #On ajuste la position du point de la deuxième ligne afin d'obtenir le prochain point lors du prochain passage dans la boucle
        ligne_nouv+=[point1,point2] #On ajoute les 2 points à la ligne
    if cote_2:#Même chose que pour cote_0
        ligne_nouv+=cote_2[(2*pos-1)*(2**(nb_etapes-i-1))]
    else:
        ligne_nouv+=[(ligne_a[-1]+ligne_b[-1])/2.0 + Point(0,0,gauss(0,sigma*0.4**i))]#Ici, on prend le milieu des derniers points des lignes,d'où le -1
    return [ligne_nouv]#On retourne la ligne de point sous forme de liste


def modif_triangle(triangle,cotes_deja_faits,nb_etapes):
    aire=aire_tri(triangle[0],triangle[1],triangle[2])
    sigma=aire
    liste=[[triangle[0]],[triangle[1],triangle[2]]] #On crée une liste avec les 3 sommets du triangle. C'est un exemple du format utilisé : une liste de liste, chaque liste est une liste de points correspondant à une ligne du triangle
    cote_0=cotes_deja_faits[0]#On stocke dans le variables les informations pour savoir si les côtéss des triangles sont déjà faits ou pas
    cote_1=cotes_deja_faits[1]
    cote_2=cotes_deja_faits[2]
    if cote_0:#Si ce coté a été déja fait, cote_0 est une liste et la boucle if sera activée.
    	if not cote_0[0]==triangle[0]:#On vérifie que le premier point est bien celui qu'on attend. Si la liste est dans le mauvais sens, on l'inverse
        	cote_0.reverse()
    if cote_1:#Idem
	if not cote_1[0]==triangle[1]:
        	cote_1.reverse()
    if cote_2:#Idem
    	if not cote_2[0]==triangle[0]:
        	cote_2.reverse()
    for i in range(nb_etapes):#Correspond aux itérations de l'algorithme de base
        liste2=[liste[0]] 
        #Cette liste contiendra le triangle avec ses nouveaux points. On commence par mettre la première ligne de 1 point, qui ne change jamais
        #La liste contenant le triangle précédant ne sera pas modifiée 
        for pos in range(1,len(liste)-1):#On crée toutes les nouvelles lignes, sauf les 2 dernières
            #Lors de l'ajout de nouveaux points, il se passe 2 choses : on créé de nouvelles lignes, et on ajoute des points aux lignes existantes, d'où les 2 procédures
            liste2 = liste2 + modif_rang_creation(liste,pos,i,cote_0,cote_2,nb_etapes,sigma) + modif_rang_ajout(liste,pos,i,sigma)
        if cote_1:#Si ce coté a été déja fait, cote_1 est une liste et la boucle if sera activée. Si il n'a pas été fait, cote_1 contien False, le la boucle else sera activée
            dernier_cote=[cote_1[0]]
            for k in range(2**(i+1)):
                dernier_cote=dernier_cote + [cote_1[k*(2**(nb_etapes-i-1))]]
            dernier_cote=[dernier_cote]
        else:
            dernier_cote = modif_rang_ajout(liste,len(liste)-1,i,sigma)
        liste2= liste2 + modif_rang_creation(liste,len(liste)-1,i,cote_0,cote_2,nb_etapes,sigma) + dernier_cote #On fait à part, car les points de la dernière ligne peuvent ou ne peuvent pas être ajoutés aléatoirement
        liste=liste2 #La liste principale est modifiée, car le nouveau triangle est totalement construit
    return liste


def main(triangles,cotes,nb_etapes):
    ''' Procédure principale qui gère les interactions entre les triangles, et surtout les côtés déjà faits'''
    etat_des_cotes=[False for i in range(len(cotes))]#Aucun côté n'est fait : la liste ne contient que des False (côté pas fait)
    liste=[]
    for tri in triangles:#Pour chaque triangle
        cotes_du_tri=[cotes[tri[0]],cotes[tri[1]],cotes[tri[2]]]#La liste des côtés du triangle considéré
        cotes_deja_faits=[etat_des_cotes[tri[0]],etat_des_cotes[tri[1]],etat_des_cotes[tri[2]]]#La liste de l'état des côtés du triangle : si déjà fait, contient la liste des points du côtés
        if cotes_du_tri[1][0]==cotes[tri[0]][0] or cotes_du_tri[1][0]==cotes[tri[0]][1]:#On crée le triangle : les 2 premiers sommets sont les 2 points du premier côté, le troisième est le point du deuxième côté qui n'est pas déjà présent dans le premier côté, d'où la condition
            point_3=cotes_du_tri[1][1]
        else:
            point_3=cotes_du_tri[1][0]
        triangle=[cotes_du_tri[0][0],cotes_du_tri[0][1],point_3]#Création du triangle
        triangle=modif_triangle(triangle,cotes_deja_faits,nb_etapes)#Formation du terrain à partir du triangle      
        if not cotes_deja_faits[0]:#Stokage des infos sur les côtés faits : si le côté vient d'être fait, la liste des points est stockée dans la liste etat_des_cotes à la bonne position
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
        liste+=[triangle]#On ajoute la liste des points du triangle à la liste global contenant tout
    creation_image(liste)#On dessine le terrain

def main2():#Procédure test
	main([(0,1,2),(2,3,4),(4,5,6)],[(Point(0,0,0),Point(1,0,0)),(Point(1,0,0),Point(1,1,0)),(Point(0,0,0),Point(1,1,0)),(Point(1,1,0),Point(0,1,0)),(Point(0,0,0),Point(0,1,0)),(Point(0,0,0),Point(-1,1,0)),(Point(-1,1,0),Point(0,1,0))],5)
