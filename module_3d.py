# -*- coding: utf-8 -*-
import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit où enregistrer
import numpy as np #Module pour l'organisation des coordonnées pour l'affichage
import os #Module pour rennomer le fichier à la fin
from mayavi import mlab #Module pour générer le dessin
def creation_image(save="True",chemin="ask"):
	'''Créé le dessin, à partir d'une liste.  La variable save gère si l'image est enregistrée (Par défaut,oui), à l'emplacement "chemin". 
	Par défaut,l'emplacement est demandé à l'utilisateur'''
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
