# Marc-Olivier Morin (20187831) et Tobias Lepoutre 

import tuiles

 # affiche la couleur au pixel demander
def  afficherImage(x,y,colormap,image):       
    setPixel(x,y,colormap[image])                               
    
    
    
 # imprime la tuile entière demandé à la position par rapport au 
 # tableau de tuile  
    
def afficherTuile(x,y,tuile):                
    x*=16                                           # multiplication par 16                                   
    y*=16                                           # pour la position par                                      
    for i in range(16):                             # au tuiles
        for j in range(16):
            afficherImage(x+j,y+i,tuiles.colormap,
                          tuiles.images[tuile][i][j])
            
 

 # fonction qui attend le clic et ensuite attend que le clic soit    
 # relâché. Return ensuite une liste contenant la position en x et en y ou le 
 # clic est relaché par rapport au tableau de tuile.
def attendreClic(): 
    buttonTrue = False                      
    infoSouris = getMouse()                  
    listeSouris = [0,0,0]                    
    while True:                                   # prend la postition quand                             
        sleep(0.01)                               # un bouton est appuyé                        
        while getMouse().button >0:          
            sleep(0.01)                      
                                            
            if getMouse().button >0:              # assure que la dernière                            
                infoSouris=getMouse()             # valeur enregistré aille le 
                                                  # clic
            buttonTrue = True
                        
        if  buttonTrue:
            listeSouris[0] =  infoSouris.x//16    # avoir position en x et y 
            listeSouris[1] =  infoSouris.y//16    # par rapport grille tuile
            
            if  infoSouris.button == 2 or (infoSouris.button == 1 and 
                                           infoSouris.ctrl):
                listeSouris[2] = 1
                
            elif infoSouris.button == 1:          # 3ieme valeur du tableau
                listeSouris[2] = 0                # retourne 0 si clic gauche
                                                  # et 1 si clic droit ou clic
            return listeSouris                    # gauche + ctrl
            buttonTrue = False

            
            

 # crée un tableau de False de la argeur et hauteur spécifié            
def grilleDeBoleens(largeur,hauteur):        
    grille = [None] * hauteur              
    
    for i in range(hauteur):
        grille[i] = [False] * largeur
    
    return grille


 # place aléatoirement des mines dans le tableau de bool. L'emplacement du mine
 # est true et un false indique qu'il n'y a pas de mine. 
def placerMines(largeur,hauteur,nbMines,x,y):   
    grille = grilleDeBoleens(largeur,hauteur)            # crée le tableau
    compteur = 0
    
    while compteur < nbMines:                           
        
        randomLargeur = math.floor(random()*largeur)     #choisi aléatoirement
        randomHauteur = math.floor(random()*hauteur)     # position de la mine
        
        if grille[randomHauteur] [randomLargeur] == True:# continue si position
            continue                                     # à déjà une mine
        
        elif randomLargeur == x and randomHauteur == y:  # assure de pas placer
            continue                                     # de mine à position 
                                                         # x et y
        elif grille[randomHauteur] [randomLargeur] == False:
            grille[randomHauteur] [randomLargeur] = True
            compteur+=1
            
    return grille




 # détermine la quantité de mine voisine à une coordonné quelquonque et 
 # retourne le nombre de mine
def nbMinesVoisines(x, y,grille):                  
    nbDeMines=0                                   
   
    for j in range(y-1,y+2):
        for i in range(x-1,x+2):
            if i>=0 and i<len(grille[0])\
            and j>=0 and j<len(grille):            # s'assure de tester si le 
                if grille[j][i]==True:             # point est dans les bornes
                    nbDeMines+=1                   # de la grille avant de
                                                   # tester si  il a une mine
    return nbDeMines




 # fonction récursive qui déterime les mines à dévoiler et à tester pour savoir
 # si elles doivent être dévoilé
