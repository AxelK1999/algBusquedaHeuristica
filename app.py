from tkinter import *
import networkx as nx
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import algBusquedaHeuristica
import random
import string
import copy


class EspacioBusqueda:
    def __init__(self):
        self.estados = ["A", "B", "C", "D", "E", "F", "G"]
        self.conexiones = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("D", "G"), ("E", "G"),
                           ("F", "G")]
        self.estado_inicial = "A"
        self.estado_final = "G"

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
        print(dir(self.inputEstadoFinal))
        
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
        
        self.btnTerminar = Button(self.frame, text="Grafo completo", command = self.on_click_crear_estados)
        self.btnTerminar.place(x=350,y=750)
        
        self.btnPasoSiguiente = Button(self.frame, text="Siguinte paso", command = self.on_click_crear_estados)
        self.btnPasoSiguiente.place(x=240,y=750)
        
        self.btnPasoAnterior = Button(self.frame, text="Paso anterior", command = self.on_click_crear_estados)
        self.btnPasoAnterior.place(x=140,y=750)
        
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
            print("Manhattan")
        else:
            tablaH = algBusquedaHeuristica.heuristicaLineaRecta(self.grafo, self.estadoFinal)
            messagebox.showinfo("Heuristica de cada nodo", tablaH)
            print("Linea recta")
     
        if self.opcion_seleccionadaAlg.get() == "Escalada simple":
            grafo = algBusquedaHeuristica.algEscaladaSimple(tablaH, self.grafo, self.estadoInicial)
            self.pasosAlgSeleccionado = self.obtenerPasosAlgEscaladaSimple(copy.deepcopy(grafo))
            print("Escalada simple")
        else:
            grafo = algBusquedaHeuristica.algEscaladaSimple(tablaH, self.grafo, self.estadoInicial)
            self.pasosAlgSeleccionado = self.obtenerPasosAlgMaximaPendiente(copy.deepcopy(grafo))
            print("Maxima pendiente")

        print("----------------------------------------")
        for paso in self.pasosAlgSeleccionado:
            print("--> ", paso)
        print("----------------------------------------")
        #print("\n\n GRAFOS PASOS: ", self.obtenerPasosAlg(self.eliminarAristasNoExploradas(grafo)),"\n\n")
        self.pintarGrafo(self.pasosAlgSeleccionado[len(self.pasosAlgSeleccionado)-1])
        #self.pintarGrafo(self.eliminarAristasNoExploradas(grafo)["grafoResultante"])
        #messagebox.showinfo("Grafo resultante", self.eliminarAristasNoExploradas(grafo))

    def obtenerPasosAlgMaximaPendiente(self, grafo):
        pasosGrafos = []
        grafoCompleto = []
        
        indiceEstado = 0

        grafoCompleto.append(copy.deepcopy( grafo["grafoResultante"][indiceEstado] ))
        grafoCompleto[0]["aristas"] = []
        grafoCompleto[0]["posicion"] = {"x":20,"y":0}
        grafoCompleto[0]["id"] = 1

        pasosGrafos.append(copy.deepcopy(grafoCompleto))

        idEstados = 2 # Utilizado para distigir entre estados con el mismo nombre a la hora de pintar

        posY = 0
        posX = 20

        indiceNodoActualCaminoSolucion = 0
        indiceNodoSiguienteCS = None
        while True:
             
            nodoCaminoSolucion = {}
            posY = posY - 5

            for indice ,arista in enumerate(grafo["grafoResultante"][indiceEstado]["aristas"]):
                
                if arista == grafo["grafoResultante"][indiceEstado + 1]["name"]:
                    nodoCaminoSolucion = {"id": idEstados,"name": arista, "posicion":{"x": posX + 2*indice ,"y": posY}, "aristas":[]}
                    indiceNodoSiguienteCS = len(grafoCompleto)
                    grafoCompleto.append(copy.deepcopy(nodoCaminoSolucion))
                    print("SE ACTUALIZO POS X")
                else: 
                    nodo = {"id": idEstados,"name": arista, "posicion":{"x": posX + 2*indice ,"y": posY}, "aristas":[]}
                    grafoCompleto.append(copy.deepcopy(nodo))

                grafoCompleto[indiceNodoActualCaminoSolucion]["aristas"].append(copy.deepcopy(arista))
                pasosGrafos.append(copy.deepcopy(grafoCompleto))

            indiceNodoActualCaminoSolucion = indiceNodoSiguienteCS
            #pasosGrafos.append(grafoCompleto)
            if nodoCaminoSolucion:
                posX = nodoCaminoSolucion["posicion"]["x"]

            idEstados = idEstados + 1
            indiceEstado = indiceEstado + 1

            print("indice: ", indiceEstado," Cantidad de estados: ",len(grafo["grafoResultante"])-1, "Grafo: ",grafo["grafoResultante"])
            if indiceEstado > len(grafo["grafoResultante"])-1:
                break
        
        #print("Grafo resultatne de Maxima pendiente : ", pasosGrafos[ len(grafo["grafoResultante"])-1 ] )
        return pasosGrafos


    def obtenerPasosAlgEscaladaSimple(self, grafo_):
        pasosGrafos = []
        grafoInterpretado = self.eliminarAristasNoExploradas(grafo_)["grafoResultante"]
        grafo = []

        indiceEstado = 0

        grafo.append(copy.deepcopy(grafoInterpretado[indiceEstado]))
        grafo[0]["aristas"] = []
        grafo[0]["posicion"] = {"x":20,"y":0}

        pasosGrafos.append(copy.deepcopy(grafo))
        indiceG = 0
        while True:
            
            aristasExploradas = [] 
            posNodoPadre = grafo[indiceG]["posicion"]
            for indice, arista in enumerate(grafoInterpretado[indiceEstado]["aristas"]):
                nodo = {"name": arista, "posicion":{"x": posNodoPadre["x"] + 2*indice ,"y": posNodoPadre["y"] - 10}, "aristas":[]}
                # Si hay mas aristas para este nodo => esta arista/ nuevo nodo esta cerrado
                print("ARISTA : ", arista)
                aristasExploradas.append(arista)
                grafo[indiceG]["aristas"] = aristasExploradas
                grafo.append(nodo)
                pasosGrafos.append(copy.deepcopy(grafo))
            
            print(grafo)

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
        print("Grafo con nodos no explorados eliminados: ", grafo)
        return grafo    

    def on_window_resize(self, event):
        self.titulo.place(x=event.width/3.5,y=20)
     
    def on_click_carga_datos_grafo_automatico(self):
        # Cambiar texto de boton de carga a cargando..
        grafo_and_posiciones = self.generar_grafo_automatico()
        print("Grafo generado de forma automatica :  ", grafo_and_posiciones)

        print(grafo_and_posiciones["grafo"][0]["name"])
        print(grafo_and_posiciones["grafo"][0]["aristas"])

        for i, fila in enumerate(self.frameEstados.scrollable_frame.winfo_children()): # Lee los hijos del frame scroll

            print("INDICE : ", i)
            #entry.delete(0, END)  # Eliminar cualquier texto existente
            fila.winfo_children()[1].delete(0, END)
            fila.winfo_children()[2].delete(0, END)
            fila.winfo_children()[3].delete(0, END)
            fila.winfo_children()[4].delete(0, END)

            name = fila.winfo_children()[1].insert(0, grafo_and_posiciones["grafo"][i]["name"])
            posX = fila.winfo_children()[2].insert(0, int( grafo_and_posiciones["pos"][i][0] ))
            posY = fila.winfo_children()[3].insert(0, int( grafo_and_posiciones["pos"][i][1] ))

            letras = grafo_and_posiciones["grafo"][i]["aristas"]
            print(letras)
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

        print(letras)    
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

            print(nodo2)
            indice = self.buscar_nodo_por_nombre(nodo2, grafo)        
            if indice != -1:
                grafo[indice]["aristas"].append(nodo1)
            else:
               grafo.append({"name": nodo2, "aristas": [nodo1]})

        return {"grafo":grafo, "pos": pos}

    def buscar_nodo_por_nombre(self, nombre, lista):
        for indice, nodo in enumerate(lista):
            print(indice, nodo)
            if nodo['name'] == nombre:
                return indice
        return -1    
                 
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
         
    def pintarGrafo(self, grafo):
        #cantidadNodos = len(grafo)
        pos = {}
        conexiones = []
        nodos = []
        
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

        
class interfazGrafoResultante:
    def __init__(self, raiz):
        self.raiz = raiz
        self.espacio_busqueda = EspacioBusqueda()

        self.frame = Frame(self.raiz)
        self.frame.pack(side="bottom",fill=BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.dibujar_grafo()

    def dibujar_grafo(self):
        G = nx.Graph()
        G.add_nodes_from(self.espacio_busqueda.estados)
        G.add_edges_from(self.espacio_busqueda.conexiones)

        pos = nx.spring_layout(G)  # Algoritmo de disposición de nodos
        print(pos)
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

        # Resaltar estado inicial y final
        nx.draw_networkx_nodes(G, pos, nodelist=[self.espacio_busqueda.estado_inicial],
                               node_color='green', node_size=700)
        nx.draw_networkx_nodes(G, pos, nodelist=[self.espacio_busqueda.estado_final],
                               node_color='red', node_size=700)

        self.ax.set_title('Grafo resultante: ')
        self.canvas.draw()

class interfazGrafo:
    def __init__(self, raiz):
        self.raiz = raiz
        self.espacio_busqueda = EspacioBusqueda()

        self.frame = Frame(self.raiz)
        self.frame.pack(side="top" , fill=BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        #self.dibujar_grafo()

    def dibujar_grafo(self, nodos, conexiones, posiciones):
        self.G = nx.Graph()
        
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
        print("===>",self.pos)
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=[nameEstado], node_color=color, node_size=tamaño)
        #nx.draw_networkx_nodes(self.G, self.pos, nodelist=[nameEstadoFinal], node_color='red', node_size=500)
        self.canvas.draw()

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
    raiz.geometry("1080x800") # Alto y ancho de la ventana => Se especifica esta propiedad a los Frame para que el raiz se adapte a los mismos
    
    interfazCargaDeGrafo(raiz)
    #interfazGrafoResultante(raiz)
    #interfazGrafo(raiz)
    
    algBusquedaHeuristica.test()
    
    raiz.mainloop()


if __name__ == "__main__":
    main()




""" 
Pendientes: 
   on_click_cargar_grafo():
        (1) Control de datos de entrada(LISTO)
        (2) Cargar nombre de nodos en deplegables de opciones de estado inicial y final (LISTO)
        (3) Armado de estructura grafo para algoritmo busuqueda (LISTO)
        (4) Armado de funcion de generado de grafo en pantalla dado la estrucutra anterior(LISTO)
        (5) Carga de datos de forma automatica (LISTO)
    (6) Mover de posicion del boton de carga automatica (LISTO)
    (7) Controlar que opciones de estado inicial y final no sean los mismos (LISTO ->  no requerido)
    (8) Pintar estado inicial y final al ser seleccionados (LISTO)
        # generar array de grafos de pasos
        # alterar posiciones de nodos en grafo para definirlos en forma de arbol
        # pintarGrafo
        # pintar estado inicial y final
        # pintar nodos cerrados
        # pintar heuristica de nodos
        # funcion estadistica (al apretar boton muestre mensaje con columnas de comparacion
        # entre ambos algortimos : nodos explorados, solucion o minimo local encontrado, 
        # tiempo de resolucion, Cantidad de niveles hasta el minimo u objetivo, 
        # indicar color de nodos cerrados )
"""
def generar_grafo_barabasi_albert(n, m):
    G = nx.barabasi_albert_graph(n, m)
    nx.draw(G, with_labels=True)
    plt.show()
    return G



