# script mdp1.py
from tkinter import *
import numpy as np


def colordraw(g,nblignes,nbcolonnes):
    pblanc=0.1
    pverte=0.3
    pbleue=0.25
    prouge=0.2
    pnoire=0.15
    for i in range(nblignes):
        for j in range(nbcolonnes):
            y =20*i+20
            x =20*j+20
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
                g[i,j]=c
                Canevas.create_oval(10+x-3,10+y-3,10+x+3,10+y+3,width=1,outline=color[c],fill=color[c])
            else:
                 Canevas.create_rectangle(x, y, x+20, y+20, fill=myblack)

def Clavier(event):
    global PosX,PosY
    touche = event.keysym
    cj=(PosX-30)/20
    li=(PosY-30)/20
    print(li,cj)
    # deplacement vers le haut
    if touche == 'a' and g[li-1,cj]>0:
        PosY -= 20
    # deplacement vers le bas
    if touche == 'q' and g[li+1,cj]>0:
        PosY += 20
    # deplacement vers la droite
    if touche == 'm' and g[li,cj+1]>0:
        PosX += 20
    # deplacement vers la gauche
    if touche == 'l' and g[li,cj-1]>0:
        PosX -= 20
    # on dessine le pion a sa nouvelle position
    Canevas.coords(Pion,PosX -10, PosY -10, PosX +10, PosY +10)

Mafenetre = Tk()
Mafenetre.title('MDP')

# position initiale du pion
PosX = 30
PosY = 30

#taille de la grille
nblignes=15
nbcolonnes=15

# Creation d'un widget Canvas (zone graphique)
Largeur = 20*nbcolonnes+40
Hauteur = 20*nblignes+40
 
# valeurs de la grille
g= np.zeros((nblignes,nbcolonnes))

myred="#F70B42"
mygreen="#1AD22C"
myblue="#0B79F7"
mygrey="#E8E8EB"
myyellow="#F9FB70"
myblack="#5E5E64"
mywhite="#FFFFFF"

color=[mywhite,mygreen,myblue,myred,myblack]

Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg =mywhite)
for i in range(nblignes+2):
    ni=20*i
    Canevas.create_line(20, ni, Largeur-20,ni)
for j in range(nbcolonnes+2):
    nj=20*j
    Canevas.create_line(nj, 20, nj, Hauteur-20)
colordraw(g,nblignes,nbcolonnes)
Pion = Canevas.create_oval(PosX-10,PosY-10,PosX+10,PosY+10,width=2,outline='black',fill=myyellow)
Canevas.focus_set()
Canevas.bind('<Key>',Clavier)
Canevas.pack(padx =5, pady =5)

# Craation d'un widget Button (bouton Quitter)
Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy).pack(side=LEFT,padx=5,pady=5)

Mafenetre.mainloop()