def dévoilerCase(x,y,grilleTuiles,grilleMines, grilleDrapeaux):
    nbMines =  nbMinesVoisines(x, y,grilleMines)
  
    if not (x>=0 and x<len(grilleTuiles[0])\
    and y>=0 and y<len(grilleTuiles)):              # s'assure d'être dans les  
                                                    # bornes de la grille
        return                                      
                                                    
    elif grilleTuiles[y][x] or grilleMines[y][x] \
    or grilleDrapeaux[y][x]:                        # évite de dévoiler si a un 
         return                                     # drapeau, bombe et si est 
                                                    # déjà dévoiler pour éviter  
    elif nbMines > 0:                               # boucle infini
        afficherTuile(x, y, nbMines)    
        grilleTuiles[y][x] = True                   # dévoile si à des mines
        return                                      # adjacente, mais ne va pas
                                                    # tester mine adjacente
    else:    
        grilleTuiles[y][x] = True                   # dévoile et teste mine 
        afficherTuile(x, y, 0)                      # adjacente à partir de la 
        for j in range(y-1,y+2):                    # tuile dévoiler
            for i in range(x-1,x+2):  
                dévoilerCase(i,j,grilleTuiles,
                             grilleMines,grilleDrapeaux)


                
                
 # détermine si un drapeau doit être placer ou enlever et enlève ou place un
 # drapeau dans le jeu. Limite la quantité de drapeau au nombre de bombe
def drapeau(x,y,nbDrapeaux,nbDrapeauxMax,grilleDrapeaux,grilleTuiles):
    i = nbDrapeaux 
    
    if not  grilleDrapeaux[y][x] and i < nbDrapeauxMax\
    and not grilleTuiles[y][x] :                     # test si un drapeau peut
        grilleDrapeaux[y][x] = True                  # être placé        
        afficherTuile(x, y, 13)
        i+=1
        
    elif grilleDrapeaux[y][x]:                       # test si un drapeau doit
        afficherTuile(x, y, 12)                      # être enlevé
        grilleDrapeaux[y][x] = False
        i-=1
    return i



 # affiche toutes les mines dans le jeu si le joueur perd. Affiche la bombe en 
 # rouge si est la bombe sélectionné, affiche un bombe avec le x rouge si il y
 # des drapeaux inutiles, et garde les drapeaux si ils étaient sur une bombe
 # x et y sont les coordonnés de la tuile appuyé
def afficherMines(x,y,grilleMines,grilleDrapeaux):
    for j in range(len( grilleMines)):                      
        for i in range(len( grilleMines[0])):   # boucle pour la grille
            
            if j == y and i == x:               # affiche bombe rouge 
                afficherTuile(i, j, 10)
                                
            elif grilleDrapeaux[j][i]\
            and grilleMines[j][i]:              # affiche drapeau    
                afficherTuile(i, j, 13)
                
            elif  grilleMines[j][i]:            # affiche bombe          
                 afficherTuile(i, j, 9)
                        
            elif  grilleDrapeaux[j][i]\
            and grilleMines[j][i] == False:     # affiche bombe avec x
                afficherTuile(i, j, 11)
 


 # fonction qui détermine si le joueur à gagner retourne False si le jeu n'est
 # pas terminé et True si oui. Prend en paramètre la grille de mines et de
 # tuiles pour les comparés
def déterminerGagner(grilleMines,grilleTuiles):
    bool = False
    compteur = 0 
    for j in range(len( grilleMines)):
        for i in range(len( grilleMines[0])):
            
            if not grilleMines[j][i]and\
            not grilleTuiles[j][i]:          # détermine si tout les tuiles      
                compteur +=1                 # sans bombes sont dévoilés
            elif compteur > 0:
                break
                
    if compteur == 0:
        bool = True
                    
    return bool

 # affiche toutes les cases avec des bombes avec des drapeaux
def Gagner(grilleMines):
    for j in range(len( grilleMines)):
        for i in range(len( grilleMines[0])):
            
            if grilleMines[j][i]:
                afficherTuile(i, j, 13)
 

 # fonction principale du jeu. Prend en paramètre le nombre de bombe, la
 # la largeur et la hauteur. Utilise une grille de bombe, drapeau et de tuile
 # chacun sont des grilles de boléens. 
