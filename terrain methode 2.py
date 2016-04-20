import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit o� enregistrer
import numpy as np #Module pour l'organisation des coordonn�es pour l'affichage
import os #Module pour rennomer le fichier � la fin
from mayavi import mlab #Module pour g�n�rer le dessin

class Point:
    """ D�finit un point avec trois coordonn�es (x,y,z). Utilisation : A=Point(x,y,z)
     Commandes : elles s'utilisent toutes comme A.commande() avec �ventuellement des arguments, sauf str
     - str , pour afficher le point (str(A)), rend : (x,y,z)
     - setAbs (changement d'abscisse)
     - setOrd (changement d'ordonn�e)
     - setAlt (changement d'altitude)
     - setCoord (changement des 3 coordonn�es)
     - dist (distance entre deux points) """
    def __init__(self, xP=0, yP=0, zP=0): #valeurs par d�faut : (0,0,0)
        self.xP=xP
        self.yP=yP
        self.zP=zP
        
    def __str__(self): #affichage
        return(str((self.xP,self.yP,self.zP)))
    
    def __add__(self,other): #Additionner 2 points : p+q
        return Point(self.xP+other.xP,self.yP+other.yP,self.zP+other.zP)
    
    def __sub__(self,other):# Soustraction : p-q
        return self+other*(-1)
    
    def __mul__(self,n):#Multiplier un point par un nombre : p*2
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __rmul__(self,n):#Multiplier un point par un nombre : 2*p
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __truediv__(self,n):#Diviser un point par un nombre
        return Point(self.xP/n,self.yP/n,self.zP/n)

    def __div__(self,n):#M�me chose que truediv, mais pour python 2
        return Point(self.xP/n,self.yP/n,self.zP/n)
    
    def __xor__(self,other):# Produit vectoriel : p^q
        L1=[self.xP,self.yP,self.zP]  
        L2=[other.xP,other.yP,other.zP]
        return Point(L1[1]*L2[2]-L1[2]*L2[1],L1[2]*L2[0]-L1[0]*L2[2],L1[0]*L2[1]-L1[1]*L2[0])
    
    def __and__(self,other):#Produit scalaire : p & q
        L1=[self.xP,self.yP,self.zP]  
        L2=[other.xP,other.yP,other.zP]
        return L1[0]*L2[0]+L1[1]*L2[1]+L1[2]*L2[2]

def creation_image(liste,save="True",chemin="ask"):
	'''Cr�� le dessin, � partir d'une liste de points.
	La variable save g�re si l'image est enregistr�e (Par d�faut,oui), � l'emplacement "chemin". Par d�faut,l'emplacement est demand� � l'utilisateur'''
	X=[]#Initialisation des 3 listes contenant les coordonn�es des sommets des triangles
	Y=[]
	Z=[]
        tri=[]
	for k in range(1,len(liste)): #Cr�ation de la liste des triangles : on s'int�resse ici aux triangles entre la ligne k-1 et k
		nb_a=(k-1)*k/2 #Position globale du premier point de la ligne k-1
		nb_b=nb_a+k #Position globale du premier point de la ligne k
		for i in range(k-1):
			tri+=[(nb_a,nb_b,nb_b+1),(nb_a,nb_a+1,nb_b+1)] #On ajoute 2 triangles
			nb_a+=1 #On passe aux points prochains
			nb_b+=1
		tri+=[(nb_a,nb_b,nb_b+1)] #On ajoute le dernier triangle
	for ligne in liste:
		for point in ligne: #On ajoute les coordonn�es des points une � une aux diff�rentes listes
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
        point = point + Point(0,0,gauss(0.3**(i-1),0.25**i)) #D�place le point verticalement
        ligne2=ligne2+[point,ligne[k+1]]#On ajoute un point cr�e, puis un point existant, qui ne bouge pas
    return [ligne2]

def modif_rang_creation(liste,pos,i):
    '''Cette proc�dure permet de cr�er une nouvelle ligne de points'''
    ligne_a=liste[pos-1] #On stocke les 2 lignes entre lesquelles sera ajout� la nouvelle ligne
    ligne_b=liste[pos]
    #On cr�e la nouvelle ligne avec le premier point, milieu du segment form� par les premiers points des 2 lignes pr�c�dentes. Ce point ne sera pas boug� afin d'avoir des bords r�alistes
    ligne_nouv=[(ligne_a[0]+ligne_b[0])/2.0]
    #On cr�e les variables contenant les positions des points dont on veut obtenir le centre
    pos_a=0
    pos_b=1
    for k in range(pos-1):
        point1=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point1 = point1 + Point(0,0,gauss(0.3**(i-1),0.25**i)) #D�place le point verticalement
        pos_a+=1 #On ajuste la position du point de la premi�re ligne afin d'obtenir le prochain point 
        point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point2 = point2 + Point(0,0,gauss(0.3**(i-1),0.25**i)) #D�place le point verticalement
        pos_b+=1 #On ajuste la position du point de la deuxi�me ligne afin d'obtenir le prochain point lors du prochain passage dans la boucle
        ligne_nouv=ligne_nouv+[point1,point2] #On ajoute les 2 points � la ligne
    ligne_nouv=ligne_nouv+[(ligne_a[-1]+ligne_b[-1])/2.0] #On ajoute le dernier point, milieu des 2 derniers points des 2 lignes
    return [ligne_nouv]


def proc():
	liste=[[Point(0,0,0)],[Point(-0.5,1,0),Point(0.5,1,0)]] 
	#Le format utilis� est le suivant : une liste de listes de points, chaque liste correspondant � une ligne du triangle, donc contenant les points de cette ligne
	for i in range(nb_etapes):
		liste2=[liste[0]] 
		#Cette liste contiendra le triangle avec ses nouveaux points. On commence par mettre la premi�re ligne de 1 point, qui ne change jamais
		#La liste contenant le triangle pr�c�dant ne sera pas modifi�e 
    		for pos in range(1,len(liste)-1):#On cr�e toutes les nouvelles lignes, sauf les 2 derni�res
            		#Lors de l'ajout de nouveaux points, il se passe 2 choses : on cr�� de nouvelles lignes, et on ajoute des points aux lignes existantes, d'o� les 2 proc�dures
			liste2 = liste2 + modif_rang_creation(liste,pos,i) + modif_rang_ajout(liste,pos,i)
		liste2= liste2 + modif_rang_creation(liste,len(liste)-1,i) + modif_rang_ajout(liste,len(liste)-1,10**3)#On fait � part, car les points de la derni�re ligne ne doivent pas �tre boug�s en hauteur, d'o� le 10^3
		liste=liste2 #La liste principale est modifi�e, car le nouveau triangle est totalement construi
	creation_image(liste)