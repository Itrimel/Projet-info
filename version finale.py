# -*- coding: utf-8 -*-
#Nécessite un environnement comprenant : Python 2.7, la librairie mayavi et toutes ses dépendances, la librairie wx, la librairie sympy
#Pour créer un environnement virtuel à l'aide d'Anaconda contenant ces librairies, voir ce lien : http://conda.pydata.org/docs/using/envs.html
from sympy import N #Pour les arrondis dans la classe Point
from random import gauss,expovariate,random #Pour les déplacements aléatoires
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
    
class Triangle:#Classe permettant de contenir les infos définissant un triangle
    def __init__(self, A=Point(0,0,0), B=Point(1,1,0), C=Point(2,-1,0)):
        self.point1=A
        self.point2=B
        self.point3=C

class Methode1:#Classe contenant tout ce qui est en rappport avec la méthode 1 : cadre graphique, méthodes
    def __init__(self,parent):#On initialise le cadre graphique
        self.frame=Tk.Frame(parent)#création du cadre, qui sera présent dans la fenêtre parent
        self.parent=parent
        #Création des variables qui pourront être modifiée par l'utilisateur
        self.decr_espeDV=Tk.DoubleVar()
        self.espeDV=Tk.DoubleVar()
        self.decr_sigmaDV=Tk.DoubleVar()
        self.sigmaDV=Tk.DoubleVar()
        self.nb_etapesIV=Tk.IntVar()
        #Paramétrages de l'organisation du cadre, pour que le rendu soit a peu près agréable
        for i in range(6):
            self.frame.columnconfigure(i,minsize=53)
        for i in range(4):
            self.frame.rowconfigure(i,minsize=50)
        #Positionnement de tous les widgets dans le cadre
        Tk.Scale(self.frame,orient="horizontal",length=150,from_=0.0,to=2.5,label="Esperance",resolution=-1,variable=self.espeDV).grid(row=0,column=0,columnspan=3)# Widget permettant de choisir une valeur pour espeDV
        Tk.Scale(self.frame,orient="horizontal",from_=0.0,to=1.0,label="Decroissance espe",resolution=-1,variable=self.decr_espeDV).grid(row=1,column=0,columnspan=3)# Widget permettant de choisir une valeur pour decr_espeDV
        Tk.Scale(self.frame,orient="horizontal",length=100,from_=0.0,to=2.5,label="Sigma",resolution=-1,variable=self.sigmaDV).grid(row=0,column=3,columnspan=3)# Widget permettant de choisir une valeur pour sigmaDV
        Tk.Scale(self.frame,orient="horizontal",from_=0.0,to=1.0,label="Decroissance sigma",resolution=-1,variable=self.decr_sigmaDV).grid(row=1,column=3,columnspan=3)# Widget permettant de choisir une valeur pour decr_sigmaDV
        Tk.Scale(self.frame,orient="horizontal",from_=1,to=8,label="Etapes",resolution=1,variable=self.nb_etapesIV).grid(row=2,column=0,columnspan=6)# Widget permettant de choisir une valeur pour nb_etapesIV. La résolution est de 1, pour avoir des valeurs entières
        Tk.Button(self.frame,text="Launch",command=self.montagne,width=8).grid(row=3,column=0,columnspan=2)#Bouton lancant montagne(), qui permet la création d'un dessin
        Tk.Button(self.frame,text='Save',command=self.process_save,width=8).grid(row=3,column=2,columnspan=2)#Bouton permettant de lancer process_save(), qui va sauvegarder l'image en un format 3d
        #On initialise les variables aux valeurs donnant des résultats les plus intéressants
        self.espeDV.set(1)
        self.decr_espeDV.set(0.2)
        self.sigmaDV.set(0.5)
        self.decr_sigmaDV.set(0.2)
        self.nb_etapesIV.set(6)
        

    def process_save(self):
        '''Procédure reliant une fenêtre graphique et la sauvegarde de l'image, qui se fera en un format VRML'''
        fig=mlab.figure(1)#Focus sur la bonne fenêtre
        chemin = tkFileDialog.asksaveasfilename(parent=self.parent,initialdir="/",defaultextension="vrml",initialfile="image", title="Selectionnez le dossier d'enregistrement")#Ouverture d'une fenêtre annexe demandant le chemin d'enregistrement.
        if chemin=='':#Petite sécurité pour moins d'erreur. Si,lors de l'instruction précédente, l'utilisateur a appuyé sur annuler, la chemin retourné est vide. On signale donc que le programme ne va pas sauvegarder
            root2=Tk.Toplevel()#On ouvre une fenêtre pour signaler la non sauvegarde
            texte=Tk.Label(root2,text='La sauvegarde a échoué.\nChemin spécifié non valide',height=2)
            btOk=Tk.Button(root2,text='Ok',command=root2.destroy)
            texte.pack()
            btOk.pack()
            root2.mainloop()
        mlab.savefig(chemin)#Le fichier est enregistré
        #Bloc pour modifier l'extension du fichier, et faire en sorte de ne pas effacer un autre fichier image. L'extension doit être modifiée, car, pour Blender, le logiciel utilisé pour lire les fichiers crées, les fichiers VRML ont une extension en .wrl
        nom, ext = os.path.splitext(chemin) #Le nom et l'extension du fichier sont séparés
        i=0# Le fichier est nommé par défaut image. Pour ne pas effacer d'autres fichiers, on rajoute _i à la fin du nom, où i est un nombre. i est incrémenté jusqu'à ce que l'emplacement soit disponible
        nom=nom+"_"
        while os.path.isfile(nom+str(i)+".wrl"):#Instrction testant si le fichier existe, et renvoyant true si c'est le cas
            i+=1
        nom=nom+str(i)
        os.rename(chemin, nom + ".wrl")#Instruction permettant de renommer le fichier "chemin" en nom +".wrl", qui est le même nom, à l'extension et un nombre à la fin près
        #Fin du bloc
    
    def montagne(self):
        '''Procédure contenant la création de la montagne et son affichage'''
        def milieu_triangle (T) :
            '''Retourne sous forme d'un point le centre du triangle donné en argument'''
            C= (T.point1+T.point2+T.point3)/3.0 #C devient le centre du triangle
            return(C)
         
        def Normale(T, distance,centre):
            '''Retourne trois triangles issus du triangle T dont le centre a été déplacé de la distance donnée.
               L'argument centre permet de déterminer l'intérieur de la structure'''
            #On initialise les variables
            M=milieu_triangle(T)
            p1=T.point1
            p2=T.point2
            p3=T.point3
            u=p1-p2#On calcule deux vecteurs, qui correspondent à 2 cotés du triangle
            v=p1-p3
            w=u^v#On calcule leur produit vectoriel
            norme=(float(w & w))**1/2 #Norme de w = produit scalaire par lui même à la racine carrée
            w=w/norme#w est maintenant normé
            a=centre-M#Vecteur allant du centre du triangle au point centre, qui est à l'interieur de la structure
            if w & a >0: #On fait le produit scalaire des 2 vecteurs. Si le produit scalaire est positif, cela signifie que les 2 vecteurs sont environ du même sens, donc que w pointe vers l'interieur
                w=-1*w#On prend l'opposé de w, qui pointe alors vers l'exterieur
            p4=M+distance*w#Centre déplacé selon la normale vers l'exterieur
            return(p4)
            
        def creation_triangle(T,distance,centre):
            '''Procédure qui au triangle T et à la distance distance retourne les 3 nouveaux triangles crées'''
            C=Normale(T,distance,centre)
            T1=Triangle(T.point1,T.point2,C)
            T2=Triangle(T.point1,T.point3,C)
            T3=Triangle(T.point2,T.point3,C)
            return[T1,T2,T3] #retourner les triangles dans une liste pour être compatible avec la boucle principale
        
        def creation_image(liste):
            '''Créé le dessin, à partir de la liste entréé'''
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
            return mlab.triangular_mesh(X,Y,Z,tri,colormap='gist_earth') #La figure est dessinée
        
        #On initialise les variables qui seront utilisées
        espe=self.espeDV.get()
        decr_espe=self.decr_espeDV.get()
        sigma=self.sigmaDV.get()
        decr_sigma=self.decr_sigmaDV.get()
        #On crée le triangle qui servira de base et on fait la prmière étape à part
        triangle_0=Triangle(Point(0,0,0),Point(1,0,0),Point(0,1,0))
        distance = abs(gauss(0.8,0.2))
        liste=creation_triangle(triangle_0,distance,Point(0,0,-1))
        #On détermine le centre de la structure, qui nous servira de point de repère pour déterminer où est l'interieur et l'exterieur
        centre_1=milieu_triangle(liste[0])
        centre_2=milieu_triangle(liste[1])
        centre_3=milieu_triangle(liste[2])
        centre=milieu_triangle(Triangle(centre_1,centre_2,centre_3))
        for i in range(self.nb_etapesIV.get()):#On fait le nombre d'itérations spécifié par l'utilisateur
            for j in range(len(liste)):#Pour chaque triangle présent dans la structure
                distance = gauss(espe*decr_espe**(i+1),sigma*decr_sigma**(i+1))#Donne un nombre aléatoire selon une répartition gaussienne. Les paramètres sont déterminés par l'utilisateur
                liste=liste+creation_triangle(liste.pop(0),distance,centre)#Enlève un triangle à la liste pour ajouter les trois nouveaux triangles qui en sont issus
        
        for i in range(len(liste)):#On transforme chaque élément de la liste d'objet Triangle à une liste de triplet, pour que le module d'affichage 3d puisse en faire qqchose
            triangle=liste[i]
            liste[i]=[(triangle.point1.xP,triangle.point1.yP,triangle.point1.zP),(triangle.point2.xP,triangle.point2.yP,triangle.point2.zP),(triangle.point3.xP,triangle.point3.yP,triangle.point3.zP)]
        fig=mlab.figure(1)
        mlab.clf()#La fenêtre de dessin est initialisée
        mlab.draw(creation_image(liste))#On dessine la montagne

