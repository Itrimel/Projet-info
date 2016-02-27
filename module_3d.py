# -*- coding: utf-8 -*-
import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit où enregistrer
import numpy as np #Module pour l'organisation des coordonnées pour l'affichage
import os #Module pour rennomer le fichier à la fin
from mayavi import mlab #Module pour générer le dessin
def lect_fichier(chemin="ask"):
	'''Premet de lire un document texte avec une liste, et reourne la liste. Demande le chemin à l'utilisateur par défaut'''
	if chemin=="ask": #Instructions permettant à l'utilisateur de choisi le fichier texte
		root = Tkinter.Tk()
		root.withdraw()
		fichier = tkFileDialog.askopenfile(mode='r',parent=root,initialdir="Documents/",title='Selectionnez le fichier image')
	else:
		fichier=open(chemin,'r')
	liste=fichier.read()#Permet de stocker dans liste la chaine de caractère contennant la liste : '[1,2,3]' par exemple
	liste=eval(liste) #Permet d'enregister dans la variable la liste au lieu de la chaine de caractère : eval('[1,2,3]')=[1,2,3] par exemple
	return liste
def creation_image(chemin1="ask",save="True",chemin2="ask"):
	'''Créé le dessin, à partir d'un document texte placé à l'emplacement "chemin1". Par défaut, cet emplacement sera demandé à l'utilisateur.
	La variable save gère si l'image est enregistrée (Par défaut,oui), à l'emplacement "chemin2". Par défaut,l'emplacement est demandé à l'utilisateur'''
	liste=lect_fichier(chemin1) #enregistre dans liste la liste contenue dans le fichier ,désigné ou pas
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