def demineur(largeur, hauteur, nbMines):
    
    if nbMines < largeur * hauteur:
        phaseInitiale = True
        game = True
        nbDrapeauMax = nbMines
        nbDrapeaux = 0
        grilleDrapeaux = grilleDeBoleens(largeur,hauteur)
        grilleMines = grilleDeBoleens(largeur,hauteur)
        grilleTuiles = grilleDeBoleens(largeur,hauteur)
   
        setScreenMode(largeur*16, hauteur*16)
    
        for lignes in range(hauteur):                  # crée la grille de
            for colonnes in range(largeur):            # tuiles visuelle
                afficherTuile(colonnes, lignes, 12)
                 
        while phaseInitiale:                           # phase avant le premier
            clic = attendreClic()                      # clic
            if clic[2] == False:                       # proc si clic gauche
                grilleMines = placerMines(largeur,hauteur,
                                          nbMines,clic[0],clic[1])
                dévoilerCase(clic[0],clic[1],grilleTuiles,grilleMines,
                             grilleDrapeaux)
                phaseInitiale = False
            
            else:                                     # proc si clic droit
                nbDrapeaux = drapeau(clic[0],clic[1],nbDrapeaux,
                                     nbDrapeauMax,grilleDrapeaux,grilleTuiles)
        while game:
                                                       # phase de jeu
            clic = attendreClic()
            if clic[2] == False:                       # proc si clic gauche
                dévoilerCase(clic[0],clic[1],
                             grilleTuiles,grilleMines,grilleDrapeaux)
            
                if  grilleMines[clic[1]] [clic[0]]\
                and not grilleDrapeaux[clic[1]] [clic[0]]:     
                    afficherMines(clic[0],clic[1],
                                  grilleMines,grilleDrapeaux)
                    game = False
                    alert("Game Over")
                    game = False
                                                      # test si gagner
                elif déterminerGagner(grilleMines,grilleTuiles):
                    Gagner(grilleMines)               
                    alert("You Won!")
                    game = False
                             
            else:                                     # proc si clic droit  
                nbDrapeaux = drapeau(clic[0],clic[1], nbDrapeaux,
                                     nbDrapeauMax,grilleDrapeaux, grilleTuiles)


    
    
