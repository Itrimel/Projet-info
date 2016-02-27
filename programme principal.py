triangle_0=Triangle(Point(0,0,0),Point(1,0,0),Point(0,1,0))
liste=[triangle_0]
for i in range(nb_etapes):
    for i in range(len(liste)):
            distance = gauss(4**(-i),0.1**(-i))#Donne un nombre aléatoire selon une répartition gaussienne. A voir pour les paramètres ( le premier est la valeur moyenne, le second l’écart type)
            liste=liste+[liste.pop(0).creation_triangle(distance)]#Enlève un triangle à la liste pour ajouter les trois triangles qui en sont issus