class Methode2:#Classe contenant tout ce qui se rapporte à la méthode 2
    def __init__(self,parent):
        self.frame=Tk.Frame(parent)
        self.parent=parent
        #Déclaration des variables, de telle sorte qu'elles puissent être utilisées par les boutons/widgets de Tkinter
        self.hauteurDV=Tk.DoubleVar()#équivalent à un nombre àvirgule flottante
        self.decroissanceDV=Tk.DoubleVar()
        self.nb_etapesIV=Tk.IntVar()#équivalent à un nombre entier
        self.generateurSV=Tk.StringVar()
        self.generateur=1
        #On paramètre le cadre graphique
        for i in range(3):
            self.frame.rowconfigure(i,minsize=80)
        for i in range(3):
            self.frame.columnconfigure(i,minsize=80)
        #On crée un nouveau carde, qui servira à une organisation plus poussée des widgets
        self.frame_org=Tk.Frame(self.frame)
        for i in range(3):
            self.frame_org.columnconfigure(i,minsize=107)
        self.frame_org.grid(column=0,columnspan=6,row=2)
        #On crée et on place tous les widgets dans le cadre principal
        Tk.Scale(self.frame,orient="horizontal",from_=0.0,to=1.0,label="Decroissance",resolution=-1,variable=self.decroissanceDV).grid(column=0,row=1)# Widget permettant de choisir une valeur pour decroissanceDV
        Tk.Scale(self.frame,orient="horizontal",length=150,from_=0.0,to=5.0,label="Hauteur",resolution=-1,variable=self.hauteurDV).grid(column=0,row=0)# Widget permettant de choisir une valeur pour hauteurDV
        Tk.Scale(self.frame,orient="horizontal",from_=1,to=8,label="Etapes",resolution=1,variable=self.nb_etapesIV).grid(column=1,row=1,columnspan=2)# Widget permettant de choisir une valeur pour nb_etapesDV. La résolution est de 1, pour avoir des valeurs entières
        Tk.Button(self.frame,command=self.change_gen,textvariable=self.generateurSV,width=8).grid(column=2,row=0)#Bouton permettant de lancer change_gen(), qui va changer le générateur aléatoire utilisé
        Tk.Label(self.frame,anchor='e',text='Generateur').grid(column=1,row=0,sticky='e')#Texte pour nommer le bouton qui change le générateur
        #On crée et on place les éléments dans le cadre secondaire
        Tk.Button(self.frame_org,text='Save',command=self.process_save,width=8).grid(column=1,row=0)#Bouton permettant de lancer process_save(), qui sauvegarde l'image
        Tk.Button(self.frame_org,text="Launch",command=self.process_launch,width=8).grid(column=0,row=0)#Bouton lancant process_launch(), qui permet la création d'un dessin
        #On change les valeurs, afin qu'elles soient plus proche des valeurs intéressantes
        self.decroissanceDV.set(0.4)
        self.hauteurDV.set(2.5)
        self.nb_etapesIV.set(6)
        self.generateurSV.set('Gaussien')
        
    def change_gen(self):#Procédure permettant de faire la rotation entre les 3 générateurs et de changer le texte du bouton lié
        self.generateur+=1
        self.generateur%=3
        if self.generateur==2:
            self.generateurSV.set('Exponentiel')
        elif self.generateur==1:
            self.generateurSV.set('Gaussien')
        else:
            self.generateurSV.set('Uniforme')

    def random(self,value):#Procédure qui permet de retourner un déplacement aléatoire en fonction du générateur de nombre demandé
        gen=self.generateur
        if gen==1:
            return gauss(0,value) #Génération gaussienne centrée en 0 et d'écart type valeur
        elif gen==2:
            return expovariate(1/value) #Géneration exponentielle d'espérance valeur
        else:
            return (random()-0.5)*value*12**0.5 #Géneration uniforme centrée en 0 et d'écart type valeur.

    def terrain(self,triangles,cotes,nb_etapes):
        '''Contient tout pour la génération de terrain'''
        def aire_tri(A,B,C):
            '''Retourne l'aire du triangle ABC'''
            a=A.dist(B) #Les longueurs des côtés 
            b=B.dist(C)
            c=C.dist(A)
            s=(a+b+c)/2
            Aire=(s*(s-a)*(s-b)*(s-c))**0.5 #La formule de Héron, donnat l'aire du triangle en fonction de la longueur des cotés
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
    
        def modif_rang_ajout(self,liste,pos,i,sigma):
            '''Cette procédure permet d'ajouter des points à des lignes de triangle déjà existantes'''
            decroissance=self.decroissanceDV.get()#On récupère la valeur de decroissance    
            ligne=liste[pos]#On stocke la ligne sur laquelle on travaille    
            ligne2=[ligne[0]]#On crée une nouvelle ligne qui contiendra les modifications : elle contient de base le premier point qui ne bougera pas
            for k in range(len(ligne)-1):#On a len-1 segments sur la ligne, donc len-1 points à ajouter
                point=(ligne[k]+ligne[k+1])/2.0 #Les points à ajouter sont les milieux des segments déjà existants
                point = point + Point(0,0,self.random(sigma*decroissance**(i+1))) #Déplace le point verticalement, selon des paramètres choisis
                ligne2=ligne2+[point,ligne[k+1]]#On ajoute le point crée, puis le point existant suivant, qui ne bouge pas
            return [ligne2] #On retourne la nouvelle ligne comprenant les points existants et les points crées
    
        def modif_rang_creation(self,liste,pos,i,cote_0,cote_2,numero_etape_actuelle,sigma):
            '''Cette procédure permet de créer une nouvelle ligne de points'''
            decroissance=self.decroissanceDV.get()#On récupère la valeur de decroissance
            ligne_a=liste[pos-1] #On stocke les 2 lignes entre lesquelles sera ajouté la nouvelle ligne
            ligne_b=liste[pos]
            if cote_0:#Si ce coté a été déja fait, cote_0 est une liste et l'içnstruction conditionelle if sera activée. Si il n'a pas été fait, cote_0 contien False, l'instruction conditionelle else sera activée
                ligne_nouv=[cote_0[(2*pos-1)*(2**(numero_etape_actuelle-i-1))]] #On crée la nouvelle ligne avec le bon premier point. Il faut me croire pour la position du point dans la liste 
            else: #On crée la nouvelle ligne avec le premier point, milieu du segment formé par les premiers points des 2 lignes précédentes.
                ligne_nouv=[(ligne_a[0]+ligne_b[0])/2.0 + Point(0,0,self.random(sigma*decroissance**(i+1)))]
            #On crée les variables contenant les positions des points dont on veut obtenir le milieu du segment
            pos_a=0
            pos_b=1
            for k in range(pos-1):
                point1=(ligne_a[pos_a]+ligne_b[pos_b])/2.0 # Milieu du segment
                point1 = point1 + Point(0,0,self.random(sigma*decroissance**(i+1))) #Déplace le point verticalement
                pos_a+=1 #On ajuste la position du point de la première ligne afin d'obtenir le prochain point 
                point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
                point2 = point2 + Point(0,0,self.random(sigma*decroissance**(i+1))) #Déplace le point verticalement
                pos_b+=1 #On ajuste la position du point de la deuxième ligne afin d'obtenir le prochain point lors du prochain passage dans la boucle
                ligne_nouv+=[point1,point2] #On ajoute les 2 points à la ligne
            if cote_2:# Même chose que pour cote_0
                ligne_nouv+=cote_2[(2*pos-1)*(2**(numero_etape_actuelle-i-1))]
            else:
                ligne_nouv+=[(ligne_a[-1]+ligne_b[-1])/2.0 + Point(0,0,self.random(sigma*decroissance**(i+1)))]#Ici, on prend le milieu des derniers points des lignes,d'où le -1
            return [ligne_nouv] #On retourne la nouvelle ligne formée
    
    
        def modif_triangle(self,triangle,cotes_deja_faits,nb_etapes):
            '''Procédure gérant la génération de terrain à l'échelle d'un triangle initial '''
            hauteur=self.hauteurDV.get() #On récupère la hauteur
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
                    liste2 = liste2 + modif_rang_creation(self,liste,pos,i,cote_0,cote_2,nb_etapes,sigma) + modif_rang_ajout(self,liste,pos,i,sigma)
                if cote_1:#Si le cote est deja fait, c'est équivalent à True, si c'est False, le coté est pas fait et on passe dans la partie else
                    dernier_cote=[cote_1[0]]
                    for k in range(2**(i+1)):#On récupère tout les points dont on a besoin pour le dernier coté
                        dernier_cote=dernier_cote + [cote_1[k*(2**(nb_etapes-i-1))]]
                    dernier_cote=[dernier_cote]
                else:
                    dernier_cote = modif_rang_ajout(self,liste,len(liste)-1,i,sigma)#On utilise la même procédure que pour étendre les autres lignes
                liste2= liste2 + modif_rang_creation(self,liste,len(liste)-1,i,cote_0,cote_2,nb_etapes,sigma) + dernier_cote #On fait à part, car les points de la dernière ligne peuvent ou ne peuvent pas être ajoutés aléatoirement
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
            triangle=modif_triangle(self,triangle,cotes_deja_faits,nb_etapes)#Formation du terrain à partir du triangle
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
    
        
    def process_launch(self):
        '''Procédure reliant une fenetre graphique et le coeur du programme'''
        nb_etapes=self.nb_etapesIV.get()#On récupère le nombre d'étapes
        fig=mlab.figure(1)
        mlab.clf()#La fenêtre de dessin est initialisée
        mlab.draw(self.terrain([(0,1,2),(2,3,4),(4,5,6)],[(Point(0,0,0),Point(1,0,0)),(Point(1,0,0),Point(1,1,0)),(Point(0,0,0),Point(1,1,0)),(Point(1,1,0),Point(0,1,0)),(Point(0,0,0),Point(0,1,0)),(Point(0,0,0),Point(-1,1,0)),(Point(-1,1,0),Point(0,1,0))],nb_etapes))#On affiche le dessin
        
    def process_save(self):
        '''Procédure reliant une fenêtre graphique et la sauvegarde de l'image, qui se fera en un format VRML'''
        fig=mlab.figure(1)#Focus sur la bonne fenêtre
        chemin = tkFileDialog.asksaveasfilename(parent=self.parent,initialdir="/",defaultextension="vrml",initialfile="image", title="Selectionnez le dossier d'enregistrement")#Ouverture d'une fenêtre annexe demandant le chemin d'enregistrement.
        if chemin=='':#Petite sécurité pour moins d'erreur. Si,lors de l'instruction précédente, l'utilisateur a appuyé sur annuler, la chemin retourné est vide. On signale donc que le programme ne va pas sauvegarder
            root2=Tk.Toplevel()#On ouvre une fenêtre pour signaler la non sauvegarde
            texte=Tk.Label(root2,text='La sauvegarde a échoué.\nChemin spécifié non valide',height=2)
            btOk=Tk.Button(root2,text='Ok',command=root2.destroy)
            texte.pack()
            btOk.pack()
            root2.mainloop()
        mlab.savefig(chemin)#Le fichier est enregistré
        #Bloc pour modifier l'extension du fichier, et faire en sorte de ne pas effacer un autre fichier image. L'extension doit être modifiée, car, pour Blender, le logiciel utilisé pour lire les fichiers crées, les fichiers VRML ont une extension en .wrl
        nom, ext = os.path.splitext(chemin) #Le nom et l'extension du fichier sont séparés
        i=0# Le fichier est nommé par défaut image. Pour ne pas effacer d'autres fichiers, on rajoute _i à la fin du nom, où i est un nombre. i est incrémenté jusqu'à ce que l'emplacement soit disponible
        nom=nom+"_"
        while os.path.isfile(nom+str(i)+".wrl"):#Instrction testant si le fichier existe, et renvoyant true si c'est le cas
            i+=1
        nom=nom+str(i)
        os.rename(chemin, nom + ".wrl")#Instruction permettant de renommer le fichier "chemin" en nom +".wrl", qui est le même nom, à l'extension et un nombre à la fin près
        #Fin du bloc

