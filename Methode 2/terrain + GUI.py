# -*- coding: utf-8 -*-
#Nécessite un environnement comprenant : Python 2.7, la librairie mayavi et toutes ses dépendances, la librairie wx, la librairie sympy
from sympy import N #Pour les arrondis dans la classe Point
from random import gauss #Pour les déplacements aléatoires
import tkFileDialog #Module pour que l'utilisateur choisisse l'endroit où enregistrer
import numpy as np #Module pour l'organisation des coordonnées lors de la phase de génération de l'image par mayavi
import os #Module pour rennomer le fichier image créé
from mayavi import mlab #Module pour générer le dessin
import Tkinter as Tk #Pour les fenêtres graphiques

class Point: #Fonctionne comme un vecteur

    def __init__(self, xP=0, yP=0, zP=0): #valeurs par défaut : (0,0,0)
        self.xP=xP
        self.yP=yP
        self.zP=zP
    
    def __add__(self,other): #Addition de 2 points
        return Point(self.xP+other.xP,self.yP+other.yP,self.zP+other.zP)
    
    def __mul__(self,n): #Multiplier un point/vecteur par un scalaire
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __rmul__(self,n): #Pareil qu'au dessus (mis pour plus de flexibilité dans l'écriture)
        return Point(self.xP*n,self.yP*n,self.zP*n)
    
    def __truediv__(self,n):#Diviser un point/vecteur par un scalaire
        return Point(self.xP/n,self.yP/n,self.zP/n)

    def __div__(self,n):#Pareil (pour compatibilité avec Python 2)
        return Point(self.xP/n,self.yP/n,self.zP/n)
    
    def __sub__(self,other):#Soustraire à un point/vecteur un autre point/vecteur
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
        
    def __eq__(self,other): #teste si 2 points/vecteurs sont égaux à 10^-7 près
        if N(self.xP,7)==N(other.xP,7) and N(self.yP,7)==N(other.yP,7) and N(self.zP,7)==N(other.zP,7):
            return True
        else:
            return False
    
    def __ne__(self,other): #teste si 2 points/vecteurs sont différents
        return not self==other
    
    def dist(self,other): #distance d'un point à un autre
        return ((self.xP - other.xP)**2+(self.yP - other.yP)**2+(self.zP-other.zP)**2)**0.5

