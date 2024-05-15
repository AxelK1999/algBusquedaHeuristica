import tkinter as tk
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


class interfazCargaDeGrafo:
    def __init__(self):
        self.frame = tk.Frame()
        frame = self.frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Etiqueta en Frame 1")
        



class InterfazGrafica:
    def __init__(self, master):
        self.master = master
        self.espacio_busqueda = EspacioBusqueda()

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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

        self.ax.set_title('Espacio de Búsqueda')
        self.canvas.draw()


def main():
    root = tk.Tk()
    root.title("Espacio de Búsqueda")
    #app = InterfazGrafica(root)
    interfazCargaDeGrafo(root)
    root.mainloop()


if __name__ == "__main__":
    main()