def main():
    '''Procédure principale créant une fenêtre graphique'''
    #On crée la fenêtre principale et les différents cadre graphiques 
    root=Tk.Tk()
    frameP=Tk.Frame(root)
    frameM1=Methode1(root)
    frameM2=Methode2(root)
    frameM1.frame.grid(row=0, column=0, sticky='news')
    frameM2.frame.grid(row=0, column=0, sticky='news')
    frameP.grid(row=0, column=0, sticky='news')
    #On configure le acdre principal
    for i in range(6):
        frameP.rowconfigure(i,minsize=40)
    for i in range(4):
        frameP.columnconfigure(i,minsize=80)
    #On ajoute les boutons au cadre principal
    Tk.Button(frameP,text='Methode 1',command=frameM1.frame.tkraise,width=12).grid(column=0,columnspan=2,row=0,rowspan=5)
    Tk.Button(frameP,text='Methode 2',command=frameM2.frame.tkraise,width=12).grid(column=2,columnspan=2,row=0,rowspan=5)
    Tk.Button(frameP,text="Quitter",command=root.destroy,width=8).grid(column=0,columnspan=4,row=5,sticky='se',pady=10,padx=10)
    #On ajoute les boutons permettant de retourner au cadre principal aux 2 cadres graphiques des 2 méthodes
    Tk.Button(frameM2.frame_org,text='Retour',command=frameP.tkraise,width=8).grid(column=2,row=0)
    Tk.Button(frameM1.frame,text='Retour',command=frameP.tkraise,width=8).grid(row=3,column=4,columnspan=2)
    fig=mlab.figure(1)#On affiche la fenêtre mayavi, afin que l'utilisateur puisse la bouger
main()
