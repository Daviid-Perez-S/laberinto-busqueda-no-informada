'''
-------------------------------------
Laberinto con algoritmo de búsqueda no informada Depth First Search (DSF)
Universidad Politécnica de Chiapas
20/nov/2019

Hecho por: Luis Fernando Hernández Morales y David Pérez S.
-------------------------------------
'''

import hashlib
import os
import random
from tkinter import NORMAL, Button, Entry, Label, Tk, messagebox, simpledialog

import cv2
import numpy as np
from anytree import Node, PreOrderIter, RenderTree
from anytree.exporter import UniqueDotExporter, DotExporter
from anytree.util import rightsibling

'''
-------------------------------------
Herramientas
-------------------------------------
'''
def obtener_ID_unico():
	return hashlib.md5(os.urandom(32)).hexdigest()[:5]

def obtener_indice_aleatorio(limite):
	return random.randint(0,limite-1)

def mostrar_tablero_consola(tablero):
	print("--------------------\n")
	for row in tablero:
		print(row)
	print("--------------------\n")

def mostrar_recorrido_consola(nodoPadre):
	print(nodoPadre)
	camino = f'{nodoPadre.name}'
	padre = nodoPadre.parent
	while padre != None:
		camino += f' > {padre}'
		padre = padre.parent
	return camino

def obtener_coordenadas(tablero, valorBuscado):
	tmp = np.array(tablero)
	return np.where(tmp==valorBuscado, )

def existeEnLaPila(pila, valor):
	result = False
	for v in pila:
		if v == valor:
			result = True
	return result

def cerrar_ventana(ventana):
	global bandera_cerrar
	bandera_cerrar = True
	ventana.destroy()
'''
-------------------------------------
Movimientos permitidos para el agente
-------------------------------------
'''
def ir_arriba(tablero, x, y):
	# Ir hacia ir_arriba
	try:
		if tablero[x-1][y] != -1 and x > 0:
			return tablero[x-1][y]
	except IndexError:
		pass
	return None

def ir_derecha(tablero, x, y):
	# Ir hacia la ir_derecha
	try:
		if tablero[x][y+1] != -1:
			return tablero[x][y+1]
	except IndexError:
		pass
	return None

def ir_abajo(tablero, x, y):
	# Ir hacia ir_abajo
	try:
		if tablero[x+1][y] != -1:
			return tablero[x+1][y]
	except IndexError:
		pass
	return None

def ir_izquierda(tablero, x, y):
	# Ir hacia la ir_izquierda
	try:
		if tablero[x][y-1] != -1 and y > 0:
			return tablero[x][y-1]
	except IndexError:
		pass
	return None

'''
-------------------------------------
Configuración del tablero
-------------------------------------
'''

array_obstaculos = []
casilla_inicio = None
casilla_fin = None
bandera_cerrar = False

def construir_tablero(cantidadFilas):
	tablero = []
	array_tablero = []

	contador = 0
	for i in range(0, cantidadFilas):
		row = []
		for j in range(contador+1, (contador + cantidadFilas)+1):
			row.append(j)
			contador = j
			array_tablero.append(contador)
		tablero.append(row)
	return tablero

def asignar_casilla_tablero(tablero, casilla, tipo):
	array_coord = obtener_coordenadas(tablero, int(casilla))
	x = int(array_coord[0])
	y = int(array_coord[1])
	tablero[x][y] = tipo
	return tablero

def ingresar_numero_casilla(pantalla_tablero, tipo_casilla, tablero):
	
	casilla = None
	global array_obstaculos
	global casilla_inicio
	global casilla_fin
	global bandera_cerrar

	if tipo_casilla == "libre":
		casilla = simpledialog.askstring(title="Casilla libre", prompt="Ingresa un número de casilla:")
		tablero = asignar_casilla_tablero(tablero, casilla, casilla)
		pantalla_tablero.destroy()
	elif tipo_casilla == "obstaculo":
		casilla = simpledialog.askstring(title="Obstáculo", prompt="Ingresa un número de casilla:")
		array_obstaculos.append(casilla)
		tablero = asignar_casilla_tablero(tablero, casilla, -1)
		pantalla_tablero.destroy()
	elif tipo_casilla == "inicio":
		casilla = simpledialog.askstring(title="Casilla inicio", prompt="Ingresa un número de casilla:")
		casilla_inicio = casilla
		tablero = asignar_casilla_tablero(tablero, casilla, 0)
		pantalla_tablero.destroy()
	elif tipo_casilla == "fin":
		casilla = simpledialog.askstring(title="Casilla fin", prompt="Ingresa un número de casilla:")
		casilla_fin = casilla
		tablero = asignar_casilla_tablero(tablero, casilla, -100)
		pantalla_tablero.destroy()
	elif tipo_casilla == "listo":
		if casilla_inicio != None and casilla_fin != None:
			print("--- Iniciando algoritmo ---")
			nodoRaiz = iniciar_algoritmo_principal(tablero)
			generar_imagen_arbol(nodoRaiz)
			messagebox.showinfo(message="Algoritmo terminado", title="Información")
			print("--- Algoritmo terminado ---")
		else:
			messagebox.showinfo(message="Aún te faltan casillas por configurar", title="Información")

