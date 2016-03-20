def modif_rang_ajout(liste,pos,i):
    '''Cette procédure permet d'ajouter des points à des lignes déjà existantes'''
    ligne=liste[pos]#On stocke la ligne sur laquelle on travaille
    ligne2=[ligne[0]]#On crée une nouvelle ligne qui contiendra les modifications : elle contient de base le premier point qui ne bougera pas
    long=len(ligne)
    for k in range(long-1):
        point=(ligne[k]+ligne[k+1])/2.0 #Les points à ajouter sont les milieux des segments
        #Bouger le point selon la normale à déterminer
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
        #Rajouter commande pour bouger point
        pos_a+=1 #On ajuste la position du point de la première ligne afin d'obtenir le prochain point 
        point2=(ligne_a[pos_a]+ligne_b[pos_b])/2.0
        #Rajouter commande pour bouger point
        pos_b+=1 #On ajuste la position du point de la deuxième ligne afin d'obtenir le prochain point lors du prochain passage dans la boucle
        ligne_nouv=ligne_nouv+[point1,point2] #On ajoute les 2 points à la ligne
    ligne_nouv=ligne_nouv+[(ligne_a[-1]+ligne_b[-1])/2.0] #On ajoute le dernier point, milieu des 2 derniers points des 2 lignes
    return [ligne_nouv]


liste=[[Point(0,0,0)],[Point(-0.5,1,0),Point(0.5,1,0)]] 
#Le format utilisé est le suivant : une liste de listes de points, chaque liste correspondant à une ligne du triangle, donc contenant les points de cette ligne
for i in range(nb_etapes):
	liste2=[liste[0]] 
	#Cette liste contiendra le triangle avec ses nouveaux points. On commence par mettre la première ligne de 1 point, qui ne change jamais
	#La liste contenant le triangle précédant ne sera pas modifiée 
    	for pos in range(1,len(liste)):
            	#Lors de l'ajout de nouveaux points, il se passe 2 choses : on créé de nouvelles lignes, et on ajoute des points aux lignes existantes, d'où les 2 procédures
		liste2 = liste2 + modif_rang_creation(liste,pos,i) + modif_rang_ajout(liste,pos,i)
	liste=liste2 #La liste principale est modifiée, car le nouveau triangle est totalement construit
