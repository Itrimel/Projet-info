def modif_rang_ajout(liste,pos,i):
    ligne=liste[pos]
    ligne2=[ligne[0]]      
    long=len(ligne)
    for k in range(long-1):
        point=(ligne[k]+ligne[k+1])/2.0
        #Bouger le point selon la normale à déterminer
        ligne2=ligne2+[point,ligne[k+1]]
    return [ligne2]

def modif_rang_creation(liste,pos,i):
    ligne_a=liste[pos-1]
    ligne_b=liste[pos]
    ligne_nouv=[(ligne_a[0]+ligne_b[0])/2.0]
    pos_a=0
    pos_b=1
    for k in range(pos-1):
        point1=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        #Rajouter commande pour bouger point
        pos_a+=1
        point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        #Rajouter commande pour bouger point
        pos_b+=1
        ligne_nouv=ligne_nouv+[point1,point2]
    ligne_nouv=ligne_nouv+[(ligne_a[-1]+ligne_b[-1])/2.0]
    return [ligne_nouv]


liste=[[Point(0,0,0)],[Point(-0.5,1,0),Point(0.5,1,0)]]
for i in range(nb_etapes):
	liste2=[liste[0]]
    	for pos in range(1,len(liste)):
            	liste2 = liste2 + modif_rang_creation(liste,pos,i) + modif_rang_ajout(liste,pos,i)
            	liste=liste2
    	creation_image(liste)