def configurar_tablero(size):

	global bandera_cerrar

	COLOR_BLANCO = "#ffffff"
	COLOR_NEGRO = "#000000"
	COLOR_LIBRE = "#a5c3f2"
	COLOR_OBSTACULO = "#b7b7b7"
	COLOR_INICIO = "#b7d6aa"
	COLOR_SALIDA = "#e8999a"

	# Construcción del tablero
	tablero = construir_tablero(size)

	while(bandera_cerrar == False):
		# Configuración de casillas
		pantalla_tablero = Tk()
		pantalla_tablero.title("Configuración de laberinto")
		b = 0

		for r in range(len(tablero)):
			for c in range(len(tablero[0])):
				b = tablero[r][c]
				if ( tablero[r][c] > 0 ):
					Button(pantalla_tablero, text = str(b), borderwidth = 1, height = 5, width = 10, bg = COLOR_LIBRE ).grid(row = r, column = c)
				elif ( tablero[r][c] == 0 ):
					Button(pantalla_tablero, text = str(b), borderwidth = 1, height = 5, width = 10, bg = COLOR_INICIO ).grid(row = r, column = c)
				elif ( tablero[r][c] == -1 ):
					Button(pantalla_tablero, text = str(b), borderwidth = 1, height = 5, width = 10, bg = COLOR_OBSTACULO ).grid(row = r, column = c)
				elif (tablero[r][c] == -100 ):
					Button(pantalla_tablero, text = str(b), borderwidth = 1, height = 5, width = 10, bg = COLOR_SALIDA ).grid(row = r, column = c)

		# Button(pantalla_tablero, command = lambda: ingresar_numero_casilla(pantalla_tablero, "libre", tablero), text = "Sel. casilla libre", borderwidth = 1, height = 3, width = 20 ).grid(row = 0, column = len(tablero) + 2)
		Button(pantalla_tablero, command = lambda: ingresar_numero_casilla(pantalla_tablero, "obstaculo", tablero), text = "Sel. obstáculo", fg = "grey", borderwidth = 1, height = 3, width = 20 ).grid(row = 0, column = len(tablero) + 2)
		Button(pantalla_tablero, command = lambda: ingresar_numero_casilla(pantalla_tablero, "inicio", tablero), text = "Sel. inicio", fg = "green", borderwidth = 1, height = 3, width = 20 ).grid(row = 1, column = len(tablero) + 2)
		Button(pantalla_tablero, command = lambda: ingresar_numero_casilla(pantalla_tablero, "fin", tablero), text = "Sel. fin", fg = "red", borderwidth = 1, height = 3, width = 20 ).grid(row = 2, column = len(tablero) + 2)
		Button(pantalla_tablero, command = lambda: ingresar_numero_casilla(pantalla_tablero, "listo", tablero), text = "Listo", fg = "blue", borderwidth = 1, height = 3, width = 20 ).grid(row = 3, column = len(tablero) + 2)
		Button(pantalla_tablero, command = lambda: cerrar_ventana(pantalla_tablero), text = "Cerrar", borderwidth = 1, height = 3, width = 20 ).grid(row = 4, column = len(tablero) + 2)
		
		pantalla_tablero.mainloop()