def terrain(triangles,cotes,nb_etapes):
    '''Contient tout pour la génération de terrain'''
    def aire_tri(A,B,C):
        '''Retourne l'aire du triangle ABC'''
        a=A.dist(B) #Les longueurs des côtés 
        b=B.dist(C)
        c=C.dist(A)
        s=(a+b+c)/2
        Aire=(s*(s-a)*(s-b)*(s-c))**0.5 #La formule magique ! Pour être précis, la formule de Héron
        return(Aire)
    
    def creation_image(liste):
        '''Créé le dessin, à partir d'une liste de points.'''
        X=[]#Initialisation de tous les paramètres
        Y=[]
        Z=[]
        tri=[]
        pos=0
        for triangle in liste:#On fait cette boucle pour chaque triangle initial
            for k in range(1,len(triangle)): #Création de la liste des triangles : on s'intéresse ici aux triangles entre la ligne k-1 et k
                nb_a=(k-1)*k/2 #Position globale du premier point de la ligne k-1
                nb_b=nb_a+k #Position globale du premier point de la ligne k
                for i in range(k-1):#Pour chaque point de la ligne k-1 considérée, sauf le dernier
                    tri+=[(pos+nb_a,pos+nb_b,pos+nb_b+1),(pos+nb_a,pos+nb_a+1,pos+nb_b+1)] #On ajoute 2 triangles
                    nb_a+=1 #On passe aux points prochains
                    nb_b+=1
                tri+=[(pos+nb_a,pos+nb_b,pos+nb_b+1)] #On ajoute le dernier triangle
            for ligne in triangle:
                for point in ligne: #On ajoute les coordonnées des points une à une aux différentes listes
                    pos+=1#On ajoute 1 à la pos, afin que les nouveaux triangles crées lors du prochain passage dans la boucle for correspondent bien aux bons points
                    X=X+[point.xP]
                    Y=Y+[point.yP]
                    Z=Z+[point.zP]
        X=np.array(X)#Les listes sont converties en un format reconnu par mayavi
        Y=np.array(Y)
        Z=np.array(Z)
        return mlab.triangular_mesh(X,Y,Z,tri,colormap="gist_earth") #La figure est dessinée, avec des couleurs correspondant à un terrain

    def modif_rang_ajout(liste,pos,i):
        '''Cette procédure permet d'ajouter des points à des lignes de triangle déjà existantes'''
        global sigma #On récupère la valeur de sigma
        global decroissanceDV
        decroissance=decroissanceDV.get()#On récupère la valeur de decroissance    
        ligne=liste[pos]#On stocke la ligne sur laquelle on travaille    
        ligne2=[ligne[0]]#On crée une nouvelle ligne qui contiendra les modifications : elle contient de base le premier point qui ne bougera pas
        for k in range(len(ligne)-1):#On a len-1 segments sur la ligne, donc len-1 points à ajouter
            point=(ligne[k]+ligne[k+1])/2.0 #Les points à ajouter sont les milieux des segments déjà existants
            point = point + Point(0,0,gauss(0,sigma*decroissance**(i+1))) #Déplace le point verticalement, selon des paramètres choisis
            ligne2=ligne2+[point,ligne[k+1]]#On ajoute le point crée, puis le point existant suivant, qui ne bouge pas
        return [ligne2] #On retourne la nouvelle ligne comprenant les points existants et les points crées

    def modif_rang_creation(liste,pos,i,cote_0,cote_2,numero_etape_actuelle):
        '''Cette procédure permet de créer une nouvelle ligne de points'''
        global sigma #On récupère la valeur de sigma
        global decroissanceDV
        decroissance=decroissanceDV.get() #On récupère la valeur de decroissance 
        ligne_a=liste[pos-1] #On stocke les 2 lignes entre lesquelles sera ajouté la nouvelle ligne
        ligne_b=liste[pos]
        if cote_0:#Si ce coté a été déja fait, cote_0 est une liste et l'içnstruction conditionelle if sera activée. Si il n'a pas été fait, cote_0 contien False, l'instruction conditionelle else sera activée
            ligne_nouv=[cote_0[(2*pos-1)*(2**(numero_etape_actuelle-i-1))]] #On crée la nouvelle ligne avec le bon premier point. Il faut me croire pour la position du point dans la liste 
        else: #On crée la nouvelle ligne avec le premier point, milieu du segment formé par les premiers points des 2 lignes précédentes.
            ligne_nouv=[(ligne_a[0]+ligne_b[0])/2.0 + Point(0,0,gauss(0,sigma*decroissance**(i+1)))]
        #On crée les variables contenant les positions des points dont on veut obtenir le milieu du segment
        pos_a=0
        pos_b=1
        for k in range(pos-1):
            point1=(ligne_a[pos_a]+ligne_b[pos_b])/2.0 # Milieu du segment
            point1 = point1 + Point(0,0,gauss(0,sigma*decroissance**(i+1))) #Déplace le point verticalement
            pos_a+=1 #On ajuste la position du point de la première ligne afin d'obtenir le prochain point 
            point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
            point2 = point2 + Point(0,0,gauss(0,sigma*decroissance**(i+1))) #Déplace le point verticalement
            pos_b+=1 #On ajuste la position du point de la deuxième ligne afin d'obtenir le prochain point lors du prochain passage dans la boucle
            ligne_nouv+=[point1,point2] #On ajoute les 2 points à la ligne
        if cote_2:# Même chose que pour cote_0
            ligne_nouv+=cote_2[(2*pos-1)*(2**(numero_etape_actuelle-i-1))]
        else:
            ligne_nouv+=[(ligne_a[-1]+ligne_b[-1])/2.0 + Point(0,0,gauss(0,sigma*decroissance**(i+1)))]#Ici, on prend le milieu des derniers points des lignes,d'où le -1
        return [ligne_nouv] #On retourne la nouvelle ligne formée


    def modif_triangle(triangle,cotes_deja_faits,nb_etapes):
        '''Procédure gérant la génération de terrain à l'échelle d'un triangle initial '''
        global hauteurDV
        hauteur=hauteurDV.get() #On récupère la hauteur
        global sigma # On déclare sigma variable globale
        aire=aire_tri(triangle[0],triangle[1],triangle[2])#On calcule l'aire du triangle
        sigma=aire*hauteur# On attribue à sigma une valeur proportionnelle à l'aire du triangle, afin de moduler les variations de hauteur en fonction de la taille du triangle
        liste=[[triangle[0]],[triangle[1],triangle[2]]] #On crée une liste avec les 3 sommets du triangle. C'est un exemple du format utilisé : une liste de liste, chaqu'une de ces listes contient des points correspondant à une ligne de points du triangle
        cote_0=cotes_deja_faits[0]#On stocke dans le variables les informations pour savoir si les côtéss des triangles sont déjà faits ou pas
        cote_1=cotes_deja_faits[1]
        cote_2=cotes_deja_faits[2]
        if cote_0:#Si ce coté a été déja fait, cote_0 est une liste et l'instruction conditionelle if sera activée.
            if not cote_0[0]==triangle[0]:#On vérifie que le premier point est bien celui qu'on attend. Si la liste est dans le mauvais sens, on l'inverse.
                                          #On sépare les 2 conditions, car si cote_0 contient False, la deuxième condition retourne une erreur, et stoppe le déroulement du programme
                cote_0.reverse()
        if cote_1:#Idem
            if not cote_1[0]==triangle[1]:
                cote_1.reverse()
        if cote_2:#Idem
            if not cote_2[0]==triangle[0]:
                cote_2.reverse()
        #Le format utilisé est le suivant : une liste de listes de points, chaque liste correspondant à une ligne du triangle, donc contenant les points de cette ligne
        for i in range(nb_etapes):#Correspond aux itérations de l'algorithme de base
            liste2=[liste[0]] 
            #Cette liste contiendra le triangle avec ses nouveaux points. On commence par mettre la première ligne de 1 point, qui ne change jamais
            #La liste contenant le triangle précédant ne sera pas modifiée et sera utilisée comme référence durant toute ce passage dans la boucle
            for pos in range(1,len(liste)-1):#On crée toutes les nouvelles lignes, sauf les 2 dernières
                #Lors de l'ajout de nouveaux points, il se passe 2 choses : on créé de nouvelles lignes, et on ajoute des points aux lignes existantes, d'où les 2 procédures
                liste2 = liste2 + modif_rang_creation(liste,pos,i,cote_0,cote_2,nb_etapes) + modif_rang_ajout(liste,pos,i)
            if cote_1:#Si le cote est deja fait, c'est équivalent à True, si c'est False, le coté est pas fait et on passe dans la partie else
                dernier_cote=[cote_1[0]]
                for k in range(2**(i+1)):#On récupère tout les points dont on a besoin pour le dernier coté
                    dernier_cote=dernier_cote + [cote_1[k*(2**(nb_etapes-i-1))]]
                dernier_cote=[dernier_cote]
            else:
                dernier_cote = modif_rang_ajout(liste,len(liste)-1,i)#On utilise la même procédure que pour étendre les autres lignes
            liste2= liste2 + modif_rang_creation(liste,len(liste)-1,i,cote_0,cote_2,nb_etapes) + dernier_cote #On fait à part, car les points de la dernière ligne peuvent ou ne peuvent pas être ajoutés aléatoirement
            liste=liste2 #La liste principale est modifiée, car le nouveau triangle est totalement construit
        return liste


 
    etat_des_cotes=[False for i in range(len(cotes))] #On crée la liste contenant l'état des cotés. De base, les cotés ne sont pas faits, d'où le False
    liste=[]#Liste qui contiendra tout les triangles après passage dans l'algorithme
    for tri in triangles:#Pour chaque triangle
        cotes_du_tri=[cotes[tri[0]],cotes[tri[1]],cotes[tri[2]]]#La liste des cotés du triangle considéré
        cotes_deja_faits=[etat_des_cotes[tri[0]],etat_des_cotes[tri[1]],etat_des_cotes[tri[2]]]#La liste de l'état des cotés. Si ils sont faits, il y a la liste des points du coté. Sinon, il y a False
        if cotes_du_tri[1][0]==cotes[tri[0]][0] or cotes_du_tri[1][0]==cotes[tri[0]][1]:#On crée le triangle : les 2 premiers sommets sont les 2 points du premier côté, le troisième est le point du deuxième côté qui n'est pas déjà présent dans le premier côté, d'où la condition
            point_3=cotes_du_tri[1][1]
        else:
            point_3=cotes_du_tri[1][0]
        triangle=[cotes_du_tri[0][0],cotes_du_tri[0][1],point_3]#Création du triangle
        triangle=modif_triangle(triangle,cotes_deja_faits,nb_etapes)#Formation du terrain à partir du triangle
        if not cotes_deja_faits[0]:#Stokage des infos sur les côtés faits : si le côté vient d'être fait, la liste des points est stockée dans la liste etat_des_cotes à la bonne position
            cote_0=[]            
            for k in range(len(triangle)):#On récupère tout les points, qui sont les premiers points de chaque ligne du triangle
                cote_0+=[triangle[k][0]]
            etat_des_cotes[tri[0]]=cote_0
        if not cotes_deja_faits[2]:#Pareil
            cote_2=[]            
            for k in range(len(triangle)):#Ici, ce sont les derniers points de chaque ligne du triangle
                cote_2+=[triangle[k][-1]]
            etat_des_cotes[tri[2]]=cote_2
        if not cotes_deja_faits[1]:#Pareil
            etat_des_cotes[tri[1]]=triangle[-1]#Ici, c'est la dernière ligne du triangle          
        liste+=[triangle]#On ajoute la liste des points du triangle à la liste globale contenant tout
    return creation_image(liste)#On retourne le dessin

    
