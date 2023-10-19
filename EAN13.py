#!/usr/bin/env python3
# -*- coding: utf-8 -*-


############################################################################
# Generación de códigos de barras de tipo EAN-13
############################################################################


#imports
import numpy as np
import matplotlib.pyplot as plt



#############################################################
# Secuencia de dígitos a codificar: El código de barras que queremos generar
digitos= "480000107107"


#######################################################################################
# Constantes a usar en el programa
zonaSilenciosa= 9 # Tamaño de la zona silenciosa en Unidades
totalUnidades= 95+2*zonaSilenciosa # Se deben reservar totalUnidades unidades para imprimir el código de barras

# Constantes con objeto único de visualización en imágenes
grosor= 2 # Ancho (en píxeles) de cada unidad
tamY= 100 # Aquí el alto de la imagen, sin contar con zona silenciosa



######################################################################
# Creación de constantes para generación de códigos EAN-13: Codificaciones B, R, G
# y selección de codificación según código de control
#######
# Definición de las diferentes codificaciones

codificaciones= np.zeros( (3, 10, 7), dtype=np.uint8)
codifB= np.uint8([ # Asignación de unidades a bandas de color (0= negro, 1=blanco) en codificación B
    [1, 1, 1, 0, 0, 1, 0],
    [1, 1, 0, 0, 1, 1, 0],
    [1, 1, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0]
])

codifR= 1-codifB # Codificación tipo R

# Codificación tipo G
codifG= np.zeros((10, 7) , dtype=np.uint8)

for i in range(7):
    codifG[:,i]= codifR[:, 6-i]

codificaciones[0, :, :]= codifB
codificaciones[1, :, :]= codifG
codificaciones[2, :, :]= codifR


# Selector de codificación según el valor de control
selectCodif= np.uint8(
    [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1],
        [0, 0, 1, 1, 0, 1],
        [0, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 1],
        [0, 1, 1, 0, 0, 1],
        [0, 1, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 0]
    ]
)



# Función para calcular el código de control
def CodigoControl(digitos):
    digits = [int(i) for i in digitos]
    return (10 - (sum(digits[1::2]) + (sum(digits[0::2]) * 3))) % 10



# Función que calcula un vector de 113 componentes con las unidades de un código de barras EAN-13
# - Tiene como entrada:
#    * codigo: el código en dígitos (cadena de caracteres)
#    * selectCodif: Las diferentes codificaciones para la parte izquierda
#    * codificaciones: Las codificaciones de cada dígito
# - Da como salida un par (tupla): 
#    * Un vector de 113 componentes con el código en 1-D. Cada componente es una unidad. Vale 0 si es negro, 1 si es blanco
#    * El dígito de control
def CalcularCodigoBarras(codigo, selectCodif, codificaciones):
    digitoControl= CodigoControl(codigo)
    barras= np.ones(95+2*9, dtype=np.uint8)
    barras[9+3+6*7+1]= barras[9+3+6*7+3]= 0
    # Rellenamos marcas
    barras[9]= barras[11]= barras[101]= barras[103]= 0
    
    # Rellenamos según haya tocado, desde la posición 9
    for i in range(12):
        for j in range(7):
            if (i<6):
                barras[9+3+i*7+j]= codificaciones[selectCodif[digitoControl, i], int(codigo[i]), j]
            else:
                barras[9+8+i*7+j]= codificaciones[2, int(codigo[i]), j]
    return (barras, digitoControl)





###############################################################
# Cálculo del código de barras 
###############################################################

# Calculamos el código de barras para el array "digitos"
resul= CalcularCodigoBarras(digitos, selectCodif, codificaciones)





###############################################################
# Visualización
###############################################################


# Función auxiliar para rellenar un área rectangular de una matriz 2D con un valor
# Se usa para la visualización del código generado
#  - matriz: Matriz a rellenar. Debe ser un array 2D numpy
#  - x0: Columna desde donde se comienza a rellenar
#  - y0: Fila desde donde se comienza a rellenar
#  - xf: Columna donde se termina de rellenar (inclusive)
#  - yf: Fila donde se termina de rellenar (inclusive)
#  - valor: Valor a rellenar
def RellenarMatriz(matriz, x0, y0, xf, yf, valor):
    matriz[y0:(yf+1), x0:(xf+1)]= valor
    return matriz



# Creación de la imagen para mostrar el código de barras
codigo= np.ones( (tamY+zonaSilenciosa*2, grosor*totalUnidades) , dtype=np.uint8)*255


# Pintamos la imagen
barras= resul[0]
for i in range(len(barras)):
    if (barras[i]==0):
        if (i<=11 or i>=100 or (i>=55 and i<=57)):
            codigo= RellenarMatriz(codigo, i*grosor, 9, (i+1)*grosor-1, tamY, 0)
        else:
            codigo= RellenarMatriz(codigo, i*grosor, 9, (i+1)*grosor-1, tamY-9, 0)
            
            
# Mostramos la imagen
imgplot = plt.imshow(codigo,cmap='gray')
imgplot.axes.get_xaxis().set_visible(False)
imgplot.axes.get_yaxis().set_visible(False)
plt.text(30, tamY+10, digitos[0:6], fontsize=30)
plt.text(120, tamY+10, digitos[6:12], fontsize=30)
plt.text(3, tamY+10, resul[1], fontsize=30)

print('El código es: ', digitos)
print('Su dígito de control es: ', resul[1])
