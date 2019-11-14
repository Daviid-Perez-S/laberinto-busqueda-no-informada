from anytree import Node, PreOrderIter, RenderTree
from anytree.exporter import UniqueDotExporter
from anytree.util import rightsibling
import numpy as np
import random
import os, hashlib
from tkinter import Tk, Label, Entry, NORMAL, messagebox, Button
import cv2
import pygame
# import tkinter
# import pygraphviz as pvg

def uniqueID():
	return hashlib.md5(os.urandom(32)).hexdigest()[:5]

def indiceAleatorio(limite):
	return random.randint(0,limite-1)

def construirTablero(cantidadFilas):
	tablero = []
	cantidadFilas = cantidadFilas

	tablero = []
	contador = 0
	for i in range(0, cantidadFilas):
		row = []
		for j in range(contador+1, (contador + cantidadFilas)+1):
			row.append(j)
			contador = j
		tablero.append(row)
	return tablero

def mostrarTablero(tablero):
	print("\n")
	for row in tablero:
		print(row)
	print("\n")

def arriba(tablero, x, y):
	# Ir hacia arriba
	try:
		if tablero[x-1][y] != -1 and x > 0:
			return tablero[x-1][y]
	except IndexError:
		pass
	return None

def derecha(tablero, x, y):
	# Ir hacia la derecha
	try:
		if tablero[x][y+1] != -1:
			return tablero[x][y+1]
	except IndexError:
		pass
	return None

def abajo(tablero, x, y):
	# Ir hacia abajo
	try:
		if tablero[x+1][y] != -1:
			return tablero[x+1][y]
	except IndexError:
		pass
	return None

def izquierda(tablero, x, y):
	# Ir hacia la izquierda
	try:
		if tablero[x][y-1] != -1 and y > 0:
			return tablero[x][y-1]
	except IndexError:
		pass
	return None

def showRecorridos(nodoPadre):
	print(nodoPadre)
	camino = f'{nodoPadre.name}'
	padre = nodoPadre.parent
	while padre != None:
		camino += f' > {padre}'
		padre = padre.parent
	return camino


def getCoords(tablero, valorBuscado):
	tmp = np.array(tablero)
	return np.where(tmp==valorBuscado, )

def existeEnLaPila(pila, valor):
	result = False
	for v in pila:
		if v == valor:
			result = True
	return result

def esperarEntrada_Salida(size, tablero):
	
	pygame.init()
	ANCHO_PANTALLA = 400
	ALTO_PANTALLA = 400
	GROSOR_BORDE = 1

	# COLORS
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0, 0)
	COLOR_LIBRE = (165, 195, 242)
	COLOR_OBSTACULO = (183, 183, 183)
	COLOR_INICIO = (183, 214, 170)
	COLOR_SALIDA = (232, 153, 154)

	PIXELES_POR_CUADRO = int( (ANCHO_PANTALLA - ( (size + 1) * GROSOR_BORDE) ) / size )
	x = GROSOR_BORDE
	y = GROSOR_BORDE

	screen = pygame.display.set_mode([ANCHO_PANTALLA, ALTO_PANTALLA])
	clock = pygame.time.Clock()
	screen.fill(BLACK)

	# for y in range(0, ALTO_PANTALLA, PIXELES_POR_CUADRO):
	# 	for x in range(0, ANCHO_PANTALLA, PIXELES_POR_CUADRO):
	# 		pygame.draw.rect(screen, WHITE, [ x, y, PIXELES_POR_CUADRO, PIXELES_POR_CUADRO ], 1)

	for i in range(0, len(tablero[0])):
		for j in range(len(tablero[0])):
			if ( tablero[i][j] > 0 ):
				rect = pygame.draw.rect(screen, COLOR_LIBRE, [ x, y, PIXELES_POR_CUADRO, PIXELES_POR_CUADRO ])
			elif ( tablero[i][j] == 0 ):
				rect = pygame.draw.rect(screen, COLOR_INICIO, [ x, y, PIXELES_POR_CUADRO, PIXELES_POR_CUADRO ])
			elif ( tablero[i][j] == -1 ):
				rect = pygame.draw.rect(screen, COLOR_OBSTACULO, [ x, y, PIXELES_POR_CUADRO, PIXELES_POR_CUADRO ])
			elif (tablero[i][j] == -100 ):
				rect = pygame.draw.rect(screen, COLOR_LIBRE, [ x, y, PIXELES_POR_CUADRO, PIXELES_POR_CUADRO ])
			x+= PIXELES_POR_CUADRO + GROSOR_BORDE
		x = GROSOR_BORDE
		y+= PIXELES_POR_CUADRO + GROSOR_BORDE


	fin = False
	while not fin:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				fin = True

		pygame.display.flip()
		clock.tick(60)
	pygame.quit()