def process_launch():
    '''Procédure reliant une fenetre graphique et le coeur du programme'''
    global nb_etapesIV
    nb_etapes=nb_etapesIV.get()#On récupère le nombre d'étapes
    fig=mlab.figure(1)
    mlab.clf()#La fenêtre de dessin est initialisée
    mlab.draw(terrain([(0,1,2),(2,3,4),(4,5,6)],[(Point(0,0,0),Point(1,0,0)),(Point(1,0,0),Point(1,1,0)),(Point(0,0,0),Point(1,1,0)),(Point(1,1,0),Point(0,1,0)),(Point(0,0,0),Point(0,1,0)),(Point(0,0,0),Point(-1,1,0)),(Point(-1,1,0),Point(0,1,0))],nb_etapes))#On affiche le dessin
    
def process_save():
    '''Procédure reliant une fenêtre graphique et la sauvegarde de l'image'''
    fig=mlab.figure(1)#Focus sur la bonne fenêtre
    global fenetre
    chemin = tkFileDialog.asksaveasfilename(parent=fenetre,initialdir="/",defaultextension="vrml",initialfile="image", title="Selectionnez le dossier d'enregistrement")
    if chemin=='':#Petite sécurité pour moins d'erreur. Si,lors de l'instruction précédente, l'utilisateur a appuyé sur annuler, la chemin retourné est vide. On signale donc que le programme ne va pas sauvegarder
        root2=Tk.Toplevel()
        texte=Tk.Label(root2,text='La sauvegarde a échoué.\nChemin spécifié non valide',height=2)
        btOk=Tk.Button(root2,text='Ok',command=root2.destroy)#Affichage d'une fenêtre pour signifier l'échec
        texte.pack()
        btOk.pack()
        root2.mainloop()
        return None
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
    return None


