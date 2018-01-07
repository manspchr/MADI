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
import gurobipy as grb
import algos as alg
import pandas as pd
from matplotlib import pyplot as plt
# definition des actions
liste_actions = [0,1,2,3]


default_tests = 1
default_nbLignes = 10
default_nbCol = 10
default_p = 1
default_gamma = 0.9
default_epsilon = 0.00001



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
    
    # on va recuperer x_sa
    
    # d'après Propriété 2
    delta_sa = np.zeros(len(g), len(g[0]), 4)
    # D'après la proposition 2
    for i in range(len(g)):
        for j in range(len(g[0])):
            somme_actions = 0
            for action in liste_actions :  
                somme_actions = x_sa[i][j][action]
            delta_sa[i][j][action]=x_sa[i][j][action]/somme_actions
                
    return delta_sa

def pl_part3_2(g,liste_actions,rewards,p,gamma,epsilon):

    # Create a new model
    m = grb.Model("politique-mixte")

    x_sa = []
    d_sa = []

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
                somme_actions += d_sa[i][j][action]
            m.addConstr(somme_actions <= 1)    
    
    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions :     
                m.addConstr((1-gamma)*x_sa[i][j][action] - d_sa[i][j][action] <= 0) 
  
    m.optimize()
            
    # d'après Propriété 2
    delta_sa = np.zeros(len(g), len(g[0]), 4)
    # D'après la proposition 2
    for i in range(len(g)):
        for j in range(len(g[0])):
            somme_actions = 0
            for action in liste_actions :  
                somme_actions += x_sa[i][j][action]
            delta_sa[i][j][action]=x_sa[i][j][action]/somme_actions
                
    return delta_sa


grille = gr.Grille_avec_chiffres(10,10,2,0.2,0.2,0.2,0.2,0.2,1000)
p = 0.6
gamma = 0.9
epsilon = 0.00001

# Test PL
delta_sa = pl_part3_1(grille.g, p, gamma, epsilon)
# attention, delta_sa devrait etre un tableau à trois dimmensions !!
print(delta_sa)

delta_sa = pl_part3_1(grille.g, p, gamma, epsilon)
print(delta_sa)


## ----- Question d)1 -----

##Tester la resolution pratique du probleme de recherche d'une trajectoire equilibrée
## sur des grilles différentes tailles avec l'approche proposee en b).
## On donnera ici encore les temps moyens de resolution.


# Fonction qui étudie l'impact de la taille de l'instance sur les performances des algorithmes. 
# Renvoie un dataframe de données ainsi que le tracé des courbes du nbre d'iteration et du temps d'execution en fonction de la taille
def impact_size(sizes,
                nbr_tests = default_tests,
                p = default_p,
                gamma = default_gamma,
                epsilon = default_epsilon):
    df = pd.DataFrame(columns = ["dimensions",
                                 "taille",
                                 "iter_val",
                                 "iter_pol",
                                 #"iter_pl",
                                 "time_val",
                                 "time_pol",
                                 #"time_pl",
                                 ])
    for i, taille in enumerate(sizes) : 
        print(taille)
        somme1_it = 0
        somme1_t = 0
        somme2_it =0 
        somme2_t =0
        for k in range(nbr_tests):
            g = grille.Grille(taille[0],taille[1],2,0.2,0.2,0.2,0.2,0.2,[0,1,2,3,4],1000).g
            #print(g)
            #print("run "+str(k+1)+" out of "+str(nbr_tests))
            # politiques mixtes
            d,v,t, time = pl_part3_1(g,p,gamma,epsilon)
            somme1_it += t
            somme1_t += time
            # politiques pures
            d,v,t, time = pl_part3_2(g,p,gamma,epsilon)
            somme2_it += t
            somme2_t += time
            line = pd.Series({'dimensions' : taille,
                              'taille' : taille[0]*taille[1],
                              'iter_pl1' : somme1_it/nbr_tests,
                              'iter_pl2': somme2_it/nbr_tests,
                              'time_pl1': somme1_t/nbr_tests,
                              'time_pl2': somme2_t/nbr_tests,
                              })
        df = df.append(line, ignore_index=True)
        
    # Affichage des résultats    
    print(df)
  
    plt.figure(1)
    ax1 = plt.subplot(211)
    plt.scatter(df.taille, df.iter_pl1, label = "Politiques mixtes")
    plt.scatter(df.taille, df.iter_pl2, label = "Politiques pures")    
    #plt.xlabel("Taille de l'instance")
    plt.ylabel("Nombre d'itérations")
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc = 0, borderaxespad = 0.)  
    
    plt.subplot(212, sharex = ax1)
    plt.scatter(df.taille, df.time_pl1, label = "Politiques mixtes")
    plt.scatter(df.taille, df.time_pl2, label = "Politiques pures")
    plt.xlabel("Taille de l'instance")
    plt.ylabel("Durée d'execution")
    
    plt.show()
    