def doAlgorithm(size):
	tablero = construirTablero(size)
	esperarEntrada_Salida(size, tablero)
	# Indicar los obstáculos, salida e inicio
	expansionMaxima = ((len(tablero) * len(tablero)) - obstaculos) * 2

	# print(f'Numero de estados => {expansionMaxima}')
	# if tablero[xInicio][yInicio] != 0:
	# 	messagebox.showerror(message="Por azares del destino, el tablero no cuenta con una casilla de salida, que mala suerte...", title="Upss")
	# 	raise Exception("Por azares del destino, el tablero no cuenta con una casilla de salida, que mala suerte...")

	# nodoRaiz = Node(tablero[xInicio][yInicio], id=uniqueID())
	# nodoCursor = None

	# nodosVisitados = []

	# mostrarTablero(tablero)

	# valorArriba = arriba(tablero, xInicio, yInicio)
	# if(valorArriba != None):
	# 	uid = uniqueID()
	# 	nodoCursor = Node(valorArriba, parent=nodoRaiz, id=uid)

	# valorDerecha = derecha(tablero, xInicio, yInicio)
	# if(valorDerecha != None):
	# 	uid = uniqueID()
	# 	nodoCursor = Node(valorDerecha, parent=nodoRaiz, id=uid)

	# valorAbajo = abajo(tablero, xInicio, yInicio)
	# if(valorAbajo != None):
	# 	uid = uniqueID()
	# 	nodoCursor = Node(valorAbajo, parent=nodoRaiz, id=uid)

	# valorIzquierda = izquierda(tablero, xInicio, yInicio)
	# if(valorIzquierda != None):
	# 	uid = uniqueID()
	# 	nodoCursor = Node(valorIzquierda, parent=nodoRaiz, id=uid)

	# nodosVisitados.append(nodoRaiz.name)
	# nodoHijoEvaluando = nodoRaiz.children[0]
	# nodoSalida = None

	# # Implementación con un nivel de profundidad máximo
	# while nodoHijoEvaluando != None: # Iteramos a lo bestia :v
	# 	profundidad = nodoHijoEvaluando.depth
	# 	if nodoHijoEvaluando.name == -100:
	# 		print("Acabo de encontrar la salida :D => ", nodoHijoEvaluando)
	# 		nodoSalida = nodoHijoEvaluando
	# 		nodoHijoEvaluando = None
	# 		break
	# 	elif profundidad > (expansionMaxima - 1):
	# 		# Pasar al siguiente nodo segun profundidad maxmma
	# 		# try:
	# 		_nodo = rightsibling(nodoHijoEvaluando)
	# 		if(_nodo != None):
	# 			nodoHijoEvaluando = _nodo
	# 		else:
	# 		# except Exception:
	# 			_nodo = rightsibling(nodoHijoEvaluando.parent)
	# 			nodoHijoEvaluando = _nodo
	# 	else:
	# 		coordenadasHijoEvaluando = getCoords(tablero, nodoHijoEvaluando.name)
	# 		_x = int(coordenadasHijoEvaluando[0])
	# 		_y = int(coordenadasHijoEvaluando[1])
	# 		valorArriba = arriba(tablero, _x, _y)
	# 		if(valorArriba != None):
	# 			uid = uniqueID()
	# 			hijo = Node(valorArriba, parent=nodoHijoEvaluando, id=uid)
	# 		valorDerecha = derecha(tablero, _x, _y)
	# 		if(valorDerecha != None):
	# 			uid = uniqueID()
	# 			hijo = Node(valorDerecha, parent=nodoHijoEvaluando, id=uid)

	# 		valorAbajo = abajo(tablero, _x, _y)
	# 		if(valorAbajo != None):
	# 			uid = uniqueID()
	# 			hijo = Node(valorAbajo, parent=nodoHijoEvaluando, id=uid)

	# 		valorIzquierda = izquierda(tablero, _x, _y)
	# 		if(valorIzquierda != None):
	# 			uid = uniqueID()
	# 			hijo = Node(valorIzquierda, parent=nodoHijoEvaluando, id=uid)

	# 		nodoHijoEvaluando = nodoHijoEvaluando.children[0]

	# return nodoRaiz, nodoSalida

def evaluarEntradas(size, txtSize):
	nodoRaiz = None
	nodoRaiz, nodoSalida = doAlgorithm(size)
	while nodoSalida == None:
		nodoRaiz, nodoSalida = doAlgorithm(size)
	print(nodoRaiz)
	print(nodoSalida)
	showRecorridos(nodoSalida)

	UniqueDotExporter(nodoRaiz).to_picture("arbol_unique.png")
	# showRecorridos(nodoRaiz)
	# showRecorridos(nodoRaiz, tablero)
	cv2.namedWindow("Arbol resultante", cv2.WINDOW_NORMAL)
	imagenResultante = cv2.imread("arbol_unique.png", cv2.IMREAD_GRAYSCALE)
	ventanaImagenResizable = cv2.resize(imagenResultante, (800, 600))
	cv2.imshow('Arbol resultante', ventanaImagenResizable)
	cv2.waitKey()
	cv2.destroyAllWindows()

	txtSize.config(state=NORMAL)
	txtObst.config(state=NORMAL)
	messagebox.showinfo(message="Algoritmo terminado", title="Información")


if __name__ == "__main__":
	window = Tk()
	window.title("DSI - DFS Obstaculos")
	# window.geometry('350x200')
	window.resizable(False, False)
	# Etiqueta de Tamaño de cuadricula
	lblCuadSize = Label(window, text="Ingresa el tamaño de la cuadrícula: ", font=("Arial Bold", 15))
	lblCuadSize.grid(column=0, row=0)
	txtCuadSize = Entry(window, width=10)
	txtCuadSize.grid(column=1, row=0)
	txtCuadSize.config(state=NORMAL)
	btnStart = Button(window, text="Ejecutar algoritmo", fg="black", command=lambda: evaluarEntradas(int(txtCuadSize.get()), txtCuadSize))
	# btnStart = Button(window, text="Let's go!", fg="black", command=lambda: evaluarEntradas(3, 1, txtCuadSize, txtObstAmmount))
	btnStart.grid(column=0, row=2)
	window.mainloop()