def testdemineur():
    setScreenMode(len(tuiles.colormap), 1)
    for i in range(len(tuiles.colormap)):
        afficherImage(0+i, 0, tuiles.colormap, i)
    imageTab1=exportScreen()
    assert\
    '#ccc' in imageTab1 and\
    '#00f' in imageTab1 and\
    '#080' in imageTab1 and\
    '#f00' in imageTab1 and\
    '#008' in imageTab1 and\
    '#800' in imageTab1 and\
    '#088' in imageTab1 and\
    '#000' in imageTab1 and\
    '#888' in imageTab1 and\
    '#fff' in imageTab1

    assert\
    len(imageTab1)==4*len(tuiles.colormap)

    setScreenMode(16, 12)
    x=math.floor(random()*10)
    y=math.floor(random()*10)
    afficherImage(x, y, tuiles.colormap, 1)

    imageTab2=exportScreen()

    couleurScreen=[]
    for i in range(len(imageTab2)):
        if imageTab2[i]!='\n':
            couleurScreen.insert(i,imageTab2[i])

    couleur=[]
    for i in range(4):
        couleur.insert(i,couleurScreen[4*x+4*y*16+i])                   

    assert couleur== ['#','0','0','f']




    setScreenMode(32, 32)
    afficherTuile(0, 0, 0)
    afficherTuile(1, 0, 0)
    afficherTuile(0, 1, 0)
    afficherTuile(1, 1, 0)

    tuileTab1=exportScreen()
    assert '#ccc' in tuileTab1 and '#000' not in tuileTab1

    setScreenMode(16, 16)
    afficherTuile(0, 0, 1)
    tuileTab2=exportScreen()
    assert '#00f' in tuileTab2 and '#000' not in tuileTab2
    afficherTuile(0, 0, 2)
    tuileTab3=exportScreen()
    assert '#080' in tuileTab3 and '#000' not in tuileTab3
    afficherTuile(0, 0, 3)
    tuileTab4=exportScreen()
    assert '#f00' in tuileTab4 and '#000' not in tuileTab4

    setScreenMode(17, 17)
    afficherTuile(0, 0, 1)
    tuileTab5=exportScreen()

    couleur1=[]
    for i in range(4):
        couleur1.insert(i,tuileTab5[17*17*4+i])
    
    assert couleur1== ['#','0','0','0']

    couleur2=[]
    for i in range(4):
        couleur2.insert(i,tuileTab5[0+i])
    
    assert couleur2==['#','8','8','8']




    minesTab1=placerMines(1, 2, 1, 0, 0)
    assert\
    minesTab1[1][0]==True and\
    minesTab1[0][0]==False

    minesTab2=placerMines(8, 8, 8*8-1, 0, 0)
    assert minesTab2[0][0]==False

    minesTab3=placerMines(8, 8, 8*8-1, 0, 0)
    minesTab3[0].pop(0)
    assert False not in minesTab3

    minesTab4=placerMines(6, 8, 10, 5, 7)
    assert minesTab4[7][5]==False

    calcMines=0
    for Y in range(8):
        for X in range(6):
            if minesTab4[Y][X]==True:
                calcMines += 1
    assert calcMines==10

    minesTab5=placerMines(10, 11, 0, 3, 4)
    minesTabModifie=[]
    index=0
    for Y in range(10):
        for X in range(11):
            minesTabModifie.insert(index,minesTab5[X][Y])
            index+=1
    assert True not in minesTabModifie



    grilleTab1=grilleDeBoleens(6,9)
    assert len(grilleTab1)==9

    grilleTab2=grilleDeBoleens(0,0)
    assert len(grilleTab2)==0

    grilleTab3=grilleDeBoleens(8,7)
    assert len(grilleTab3[0])==8

    grilleTab3=grilleDeBoleens(0,1)
    assert len(grilleTab3[0])==0

    grilleTab4=grilleDeBoleens(12,9)
    calcFalse=0
    for Y in range(9):
        for X in range(12):
            if grilleTab4[Y][X]==False:
                calcFalse+= 1           
    assert calcFalse==9*12

    grilleTab5=grilleDeBoleens(0,9)
    calcFalse=0
    for Y in range(9):
        for X in range(0):
            if grilleTab5[Y][X]==False:
                calcFalse+= 1           
    assert calcFalse==9*0

    grilleTab6=grilleDeBoleens(1,9)
    calcFalse=0
    for Y in range(9):
        for X in range(1):
            if grilleTab6[Y][X]==False:
                calcFalse+= 1           
    assert calcFalse==9*1



    minesExTab=placerMines(1, 2, 1, 0, 0)
    nombreCalc=nbMinesVoisines(0, 0, minesExTab)
    assert nombreCalc==1

    minesExTab=placerMines(2, 2, 1, 0, 1)
    nombreCalc=nbMinesVoisines(0, 1, minesExTab)
    assert nombreCalc==1

    minesExTab=placerMines(3, 3, 8, 1, 1)
    nombreCalc=nbMinesVoisines(1, 1, minesExTab)
    assert nombreCalc==8

    minesExTab=placerMines(10, 10, 0, 4, 7)
    x=math.floor(random()*10)
    y=math.floor(random()*10)
    nombreCalc=nbMinesVoisines(x, y, minesExTab)
    assert nombreCalc==0

    minesExTab=placerMines(10, 10, 99, 4, 7)
    nombreCalc=nbMinesVoisines(13, 12, minesExTab)
    assert nombreCalc==0

    minesExTab=placerMines(10, 10, 99, 4, 7)
    nombreCalc=nbMinesVoisines(-2, -4, minesExTab)
    assert nombreCalc==0
    
    
testdemineur()