def kill():
    '''Procédure pour fermer les fenêtres'''
    global fenetre
    mlab.close(all=True)#Fermeture des dessins
    fenetre.destroy()#Fermeture des interfaces graphiques

def main():
    '''Procédure principale créant une fenêtre graphique'''
    global decroissanceDV #Déclaration des variables globales réutilisées ailleurs
    global hauteurDV
    global nb_etapesIV
    global fenetre    
    fenetre = Tk.Tk()
    #Déclaration des variables, de telle sorte qu'elles puissent être utilisées par les boutons/widgets de Tkinter
    hauteurDV=Tk.DoubleVar()#équivalent à un nombre àvirgule flottante
    decroissanceDV=Tk.DoubleVar()
    nb_etapesIV=Tk.IntVar()#équivalent à un nombre entier
    btSave=Tk.Button(fenetre,text='Save',command=process_save)#Bouton permettant de lancer process_save(), qui sauvegarde l'image
    btDecr=Tk.Scale(fenetre,orient="horizontal",from_=0.0,to=1.0,label="Decroissance",resolution=-1,variable=decroissanceDV)# Widget permettant de choisir une valeur pour decroissanceDV
    btHt=Tk.Scale(fenetre,orient="horizontal",length=200,from_=0.0,to=5.0,label="Hauteur",resolution=-1,variable=hauteurDV)# Widget permettant de choisir une valeur pour hauteurDV
    btEtapes=Tk.Scale(fenetre,orient="horizontal",from_=1,to=8,label="Etapes",resolution=1,variable=nb_etapesDV)# Widget permettant de choisir une valeur pour nb_etapesDV. La résolution est de 1, pour avoir des valeurs entières
    btLaunch=Tk.Button(fenetre,text="Launch",command=process_launch)#Bouton lancant process_launch(), qui permet la création d'un dessin
    btQuit=Tk.Button(fenetre,text="Quitter",command=kill)#Bouton permettant de lancer kill(), qui ferme les fenêtres
    #On affiche tous, sans organisation particulière, grace à pack(), qui ajoute le nouveau widget/bouton en dessous des autres
    btHt.pack()
    btDecr.pack()
    btEtapes.pack()
    btLaunch.pack()
    btSave.pack()
    btQuit.pack()
    #On change les valeurs, afin qu'elles soient plus proche des valeurs intéressantes
    btDecr.set(0.4)
    btHt.set(2.5)
    btEtapes.set(6)
    fig=mlab.figure(1)#On affiche la fenêtre mayavi, afin que l'utilisateur puisse la bouger
    fenetre.mainloop()







