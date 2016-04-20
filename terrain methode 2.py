import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit où enregistrer
import numpy as np #Module pour l'organisation des coordonnées pour l'affichage
import os #Module pour rennomer le fichier à la fin
from mayavi import mlab #Module pour générer le dessin

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
    
    def __sub__(self,other):# Soustraction : p-q
        return self+other*(-1)
    
    def __mul__(self,n):#Multiplier un point par un nombre : p*2
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __rmul__(self,n):#Multiplier un point par un nombre : 2*p
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __truediv__(self,n):#Diviser un point par un nombre
        return Point(self.xP/n,self.yP/n,self.zP/n)

    def __div__(self,n):#Même chose que truediv, mais pour python 2
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
	'''Créé le dessin, à partir d'une liste de points.
	La variable save gère si l'image est enregistrée (Par défaut,oui), à l'emplacement "chemin". Par défaut,l'emplacement est demandé à l'utilisateur'''
	X=[]#Initialisation des 3 listes contenant les coordonnées des sommets des triangles
	Y=[]
	Z=[]
        tri=[]
	for k in range(1,len(liste)): #Création de la liste des triangles : on s'intéresse ici aux triangles entre la ligne k-1 et k
		nb_a=(k-1)*k/2 #Position globale du premier point de la ligne k-1
		nb_b=nb_a+k #Position globale du premier point de la ligne k
		for i in range(k-1):
			tri+=[(nb_a,nb_b,nb_b+1),(nb_a,nb_a+1,nb_b+1)] #On ajoute 2 triangles
			nb_a+=1 #On passe aux points prochains
			nb_b+=1
		tri+=[(nb_a,nb_b,nb_b+1)] #On ajoute le dernier triangle
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
		os.rename(chemin, nom + ".wrl")#Instruction permettant de renommer le fichier "chemin" en nom +".wrl", qui est le même nom, à l'extension et un nombre à la fin près
		#Fin du bloc
def modif_rang_ajout(liste,pos,i):
    '''Cette procédure permet d'ajouter des points à des lignes déjà existantes'''
    ligne=liste[pos]#On stocke la ligne sur laquelle on travaille
    ligne2=[ligne[0]]#On crée une nouvelle ligne qui contiendra les modifications : elle contient de base le premier point qui ne bougera pas
    long=len(ligne)
    for k in range(long-1):
        point=(ligne[k]+ligne[k+1])/2.0 #Les points à ajouter sont les milieux des segments
        point = point + Point(0,0,gauss(0.3**(i-1),0.25**i)) #Déplace le point verticalement
        ligne2=ligne2+[point,ligne[k+1]]#On ajoute un point crée, puis un point existant, qui ne bouge pas
    return [ligne2]

def modif_rang_creation(liste,pos,i):
    '''Cette procédure permet de créer une nouvelle ligne de points'''
    ligne_a=liste[pos-1] #On stocke les 2 lignes entre lesquelles sera ajouté la nouvelle ligne
    ligne_b=liste[pos]
    #On crée la nouvelle ligne avec le premier point, milieu du segment formé par les premiers points des 2 lignes précédentes. Ce point ne sera pas bougé afin d'avoir des bords réalistes
    ligne_nouv=[(ligne_a[0]+ligne_b[0])/2.0]
    #On crée les variables contenant les positions des points dont on veut obtenir le centre
    pos_a=0
    pos_b=1
    for k in range(pos-1):
        point1=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point1 = point1 + Point(0,0,gauss(0.3**(i-1),0.25**i)) #Déplace le point verticalement
        pos_a+=1 #On ajuste la position du point de la première ligne afin d'obtenir le prochain point 
        point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        point2 = point2 + Point(0,0,gauss(0.3**(i-1),0.25**i)) #Déplace le point verticalement
        pos_b+=1 #On ajuste la position du point de la deuxième ligne afin d'obtenir le prochain point lors du prochain passage dans la boucle
        ligne_nouv=ligne_nouv+[point1,point2] #On ajoute les 2 points à la ligne
    ligne_nouv=ligne_nouv+[(ligne_a[-1]+ligne_b[-1])/2.0] #On ajoute le dernier point, milieu des 2 derniers points des 2 lignes
    return [ligne_nouv]


def proc():
	liste=[[Point(0,0,0)],[Point(-0.5,1,0),Point(0.5,1,0)]] 
	#Le format utilisé est le suivant : une liste de listes de points, chaque liste correspondant à une ligne du triangle, donc contenant les points de cette ligne
	for i in range(nb_etapes):
		liste2=[liste[0]] 
		#Cette liste contiendra le triangle avec ses nouveaux points. On commence par mettre la première ligne de 1 point, qui ne change jamais
		#La liste contenant le triangle précédant ne sera pas modifiée 
    		for pos in range(1,len(liste)-1):#On crée toutes les nouvelles lignes, sauf les 2 dernières
            		#Lors de l'ajout de nouveaux points, il se passe 2 choses : on créé de nouvelles lignes, et on ajoute des points aux lignes existantes, d'où les 2 procédures
			liste2 = liste2 + modif_rang_creation(liste,pos,i) + modif_rang_ajout(liste,pos,i)
		liste2= liste2 + modif_rang_creation(liste,len(liste)-1,i) + modif_rang_ajout(liste,len(liste)-1,10**3)#On fait à part, car les points de la dernière ligne ne doivent pas être bougés en hauteur, d'où le 10^3
		liste=liste2 #La liste principale est modifiée, car le nouveau triangle est totalement construi
	creation_image(liste)