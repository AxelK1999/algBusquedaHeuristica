from tkinter import *
import networkx as nx
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import algBusquedaHeuristica
import random
import string
import copy

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        #configurar alto y acnho aqui:
        self.canvas.configure(yscrollcommand=scrollbar.set, width=450)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class ScrollableFrameHorizontal(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar_h = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar_h.set)

        scrollbar_h.pack(side="bottom", fill="x")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

class interfazCargaDeGrafo:
    
    grafo = []
    estadoInicial = {"name":""}
    estadoFinal = {"name":""}
        
    pasoActual = 0

    def __init__(self, raiz):
        self.raiz = raiz
        
        self.frame = Frame(raiz)
        self.frame.config(width=500, height=500) #bg="lightblue"
        self.frame.pack(side="left", fill="both", expand=True)
    
        #self.frame.bind("<Configure>", self.on_window_resize) # responsive
        self.titulo = Label(self.frame,text="Carga de datos de grafo",font=(18))
        self.titulo.place(x=500/3.5,y=20)

        self.seccionCargaDeEstados(raiz)
        
        barra3 = Label(self.frame, text="____________________________________________________________________________________________________")
        barra3.place(x=0,y=535)
        
        self.seccionSeleccionAlgH(raiz)
        
        barra4 = Label(self.frame, text="____________________________________________________________________________________________________")
        barra4.place(x=0,y=680)
        
        self.seccionResultado(raiz)
        
    def seccionCargaDeEstados(self,raiz):
        self.lblNroEstados = Label(self.frame,text="Nro. de estados: ")
        self.lblNroEstados.place(x=20, y=60)
        
        self.inputNroEstados = Entry(raiz, width=5)
        self.inputNroEstados.place(x= 140, y=60)
    
        self.btnCrearEstados = Button(self.frame, text="crear estados", command = self.on_click_crear_estados)
        self.btnCrearEstados.place(x=200, y= 58)

        self.titleTableEstados = Label(self.frame,text="Nro.               Name                                     Pos.(x,y)                        Conexiones            ")
        self.titleTableEstados.place(x=20, y=100)
    
        self.frameEstados = ScrollableFrame(self.frame)
        self.frameEstados.place(x=10, y=120)
    
        self.btnCargaAleatoriaEstados = Button(self.frame, text="Carga datos de estados automatico", command = self.on_click_carga_datos_grafo_automatico)
        self.btnCargaAleatoriaEstados.place(x=290, y= 58)
        self.btnCargaAleatoriaEstados.config(state="disabled")
        
        self.btnCargarGrafo = Button(self.frame, text="Cargar grafo", command = self.on_click_cargar_grafo)
        self.btnCargarGrafo.place(x=200,y=410)
    
        barra2 = Label(self.frame, text="____________________________________________________________________________________________________")
        barra2.place(x=0,y=450)
        
        # En lugar de posicionar elementos con place -> hacerlo con pack (lo que se hace dentro del frame a continuacion):
        frame = Frame(self.frame)
        frame.config(width=500, height=500)
        frame.place(x=0, y=490)
        
        self.frameOptionMenuInputEstadosInicialFinal = frame
        self.seccionSeleccionEstadoInicialFinal(frame)
    
        # apunte : ver propiedades y funciones de un elemento/objeto en python
        #print(dir(self.inputEstadoFinal))
        
    def seccionSeleccionEstadoInicialFinal(self, frame, opciones=["Ninguno"]):    
        self.lblEstadoInicial = Label(frame,text="Estado inicial: ")
        self.lblEstadoInicial.pack(side="left",padx=15, pady=5)
        
        self.opcionesDeEstadosInicialFinal = opciones
        #self.opcionesEstadoInicial = ["Ninguno"]
        self.opcionSeleccionadaEstadoInicial = StringVar(self.frame)
        self.opcionSeleccionadaEstadoInicial.set("Ninguno")  # Opción predeterminada
           
        self.inputEstadoInicial = OptionMenu(frame, self.opcionSeleccionadaEstadoInicial, *self.opcionesDeEstadosInicialFinal, command=self.on_envent_seleccion_estado_Inicial)
        self.inputEstadoInicial.pack(side="left", padx=10, pady=5)
        
        #-------
        self.lblEstadoFinal = Label(frame,text="Estado final: ")
        self.lblEstadoFinal.pack(side="left", padx=15, pady=5)
        
        
        #self.opcionesEstadoFinal = ["Ninguno","Ninguno2"]
        self.opcionSeleccionadaEstadoFinal = StringVar(self.frame)
        self.opcionSeleccionadaEstadoFinal.set("Ninguno")  # Opción predeterminada
        
        self.inputEstadoFinal = OptionMenu(frame, self.opcionSeleccionadaEstadoFinal, *self.opcionesDeEstadosInicialFinal, command=self.on_envent_seleccion_estado_Final)
        self.inputEstadoFinal.pack(side="left", padx=10, pady=5)
        
    def seccionSeleccionAlgH(self,raiz):
        
        algBusquedaOpciones = ["Escalada simple", "Maxima pendiente"]
        
        self.opcion_seleccionadaAlg = StringVar(self.frame)
        self.opcion_seleccionadaAlg.set(algBusquedaOpciones[0])
        
        
        self.lblEstadoFinal = Label(self.frame,text="Algoritmo de busqueda: ")
        self.lblEstadoFinal.place(x=100,y=570)
        
        self.inputEstadoFinal = OptionMenu(self.frame, self.opcion_seleccionadaAlg, *algBusquedaOpciones)
        self.inputEstadoFinal.place(x=100,y=590)
        
        funcHeuristicaOpciones = ["Linea recta", "Manhattan"]
        
        self.opcion_seleccionadaFH = StringVar(self.frame)
        self.opcion_seleccionadaFH.set(funcHeuristicaOpciones[0])
        
        self.lblEstadoFinal = Label(self.frame,text="Funcion heuristica: ")
        self.lblEstadoFinal.place(x=290,y=570)
        
        self.inputEstadoFinal = OptionMenu(self.frame, self.opcion_seleccionadaFH, *funcHeuristicaOpciones)
        self.inputEstadoFinal.place(x=290,y=590)
        
        barra4 = Label(self.frame, text="____________________________________________________________________________________________________")
        barra4.place(x=0,y=620)
        
        self.btnResolver = Button(self.frame, text="Ejecutar algoritmo", command = self.on_click_ejecutar_algoritmo)
        self.btnResolver.place(x=185,y=655)
           
    def seccionResultado(self, raiz):
        self.lblTitleResult = Label(self.frame,text="Resultado",font=(18))
        self.lblTitleResult.place(x=500/2.6,y=705)
        
        #self.lblEstadoFinal = Label(self.frame,text="Tiempo de resolucion: ")
        #self.lblEstadoFinal.place(x=20,y=735)

        self.btnEstadisticas = Button(self.frame, text="Ver estadisticas", command = self.on_click_crear_estados)
        self.btnEstadisticas.place(x=30,y=750)
        
        self.btnTerminar = Button(self.frame, text="Grafo completo", command = self.on_click_grafo_completo)
        self.btnTerminar.place(x=350,y=750)
        
        self.btnPasoSiguiente = Button(self.frame, text="Siguinte paso", command = self.on_click_soguiente_paso)
        self.btnPasoSiguiente.place(x=240,y=750)
        
        self.btnPasoAnterior = Button(self.frame, text="Paso anterior", command = self.on_click_aterior_paso)
        self.btnPasoAnterior.place(x=140,y=750)

    def on_click_soguiente_paso(self):
        self.clearFramesPartiendoIndice(self.raiz, 2)
        if not self.pasoActual >= len(self.pasosAlgSeleccionado)-1:
            self.pasoActual = self.pasoActual + 1

        self.pintarGrafoConId(self.pasosAlgSeleccionado[self.pasoActual])
        self.G.resaltarEstadoInicialFinal(self.pasosAlgSeleccionado[self.pasoActual], self.estadoInicial["name"], self.estadoFinal["name"]) 

    def on_click_grafo_completo(self):
        self.clearFramesPartiendoIndice(self.raiz, 2)
        ultimoPaso = len(self.pasosAlgSeleccionado)-1
        self.pasoActual = ultimoPaso 

        grafo = self.pasosAlgSeleccionado[ultimoPaso]

        self.pintarGrafoConId(grafo)
        result = self.G.resaltarEstadoInicialFinal(grafo, self.estadoInicial["name"], self.estadoFinal["name"])
        
        #minimoLocal = {}
        #if not result["final"]:
            #for nodo in grafo:
                


    def on_click_aterior_paso(self):
        self.clearFramesPartiendoIndice(self.raiz, 2)
        if self.pasoActual > 0:
            self.pasoActual = self.pasoActual - 1

        self.pintarGrafoConId(self.pasosAlgSeleccionado[self.pasoActual])
        self.G.resaltarEstadoInicialFinal(self.pasosAlgSeleccionado[self.pasoActual], self.estadoInicial["name"], self.estadoFinal["name"]) 

    # Función para manejar la selección del menú desplegable
    def on_envent_seleccion_estado_Inicial(self, opcion):
        
        if len(self.estadoInicial["name"]) > 0:
            self.G.resaltar_estado(self.estadoInicial["name"], "skyblue")
            
        self.G.resaltar_estado(opcion)
        self.estadoInicial = self.busquedaNodoEnGrafo(opcion)
        print("Opción seleccionada:", opcion)  
    
    def busquedaNodoEnGrafo(self, nombreNodo):
        for nodo in self.grafo:
            if nodo["name"] == nombreNodo:
                return nodo

    def on_envent_seleccion_estado_Final(self, opcion):
        
        if len(self.estadoFinal["name"]) > 0:
            self.G.resaltar_estado(self.estadoFinal["name"], "skyblue")
            
        self.G.resaltar_estado(opcion, "red")
        self.estadoFinal = self.busquedaNodoEnGrafo(opcion)
        print("Opción seleccionada:", opcion)  
    
    def on_click_ejecutar_algoritmo(self):
        if not( len(self.estadoFinal["name"]) > 0 and len(self.estadoInicial["name"]) > 0 ):
            messagebox.showinfo("Advertencia","Debe seleccionar el estado inicial y final para ejecutar el algoritmo especificado")
            return
        
        if self.opcion_seleccionadaFH.get() == "Manhattan":
            tablaH = algBusquedaHeuristica.heuristicaManhattan(self.grafo, self.estadoFinal)
            messagebox.showinfo("Heuristica de cada nodo", tablaH)
        else:
            tablaH = algBusquedaHeuristica.heuristicaLineaRecta(self.grafo, self.estadoFinal)
            messagebox.showinfo("Heuristica de cada nodo", tablaH)
     
        if self.opcion_seleccionadaAlg.get() == "Escalada simple":
            grafo = algBusquedaHeuristica.algEscaladaSimple(tablaH, self.grafo, self.estadoInicial)
            self.pasosAlgSeleccionado = self.obtenerPasosAlgEscaladaSimple(copy.deepcopy(grafo))
        else:
            grafo = algBusquedaHeuristica.algMaximaPendiente(tablaH, self.grafo, self.estadoInicial)
            self.pasosAlgSeleccionado = self.obtenerPasosAlgMaximaPendiente(copy.deepcopy(grafo))

        self.clearFramesPartiendoIndice(self.raiz, 2)
        # Estadisticas:
        # (1)canidad de niveles al recorrer nodos y ver que cambia PosY
        # (2)Cantidad de pasos = longitud del array pasosAlgSeleccionado
        # (3)cantidad de nodos recorridos al objetivo = cantidad de nodos objetos en resultado alg = grafo
        # (4)Verificar si en el grafo obtenido del algoritmo heuristico, se encuentra el nodo objeto final => SI
        # De no encontrarse => el nodo del grafo con menor costo
        # (5) tiempo en ms de cada uno
        # ----------
        # Botono ver tabla heurisitica
        self.pasoActual = 0
        self.pintarGrafoConId(self.pasosAlgSeleccionado[self.pasoActual])
        self.G.resaltarEstadoInicialFinal(self.pasosAlgSeleccionado[self.pasoActual], self.estadoInicial["name"], self.estadoFinal["name"])

    def obtenerPasosAlgMaximaPendiente(self, grafo):
        pasosGrafos = []
        grafoCompleto = []
        indiceEstado = 0

        grafoCompleto.append(copy.deepcopy( grafo["grafoResultante"][indiceEstado] ))
        posX = (len(grafoCompleto[0]["aristas"]) / 2) * 5

        grafoCompleto[0]["aristas"] = []
        grafoCompleto[0]["posicion"] = {"x":posX,"y":0}
        grafoCompleto[0]["id"] = 1

        pasosGrafos.append(copy.deepcopy(grafoCompleto))

        idEstados = 2 # Utilizado para distigir entre estados con el mismo nombre a la hora de pintar
        posY = 0
        indiceNodoActualCaminoSolucion = 0
        indiceNodoSiguienteCS = None

        while True:
             
            nodoCaminoSolucion = {}
            posY = posY - 40
            control = True

            for indice, arista in enumerate(grafo["grafoResultante"][indiceEstado]["aristas"]):

                control = self.contolRedundanciaMismaRama(indiceEstado, arista ,grafo["grafoResultante"])
        
                if len(grafo["grafoResultante"]) > indiceEstado + 1:
                    
                    if arista == grafo["grafoResultante"][indiceEstado + 1]["name"]:
                        nodoCaminoSolucion = {"id": idEstados,"name": arista, "posicion":{"x": indice*8 ,"y": posY}, "aristas":[]}
                        indiceNodoSiguienteCS = len(grafoCompleto)
                        grafoCompleto.append(copy.deepcopy(nodoCaminoSolucion)) 
                        control = False
                        grafoCompleto[indiceNodoActualCaminoSolucion]["aristas"].append(copy.deepcopy(idEstados))
                        idEstados = idEstados + 1

                if control: 
                    nodo = {"id": idEstados,"name": arista, "posicion":{"x": indice*8 ,"y": posY}, "aristas":[]}
                    grafoCompleto.append(copy.deepcopy(nodo))
                    grafoCompleto[indiceNodoActualCaminoSolucion]["aristas"].append(copy.deepcopy(idEstados))
                    idEstados = idEstados + 1

                pasosGrafos.append(copy.deepcopy(grafoCompleto))
                control = True

            indiceNodoActualCaminoSolucion = indiceNodoSiguienteCS
            indiceEstado = indiceEstado + 1
           
            if indiceEstado > len(grafo["grafoResultante"])-1:
                break
    
        return pasosGrafos

    def contolRedundanciaMismaRama(self, indiceEstadoActual, arista, grafo):
        indiceControlRama = 0
        while True:
            if not indiceControlRama < indiceEstadoActual:
                break

            print("IndiceEstado:", indiceEstadoActual, " Indice control rama: ", indiceControlRama)
            if arista == grafo[indiceControlRama]["name"]:
                return False
                        
            indiceControlRama  = indiceControlRama + 1
        return True

    def obtenerPasosAlgEscaladaSimple(self, grafo_):
        pasosGrafos = []
        grafoInterpretado = self.eliminarAristasNoExploradas(grafo_)["grafoResultante"]
        grafo = []

        indiceEstado = 0

        grafo.append(copy.deepcopy(grafoInterpretado[indiceEstado]))
        grafo[0]["aristas"] = []
        grafo[0]["posicion"] = {"x":20,"y":0}
        grafo[0]["id"] = 1
        pasosGrafos.append(copy.deepcopy(grafo))
        indiceG = 0

        idEstados = 2

        while True:
            
            aristasExploradas = [] 
            posNodoPadre = grafo[indiceG]["posicion"]
            for indice, arista in enumerate(grafoInterpretado[indiceEstado]["aristas"]):
                nodo = {"id":idEstados,"name": arista, "posicion":{"x": posNodoPadre["x"] + 2*indice ,"y": posNodoPadre["y"] - 10}, "aristas":[]}
                # Si hay mas aristas para este nodo => esta arista/ nuevo nodo esta cerrado
                #print("ARISTA : ", arista)
                aristasExploradas.append(idEstados)
                grafo[indiceG]["aristas"] = aristasExploradas
                grafo.append(nodo)
                pasosGrafos.append(copy.deepcopy(grafo))
                idEstados = idEstados + 1
            
            #print(grafo)

            indiceG = len(grafo)-1
            indiceEstado = indiceEstado + 1
            if indiceEstado > len(grafoInterpretado)-1:
                break
        
        return pasosGrafos

    # Solo aplica para resultado de algoritmo escalada simple   
    def eliminarAristasNoExploradas(self, grafo):
        for indice, estado in enumerate( grafo["grafoResultante"] ):
            i = 0
            while True:
                if i < indice:
                    if grafo["grafoResultante"][i]["name"] in estado["aristas"]:
                        estado["aristas"].remove(grafo["grafoResultante"][i]["name"])
                else:
                    break

                i = i + 1
            
            if len(grafo["grafoResultante"]) > indice + 1:
                estadosExplorados = []
                for arista in estado["aristas"]:
                    if grafo["grafoResultante"][indice + 1]["name"] == arista:
                        estadosExplorados.append(arista)
                        break

                    estadosExplorados.append(arista)  
                
                grafo["grafoResultante"][indice]["aristas"] = estadosExplorados

        return grafo    

    def on_window_resize(self, event):
        self.titulo.place(x=event.width/3.5,y=20)
     
    def on_click_carga_datos_grafo_automatico(self):
        # Cambiar texto de boton de carga a cargando..
        grafo_and_posiciones = self.generar_grafo_automatico()

        for i, fila in enumerate(self.frameEstados.scrollable_frame.winfo_children()): # Lee los hijos del frame scroll

            #entry.delete(0, END)  # Eliminar cualquier texto existente
            fila.winfo_children()[1].delete(0, END)
            fila.winfo_children()[2].delete(0, END)
            fila.winfo_children()[3].delete(0, END)
            fila.winfo_children()[4].delete(0, END)

            name = fila.winfo_children()[1].insert(0, grafo_and_posiciones["grafo"][i]["name"])
            posX = fila.winfo_children()[2].insert(0, int( grafo_and_posiciones["pos"][i][0] ))
            posY = fila.winfo_children()[3].insert(0, int( grafo_and_posiciones["pos"][i][1] ))

            letras = grafo_and_posiciones["grafo"][i]["aristas"]
           
            formato_conexiones = ",".join(letras)

            conexiones = fila.winfo_children()[4].insert(0, formato_conexiones)

        # Restablecer el nombre original del boton de carga una ves terminado la carga 

    def generar_grafo_automatico(self):
        # m >= 1 and m < n, m = 5, n = 5
        N = len( self.frameEstados.scrollable_frame.winfo_children() )
        M = random.randint(1, 4)
        G = nx.barabasi_albert_graph(N, M) # Grafo Barabasi-Albert con N nodos y M conexiones por cada nuevo nodo

        if N > 27:
            letras = list(string.ascii_uppercase[:N] + string.ascii_lowercase[: N-26 ])
        else:
            letras = list(string.ascii_uppercase[:N]) # Generacion de lista de letras para los nuevos nodos

        mapeo = {i: letras[i] for i in range(N)} #mapeo de números a letras  -->  {0:"A", ... }
        # Convertir las aristas de números a letras usando el mapeo
        edges_letras = [(mapeo[u], mapeo[v]) for u, v in G.edges()] # [(0, 1), (0, 2), (0, 3)]  -->   [('A', 'B'), ('A', 'C'), ('A', 'D')]
        posiciones = nx.spring_layout(G)
        pos = []
        for nodo, posicion in posiciones.items():
            pos.append( posicion * 100 )
        
        # apunte : Renombrar los nodos del grafo utilizando el mapeo
        # G_letras = nx.relabel_nodes(G, mapeo)

        grafo = []
        for edge in edges_letras:
            nodo1, nodo2 = edge
            indice = self.buscar_nodo_por_nombre(nodo1, grafo)
            if indice != -1 :
                grafo[indice]["aristas"].append(nodo2)
            else:
               grafo.append({"name": nodo1, "aristas": [nodo2]}) 

            indice = self.buscar_nodo_por_nombre(nodo2, grafo)        
            if indice != -1:
                grafo[indice]["aristas"].append(nodo1)
            else:
               grafo.append({"name": nodo2, "aristas": [nodo1]})

        return {"grafo":grafo, "pos": pos}

    def buscar_nodo_por_nombre(self, nombre, lista):
        for indice, nodo in enumerate(lista):
            if nodo['name'] == nombre:
                return indice
        return -1    

    def buscar_ultimo_nodo_por_nombre(self, nombre, lista):
        result = None
        for indice, nodo in enumerate(lista):
            if nodo['name'] == nombre:
                result = indice
        return result 

    # ---------- Modulos de control de datos de entrada --------------
    
    def verificar_numero(self, valor):
        try:
            numero = float(valor)
            return True
        except ValueError:
            messagebox.showwarning("Advertencia", f"'{valor}' no es un número válido.")
            return False
    
    def es_letra_sola(self, valor):
        
        result = isinstance(valor, str) and len(valor) == 1 and valor.isalpha()
        #if not result:
        #    messagebox.showwarning("Advertencia", f"'{valor}'. Debe ser una letra unica (Ej : A)")
            
        return result
        #isinstance(letra, str): Verifica que el valor proporcionado sea una cadena.
        #len(letra) == 1: Verifica que la longitud de la cadena sea exactamente 1, asegurando que se trata de un solo carácter.
        #letra.isalpha(): Verifica que el carácter sea una letra del alfabeto.         
    
    def verificarFormatoConexiones(self, conexiones):
        # letra.upper() # --> Convierte una letra a su versión mayúscula
        #elementos = valores.split(',') # => input: valores = "a, b, c, 1, d, e, ab, f" output : ['a', 'b', 'c', '1', 'd', 'e', 'ab','f']
        # Controlar con es_letra_sola()
        valores = conexiones.split(',')
        for valor in valores:
            if not (self.es_letra_sola(valor)):
                messagebox.showwarning("Advertencia", f"' La conexion: {valor}'. Debe ser una letra unica (Ej : A)")
                return False
        
        return True
          
    # ----------------------------------------------------------------          
            
    def on_click_crear_estados(self):
        
        estados_crear_input = self.inputNroEstados.get()
        
        if not (self.verificar_numero( estados_crear_input )) :
            return
        
        if float(estados_crear_input) > 26:
            messagebox.showwarning("Advertencia", f"' Cantidad maxima de nodos posibles: 26 !!")
            return

        estadosCreados = self.frameEstados.scrollable_frame.winfo_children()
        if len(estadosCreados) > 0:
            self.clearElementsOfFrame(self.frameEstados.scrollable_frame)
         
        self.btnCargaAleatoriaEstados.config(state="normal")

        self.entradas_nombres_conexiones = []    

        cantidadNodos = 0    
        while True:  
            cantidadNodos = cantidadNodos + 1
            
            # Fila
            frame = Frame(self.frameEstados.scrollable_frame)
            frame.config(width=500, height=30) #bg="lightblue"
            frame.pack(fill="both", expand=True)
           

            entrada = {"fila": cantidadNodos, "name":StringVar(), "conexiones": StringVar()}
            self.entradas_nombres_conexiones.append(entrada)

            # columnas
            Label(frame , text = cantidadNodos).place(x=15 , y=0) #nroEstado
            entradaName = Entry(frame, width=15, textvariable=entrada["name"]).place(x= 80, y=0) #name

            entrada["name"].trace_add("write", lambda *args: self.convertir_mayusculas(cantidadNodos-1, "name", *args))

            entradaPosX = Entry(frame, width=4).place(x= 220, y=0) #posX
            entradaPosY = Entry(frame, width=4).place(x= 250, y=0) #posY
            entradaConexiones = Entry(frame, width=17, textvariable=entrada["conexiones"]).place(x= 340, y=0) #conexiones
            entrada["conexiones"].trace_add("write", lambda *args: self.convertir_mayusculas(cantidadNodos-1, "conexiones", *args))
          
            if (cantidadNodos + 1) > float(estados_crear_input):
                break

    def convertir_mayusculas(self, *args):
        tipo_entrada = args[1]
        fila = args[0]
        if tipo_entrada == "name":
            name = self.entradas_nombres_conexiones[fila]["name"].get()
            self.entradas_nombres_conexiones[fila]["name"].set(name.upper())
        
        if tipo_entrada == "conexiones":
            name = self.entradas_nombres_conexiones[fila]["conexiones"].get()
            self.entradas_nombres_conexiones[fila]["conexiones"].set(name.upper())

    def leer_grafo_cargado(self):
        self.grafo = []
        # apunte: lectura de valores de elementos del frame (estados)
        for fila in self.frameEstados.scrollable_frame.winfo_children(): # Lee los hijos del frame scroll
            #print("--->",fila.winfo_children()[1].get()) # frame fila = [Label, entry, entry, entry, entry]
            #for columna in fila.winfo_children(): # Lee los hijos del frame fila que se encuntra en el padre frame scroll
            #    if isinstance(columna, Entry):
            #        print(columna.get())
            name = fila.winfo_children()[1].get()
            posX = fila.winfo_children()[2].get()
            posY = fila.winfo_children()[3].get()
            conexiones = fila.winfo_children()[4].get()
            
            if not self.es_letra_sola(name):
                messagebox.showwarning("Advertencia", f"'{name}'. Debe ser una letra unica (Ej : A)")
                return
            if not ( self.verificar_numero(posX) and self.verificar_numero(posY) ):
                return
            if not (self.verificarFormatoConexiones(conexiones) ):
                return
            
            self.grafo.append({"name":name,"posicion":{"x":float(posX),"y":float(posY)}, "aristas": conexiones.split(',')})

    def on_click_cargar_grafo(self):
        # lee las entradasm crea la estrucutra grafo en la variable grafo global de esta clase   
        self.leer_grafo_cargado() 

        self.clearFramesPartiendoIndice(self.raiz, 1)
        #print("\n\nGrafo cargado: ", self.grafo,"\n")
        try:
            self.pintarGrafo(self.grafo)
        except Exception as e:
            messagebox.showwarning("Advertencia", f"'{e}': Verifique conexiones a nodos inexsistentes")
    
        self.actualizarOpcionesEstadosInicialFinal(self.grafo)    
     
    def actualizarOpcionesEstadosInicialFinal(self, grafo):
        opciones = []
        
        for nodo in grafo:
            opciones.append(nodo["name"])
        
        for elemento in self.frameOptionMenuInputEstadosInicialFinal.winfo_children():
            elemento.destroy()

        self.seccionSeleccionEstadoInicialFinal(self.frameOptionMenuInputEstadosInicialFinal, opciones)

    def pintarGrafoConId(self, grafo):
        pos = {}
        conexiones = []
        nodos = []

        for nodo in grafo:
            for arista in nodo["aristas"]:
                #indice = self.buscar_ultimo_nodo_por_nombre(arita, grafo)
                conexiones.append((nodo["id"], arista))
                
            pos[nodo["id"]] = ( float( nodo["posicion"]["x"] ), float( nodo["posicion"]["y"] ) )
            nodos.append(nodo)
        
        print(pos, nodos)
        self.G = interfazGrafo(self.raiz)
        self.G.dibujar_grafo_por_id(nodos, conexiones, pos, "Grafo resultante")

    def pintarGrafo(self, grafo):
        #cantidadNodos = len(grafo)
        pos = {}
        conexiones = []
        nodos = []
        print("-->",grafo)
        for nodo in grafo:
            for arita in nodo["aristas"]:
                conexiones.append((nodo["name"],arita))
                
            pos[nodo["name"]] = ( float( nodo["posicion"]["x"] ), float( nodo["posicion"]["y"] ) )
            nodos.append(nodo["name"])
        
        self.G = interfazGrafo(self.raiz)
        self.G.dibujar_grafo(nodos, conexiones, pos)
               
    def clearFramesPartiendoIndice(self, frame ,index):
        countFrames = 0
        for widget in frame.winfo_children():
            if isinstance(widget, Frame):
                countFrames = countFrames + 1
            if(countFrames > index):
                widget.destroy()     
            
    def clearElementsOfFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        