sizes = [[5,5],
         [5,10],
         [10,10],
         [10,15],
         [15,15],
         [15,20],
         [20,20]]

impact_size(sizes)



## ----- Question d)2 -----


## Comparer les valeurs de politiques mixtes optimales à des valeurs de politiques
## pure obtimales que l'on obtient

# comment comparer ??
# politique mixte -> probabilité
# comparer celle qui a la plus grande proba à la politique pure s


## ----- Question d)3 -----

# Simuler les politiques obtenues pour observer leurs performances en pratiques
  
# Fonction qui pour une grille donnée va calculer les politiques mixtes et pures optimales
# et les simuler un nbr nbr_tests de fois pour evaluer leurs couts respectifs.
def simul_politiques(g,
                     nbr_tests = default_tests,
                     p = default_p,
                     gamma = default_gamma,
                     epsilon = default_epsilon
                     ):
    # on calcul les deux politiques optimales
    d_mixte,v,t,time = pl_part3_1(g,p,gamma,epsilon)
    d_pur,v,t,time = pl_part3_2(g,p,gamma,epsilon)
    # on calcul le cout moyen pour chacune des ces politiques, en pratique
    mean_mixte_cost = ot.mean_experienced_cost_p3(d_mixte,g,p,nbr_tests)
    mean_pur_cost = ot.mean_experienced_cost_p3(d_pur,g,p,nbr_tests)
    return(mean_mixte_cost,mean_pur_cost)
  
    
# créer une grille
g = gr.Grille_avec_chiffre(default_nbLignes,default_nbCol,2,0.2,0.2,0.2,0.2,0.2,1000).g
# TODO : à refaire sur plusieurs grilles différentes ?
mean_mixte_cost,mean_pur_cost = simul_politiques(g,
                                                 nbr_tests = default_tests,
                                                 p = default_p,
                                                 gamma = default_gamma,
                                                 epsilon = default_epsilon
                                                 )  
print(mean_mixte_cost) 
print(mean_pur_cost)




## ===== Question d) =====

# Pour une instance donnée comparer le vecteur cout que vous obternez pour une politique optimale
# calculee avec l'approche multi-obj a celui de l'approche proposée en a.
# Simulez 10 ou 20 fois ces deux politiques et observez les couts moyens obtenus

def compare_methods(g,
                    nbr_tests = default_tests,
                    p = default_p,
                    gamma = default_gamma,
                    epsilon = default_epsilon):
    d_multi_obj,v,t,time = pl_part3_1(g,p,gamma,epsilon)
    d_pdm,v,t,time = alg.iteration_de_la_valeur(g,p,gamma,epsilon)
    # on calcul le cout moyen pour chacune des ces politiques, en pratique
    mean_multi_obj = ot.mean_experienced_cost_p3(d_multi_obj,g,p,nbr_tests)
    mean_pdm = ot.mean_experienced_cost_p3(d_pdm,g,p,nbr_tests) 
    return(mean_multi_obj,mean_pdm)        
 
g = gr.Grille_avec_chiffre(default_nbLignes,default_nbCol,2,0.2,0.2,0.2,0.2,0.2,1000).g
# TODO : à refaire sur plusieurs grilles différentes ?
mean_mixte_cost,mean_pur_cost = simul_politiques(g,
                                                 nbr_tests = default_tests,
                                                 p = default_p,
                                                 gamma = default_gamma,
                                                 epsilon = default_epsilon
                                                 )  
print(mean_mixte_cost) 
print(mean_pur_cost)


    
    