from tkinter import *
import networkx as nx
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import algBusquedaHeuristica
import random
import string

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

        self.titleTableEstados = Label(self.frame,text="Nro.               Name(M != m)                     Pos.(x,y)                        Conexiones(M != m)          ")
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
        
        opcion_seleccionadaAlg = StringVar(self.frame)
        opcion_seleccionadaAlg.set(algBusquedaOpciones[0])
        
        
        self.lblEstadoFinal = Label(self.frame,text="Algoritmo de busqueda: ")
        self.lblEstadoFinal.place(x=100,y=570)
        
        self.inputEstadoFinal = OptionMenu(self.frame, opcion_seleccionadaAlg, *algBusquedaOpciones)
        self.inputEstadoFinal.place(x=100,y=590)
        
        funcHeuristicaOpciones = ["Linea recta", "Manhattan"]
        
        opcion_seleccionadaFH = StringVar(self.frame)
        opcion_seleccionadaFH.set(funcHeuristicaOpciones[0])
        
        self.lblEstadoFinal = Label(self.frame,text="Funcion heuristica: ")
        self.lblEstadoFinal.place(x=290,y=570)
        
        self.inputEstadoFinal = OptionMenu(self.frame, opcion_seleccionadaFH, *funcHeuristicaOpciones)
        self.inputEstadoFinal.place(x=290,y=590)
        
        barra4 = Label(self.frame, text="____________________________________________________________________________________________________")
        barra4.place(x=0,y=620)
        
        self.btnResolver = Button(self.frame, text="Ejecutar algoritmo", command = self.on_click_ejecutar_algoritmo)
        self.btnResolver.place(x=180,y=650)
           
    def seccionResultado(self, raiz):
        self.lblTitleResult = Label(self.frame,text="Resultado",font=(18))
        self.lblTitleResult.place(x=500/2.8,y=705)
        
        self.lblEstadoFinal = Label(self.frame,text="Tiempo de resolucion: ")
        self.lblEstadoFinal.place(x=20,y=735)
        
        self.btnTerminar = Button(self.frame, text="Grafo completo", command = self.on_click_crear_estados)
        self.btnTerminar.place(x=300,y=765)
        
        self.btnPasoSiguiente = Button(self.frame, text="Siguinte paso", command = self.on_click_crear_estados)
        self.btnPasoSiguiente.place(x=200,y=765)
        
        self.btnPasoAnterior = Button(self.frame, text="Paso anterior", command = self.on_click_crear_estados)
        self.btnPasoAnterior.place(x=100,y=765)
        
    # Función para manejar la selección del menú desplegable
    def on_envent_seleccion_estado_Inicial(self, opcion):
        
        if len(self.estadoInicial["name"]) > 0:
            self.G.resaltar_estado(self.estadoInicial["name"], "skyblue")
            
        self.G.resaltar_estado(opcion)
        self.estadoInicial["name"] = opcion
        print("Opción seleccionada:", opcion)  
    
    def on_envent_seleccion_estado_Final(self, opcion):
        
        if len(self.estadoFinal["name"]) > 0:
            self.G.resaltar_estado(self.estadoFinal["name"], "skyblue")
            
        self.G.resaltar_estado(opcion, "red")
        self.estadoFinal["name"] = opcion
        print("Opción seleccionada:", opcion)  
    
    def on_click_ejecutar_algoritmo(self):
        if len(self.estadoFinal["name"]) > 0 and len(self.estadoInicial["name"]) > 0:
            print("ejecutando algoritmo")
        else:
            messagebox.showinfo("Advertencia","Debe seleccionar el estado inicial y final para ejecutar el algoritmo especificado")
                   
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
            
        cantidadNodos = 0    
        while True:  
            cantidadNodos = cantidadNodos + 1
            
            # Fila
            frame = Frame(self.frameEstados.scrollable_frame)
            frame.config(width=500, height=30) #bg="lightblue"
            frame.pack(fill="both", expand=True)
            
            # columnas
            Label(frame , text = cantidadNodos).place(x=15 , y=0) #nroEstado
            Entry(frame, width=15).place(x= 80, y=0) #name
            Entry(frame, width=4).place(x= 220, y=0) #posX
            Entry(frame, width=4).place(x= 250, y=0) #posY
            Entry(frame, width=17).place(x= 340, y=0) #conexiones
          
            if (cantidadNodos + 1) > float(estados_crear_input):
                break
                       
    def on_click_cargar_grafo(self):
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
            
            self.grafo.append({"name":name,"posicion":{"x":posX,"y":posY}, "aristas": conexiones.split(',')})
            
        self.clearFramesPartiendoIndice(self.raiz, 1)
        
        print("\n\nGrafo cargado: ", self.grafo,"\n")
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
        (5) Carga de datos de forma automatica
    (6) Mover de posicion del boton de carga automatica (LSITO)
    (7) Controlar que opciones de estado inicial y final no sean los mismos (LISTO ->  no requerido)
    (8) Pintar estado inicial y final al ser seleccionados (LISTO)
     .....
"""
def generar_grafo_barabasi_albert(n, m):
    G = nx.barabasi_albert_graph(n, m)
    nx.draw(G, with_labels=True)
    plt.show()
    return G

# Generar un grafo Barabasi-Albert con 10 nodos y 2 conexiones por cada nuevo nodo
#grafo_barabasi_albert = generar_grafo_barabasi_albert(10, 2)

