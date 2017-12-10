# script mdp4.py
from tkinter import *
import numpy as np

def initialize():
    global PosX,PosY,cost
# position initiale du robot
    PosX = 20+10*zoom
    PosY = 20+10*zoom
    for k in range(5):
        cost[k]=0
# cout et affichage
    Canevas.coords(Pion,PosX -9*zoom, PosY -9*zoom, PosX +9*zoom, PosY +9*zoom)
    wg.config(text=str(cost[1]))
    wb.config(text=str(cost[2]))
    wr.config(text=str(cost[3]))
    wn.config(text=str(cost[4]))
    ws.config(text='     total = '+str(cost[0]))


def colordraw(g,nblignes,nbcolonnes):
    p=0.15
    q=(1-p)/4
    pblanc=p
    pverte=q
    pbleue=q
    prouge=q
    pnoire=q
    for i in range(nblignes):
        for j in range(nbcolonnes):
            z=np.random.uniform(0,1)
            if z < pblanc:
                c=0
            else:
                if z < pblanc+ pverte:
                    c=1
                else:
                    if z < pblanc+ pverte + pbleue:
                        c=2
                    else:
                        if z< pblanc+ pverte + pbleue +prouge:
                            c=3
                        else:
                            c=4   
            if c>0:
                g[i,j,0]=c
                g[i,j,1]=np.random.random_integers(9)
    g[0,0,0]=np.random.random_integers(3)
    g[0,1,0]=np.random.random_integers(3)
    g[2,0,0]=np.random.random_integers(3)     
    g[nblignes-1,nbcolonnes-1]=np.random.random_integers(3)
    g[nblignes-2,nbcolonnes-1]=np.random.random_integers(3)
    g[nblignes-1,nbcolonnes-2]=np.random.random_integers(3)
    for i in range(nblignes):
        for j in range(nbcolonnes):          
            y =zoom*20*i+20
            x =zoom*20*j+20
            if g[i,j,0]>0:            
                #Canevas.create_oval(x+zoom*(10-3),y+zoom*(10-3),x+zoom*(10+3),y+zoom*(10+3),width=1,outline=color[g[i,j]],fill=color[g[i,j]])
                Canevas.create_text(x+zoom*(10),y+zoom*(10), text=str(g[i,j,1]),fill=color[g[i,j,0]],font = "Verdana "+str(int(6*zoom))+" bold")
            else:
                Canevas.create_rectangle(x, y, x+zoom*20, y+zoom*20, fill=mywalls)
                
def Clavier(event):
    global PosX,PosY,cost,g
    touche = event.keysym
    cj=(PosX-30)/(20*zoom)
    li=(PosY-30)/(20*zoom)
    #print(li,cj)
    # deplacement vers le haut
    if touche == 'space':
        if np.random.uniform(0,1)<0.4:
            touche = 'm'
        else:
            if np.random.uniform(0,1)<0.8: 
                touche ='q'
            else:
                if np.random.uniform(0,1)<0.9: 
                    touche ='a'
                else:
                    touche = 'l'
    if touche == 'a' and li>0 and g[li-1,cj,0]>0:
        PosY -= zoom*20
        cost[g[li-1,cj,0]]+=g[li-1,cj,1]        
    # deplacement vers le bas
    if touche == 'q' and li<nblignes-1 and g[li+1,cj,0]>0:
        PosY += zoom*20
        cost[g[li+1,cj,0]]+=g[li+1,cj,1] 
    # deplacement vers la droite
    if touche == 'm' and cj< nbcolonnes-1 and g[li,cj+1,0]>0:
        PosX += zoom*20
        cost[g[li,cj+1,0]]+=g[li,cj+1,1] 
    # deplacement vers la gauche
    if touche == 'l' and cj >0 and g[li,cj-1,0]>0:
        PosX -= zoom*20
        cost[g[li,cj-1,0]]+=g[li,cj-1,1] 
    # on dessine le pion a sa nouvelle position
    Canevas.coords(Pion,PosX -9*zoom, PosY -9*zoom, PosX +9*zoom, PosY +9*zoom)
    cost[0]=0    
    for k in range(4):
        cost[0]+=cost[k+1]*weight[k+1]        
    wg.config(text=str(cost[1]))
    wb.config(text=str(cost[2]))
    wr.config(text=str(cost[3]))
    wn.config(text=str(cost[4]))
    ws.config(text='     total = '+str(cost[0]))

Mafenetre = Tk()
Mafenetre.title('MDP')

zoom=2


#taille de la grille
nblignes=10
nbcolonnes=20

# Creation d'un widget Canvas (pour la grille)
Largeur = zoom*20*nbcolonnes+40
Hauteur = zoom*20*nblignes+40
 
# valeurs de la grille
g= np.zeros((nblignes,nbcolonnes,2), dtype=np.int)
cost= np.zeros(5, dtype=np.int)
weight= np.zeros(5, dtype=np.int)
weight[1] = 1
weight[2] = 1
weight[3] = 1
weight[4] = 1

# def des couleurs
myred="#D20B18"
mygreen="#25A531"
myblue="#0B79F7"
mygrey="#E8E8EB"
myyellow="#F9FB70"
myblack="#2D2B2B"
mywalls="#5E5E64"
mywhite="#FFFFFF"
color=[mygrey,mygreen,myblue,myred,myblack]

# ecriture du quadrillage et coloration
Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg =mywhite)
for i in range(nblignes+1):
    ni=zoom*20*i+20
    Canevas.create_line(20, ni, Largeur-20,ni)
for j in range(nbcolonnes+1):
    nj=zoom*20*j+20
    Canevas.create_line(nj, 20, nj, Hauteur-20)
colordraw(g,nblignes,nbcolonnes)

 
Canevas.focus_set()
Canevas.bind('<Key>',Clavier)
Canevas.pack(padx =5, pady =5)

PosX = 20+10*zoom
PosY = 20+10*zoom

# Creation d'un widget Button (bouton Quitter)
Button(Mafenetre, text ='Restart', command = initialize).pack(side=LEFT,padx=5,pady=5)
Button(Mafenetre, text ='Quit', command = Mafenetre.destroy).pack(side=LEFT,padx=5,pady=5)

w = Label(Mafenetre, text='     Costs: ', fg=myblack,font = "Verdana "+str(int(5*zoom))+" bold")
w.pack(side=LEFT,padx=5,pady=5) 
wg = Label(Mafenetre, text=str(cost[1]),fg=mygreen,font = "Verdana "+str(int(5*zoom))+" bold")
wg.pack(side=LEFT,padx=5,pady=5) 
wb = Label(Mafenetre, text=str(cost[2]),fg=myblue,font = "Verdana "+str(int(5*zoom))+" bold")
wb.pack(side=LEFT,padx=5,pady=5) 
wr = Label(Mafenetre, text=str(cost[3]),fg=myred,font = "Verdana "+str(int(5*zoom))+" bold")
wr.pack(side=LEFT,padx=5,pady=5) 
wn = Label(Mafenetre, text=str(cost[4]),fg=myblack,font = "Verdana "+str(int(5*zoom))+" bold")
wn.pack(side=LEFT,padx=5,pady=5) 
ws = Label(Mafenetre, text='     total = '+str(cost[0]),fg=myblack,font = "Verdana "+str(int(5*zoom))+" bold")
ws.pack(side=LEFT,padx=5,pady=5) 
Pion = Canevas.create_oval(PosX-10,PosY-10,PosX+10,PosY+10,width=2,outline='black',fill=myyellow)

initialize()

Mafenetre.mainloop()

