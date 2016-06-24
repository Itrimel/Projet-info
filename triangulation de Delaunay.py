# -*- coding: utf-8 -*-
import numpy as np
from random import random
import matplotlib.pyplot as plt
def creation_triangle(A,B,C):
    x1,y1,x2,y2,x3,y3=A[0],A[1],B[0],B[1],C[0],C[1]
    xc= ((x3**2-x2**2+y3**2-y2**2)/(2*(y3-y2))-(x2**2-x1**2+y2**2-y1**2)/(2*(y2-y1)))/((x3-x2)/(y3-y2)-(x2-x1)/(y2-y1))
    sommet= np.array([xc,-(x2-x1)/(y2-y1)*xc+(x2**2-x1**2+y2**2-y1**2)/(2*(y2-y1))])
    rayon=np.linalg.norm(A-sommet)
    return [A,B,C,sommet,rayon]

def point_interieur(A,B,C,X): 
    if (np.cross(A-X,B-X)>0 and np.cross(B-X,C-X)>0 and np.cross(C-X,A-X)>0) or (np.cross(A-X,B-X)<0 and np.cross(B-X,C-X)<0 and np.cross(C-X,A-X)<0):
        return True
    else:
        return False

def maj_pointeur(triangulation,matr_relation,num_nouv,num_tri):
    cote1_nouv_tri=[triangulation[num_nouv][0],triangulation[num_nouv][1]]
    tri_prec=[triangulation[num_tri][0],triangulation[num_tri][1],triangulation[num_tri][2]]
    if ((tri_prec[1]==cote1_nouv_tri[0]).all() and (tri_prec[0]==cote1_nouv_tri[1]).all()) or ((tri_prec[0]==cote1_nouv_tri[1]).all() and (tri_prec[1]==cote1_nouv_tri[0]).all()):
        i=1
    elif ((tri_prec[1]==cote1_nouv_tri[0]).all() and (tri_prec[2]==cote1_nouv_tri[1]).all()) or ((tri_prec[1]==cote1_nouv_tri[1]).all() and (tri_prec[2]==cote1_nouv_tri[0]).all()):
        i=2
    else:
        i=3
    try:
        relation=matr_relation[num_tri].tolist()
        relation=relation.index(i)
        matr_relation[num_nouv][relation]=1
        matr_relation[relation][num_nouv]=matr_relation[relation][num_tri]
    except:
        1==1
    return matr_relation

def test_triangle(relations,triangulation,point,i):
    try:
        triangle=relations.index(i)
        triangle_temp=triangulation[triangle]
        if np.linalg.norm(point-triangle_temp[3])>triangle_temp[4]:
            triangle=False
        else:
            triangle+=1
    except ValueError:
        triangle=False
    return triangle

nb_points=10
points=[np.array([random()*2,random()*2]) for i in range(nb_points)]
plt.plot([i[0] for i in points],[i[1] for i in points],'ro')
centre=sum(points)/nb_points
maximum=0
for point in points:
    rayon=np.linalg.norm(point-centre)
    if rayon>maximum:
        maximum=rayon
maximum*=4
orgA,orgB,orgC=centre+maximum*np.array([2**-0.5,2**-0.5]),centre+maximum*np.array([-0.9659258263,0.2588190451]),centre+maximum*np.array([0.2588190451,-0.9659258263])
triangulation=[creation_triangle(orgA,orgB,orgC)]
matr_relation=np.array([0])[np.newaxis]
for point in points:
    #Cherche point se trouve dans quel triangle
    for i in range(len(triangulation)):
        triangle_base=i
        if point_interieur(triangulation[i][0],triangulation[i][1],triangulation[i][2],point):
            break
    #Cherche si suppression des triangles voisins
    relations=matr_relation[triangle_base].tolist()
    triangle1=test_triangle(relations,triangulation,point,1)
    triangle2=test_triangle(relations,triangulation,point,2)
    triangle3=test_triangle(relations,triangulation,point,3)
    #Création du contour
    contour=[triangulation[triangle_base][0]]
    if triangle1:
        pos=matr_relation[triangle1-1][triangle_base]
        dico={1:triangulation[triangle1-1][2],2:triangulation[triangle1-1][0],3:triangulation[triangle1-1][1]}
        contour+=[dico[pos]]
    contour+=[triangulation[triangle_base][1]]
    if triangle2:
        pos=matr_relation[triangle2-1][triangle_base]
        dico={1:triangulation[triangle2-1][2],2:triangulation[triangle2-1][0],3:triangulation[triangle2-1][1]}
        contour+=[dico[pos]]
    contour+=[triangulation[triangle_base][2]]
    if triangle3:
        pos=matr_relation[triangle3-1][triangle_base]
        dico={1:triangulation[triangle3-1][2],2:triangulation[triangle3-1][0],3:triangulation[triangle3-1][1]}
        contour+=[dico[pos]]
    contour+=[triangulation[triangle_base][0]]
    #Ajout des nouveaux triangles, des colonnes et des lignes vides
    n0=matr_relation.shape[0]
    for i in range(len(contour)-1):
        triangulation+=[creation_triangle(contour[i+1],contour[i],point)]
        dim=matr_relation.shape[0]
        matr_relation=np.vstack((matr_relation,np.array([0 for i in range(dim)])))
        matr_relation=np.hstack((matr_relation,np.array([0 for i in range(dim+1)])[np.newaxis].T))
    #Ajout des 2 et 3
    matr_relation[n0][-1]=2
    for i in range(1,len(contour)-1):
        matr_relation[n0+i][n0+i-1]=2
    matr_relation[-1][n0]=3
    for i in range(len(contour)-2):
        matr_relation[n0+i][n0+i+1]=3
    #Ajout des 1 et modif des triangles voisins
    pos=n0
    if triangle1:
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle1-1)
        pos+=1
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle1-1)
        pos+=1
    else:
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle_base)
        pos+=1
    if triangle2:
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle2-1)
        pos+=1
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle2-1)
        pos+=1
    else:
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle_base)
        pos+=1
    if triangle3:
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle3-1)
        pos+=1
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle3-1)
        pos+=1
    else:
        matr_relation=maj_pointeur(triangulation,matr_relation,pos,triangle_base)
        pos+=1
    positions=[triangle_base]
    if triangle1:
        positions+=[triangle1-1]
    if triangle2:
        positions+=[triangle2-1]
    if triangle3:
        positions+=[triangle3-1]
    for i in range(len(positions)):
        pos=max(positions)
        triangulation.pop(pos)
        matr_relation=np.delete(matr_relation,(pos),axis=0)
        matr_relation=np.delete(matr_relation,(pos),axis=1)
        positions.remove(pos)

triangles=[]
for triangle in triangulation:
    if (triangle[0] != orgA).all() and (triangle[0] != orgB).all() and (triangle[0] != orgC).all() and (triangle[1] != orgA).all() and (triangle[1] != orgB).all() and (triangle[1] != orgC).all() and (triangle[2] != orgA).all() and (triangle[2] != orgB).all() and (triangle[2] != orgC).all():
        triangles+=[[triangle[0],triangle[1],triangle[2]]]
        plt.plot([i[0] for i in triangles[-1]]+[triangles[-1][0][0]],[i[1] for i in triangles[-1]]+[triangles[-1][0][1]])
plt.show()


    
    

    
        
