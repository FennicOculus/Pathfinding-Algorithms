import random
import pygame
import tkinter as tk
from tkinter import messagebox
from collections import deque as queue
import numpy as np

# Vecteur de directions utilisé dans les calcule des voisins
dRow = [-1, 0, 1, 0]
dCol = [0, 1, 0, -1]

#Point de dépard
Xdep = 5
Ydep = 5

#Point d'arrivé
Xarr = 18
Yarr = 18

#Nombre d'obstacles dans la grille
NbrObstcl = 100

def isValid(vis, row, col):
    global obstacles
    # Vérifie si la position n'est pas hors limite
    if (row < 0 or col < 0 or row >= 20 or col >= 20):
        return False

    # Vérifie si la cellule a été visité
    if (vis[row][col]):
        return False
	
	#vérifie c'est il y'a un obstacle a cette position
    if (row, col) in obstacles:

        return False

    return True


def BFS(grid, vis, row, col, xf, yf):
    global visi, visi2, fathers
    q = queue()
    q.append((row, col))
    visi2.append((row, col))
    fathers.append((row, col))
    vis[row][col] = True

    # on parcours la file tant qu'elle n'est pas vide
    while (len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]
        visi.append((x, y))

        if x == xf and y == yf:
            break


        # on parcours les cellules adjacente
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if (isValid(vis, adjx, adjy)):
                q.append((adjx, adjy))
                visi2.append((adjx, adjy))
                fathers.append((x, y))
                vis[adjx][adjy] = True

def PathBFS(): #fonction pour afficher le chemin qui a conduit au résultat
    global visi2, fathers, win, ppt
    (x, y) = (Xarr, Yarr)
	#tant qu'on n'est pas arrivé au point de départ, on sauvegarde le père de la cellule courante
    while (x, y) != (Xdep, Ydep):
        index = visi2.index((x, y))
        x, y = fathers[index]
        ppt.append((x, y))

def PathDFS():
    global visi, fathers, win, ppt
    x, y = visi[len(visi)-1]
    i = len(visi)-1
	#tant qu'on est pas arrivé au point de dépard et que i n'est pas null on continue le traitement
    while (x, y) != (Xdep, Ydep) and i >= 0:
        if i < len(visi) - 1:
            xnext, ynext = visi[i]
            if (xnext, ynext) == (x + 1, y) or (xnext, ynext) == (x, y + 1) or (x - 1, y) == (xnext, ynext) or (
                    xnext, ynext) == (x, y - 1):
                ppt.append((x, y))#si xnext et ynext est voisins de x, y alors on sauvegarde x et y
                (x, y) = visi[i] #x, y recois la valeur de xnext et ynext
            i -= 1
        if i == len(visi) - 1:
            xnext, ynext = visi[i - 1]
            if (xnext, ynext) == (x + 1, y) or (xnext, ynext) == (x, y + 1) or (x - 1, y) == (xnext, ynext) or (
                    xnext, ynext) == (x, y - 1):
                ppt.append((x, y))
                (x, y) = visi[i]
            i -= 1

def DFS(grid, vis, row, col, xf, yf):
    global visi

    st = []
    st.append([row, col])
    fathers.append([row, col])

    while (len(st) > 0):
        # on dépile la position
        curr = st[len(st) - 1]
        st.remove(st[len(st) - 1])

        row = curr[0]
        col = curr[1]

        if (isValid(vis, row, col) == False):
            continue

        vis[row][col] = True
        visi.append((row,col))

        if row == xf and col == yf:
            break
			
        for i in range(4):
            adjx = row + dRow[i]
            adjy = col + dCol[i]
            st.append([adjx, adjy])


class cube(object):
    rows = 20
    w = 500
	#Fonction qui permet de dessiner les cercles 
    def __init__(self, start, color=(0, 0, 0)):
        self.pos = start
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.ellipse(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class PointDepard(object):
    body = []
    turns = {}
	#Fonction qui crée le point de dépard
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
	#Dessiner la grille
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, w))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (w, y))


def redrawWindow(surface):#fonction qui redessine la grille chaque x secondes
    global rows, width, pointDep, obstcl1, obstcl2, obstcl3, pointArr, testes, ppt, CubeObsct
    surface.fill((128, 128, 128))
    for i in testes:
        i.draw(surface)
    for i in CubeObsct:
        i.draw(surface)
    pointDep.draw(surface)
    obstcl1.draw(surface)
    obstcl2.draw(surface)
    obstcl3.draw(surface)
    pointArr.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def ObstaclePos(rows, item):
    positions = item.body
	#fonction qui créer les obstacles avec une positions aléatoire
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def main():
    global width, rows, pointDep, obstcl1, obstcl2, obstcl3, pointArr, obstacles, testes, visi, visi2, fathers, ppt, CubeObsct
    visi = queue()
    visi2 = []
    fathers = []
    N = 20
    data = np.zeros((N, N), dtype=int) #Matrice utilisé pour le calcule du DFS et BFS
    vis = [[False for i in range(20)] for i in range(20)] #Matrice des cellule visité

    ppt = []#variable pour sauvegarder le chemin parcouru
    obstacles = [] #liste des obstacles
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    pointDep = PointDepard((0, 0, 0), (Xdep, Ydep))
    pointArr = cube((Xarr, Yarr), color=(255, 255, 255))
    obstcl1 = cube(ObstaclePos(rows, pointDep), color=(255, 0, 0))
    obstacles.append(obstcl1.pos)
    obstcl2 = cube(ObstaclePos(rows, pointDep), color=(0, 255, 0))
    obstacles.append(obstcl2.pos)
    obstcl3 = cube(ObstaclePos(rows, pointDep), color=(0, 0, 255))
    obstacles.append(obstcl3.pos)
    CubeObsct = []
    for i in range(NbrObstcl):
        x = random.randrange(3)
        if x == 0:
            CubeObsct.append(cube(ObstaclePos(rows, pointDep), color=(255, 0, 0)))
        if x == 1:
            CubeObsct.append(cube(ObstaclePos(rows, pointDep), color=(0, 255, 0)))
        if x == 2:
            CubeObsct.append(cube(ObstaclePos(rows, pointDep), color=(0, 0, 255)))
        obstacles.append(CubeObsct[i].pos)
    flag = True
    clock = pygame.time.Clock()
    DFS(data, vis, Xdep, Ydep, Xarr, Yarr)
    PathDFS()
    pathcol = queue()
    for i in ppt:
        pathcol.append(i)
    testes = []

    while flag:
        pygame.time.delay(10)
        clock.tick(20)
        pointDep.move()

        if len(visi)>0:
            testes.append(cube(visi.popleft(), color=(0, 255, 255)))
        else:
            if len(pathcol) > 0:
                testes.append(cube(pathcol.popleft(), color=(255, 215, 0)))
        if pointDep.body[0].pos == obstcl1.pos:
            obstcl1 = cube(ObstaclePos(rows, pointDep), color=(255, 0, 0))
            obstacles.append(obstcl1.pos)
        if pointDep.body[0].pos == obstcl2.pos:
            obstcl2 = cube(ObstaclePos(rows, pointDep), color=(0, 255, 0))
            obstacles.append(obstcl2.pos)
        if pointDep.body[0].pos == obstcl3.pos:
            obstcl3 = cube(ObstaclePos(rows, pointDep), color=(0, 0, 255))
            obstacles.append(obstcl3.pos)
        if pointDep.body[0].pos == obstcl3.pos:
            pointArr = cube(ObstaclePos(rows, pointDep), color=(255, 255, 255))

        redrawWindow(win)

    pass


main()
