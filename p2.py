
import numpy as np
import outils as ot
import time as tm
import grille as gr
#import gurobipy as grb

# definition des actions
liste_actions = [0,1,2,3]

def iteration_de_la_valeur(g,p,gamma,epsilon):
    global liste_actions
    start = tm.time()
    
    #2 etats :  - pour t-1 
    #           - pour t 
    val_etats =  np.zeros((len(g),len(g[0])))
    vt =  np.zeros((len(g),len(g[0])))
    q = np.zeros((len(g),len(g[0]),len(liste_actions)))
    t = 0
    #critere d'arret
    while np.max(np.abs(vt - val_etats)) >= epsilon or t==0:
        t += 1
        #etat precedant
        vt = np.copy(val_etats) 
        for i in range(len(val_etats)):#TODO : plus propre de mettre nbLignes non ?
            for j in range(len(val_etats[0])): # pareil 
                for action in liste_actions:
                    r = - g[i][j][1]                     
                    q[i][j][action] = r + gamma * ot.sum_p_v(g,val_etats,i,j,p,action)
                val_etats[i][j] = max(q[i][j])
    
    #politique optimal
    d = np.zeros((len(g),len(g[0])))
    for i in range(len(val_etats)):
            for j in range(len(val_etats[0])):
                d[i][j] = np.argmax(q[i][j])
    end = tm.time()
    time = end - start
    return d,val_etats,t, time 

# Bizarre on fait une premiere boucle pour calculer les valeurs de la politique pour la politique d
# et ensuite on calcul pour tout les actions possible ensuite (en vrai peut etre pas si bizarre a voir)
# verifier les resultats 

def iteration_de_la_politique(g,p,gamma,epsilon):
    global liste_actions

    #2 etats :  - pour t-1 
    #           - pour t 
    start = tm.time()

    val_etats =  np.zeros((len(g),len(g[0])))
    d = np.zeros((len(g),len(g[0])))

    t = 0
    vt = val_etats,val_etats
    
    #critere d'arret
    while np.max(np.abs(vt - val_etats)) >= epsilon or t==0:
#     while not(np.array_equal(d_pred,d)) or t == 0:
        t += 1
        #valeur de la politique courant
        vt = np.copy(val_etats)
        
        #evaluation de la politique courante
        for i in range(len(val_etats)):
            for j in range(len(val_etats[0])):
                r = -g[i][j][1]
                #arrivé au but
                val_etats[i][j] =  r + gamma * ot.sum_p_v(g,val_etats,i,j,p,d[i][j])
    
        #amelioration de la politique
        for i in range(len(val_etats)):
            for j in range(len(val_etats[0])):
                arg = []
                for action in liste_actions:
                    #arrivé au but
                    r = -g[i][j][1]
                    arg.append(r + gamma*ot.sum_p_v(g,val_etats,i,j,p,action))
                arg = np.array(arg)
                d[i][j] = np.argmax(arg)
#    print(g)
 #   print(ot.from_action_to_dir(d,g))
#    #print(v)
#    print(t)
    end = tm.time()
    time = end - start
    return d,val_etats,t, time

# TODO : decommenter et verifier que ca marche
#
#def pl(g,p,gamma,epsilon):
#    global liste_actions
#    start = tm.time()
#
#    # Create a new model
#    m = grb.Model("test")
#
#    val_etats = []
#
#    # Create variables
#    for i in range(len(g[0])): # EST-ce que c'est pas simplement len(g)
#        for j in range(len(g[1])): # ET len(g[0]) ?
#            n = "v["+str(i)+"]["+str(j)+"]"
#            r = - g[i][j][1]
#            x = m.addVar(vtype=grb.GRB.CONTINUOUS, name=n)
#            val_etats.append(x)
#
#    # Set objective
#    # print(val_etats[0])
#    # print(m.getVars())
#    # for v in m.getVars():
#    #     print('la')
#    #     print('%s %g' % (v.varName, v.x))
#    # print(y)
#
#    val_etats = np.array(val_etats)
#    val_etats = np.reshape(val_etats,(len(g),len(g[0])))
#
#    m.setObjective(np.sum(val_etats), grb.GRB.MINIMIZE)
#    print((val_etats.shape))
#    for i in range(len(g)):
#        for j in range(len(g[0])):
#            for action in liste_actions: 
#                r = -g[i][j][1]
#                m.addConstr(val_etats[i][j] >= r + gamma * ot.sum_p_v(g, val_etats, i, j, p, action))
#
#    m.optimize()
#
#    # for v in m.getVars():
#    #     print('%s %g' % (v.varName, v.x))
#    val_etats = np.reshape(np.array([v.x for v in m.getVars()]),(len(g),len(g[0])))
#    # print(val_etats)
#    # print(val_etats.shape)
#
#    # for v in m.getConstrs():
#    #     print('%s' % (v.getAttr("slack")))
#
#    # print('Obj: %g' % m.objVal)
#
#    # Affiche le pl dans un fichier
#    # m.write('debug.lp')
#
#    d = np.zeros((len(g), len(g[0])))
#    for i in range(len(val_etats)):
#        for j in range(len(val_etats[0])):
#            val_par_action = np.zeros(len(liste_actions))
#            for action in liste_actions:
#                    val_par_action[action] = r + gamma * ot.sum_p_v(g, val_etats, i, j, p, action)
#            d[i][j] = np.argmax(val_par_action)
#    end = tm.time()
#    time = end - start
#    # TODO  : récupérer le nombre d'iteration
#    return d, val_etats, time


#
#grille = gr.Grille(10,10,2,0.2,0.2,0.2,0.2,0.2,[0,1,2,3,4], 1000)
#p = 0.6
#gamma = 0.9
#epsilon = 0.00001

## Test iteration de la valeur
#d,v,t,time = iteration_de_la_valeur(grille.g,p,gamma,epsilon)
#print(ot.from_action_to_dir(d,grille.g))
##print(v)
##print(t)
#

## Test iteration de la politique
#d,v,t,time = iteration_de_la_politique(grille.g,p,gamma,epsilon)
#print(ot.from_action_to_dir(d,grille.g))

# Test PL
#d,v,time = pl(grille.g, p, gamma, epsilon)
#print(ot.from_action_to_dir(d,g))

#grille.Mafenetre.mainloop() #Affichage 


