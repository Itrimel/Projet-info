# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
from random import *
from math import *

def appartenance_Triangle(L_Triangle, P):
    #permutations pour effectuer la procédure sur les 3 côtés du triangle
    #on utilise cette liste pour alléger l'écriture
    L_Permutations=[(0,1,2),(0,2,1),(1,2,0)]
    #la boucle effectue la vérification sur les 3 côtés
    for (a,b,c) in L_Permutations:
        if ((L_Triangle[a][1]-L_Triangle[b][1])*L_Triangle[c][0]+(L_Triangle[b][0]-L_Triangle[a][0])*L_Triangle[c][1]+(L_Triangle[a][0]*L_Triangle[b][1]-L_Triangle[b][0]*L_Triangle[a][1]))*((L_Triangle[a][1]-L_Triangle[b][1])*P.xP+(L_Triangle[b][0]-L_Triangle[a][0])*P.yP+(L_Triangle[a][0]*L_Triangle[b][1]-L_Triangle[b][0]*L_Triangle[a][1]))<0:
            #si le produit est négatif, donc si le point n'est pas du même côté que le 3ème sommet, on abandonne
            return(False)
            #sinon, si c'est bon pour les 3 côtés, le point appartient au triangle
    return(True)
    

def base_Triangle(nb_points,xmax,ymax):
    L_Rectangle=[(0,0),(xmax,0),(xmax,ymax),(0,ymax)]
    #LL_Triangles est une liste de listes, chaque sous-liste représentant 1 triangle
    LL_Triangles=[]
    x=uniform(1,xmax-1)
    y=uniform(1,ymax-1)
    #on crée à la main les 4 premières sous-listes à partir du rectangle et du premier point aléatoire
    LL_Triangles.append([L_Rectangle[0],L_Rectangle[1],(x,y)])
    LL_Triangles.append([L_Rectangle[1],L_Rectangle[2],(x,y)])
    LL_Triangles.append([L_Rectangle[2],L_Rectangle[3],(x,y)])
    LL_Triangles.append([L_Rectangle[3],L_Rectangle[1],(x,y)])
    for i in range(nb_points-1):
        L_BTriangle=[]
        #pour que le point aléatoire ne soit pas sur le bord du rectangle
        x=uniform(1,xmax-1)
        y=uniform(1,ymax-1)
        #on définit L_Triangle comme étant un élément de LL_Triangles, càd une liste de 3 points
        for L_Triangle in LL_Triangles:
            #on teste l'appartenance de P à l'un des triangles, si c'est validé on renomme la bonne sous-liste
            if appartenance_Triangle(L_Triangle,Point(x,y)):
                L_BTriangle=L_Triangle
        #on crée trois nouveaux triangles à partir de la bonne sous-liste
        LL_Triangles.append([L_BTriangle[0],L_BTriangle[1],(x,y)])
        LL_Triangles.append([L_BTriangle[0],L_BTriangle[2],(x,y)])
        LL_Triangles.append([L_BTriangle[1],L_BTriangle[2],(x,y)])
        #et on supprime l'ancien triangle de la liste
        LL_Triangles.remove(L_Triangle)
    #liste temporaire d'arêtes, il y aura des doublons dedans
    L_TempoAretes=[]
    #liste finale des arêtes, sans doublons
    L_Aretes=[]
    LF_Triangles=[]
    #on crée une liste d'arêtes temporaire à partir de la liste de tous les triangles  
    for L_Triangle in LL_Triangles:
        L_TempoAretes.append([L_Triangle[0],L_Triangle[1]])
        L_TempoAretes.append([L_Triangle[0],L_Triangle[2]])
        L_TempoAretes.append([L_Triangle[1],L_Triangle[2]])
        LF_Triangles.append([L_TempoAretes[0],L_TempoAretes[1],L_TempoAretes[2]])
    #on crée la liste finale des arêtes en supprimant les doublons
    for k in L_TempoAretes:
        if k not in L_Aretes:
            L_Aretes.append(k)
    
    return(LF_Triangles,L_Aretes)
