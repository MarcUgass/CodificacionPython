# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

digitos= "01234567890"

zonaSilenciosa= 9 # Tamaño de la zona silenciosa en Unidades
totalUnidades= ((12*7)+3+3+5)+2*zonaSilenciosa #10 numeros que ocupan 7 unidades + 11 unidades

grosor= 2
tamY= 100

codificaciones= np.zeros( (2, 10, 7), dtype=np.uint8)
codifL= np.uint8([ #zona izquierda
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

codifR= 1-codifL #zona derecha

codificaciones[0, :, :]= codifL
codificaciones[1, :, :]= codifR

def CodigoControl(digitos):
    digits = [int(i) for i in digitos]
    return ((sum(digits[1::2])*3 + sum(digits[0::2]) - 10)  % 10 )
    


def CalcularCodigoBarras(codigo, codificaciones):
    digitoControl= CodigoControl(codigo)
    d = digitos + str(digitoControl)
    barras= np.ones(totalUnidades, dtype=np.uint8)
    
    barras[9+3+6*7+1]= barras[9+3+6*7+3]= 0
    # Rellenamos marcas
    barras[9]= barras[11]= barras[101]= barras[103]= 0
    
    for i in range(12):
        for j in range(7):
            if (i<6):
                barras[9+3+i*7+j]= codificaciones[0, int(d[i]), j]
            else:
                barras[9+8+i*7+j]= codificaciones[1, int(d[i]), j]
    return (barras, digitoControl)

# Calculamos el código de barras para el array "digitos"
resul= CalcularCodigoBarras(digitos, codificaciones)

def RellenarMatriz(matriz, x0, y0, xf, yf, valor):
    matriz[y0:(yf+1), x0:(xf+1)]= valor
    return matriz

codigo= np.ones( (tamY+zonaSilenciosa*2, grosor*totalUnidades) , dtype=np.uint8)*255

barras= resul[0]
for i in range(len(barras)):
    if (barras[i]==0):
        if (i<=18 or i>=93 or (i>=55 and i<=57)):
            codigo= RellenarMatriz(codigo, i*grosor, 9, (i+1)*grosor-1, tamY, 0)
        else:
            codigo= RellenarMatriz(codigo, i*grosor, 9, (i+1)*grosor-1, tamY-9, 0)

imgplot = plt.imshow(codigo,cmap='gray')
imgplot.axes.get_xaxis().set_visible(False)
imgplot.axes.get_yaxis().set_visible(False)
plt.text(40, tamY+10, digitos[1:6], fontsize=30)
plt.text(120, tamY+10, digitos[6:11], fontsize=30)
plt.text(3, tamY+10, digitos[0], fontsize=30)
plt.text(210, tamY+10, resul[1], fontsize=30)


print('El código es: ', digitos)
print('Su dígito de control es: ', resul[1])