class interfazGrafo:
    def __init__(self, raiz):
        self.raiz = raiz
        self.frame = Frame(self.raiz)
        self.frame.pack(side="top" , fill=BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        #self.dibujar_grafo()

    def dibujar_grafo_por_id(self, nodos, conexiones, posiciones, titulo):
       
        self.G = nx.Graph()
        
        self.nodos = nodos
        self.conexiones = conexiones
        self.pos = posiciones

        for nodo in nodos:
            self.G.add_node(nodo["id"], label=nodo["name"]) 

        #self.G.add_nodes_from(nodos)
        self.G.add_edges_from(conexiones)
    
        nx.draw_networkx_nodes(self.G, pos=self.pos, node_size=300, node_color='skyblue',label=True)
        #nx.draw_networkx_labels(self.G, pos=self.pos, font_size=10, font_family='sans-serif')

        labels = nx.get_node_attributes(self.G, 'label')
        nx.draw_networkx_labels(self.G, pos=self.pos, labels=labels, font_size=10, font_family='sans-serif')

        
        nx.draw_networkx_edges(self.G, pos=self.pos, width=2)
      
        self.ax.margins(0.2)
        self.ax.set_title(titulo)
        self.canvas.draw()

    def dibujar_grafo(self, nodos, conexiones, posiciones):
        self.G = nx.Graph()
        
        print(nodos,"  -------------- ", conexiones, " ----------------- ", posiciones)

        self.nodos = nodos
        self.conexiones = conexiones
        self.pos = posiciones
        
        self.G.add_nodes_from(nodos)
        self.G.add_edges_from(conexiones)
        
        #self.G.add_nodes_from(["A", "B", "C", "D", "E"])
        #self.G.add_edges_from([("A", "B"),("B", "A"), ("A", "C"), ("B", "D"), ("B", "E")])
        #pos = {"A":(-10,50),}
        
        nx.draw_networkx_nodes(self.G, pos=self.pos, node_size=500, node_color='skyblue')
        nx.draw_networkx_labels(self.G, pos=self.pos, font_size=10, font_family='sans-serif')
        
        nx.draw_networkx_edges(self.G, pos=self.pos, width=2)
      
        self.ax.margins(0.2)
        self.ax.set_title('Grafo:')
        self.canvas.draw()

    def resaltar_estado(self, nameEstado, color="green", tamaño=500):
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=[nameEstado], node_color=color, node_size=tamaño)
        #nx.draw_networkx_nodes(self.G, self.pos, nodelist=[nameEstadoFinal], node_color='red', node_size=500)
        self.canvas.draw()


     #def resaltarEstadosCerrados():

    def limpiar():
        plt.cla()

    def resaltarEstadoInicialFinal(self, grafo, estadoInicial, estadoFinal):
        inicialPintado = False
        finalPintado = False
        print("GRAFO: ", self.G)
        for nodo in grafo:
            if nodo["name"] == estadoInicial:
                self.resaltar_estado(color="green",nameEstado=nodo["id"])
                inicialPintado = True

            if nodo["name"] == estadoFinal:
                self.resaltar_estado(color="red",nameEstado=nodo["id"])
                finalPintado = True

        return {"inicial": inicialPintado, "final": finalPintado}


    def dibujar_heurisitca_cada_nodo(self, tablaH):
        # Añadir etiquetas adicionales
        labels = {
            "A": "H = 68",
            "B": "H = 20",
            "C": "H = 24",
            "D": "H = 14",
            "E": "H = 2"
        }
        
        #for node, (x, y) in self.pos.items():
        #    self.ax.annotate(labels[node], (x, y), textcoords="offset points", xytext=(30, -5), ha='center')

def main():
    raiz = Tk()
    raiz.title("Espacio de Búsqueda")
    raiz.resizable(False,False) # Si se permitira redimencionar el tamaño en alto y ancho
    raiz.geometry("1080x900") # Ancho y alto de la ventana => Se especifica esta propiedad a los Frame para que el raiz se adapte a los mismos
    
    interfazCargaDeGrafo(raiz)
    #interfazGrafoResultante(raiz)
    #interfazGrafo(raiz)
    
    algBusquedaHeuristica.test()
    
    raiz.mainloop()


if __name__ == "__main__":
    main()


def generar_grafo_barabasi_albert(n, m):
    G = nx.barabasi_albert_graph(n, m)
    nx.draw(G, with_labels=True)
    plt.show()
    return G



