# -*- coding: utf-8 -*-
import Tkinter, tkFileDialog #Module pour que l'utilisateur choisisse l'endroit o� enregistrer
import numpy as np #Module pour l'organisation des coordonn�es pour l'affichage
import os #Module pour rennomer le fichier � la fin
from mayavi import mlab #Module pour g�n�rer le dessin
def creation_image(liste,save="True",chemin="ask"):
	'''Cr�� le dessin, � partir d'une liste de points.
	La variable save g�re si l'image est enregistr�e (Par d�faut,oui), � l'emplacement "chemin". Par d�faut,l'emplacement est demand� � l'utilisateur'''
	X=[]#Initialisation des 3 listes contenant les coordonn�es des sommets des triangles
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