from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

        #------------------- Fila 1 -----------------------
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
       
        self.btnCargaAleatoriaEstados = Button(self.frame, text="Cargar datos de estados aleatorio", command = self.on_click_crear_estados)
        self.btnCargaAleatoriaEstados.place(x=160, y= 390)
        
        barra1 = Label(self.frame, text="___________________________________________________________________________________________________________________________________")
        barra1.place(x=0,y=415)
        
        #----------------------------------------------
        # En lugar de posicionar elementos con place -> hacerlo con pack (lo que se hace dentro del frame a continuacion):
        frame = Frame(self.frame)
        frame.config(width=500, height=500)
        frame.place(x=0, y=440)
        
        # Lista de opciones para el menú desplegable
        opciones = ["Opción 1", "Opción 2", "Opción 3", "Opción 4"]

        # Variable de control para el menú desplegable
        opcion_seleccionada = StringVar(frame)
        opcion_seleccionada.set(opciones[0])  # Opción predeterminada
        
        
        self.lblEstadoInicial = Label(frame,text="Estado inicial: ")
        self.lblEstadoInicial.pack(side="left",padx=15, pady=5)
        
        self.inputEstadoInicial = OptionMenu(frame, opcion_seleccionada, *opciones, command=self.seleccionar_opcion)
        self.inputEstadoInicial.pack(side="left", padx=10, pady=5)
        
        self.lblEstadoFinal = Label(frame,text="Estado final: ")
        self.lblEstadoFinal.pack(side="left", padx=15, pady=5)
        
        self.inputEstadoFinal = OptionMenu(frame, opcion_seleccionada, *opciones, command=self.seleccionar_opcion)
        self.inputEstadoFinal.pack(side="left", padx=10, pady=5)
        
        #----------------------------------------------------------------
        
        barra2 = Label(self.frame, text="___________________________________________________________________________________________________________________________________")
        barra2.place(x=0,y=475)
        
        self.btnCargarGrafo = Button(self.frame, text="Cargar grafo", command = self.on_click_crear_estados)
        self.btnCargarGrafo.place(x=200,y=510)
        
        barra3 = Label(self.frame, text="___________________________________________________________________________________________________________________________________")
        barra3.place(x=0,y=535)
        
        self.lblEstadoFinal = Label(self.frame,text="Algoritmo de busqueda: ")
        self.lblEstadoFinal.place(x=100,y=560)
        
        self.inputEstadoFinal = OptionMenu(self.frame, opcion_seleccionada, *opciones, command=self.seleccionar_opcion)
        self.inputEstadoFinal.place(x=100,y=590)
        
        self.lblEstadoFinal = Label(self.frame,text="Funcion heuristica: ")
        self.lblEstadoFinal.place(x=290,y=560)
        
        self.inputEstadoFinal = OptionMenu(self.frame, opcion_seleccionada, *opciones, command=self.seleccionar_opcion)
        self.inputEstadoFinal.place(x=290,y=590)
        
        barra4 = Label(self.frame, text="___________________________________________________________________________________________________________________________________")
        barra4.place(x=0,y=620)
        
        self.btnResolver = Button(self.frame, text="Ejecutar algoritmo", command = self.on_click_crear_estados)
        self.btnResolver.place(x=180,y=650)
        
    # Función para manejar la selección del menú desplegable
    def seleccionar_opcion(opcion):
        print("Opción seleccionada:", opcion)  
    
    def on_window_resize(self, event):
        self.titulo.place(x=event.width/3.5,y=20)
        
    def on_click_crear_estados(self):
        #print("Numero de estados: ", self.inputNroEstados.get())
        fila = []
        cantidadNodos = len(self.estados) + 1 
        
        frame = Frame(self.frameEstados.scrollable_frame)
        frame.config(width=500, height=30) #bg="lightblue"
        frame.pack(fill="both", expand=True)
        
        nroEstado = Label(frame , text = cantidadNodos).place(x=15 , y=0)
        name = Entry(frame, width=15).place(x= 80, y=0)
        posX = Entry(frame, width=4).place(x= 220, y=0)
        posY = Entry(frame, width=4).place(x= 250, y=0)
        conexiones = Entry(frame, width=15).place(x= 340, y=0)
        
        fila.append(name)
        fila.append(posX)
        fila.append(posY)
        fila.append(conexiones)
        
        self.estados.append(fila)
        
        print(self.estados)
          
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
        G.add_nodes_from(self.espacio_busqueda.estados)
        G.add_edges_from(self.espacio_busqueda.conexiones)

        pos = nx.spring_layout(G)  # Algoritmo de disposición de nodos

        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

        # Resaltar estado inicial y final
        nx.draw_networkx_nodes(G, pos, nodelist=[self.espacio_busqueda.estado_inicial],
                               node_color='green', node_size=700)
        nx.draw_networkx_nodes(G, pos, nodelist=[self.espacio_busqueda.estado_final],
                               node_color='red', node_size=700)

        self.ax.set_title('Grafo: ')
        self.canvas.draw()


def main():
    raiz = Tk()
    raiz.title("Espacio de Búsqueda")
    raiz.resizable(True,True) # Si se permitira redimencionar el tamaño en alto y ancho
    raiz.geometry("1080x950") # Alto y ancho de la ventana => Se especifica esta propiedad a los Frame para que el raiz se adapte a los mismos
    
    interfazCargaDeGrafo(raiz)
    interfazGrafoResultante(raiz)
    interfazGrafo(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
