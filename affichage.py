'''Pour afficher une image'''
from tkinter.filedialog import *
# On crée une fenêtre, fenêtre principale de notre interface
fenetre = Tk()
#La fonction askopenfilename retourne le chemin du fichier que vous avez choisi avec le nom de celui-ci.
filepath = askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png'),('all files','.*')])
photo = PhotoImage(file=filepath)
canvas = Canvas(fenetre, width=photo.width(), height=photo.height(), bg="yellow")
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack()
