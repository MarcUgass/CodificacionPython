#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 11:00:03 2023

Ejemplo de implementación del algoritmo de Shannon-Fano para generación de árboles
de códigos instantáneos

@author: mpc
"""

from copy import deepcopy
import numpy as np


"""
Método de Shannon-Fano. Tiene como entrada una lista de pares (mensaje, probabilidad),
y da como salida el árbol de codificación binaria.
El árbol A se implementa como una lista de nodos, donde A=[ HijoIzq, HijoDcha ]
Si HijoIzq/HijoDcha son listas, entonces no son nodos hoja. En caso contrario, sí son nodos hoja
y contienen el mensaje codificado

ENTRADA:
    S: Lista de pares (mensaje, probabilidad). 
    root_node: True si estamos creando el nodo raíz (por defecto) o False en caso contrario
               Es una entrada auxiliar para no ordenar probabilidades varias veces. No debe usarse.


SALIDA:
    A: árbol de codificación binaria para el conjunto de mensajes dado en S
"""
def ShannonFano(S, root_node= True):
    
    # Comprobamos si la lista de mensajes contiene un único mensaje. 
    # En tal caso, hemos llegado a un nodo hoja y devolvemos sólo el mensaje
    if len(S) == 1:
        return S[0][0]
    
    # Ordenar fuente por probabilidad decreciente si estamos en el nodo raíz
    if root_node:
        for i in range(len(S)-1): # Ordenación básica
            for j in range(i+1, len(S)):
                if S[j][1] > S[i][1]:
                    aux= S[j]
                    S[j]= S[i]
                    S[i]= aux
                
    # División del conjunto de mensajes en dos partes lo más equiprobables posibles
    corte= 0 # Punto de corte donde se divide la lista de mensajes
    
    # Cálculo del punto de corte
    P= [ s[1] for s in S ]
    ProbCentral= np.sum(P)/2
    for i in range(len(P)):
        ProbEnI= np.abs(np.sum(P[:i]) - ProbCentral)
        ProbEnCorte= np.abs(np.sum(P[:corte]) - ProbCentral)
        if ProbEnI < ProbEnCorte:
            corte= i
    
    # Cogemos mensajes de la parte izquierda
    ParteIzq= [S[i] for i in range(corte)]
    
    # Cogemos mensajes de la parte derecha
    ParteDcha= [S[i] for i in range(corte, len(P))]
    
    # Aplicamos Shannon-Fano a izq y a dcha para calcular sub-árboles hijoIzq e HijoDcha
    HijoIzq= ShannonFano(ParteIzq, root_node= False)
    HijoDcha= ShannonFano(ParteDcha, root_node= False)
    
    # Creamos el árbol: 
    #      A[0] es hijo izquierda y tiene asociado el 0
    #      A[1] es hijo derecha y tiene asociado el 1
    A= [HijoIzq, HijoDcha]
    
    return A
    
    
    
"""
Función para realizar un recorrido sobre el árbol de codificación dado como entrada
y mostrar por consola la función de codificación implementada en dicho árbol

ENTRADA:
    A: Arbol de codificación generado con la función Shannon-Fano
    palabra: Argumento auxiliar usado en la recursividad. NO USAR.
             Se utiliza para llevar la cuenta de los códigos 0/1 a usar en cada palabra,
             desde la raíz hasta los nodos hoja
    
SALIDA:
    Ninguna. La función de codificación se muestra por consola
"""
def MostrarFuncionCodificacion(A, palabra=[]):
    
    # Comprobar si estamos en nodo hoja
    if not isinstance(A, list):
        print('\t', A, '-->', palabra) # Lo estamos: Mostramos la palabra asociada
    else: # No es nodo hoja
    
        # Recorremos Hijo Izquierda añadiendo un 0 a la palabra del código
        nuevapalabra= deepcopy(palabra)
        nuevapalabra.append(0)
        MostrarFuncionCodificacion(A[0], nuevapalabra)
        
        # Recorremos Hijo Derecha añadiendo un 1 a la palabra del código
        nuevapalabra= deepcopy(palabra)
        nuevapalabra.append(1)
        MostrarFuncionCodificacion(A[1], nuevapalabra)
        
    
######################################################################
# Código genérico para proebas 
"""
NumMensajes= 7 # Número total de mensajes a crear

# Mensajes de la fiente
M= [ 'M'+str(i+1) for i in range(NumMensajes) ]

# Probabilidades de los mensajes
P= np.random.rand(NumMensajes)
P/= np.sum(P)
"""

######################################################################
# Código específico con el ejemplo de las diapositivas de clase
NumMensajes= 6 # Número total de mensajes a crear
M= [ 'M'+str(i+1) for i in range(NumMensajes) ]
P= np.array([0.05, 0.1, 0.25, 0.2, 0.1, 0.3]) # Probabilidades de los mensajes


#########
# Generación de la fuente
S= [] # FUENTE: Lista de pares (mensaje , probabilidad)
for m,prob in zip(M, P):
    S.append( (m, prob) )

# Mostramos cada mensaje y su probabilidad:
print('Mensajes de la fuente y su probabilidad:')
for m,p in S:
    print('\t', m, '=>', p)


# Generación del árbol de codificación con Shannon-Fano
Arbol= ShannonFano(S)

# Mostramos la implementación de lista de listas del árbol generado
print('\nArbol del codigo como lista de listas:\n', Arbol)


# Mostramos la función de codificación generada por el árbol
print('\nFunción de codificación implementada en el árbol:')
MostrarFuncionCodificacion(Arbol)

