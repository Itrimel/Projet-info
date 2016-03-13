from random import * #Utilisé pour le calcul de la distance, à l'aide d'un générateur gaussien

def milieu_triangle0 (Triangle(p1,p2,p3)) :
    C=Point(0,0,0) #somme des sommets du triangle
    C=Point((xp1+xp2+xp3)/3,(yp1+yp2+yp3)/3,(zp1+zp2+zp3)/3)#C devient le centre du triangle
    return (C)

def milieu_triangle (T) :
    C= (T.point1+T.point2+T.point3)/3 #C devient le centre du triangle
    return(C)

def Normale0(Triangle(p1,p2,p3), distance):
    u=array([xp1-px2),(yp1-yp2),(zp1-zp2)])#On calcule les deux vecteurs
    v=array([xp1-px3),(yp1-yp3),(zp1-zp3)])
    #Voilà fifi le produit vectoriel
    w=array([(yp1-yp2)*(zp1-zp3)-(zp1-zp3)*(yp1-yp3),(zp1-zp2)*(xp1-xp3)-(xp1-xp3)*(zp1-zp3),(xp1-xp2)*(yp1-yp3)-(yp1-yp3)*(xp1-xp3)])
    p4=milieu_triangle(Triangle(p1,p2,p3)+ w*distance#point sur la normale
    return(p4)
    
def Normale(T, distance,centre):
    M=milieu_triangle(T)
    p1=T.point1
    p2=T.point2
    p3=T.point3
    u=p1-p2#On calcule les deux vecteurs
    v=p1-p3
    #Voilà fifi le produit vectoriel
    w=u^v
    norme=(u & u)**1/2 #Norme de w=produit scalaire par lui même à la racine carrée
    w=w/norme#w est maintenant normé
    a=centre-M#Vecteur allant du centre du triangle au point centre, qui est à l'interieur de la structure
    if w & a >0: #On fait le produit scalaire des 2 vecteurs. Si le produit scalaire est positif, cela signifie que les 2 vecteurs sont environ du même sens, donc que w pointe vers l'interieur
        w=-1*w#On prend l'opposé de w, qui pointe alors vers l'exterieur
    p4=M+distance*w#point sur la normale
    return(p4)

def creation_triangle(T,distance,centre):
    C=Normale(T,distance,centre)
    T1=Triangle(T.point1,T.point2,C)
    T2=Triangle(T.point1,T.point3,C)
    T3=Triangle(T.point2,T.point3,C)
    return[T1,T2,T3] #retourner les triangles dans une liste pour être compatible avec la boucle principale

triangle_0=Triangle(Point(0,0,0),Point(1,0,0),Point(0,1,0))#Triangle de la base: points éventuellement modifiables
distance = abs(gauss(1,0.3))
liste=creation_triangle(triangle_0,distance,Point(0,0,-1))#On fait la première étape à part
centre_1=milieu_triangle(liste[0])
centre_2=milieu_triangle(liste[1])
centre_3=milieu_triangle(liste[2])
centre=milieu_triangle(Triangle(centre_1,centre_2,centre_3))#On crée un point qui sera au centre de la montagne, et qui permettera de bien extruder vers l'extérieur
for i in range(nb_etapes):
    for j in range(len(liste)):
        distance = abs(gauss(4**(-i-1),3**(-i-1)))#Donne un nombre aléatoire selon une répartition gaussienne. A voir pour les paramètres ( le premier est la valeur moyenne, le second l’écart type)
        liste=liste+creation_triangle(liste.pop(0),distance,centre)#Enlève un triangle à la liste pour ajouter les trois triangles qui en sont issus

for i in range(len(liste)):#On transforme chaque élément de la liste, pour que le module d'affichage 3d puisse en faire qqchose
    triangle=liste[i]
    liste[i]=[(triangle.point1.xP,triangle.point1.yP,triangle.point1.zP),(triangle.point2.xP,triangle.point2.yP,triangle.point2.zP),(triangle.point3.xP,triangle.point3.yP,triangle.point3.zP)]
