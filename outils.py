#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 13:42:25 2017

@author: Manon
"""

# -*- coding: utf-8 -*-


import numpy as np
# cases dispo prenant en compte les limite 
# pas les murs !!!

# 0 : droite
# 1 : gauche
# 2 : bas
# 3 :haut

# Nouvelle fonction case dispo :
# elle renvoit un vecteur de trois cases (dont les coordonnées peuvent ne pas 
# être dans la grille)
# qui correspondent aux trois cases "théoriques" que pourraient atteindre le
# pion. Selon la position du pion, certaines sont rendus inaccessibles
# TODO : utiliser is in grid pour simplifier la fonction
def cases_dispo(g,i,j,action):
    cases = np.zeros((3,3))
    #si on va a droite  
    if action == 0 :
        cases = [[i-1, j+1,0], [i,j+1,0], [i+1,j+1,0]]
        if j!=(len(g[0])-1):
            cases[1][2]=1
            if i != 0:
                cases[0][2]=1
            if i != (len(g)-1):
                cases[2][2]=1
    #gauche           
    if action == 1 :
        cases = [[i-1, j-1,0], [i,j-1,0], [i+1,j-1,0]]
        if j!=0:
            cases[1][2]=1
            if i != 0:
                cases[0][2]=1
            if i != (len(g)-1):
                cases[2][2]=1   
    #bas
    if action == 2 :
        cases = [[i+1, j-1,0], [i+1,j,0], [i+1,j+1,0]]
        if i!=(len(g)-1):
            cases[1][2]=1
            if j != 0:
                cases[0][2]=1
            if j != (len(g[0])-1):
                cases[2][2]=1
    #haut
    if action == 3 :
        cases = [[i-1, j-1,0], [i-1,j,0], [i-1,j+1,0]]
        if i!=0:
            cases[1][2]=1
            if j != 0:
                cases[0][2]=1
            if j != (len(g[0])-1):
                cases[2][2]=1           
    return cases

#cases_dispo(g,9,0,2)

def is_in_grid(g, i, j):
    if 0<=i and i < len(g) and 0<=j and j < len(g[0]) :
        return True
    else : 
        return False

#Calcul des probas d'aller en x et a droite et a gauche de x 
#prend en compte l'incertain
# i et j sont les coordonnées du point d'origine
def probas_action(g,i,j,p,action):
    cases = cases_dispo(g,i,j,action)
        
    if (len(g.shape)== 3) :   
        for i,case in enumerate(cases):
            print(case)
            if is_in_grid(g, case[0], case[1]) and g[case[0]][case[1]][0] == 0 :
                case[2] = 0
    
    else :
        for i,case in enumerate(cases):
            #print(case)
            if is_in_grid(g, case[0], case[1]) and g[case[0]][case[1]] == 0 :
                case[2] = 0
    #terme du milieu est un mur
    if cases[1][2] == 0:
        cases[0][2] = 0
        cases[1][2] = 0
        cases[2][2] = 0
    else :
        if cases[0][2] == 0:
            if cases[2][2] == 0:
                # les cases voisines sont des murs
                cases[1][2] = 1
            # la derniere case est accessible
            else:
                cases[1][2] = (1+p)/2
                cases[2][2] = (1-p)/2
        #premiere case n'est pas un mur
        else:
            if cases[2][2] == 0:
                cases[0][2] = (1-p)/2
                cases[1][2] = (1+p)/2
            # toutes les cases sont accessibles
            else:
                cases[0][2] = (1-p)/2
                cases[1][2] = p
                cases[2][2] = (1-p)/2   
   # print(cases)
    return cases

# probas_action(g,0,0,0.25,1)


# Méthode qui prend en entrée une matrice de politique et qui en ressort
# un affichage simplifié de cette politique
def from_action_to_dir(matrix, g):
    result = np.zeros((len(matrix), len(matrix[0])), dtype=str)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if g[i][j] == 0 : # on est sur un mur
                result[i][j]='x'
            else :
                if matrix[i][j]==0:
                    result[i][j]= ">"
                elif matrix[i][j]==1:
                    result[i][j]= "<"
                elif matrix[i][j]==2:
                    result[i][j]= "v"    
                else :
                    result[i][j]= "^"
    return result

#prend en compte l'incertain
def sum_p_v(g,val_etats,i,j,p,action):
    somme = 0
    cases = probas_action(g,i,j,p,action)
    for i,c in enumerate(cases): 
        if c[2] != 0: # on teste si la case est accessible (permet de ne pas
            # avoir de problème avec les cases exterieurs)
            somme += c[2] * val_etats[c[0]][c[1]]
    return somme

     

# val_etats =  np.random.rand(10,15)
# sum_p_v(g,val_etats,0,0,0.25,1

#renvoi reward apres l'action
# None si action hors limite
