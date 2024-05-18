from tkinter import *
import networkx as nx
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import algBusquedaHeuristica


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
    
    estados = []
    
    def __init__(self, raiz):
        self.frame = Frame(raiz)
        self.frame.config(width=500, height=500) #bg="lightblue"
        self.frame.pack(side="left", fill="both", expand=True)
    
        self.frame.bind("<Configure>", self.on_window_resize)
        
        self.titulo = Label(self.frame,text="Carga de datos de grafo",font=(18))
        self.titulo.place(x=500/3.5,y=20)

        self.seccionCargaDeEstados(raiz)
        
        barra3 = Label(self.frame, text="___________________________________________________________________________________________________________________________________")
        barra3.place(x=0,y=535)
        
        self.seccionSeleccionAlgH(raiz)
        
        barra4 = Label(self.frame, text="___________________________________________________________________________________________________________________________________")
        barra4.place(x=0,y=680)
        
        self.seccionResultado(raiz)
        
    def seccionCargaDeEstados(self,raiz):
        self.lblNroEstados = Label(self.frame,text="Nro. de estados: ")
        self.lblNroEstados.place(x=20, y=60)
        
        self.inputNroEstados = Entry(raiz, width=5)
        self.inputNroEstados.place(x= 140, y=60)
    
        self.btnCrearEstados = Button(self.frame, text="crear estados", command = self.on_click_crear_estados)
        self.btnCrearEstados.place(x=200, y= 58)
        #------------------------------------------------
        self.titleTableEstados = Label(self.frame,text="Nro.                          Name                          Pos.(x,y)                        Conexiones             ")
        self.titleTableEstados.place(x=20, y=100)
    
        self.frameEstados = ScrollableFrame(self.frame)
        self.frameEstados.place(x=10, y=120)
        #-----------------------------------------------
       
        self.btnCargaAleatoriaEstados = Button(self.frame, text="Cargar datos de estados en forma aleatorio", command = self.on_click_crear_estados)
        self.btnCargaAleatoriaEstados.place(x=140, y= 390)
        
        #----------------------------------------------
    
        self.btnCargarGrafo = Button(self.frame, text="Cargar grafo", command = self.on_click_cargar_grafo)
        self.btnCargarGrafo.place(x=200,y=425)
    
        barra2 = Label(self.frame, text="___________________________________________________________________________________________________________________________________")
        barra2.place(x=0,y=450)
        
        # En lugar de posicionar elementos con place -> hacerlo con pack (lo que se hace dentro del frame a continuacion):
        frame = Frame(self.frame)
        frame.config(width=500, height=500)
        frame.place(x=0, y=490)
        
        # Lista de opciones para el menú desplegable
        opciones = ["Estado A", "Estado B"]

        # Variable de control para el menú desplegable
        opcion_seleccionada = StringVar(self.frame)
        opcion_seleccionada.set(opciones[0])  # Opción predeterminada
        
        
        self.lblEstadoInicial = Label(frame,text="Estado inicial: ")
        self.lblEstadoInicial.pack(side="left",padx=15, pady=5)
        
        self.inputEstadoInicial = OptionMenu(frame, opcion_seleccionada, *opciones, command=self.seleccionar_opcion)
        self.inputEstadoInicial.pack(side="left", padx=10, pady=5)
        
        self.lblEstadoFinal = Label(frame,text="Estado final: ")
        self.lblEstadoFinal.pack(side="left", padx=15, pady=5)
        
        self.inputEstadoFinal = OptionMenu(frame, opcion_seleccionada, *opciones, command=self.seleccionar_opcion)
        self.inputEstadoFinal.pack(side="left", padx=10, pady=5)
        
    def seccionSeleccionAlgH(self,raiz):
        
        algBusquedaOpciones = ["Escalada simple", "Maxima pendiente"]
        
        opcion_seleccionadaAlg = StringVar(self.frame)
        opcion_seleccionadaAlg.set(algBusquedaOpciones[0])
        
        
        self.lblEstadoFinal = Label(self.frame,text="Algoritmo de busqueda: ")
        self.lblEstadoFinal.place(x=100,y=570)
        
        self.inputEstadoFinal = OptionMenu(self.frame, opcion_seleccionadaAlg, *algBusquedaOpciones, command=self.seleccionar_opcion)
        self.inputEstadoFinal.place(x=100,y=590)
        
        funcHeuristicaOpciones = ["Linea recta", "Manhattan"]
        
        opcion_seleccionadaFH = StringVar(self.frame)
        opcion_seleccionadaFH.set(funcHeuristicaOpciones[0])
        
        self.lblEstadoFinal = Label(self.frame,text="Funcion heuristica: ")
        self.lblEstadoFinal.place(x=290,y=570)
        
        self.inputEstadoFinal = OptionMenu(self.frame, opcion_seleccionadaFH, *funcHeuristicaOpciones, command=self.seleccionar_opcion)
        self.inputEstadoFinal.place(x=290,y=590)
        
        barra4 = Label(self.frame, text="___________________________________________________________________________________________________________________________________")
        barra4.place(x=0,y=620)
        
        self.btnResolver = Button(self.frame, text="Ejecutar algoritmo", command = self.on_click_crear_estados)
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
    def seleccionar_opcion(opcion):
        print("Opción seleccionada:", opcion)  
    
    def on_window_resize(self, event):
        self.titulo.place(x=event.width/3.5,y=20)
    
    def verificar_numero(self, valor):
        try:
            numero = float(valor)
            return True
        except ValueError:
            messagebox.showwarning("Advertencia", f"'{valor}' no es un número válido.")
            return False
            
    def on_click_crear_estados(self):
        
        estados_crear_input = self.inputNroEstados.get()
        
        if not (self.verificar_numero( estados_crear_input )) :
            return
        
        estadosCreados = self.frameEstados.scrollable_frame.winfo_children()
        if len(estadosCreados) > 0:
            self.clearElementsOfFrame(self.frameEstados.scrollable_frame)
            
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
            Entry(frame, width=15).place(x= 340, y=0) #conexiones
          
            if (cantidadNodos + 1) > float(estados_crear_input):
                break
                       
    def on_click_cargar_grafo(self):
        
        
        
        # Nota: lectura de valores de elementos del frame (estados)
        for fila in self.frameEstados.scrollable_frame.winfo_children(): # Lee los hijos del frame scroll
            print("--->",fila.winfo_children()[1].get()) # frame fila = [Label, entry, entry, entry, entry]
            
            
            
            #for columna in fila.winfo_children(): # Lee los hijos del frame fila que se encuntra en el padre frame scroll
            #    if isinstance(columna, Entry):
            #        print(columna.get())
   
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
        self.frame.pack(side="bottom" , fill=BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.dibujar_grafo()

    def dibujar_grafo(self):
        G = nx.Graph()
        
        G.add_nodes_from(["A", "B", "C", "D", "E"])
        G.add_edges_from([("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")])
        
        pos = {
            "A":(-10,50),
            "B":(45,66),
            "C":(36,14),
            "D":(50,35),
            "E":(70,25)
        }
        
        nx.draw_networkx_nodes(G, pos=pos, node_size=500, node_color='skyblue')
        nx.draw_networkx_labels(G, pos=pos, font_size=10, font_family='sans-serif')
        
        nx.draw_networkx_edges(G, pos=pos, width=2)
      
        
        self.ax.set_title('Grafo:')
         
        # Añadir etiquetas adicionales
        labels = {
            "A": "H = 68",
            "B": "H = 20",
            "C": "H = 24",
            "D": "H = 14",
            "E": "H = 2"
        }
        
        for node, (x, y) in pos.items():
            self.ax.annotate(labels[node], (x, y), textcoords="offset points", xytext=(30, -5), ha='center')

        self.ax.margins(0.2)
        self.ax.set_title('Grafo:')

        # Resaltar estado inicial y final
        nx.draw_networkx_nodes(G, pos, nodelist=["A"], node_color='green', node_size=500)
        nx.draw_networkx_nodes(G, pos, nodelist=["C"], node_color='red', node_size=700)
        
        self.canvas.draw()


def main():
    raiz = Tk()
    raiz.title("Espacio de Búsqueda")
    raiz.resizable(False,False) # Si se permitira redimencionar el tamaño en alto y ancho
    raiz.geometry("1080x800") # Alto y ancho de la ventana => Se especifica esta propiedad a los Frame para que el raiz se adapte a los mismos
    
    interfazCargaDeGrafo(raiz)
    interfazGrafoResultante(raiz)
    interfazGrafo(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()




""" 
Pendientes: 
   on_click_cargar_grafo():
        (1) Control de datos de entrada
        (2) Cargar nombre de nodos en deplegables de opciones de estado inicial y final
        (3) Armado de estructura grafo para algoritmo busuqueda
        (4) Armado de funcion de generado de grafo en pantalla dado la estrucutra anterior
        (5) Carga de datos de forma automatica
    (6) Mover de posicion del boton de carga automatica
    (7) Controlar que opciones de estado inicial y final no sean los mismos
    (8) Pintar estado inicial y final al ser seleccionados
     .....
"""


def es_letra_sola(valor):
    return isinstance(valor, str) and len(valor) == 1 and valor.isalpha()
    #isinstance(letra, str): Verifica que el valor proporcionado sea una cadena.
    #len(letra) == 1: Verifica que la longitud de la cadena sea exactamente 1, asegurando que se trata de un solo carácter.
    #letra.isalpha(): Verifica que el carácter sea una letra del alfabeto.

# letra.upper() # --> Convierte una letra a su versión mayúscula

#elementos = valores.split(',') # => input: valores = "a, b, c, 1, d, e, ab, f" output : ['a', 'b', 'c', '1', 'd', 'e', 'ab','f']
# Controlar con es_letra_sola()


def generar_grafo_barabasi_albert(n, m):
    G = nx.barabasi_albert_graph(n, m)
    nx.draw(G, with_labels=True)
    plt.show()
    return G

# Generar un grafo Barabasi-Albert con 10 nodos y 2 conexiones por cada nuevo nodo
#grafo_barabasi_albert = generar_grafo_barabasi_albert(10, 2)

