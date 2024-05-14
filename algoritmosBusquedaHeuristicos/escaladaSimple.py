import copy

# Al momento de crear el grafo, especificar cantidad de nodos => especificar el tamaño de array para nodos => mayor rendimiento al insertar

def heuristicaLineaRecta(grafo, estadoFinal):
    
    tablaH = [{"name":"A","distancia":0}]
    return tablaH


def heuristicaManhattan(grafo, estadoFinal):
    
    tablaH = [ {"name":"A","distancia":0}]
    return tablaH

# Operador(criterio): recorrer en orden alfabetico.
# Parametros:
# grafo : [{"name":"A","posicion":{"x":0,"y":0}, "aristas": ["D","B","H"]}]
# tablaH : [{"name":"A","distancia":0}]
# estadoInicial : {"name":"A","distancia":0}
def algEscaladaSimple(tablaH, grafo, estadoInicial):
    
    resultado = { "grafoResultante": [] }
    
    if(estadoInicial["distancia"] == 0): # Verifica si es el estado objetivo
        estadoFinal = buscarEstadoEnGrafo(grafo, estadoInicial["name"])
        estadoFinal["aristas"] = []
        resultado["grafoResultante"].append(estadoFinal)
        return resultado
    
    estadoActual = estadoInicial
    
    while True :
        
        nodo = buscarEstadoEnGrafo(grafo, estadoActual["name"])
        #if(len(nodo["aristas"]) == 0):
        #    break
        
        nodo["aristas"] = sorted(nodo["aristas"])
        resultado["grafoResultante"].append(nodo)
        
        for arista in nodo["aristas"]: 
            
            newEstado = buscarEstadoEnGrafo(tablaH, arista)
            
            if(newEstado["distancia"] == 0):
                estadoFinal = buscarEstadoEnGrafo(grafo, newEstado["name"])
                estadoFinal["aristas"] = []
                resultado["grafoResultante"].append(estadoFinal)
                return resultado
                
            if(newEstado["distancia"] < estadoActual["distancia"]):
                estadoActual = newEstado
                break
            
        if(estadoActual["name"] == nodo["name"]):
            break
    
    return resultado
   
      
def buscarEstadoEnGrafo(grafo, estadoName):
    for nodo in grafo:
        if(nodo["name"] == estadoName):
            # copia del objeto por valor y no referencia
            return copy.deepcopy(nodo)
      

# Operador(criterio): recorrer en orden alfabetico.
# Parametros:
# grafo : [{"name":"A","posicion":{"x":0,"y":0}, "aristas": ["D","B","H"]}]
# tablaH : [{"name":"A","distancia":0}]
# estadoInicial : {"name":"A","distancia":0}   
def algMaximaPendiente(tablaH, grafo, estadoInicial):
    
    resultado = { "grafoResultante": [] }
    
    if(estadoInicial["distancia"] == 0): # Verifica si es el estado objetivo
        estadoFinal = buscarEstadoEnGrafo(grafo, estadoInicial["name"])
        estadoFinal["aristas"] = []
        resultado["grafoResultante"].append(estadoFinal)
        return resultado
    
    estadoActual = estadoInicial
    estadoSucesor = estadoInicial
    
    while True:
        
        nodo = buscarEstadoEnGrafo(grafo, estadoActual["name"])
        
        nodo["aristas"] = sorted(nodo["aristas"])
        resultado["grafoResultante"].append(nodo)
    
        for arista in nodo["aristas"]:
            newEstado = buscarEstadoEnGrafo(tablaH, arista)
            
            if(newEstado["distancia"] == 0):
                estadoFinal = buscarEstadoEnGrafo(grafo, newEstado["name"])
                estadoFinal["aristas"] = []
                resultado["grafoResultante"].append(estadoFinal)
                return resultado
                
            if(newEstado["distancia"] < estadoSucesor["distancia"]):
                estadoSucesor = newEstado
                
        if(estadoSucesor["name"] == nodo["name"]):
            break
        else:
            estadoActual = estadoSucesor
        
    return resultado


#TEST:

# Los datos del grafo y tabla de heuristica utilizados en las pruebas para la verificacion del correcto funcionamiento, fueron obtenidos
# de los ejercicios realizados en clase. Estos ejericios reusltos fueron comparados con los resultados de esta implementacion para verificar 
# el comportamiento esperado

def test():
    grafo = [ {"name":"A","posicion":{"x":0,"y":0}, "aristas": ["D","B","C","E"]},
              {"name":"B","posicion":{"x":0,"y":0}, "aristas": ["A","D","G"]},
              {"name":"C","posicion":{"x":0,"y":0}, "aristas": ["A","H"]},
              {"name":"D","posicion":{"x":0,"y":0}, "aristas": ["A","B","F","I"]},
              {"name":"E","posicion":{"x":0,"y":0}, "aristas": ["A","H","G"]},
              {"name":"F","posicion":{"x":0,"y":0}, "aristas": ["D","K"]},
              {"name":"G","posicion":{"x":0,"y":0}, "aristas": ["E","B"]},
              {"name":"H","posicion":{"x":0,"y":0}, "aristas": ["C","E"]},
              {"name":"I","posicion":{"x":0,"y":0}, "aristas": ["D","J"]},
              {"name":"J","posicion":{"x":0,"y":0}, "aristas": ["I","K"]},
              {"name":"K","posicion":{"x":0,"y":0}, "aristas": ["J","F"]}
        ]
    
    tablaH = [{"name":"A","distancia":58},
          {"name":"B","distancia":60},
          {"name":"C","distancia":32},
          {"name":"D","distancia":20},
          {"name":"E","distancia":25},
          {"name":"F","distancia":10},
          {"name":"G","distancia":20},
          {"name":"H","distancia":20},
          {"name":"I","distancia":80},
          {"name":"J","distancia":20},
          {"name":"K","distancia":0}
        ]
    
    #Interpretacion de resutado: Objetos nodos Son camino/rama de menor costo al estado final, de las aristas de cada nodo(se consideran recorridas hasta la arista que
    # se encuantra como objeto nodo a continuacion de esta, de no haber nodo a continuacion => se recorrieron todas pero nunguna es mejor que el nodo actual).
    # Asi como tambien las aristas de los nodos que ya se encuentran como objetos nodos anteriores(estan en el camino, rama) => no se consideran evaluadas.
    # Nodo objeto que tenga aristas un array vacio significa que ese es el nodo objetivo(estado final)
    result = algEscaladaSimple(tablaH, grafo, {"name":"A","distancia":58})
    print(result)
    
    #Interpretacion de resultado: Lo nodos objetos no el camino o rama de monor costo al estado final, las aristas de cada nodo objeto son recorridas por lo tanto formaran parte
    #del arbol resultante(estando estas conectadas unicamente con nodo objeto que las contiene). 
    #Los nodos que ya se encuentran como objetos nodos anteriores(estan en el camino, rama) => no se consideran evaluadas.
    #Nodo objeto que tenga aristas un array vacio significa que ese es el nodo objetivo(estado final)
    result = algMaximaPendiente(tablaH, grafo, {"name":"A","distancia":58})
    print(result)
    
    