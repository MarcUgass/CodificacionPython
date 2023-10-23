# -*- coding: utf-8 -*-

import numpy as np

def entropia(probabilidades):
    entropia = 0
    if not np.any(probabilidades == 0):
        entropia = -np.sum(probabilidades * np.log2(probabilidades))
    else:
        for e in probabilidades:
            if not e == 0:
                entropia = entropia + e * np.log2(e)
    #sumatorio del calculo de la entropia (uso de la formula)
    return entropia

def entropia_fuente(probabilidades_conjuntas):
    #H(X)
    fuente = np.sum(probabilidades_conjuntas, axis=1) 
    #axis = 1, sirve para coger los valores de las filas, ya que queremos la fuente
    return entropia(fuente)

def entropia_receptor(probabilidades_conjuntas):
    #H(Y)
    receptor = np.sum(probabilidades_conjuntas, axis=0)
    #axis = 0, sirve para coger los valores de las columnas, ya que queremos de salida
    return entropia(receptor)

def entropia_fuente_condicionada_receptor(probabilidades_conjuntas):
    #H(X|Y) 
    receptor = np.sum(probabilidades_conjuntas, axis=0) 
    rentropia = 0
    for i in range(probabilidades_conjuntas.shape[1]):
        probabilidades_salida = probabilidades_conjuntas[:, i] / receptor[i]
        #P(X|Y) = P (X ∩ Y) / P(Y)
        rentropia -= receptor[i] * entropia(probabilidades_salida)
    return rentropia

def entropia_receptor_condicionada_fuente(probabilidades_conjuntas):
    #H(Y|X)
    fuente = np.sum(probabilidades_conjuntas, axis=1)
    rentropia = 0
    for i in range(probabilidades_conjuntas.shape[0]):
        probabilidades_salida = probabilidades_conjuntas[i, :] / fuente[i]
        #P(Y|X) = P (X ∩ Y) / P(X)
        rentropia -= fuente[i] * entropia(probabilidades_salida)
    return rentropia

def informacion_mutua(probabilidades_conjuntas):
    # I(X,Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)
    hx = entropia(np.sum(probabilidades_conjuntas, axis=1)) #H(X)
    hxy = float(entropia_fuente_condicionada_receptor(probabilidades_conjuntas)) #H(X|Y)
    informacion_mutua = hx - hxy
    return informacion_mutua

matriz = np.array([ #matriz 1 (con ruido)
                   [[0.2, 0.1],
                    [0.3, 0.4]],
                    #matriz 2 (sin ruido)
                    [[0.25, 0.25],
                     [0.25, 0.25]],
                    #matriz 3 (inutil)
                    [[0.5, 0],
                     [0, 0.5]]
                    ])
fuente = [] 
receptor = []
fuente_condicionada_receptor = []
recpetor_condicionada_fuente = []
informacionmutua = []
entropiar = []

for p in range(3):
    m =matriz[p]
    fuente.append(entropia_fuente(m))
    receptor.append(entropia_receptor(m))
    fuente_condicionada_receptor.append( entropia_fuente_condicionada_receptor(m))
    recpetor_condicionada_fuente.append(entropia_receptor_condicionada_fuente(m))
    informacionmutua.append( informacion_mutua(m))
    entropiar.append(entropia(m.flatten()))

    print("Resultados matriz", p+1, ": ")
    print("La entropia de la fuente es: ", fuente[p])
    print("La entropia del receptor es: ",receptor[p])
    print("La entropía conjunta de la fuente y el receptor: ", entropiar[p])
    print("La entropía condicionada de la fuente: ",fuente_condicionada_receptor[p])
    print("La entropía condicionada del receptor: ", recpetor_condicionada_fuente[p])
    print("La información mutua: ", informacionmutua[p],"\n") 