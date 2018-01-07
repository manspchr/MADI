#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 16:52:13 2018

@author: Manon
"""
import numpy as np
import outils as ot
import time as tm
import grille_avec_chiffre as gr
#import gurobipy as grb

# definition des actions
liste_actions = [0,1,2,3]

## TODO : vérifier que ça marche !!
def pl_part3_1(g,liste_actions,rewards,p,gamma,epsilon):

    # Create a new model
    m = grb.Model("politique-mixte")

    x_sa = []

    # Create variables
    # variable objective
    z = m.addVar(name="z")

    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                n = "x["+str(i)+"]["+str(j)+"]["+str(action)+']'
                x = m.addVar(vtype=grb.GRB.CONTINUOUS, name=n)
                x_sa.append(x)

    # x_sa tableau à trois dimension, 2 pour l'état, et 1 pour l'action
    # pour chaque etat on renvoit un vecteur en principe de zeros et de 1 avec 1 sur 
    x_sa = np.array(x_sa)
    x_sa = np.reshape(x_sa,(len(g),len(g[0]),len(liste_actions)))

    m.setObjective(z, grb.GRB.MINIMIZE)
    print((x_sa.shape))
    
    # Create constraints 
        # autre méthode : 
    # dans chaque case, on teste la ressource et on l'ajoute au bon cout
    # -> permet de ne parcourir qu'une seule fois la grille au lieu de 4
    f_x=np.zeros(5)
    for i in range(len(g)):
        for j in range(len(g[0])):
            # on teste la ressource
            ressource = g[i][j][0]
            if ressource != 0: # si il s'agit bien d'une ressource et pas d'un mur
                somme_actions = 0
                for action in liste_actions:
                    somme_actions += x_sa[i][j][action]
                r = -g[i][j][1]
                terme_etat = -r * somme_actions
                f_x[ressource] += terme_etat             
    
    # Contraintes
    
    for ressource in range(4)+1 : 
        m.addConstr(z <= f_x[ressource])

    for i in range(len(g)):
        for j in range(len(g[0])): # pour chaque etat
            sum_actions = 0
            for action in liste_actions :
                sum_actions += x_sa[i][j][action]
            sum_2 = 0
            for k in range(len(g)):
                for l in range(len(g[0])):
                    somme = 0
                    for action in liste_actions : 
                        cases = ot.probas_action(g, k, l, p, action)
                        for i, c in enumerate(cases):
                            somme += cases[2] * x_sa[k][l]
                    sum_2 += somme
            
            m.addConstr(sum_actions + gamma * sum_2 == 1)
     
    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions : 
                m.addConstr(x_sa[i][j] >= 0)

    m.optimize()

## TODO : tester la forme de x_sa et voir si on peut se ramener à x_sa_2
#    x_sa = np.reshape(np.array([v.x for v in m.getVars()]),(len(g),len(g[0])))
#    # print(x_sa)
#    # print(x_sa.shape)
#    x_sa_2 = np.zeros(2,2)
#    for i in range(len(g)):
#        for j in range(len(g[0])): # pour chaque etat 
#            if not x_sa[i][j] == np.zeros(4):
#                x_sa_2 = x_sa[i][j].index(1)
#            else :
#                x_sa_2 = 5
 
    return x_sa

def pl_part3_2(g,liste_actions,rewards,p,gamma,epsilon):

    # Create a new model
    m = grb.Model("politique-mixte")

    x_sa = []

    # Create variables
    # variable objective
    z = m.addVar(name="z")

    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                n = "x["+str(i)+"]["+str(j)+"]["+str(action)+']'
                x = m.addVar(vtype=grb.GRB.CONTINUOUS, name=n)
                x_sa.append(x)
       
   for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                n = "d["+str(i)+"]["+str(j)+"]["+str(action)+']'
                d = m.addVar(vtype=grb.GRB.BINARY, name=n)
                d_sa.append(d)         
    

    # x_sa tableau à trois dimension, 2 pour l'état, et 1 pour l'action
    # pour chaque etat on renvoit un vecteur en principe de zeros et de 1 avec 1 sur 
    x_sa = np.array(x_sa)
    x_sa = np.reshape(x_sa,(len(g),len(g[0]),len(liste_actions)))

    d_sa = np.array(d_sa)
    d_sa = np.reshape(d_sa,(len(g),len(g[0]),len(liste_actions)))


    m.setObjective(z, grb.GRB.MINIMIZE)
    print((x_sa.shape))
    
    # Create constraints 
        # autre méthode : 
    # dans chaque case, on teste la ressource et on l'ajoute au bon cout
    # -> permet de ne parcourir qu'une seule fois la grille au lieu de 4
    f_x=np.zeros(5)
    for i in range(len(g)):
        for j in range(len(g[0])):
            # on teste la ressource
            ressource = g[i][j][0]
            if ressource != 0: # si il s'agit bien d'une ressource et pas d'un mur
                somme_actions = 0
                for action in liste_actions:
                    somme_actions += x_sa[i][j][action]
                r = -g[i][j][1]
                terme_etat = -r * somme_actions
                f_x[ressource] += terme_etat             
    
    # Contraintes
    
    for ressource in range(4)+1 : 
        m.addConstr(z <= f_x[ressource])

    for i in range(len(g)):
        for j in range(len(g[0])): # pour chaque etat
            sum_actions = 0
            for action in liste_actions :
                sum_actions += x_sa[i][j][action]
            sum_2 = 0
            for k in range(len(g)):
                for l in range(len(g[0])):
                    somme = 0
                    for action in liste_actions : 
                        cases = ot.probas_action(g, k, l, p, action)
                        for i, c in enumerate(cases):
                            somme += cases[2] * x_sa[k][l]
                    sum_2 += somme
            
            m.addConstr(sum_actions + gamma * sum_2 == 1)
     
    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions : 
                m.addConstr(x_sa[i][j] >= 0)

    # Ajout des contraintes des politiques pures
    for i in range(len(g)):
        for j in range(len(g[0])):
            somme_actions =0
            for action in liste_actions : 
                somme_actions += d_sa[i][j][a]
            m.addConstr(somme_actions <= 1)    
    
    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions :     
                m.addConstr((1-gamma)*x_sa[i][j][a] - d_sa[i][j][a] <= 0) 
                
    
  
    m.optimize()

## TODO : tester la forme de x_sa et voir si on peut se ramener à x_sa_2, à renvoyer à la place
#    x_sa = np.reshape(np.array([v.x for v in m.getVars()]),(len(g),len(g[0])))
#    # print(x_sa)
#    # print(x_sa.shape)
#    x_sa_2 = np.zeros(2,2)
#    for i in range(len(g)):
#        for j in range(len(g[0])): # pour chaque etat 
#            if not x_sa[i][j] == np.zeros(4):
#                x_sa_2 = x_sa[i][j].index(1)
#            else :
#                x_sa_2 = 5
 
    return x_sa


grille = gr.Grille_avec_chiffres(10,10,2,0.2,0.2,0.2,0.2,0.2,1000)
p = 0.6
gamma = 0.9
epsilon = 0.00001

# Test iteration de la valeur
#d,v,t,time = iteration_de_la_valeur(grille.g,p,gamma,epsilon)
#print(ot.from_action_to_dir(d,grille.g))

## Test iteration de la politique
#d,v,t,time = iteration_de_la_politique(grille.g,p,gamma,epsilon)
#print(ot.from_action_to_dir(d,grille.g))

# Test PL
#d,v,time = pl_part3_1(grille.g, p, gamma, epsilon)
#print(ot.from_action_to_dir(d,g))

#grille.Mafenetre.mainloop() #Affichage 

#print(mean_experienced_cost(d,grille.g,p,10))


    
    