'''
-------------------------------------
Algoritmo principal
-------------------------------------
'''
def iniciar_algoritmo_principal(tablero):
	# Indicar los obstáculos, salida e inicio
	expansionMaxima = ((len(tablero) * len(tablero)) - len(array_obstaculos)) * 2

	print(f'Numero de estados: {expansionMaxima}')

	array_tmp = obtener_coordenadas(tablero, 0)
	xInicio = int(array_tmp[0])
	yInicio = int(array_tmp[1])
	nodoRaiz = Node(tablero[xInicio][yInicio], id=obtener_ID_unico())
	banderaSalidaEncontrada = False

	valorir_arriba = ir_arriba(tablero, xInicio, yInicio)
	if(valorir_arriba != None):
		uid = obtener_ID_unico()
		Node(valorir_arriba, parent=nodoRaiz, id=uid)

	valorir_derecha = ir_derecha(tablero, xInicio, yInicio)
	if(valorir_derecha != None):
		uid = obtener_ID_unico()
		Node(valorir_derecha, parent=nodoRaiz, id=uid)

	valorir_abajo = ir_abajo(tablero, xInicio, yInicio)
	if(valorir_abajo != None):
		uid = obtener_ID_unico()
		Node(valorir_abajo, parent=nodoRaiz, id=uid)

	valorir_izquierda = ir_izquierda(tablero, xInicio, yInicio)
	if(valorir_izquierda != None):
		uid = obtener_ID_unico()
		Node(valorir_izquierda, parent=nodoRaiz, id=uid)

	nodoHijoEvaluando = nodoRaiz.children[0]

	# Implementación con un nivel de profundidad máximo
	while banderaSalidaEncontrada == False: # Iteramos a lo bestia :v
		profundidad = nodoHijoEvaluando.depth

		if nodoHijoEvaluando.name == -100:
			print("Acabo de encontrar la salida :D => ", nodoHijoEvaluando)
			# nodoHijoEvaluando = None
			banderaSalidaEncontrada = True
		elif profundidad > (expansionMaxima - 1):
			# Pasar al siguiente nodo segun profundidad maxima
			_nodo = rightsibling(nodoHijoEvaluando)
			if(_nodo != None):
				nodoHijoEvaluando = _nodo
			else:
				while(_nodo == None):
					nodoHijoEvaluando = nodoHijoEvaluando.parent
					_nodo = rightsibling(nodoHijoEvaluando)
				nodoHijoEvaluando = _nodo
		else:
			coordenadasHijoEvaluando = obtener_coordenadas(tablero, nodoHijoEvaluando.name)
			_x = int(coordenadasHijoEvaluando[0])
			_y = int(coordenadasHijoEvaluando[1])

			valorir_arriba = ir_arriba(tablero, _x, _y)
			if(valorir_arriba != None):
				uid = obtener_ID_unico()
				Node(valorir_arriba, parent=nodoHijoEvaluando, id=uid)

			valorir_derecha = ir_derecha(tablero, _x, _y)
			if(valorir_derecha != None):
				uid = obtener_ID_unico()
				Node(valorir_derecha, parent=nodoHijoEvaluando, id=uid)

			valorir_abajo = ir_abajo(tablero, _x, _y)
			if(valorir_abajo != None):
				uid = obtener_ID_unico()
				Node(valorir_abajo, parent=nodoHijoEvaluando, id=uid)

			valorir_izquierda = ir_izquierda(tablero, _x, _y)
			if(valorir_izquierda != None):
				uid = obtener_ID_unico()
				Node(valorir_izquierda, parent=nodoHijoEvaluando, id=uid)

			nodoHijoEvaluando = nodoHijoEvaluando.children[0]

	return nodoRaiz

def generar_imagen_arbol(nodoRaiz):
	UniqueDotExporter(nodoRaiz).to_picture("arbol_unique.png")
	cv2.namedWindow("Arbol resultante", cv2.WINDOW_NORMAL)
	imagenResultante = cv2.imread("arbol_unique.png", cv2.IMREAD_GRAYSCALE)
	ventanaImagenResizable = cv2.resize(imagenResultante, (800, 600))
	cv2.imshow('Arbol resultante', ventanaImagenResizable)
	cv2.waitKey()
	cv2.destroyAllWindows()
'''
-------------------------------------
Inicio
-------------------------------------
'''
def evaluar_entradas_iniciales(size, txtSize):
	
	try:
		size = int(size)
		# Construimos, configuramos el tablero e iniciamos el algoritmo de búsqueda
		configurar_tablero(size)

	except Exception:
		messagebox.showinfo(message="Ingresa un número por favor", title="Advertencia")

if __name__ == "__main__":
	
	window = Tk()
	window.title("Búsqueda no informada DFS")
	# window.geometry('350x200')
	window.resizable(False, False)

	# Etiqueta de Tamaño de cuadricula
	lblCuadSize = Label(window, text="Ingresa el tamaño de la cuadrícula: ", font=("Arial Bold", 15))
	lblCuadSize.grid(column=0, row=0)

	# Entradas
	txtCuadSize = Entry(window, width=10)
	txtCuadSize.grid(column=1, row=0)
	txtCuadSize.config(state=NORMAL)

	btnStart = Button(window, text="Ejecutar algoritmo", fg="black", command=lambda: evaluar_entradas_iniciales(txtCuadSize.get(), txtCuadSize))
	# btnStart = Button(window, text="Let's go!", fg="black", command=lambda: evaluar_entradas_iniciales(3, 1, txtCuadSize, txtObstAmmount))
	btnStart.grid(column=0, row=2)
	
	window.mainloop()
