#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy
import numpy as np


def LeerFicheroDiccionario(nombre_archivo):
    # Inicializar el diccionario con todas las letras del abecedario
    simbolos_letras = [',', '.', ';', ':'] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    diccionario = {simbolo: 0 for simbolo in simbolos_letras}

    # Abrir el archivo en modo lectura
    with open(nombre_archivo, 'r') as archivo:
        # Leer el contenido del archivo
        contenido = archivo.read()

        # Contar la frecuencia de cada letra en el texto
        total_letras = 0
        for letra in contenido:
            if letra in diccionario:
                diccionario[letra.upper()] += 1
                total_letras += 1

    # Calcular las probabilidades relativas
    for letra in diccionario:
        diccionario[letra] /= total_letras

    return diccionario

def construir_arbol_huffman(diccionario_probabilidades):
    NodoHuffman = tuple  # Definir la tupla NodoHuffman aquí
    
    #crear una serie de tuplas que contangane el simbolo y probabilidad
    #valores None, mas adelante nos sirve para izquierda o derecha
    nodos = [NodoHuffman((None, None, símbolo, probabilidad)) for símbolo, probabilidad in diccionario_probabilidades.items()] 

    #se queda hasta un elemento en la lista, ya que será como el "tronco del arbol", ej = [[1,[2,[3,4]]]]
    while len(nodos) > 1: 

        nodos.sort(key=lambda x: x[3])  # Ordenar por probabilidad
        izquierda = nodos.pop(0) #sacar el primer elemento
        derecha = nodos.pop(0) #sacar el segundo elemento
        
        #Crear nuevo nodo con la suma de las probabilidades de los dos nodos sacados del pop
        nuevo_nodo = NodoHuffman((None, None, None, izquierda[3] + derecha[3], izquierda, derecha)) 
        nodos.append(nuevo_nodo)

    return nodos[0]

def generar_diccionario_codificación(arbol, prefijo="", diccionario=None):
     if diccionario is None:  
        diccionario = {}

     if arbol[2] is not None:  # Símbolo presente
        diccionario[arbol[2]] = prefijo
     if len(arbol) > 4 and arbol[4] is not None:  # Nodo izquierdo presente
        generar_diccionario_codificación(arbol[4], prefijo + "0", diccionario) # Prefijo + 0 = 0 para la izquierda 
     if len(arbol) > 5 and arbol[5] is not None:  # Nodo derecho presente
        generar_diccionario_codificación(arbol[5], prefijo + "1", diccionario) # Prefijo + 1 = 1 para la derecha


     return diccionario

def decodificar_cadena(cadena, diccionario):
    mensaje_decodificado = ""
    codigo_actual = ""

    for bit in cadena:
        codigo_actual += bit
        # Verifica si el código actual está en el diccionario
        if codigo_actual in diccionario.values():
            # Busca el símbolo correspondiente al código actual
            simbolo = next(key for key, value in diccionario.items() if value == codigo_actual)
            mensaje_decodificado += simbolo
            codigo_actual = ""  # Reinicia el código actual

    return mensaje_decodificado


diccprob = LeerFicheroDiccionario("TextoAComprimir.txt")

arbol_huffman = construir_arbol_huffman(diccprob)

diccionario_codificación = generar_diccionario_codificación(arbol_huffman)

print(diccionario_codificación)

#EJEMPLOS

mensaje = decodificar_cadena("1011010101110100", diccionario_codificación)

