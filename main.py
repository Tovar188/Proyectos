import tkinter as tk
from tkinter import ttk, Label, Entry, Button, messagebox
import networkx as nx
import matplotlib.pyplot as plt

class AutomataApp:
    def __init__(self, master):
        self.master = master
        master.title("Automata Finito y Expresión Regular")

        # Marco principal
        self.marco_principal = tk.Frame(master, background='#E8E8E8')
        self.marco_principal.pack(expand=True, fill='both')

        # Etiqueta
        self.label = Label(self.marco_principal, text="Ingrese la cadena:", background='#E8E8E8', font=('Arial', 12))
        self.label.pack(pady=(20, 10))

        # Entrada de texto
        self.entry = Entry(self.marco_principal, background='#FFF', font=('Arial', 12))
        self.entry.pack(pady=10)

        # Botón
        self.button = Button(self.marco_principal, text="Convertir y Mostrar Expresión Regular", background='#4CAF50', foreground='#FFF', font=('Arial', 12), command=self.convertir_mostrar)
        self.button.pack(pady=20)

    def convertir_mostrar(self):
        cadena = self.entry.get()
        if len(cadena) != 4:
            messagebox.showerror("Error", "La cadena debe tener exactamente 4 caracteres.")
            return

        # Crear autómata finito
        expresion_regular, automata = self.automata_a_expresion_regular(cadena)

        # Mostrar expresión regular
        resultado_label = ttk.Label(self.master, text=f"Expresión Regular: {expresion_regular}")
        resultado_label.pack()

        # Dibujar el autómata
        self.dibujar_automata(automata)

    def automata_a_expresion_regular(self, cadena):
        # Definir el autómata finito
        automata = {f'q{i}': {cadena[i]: f'q{i+1}'} for i in range(len(cadena)-1)}
        automata[f'q{len(cadena)-1}'] = {cadena[-1]: ''}

        # Estado inicial y estado final
        estado_inicial = 'q0'
        estado_final = f'q{len(cadena)-1}'

        # Obtener la secuencia de transiciones
        transiciones = []
        estado_actual = estado_inicial
        for simbolo in cadena:
            estado_siguiente = automata[estado_actual][simbolo]
            transiciones.append(f"{estado_actual} -> {estado_siguiente} ({simbolo})")
            estado_actual = estado_siguiente

        # Crear la expresión regular
        expresion_regular = ''.join(transiciones)

        return expresion_regular, automata

    def dibujar_automata(self, automata):
        G = nx.DiGraph()
        for estado, transiciones in automata.items():
            for simbolo, estado_siguiente in transiciones.items():
                G.add_edge(estado, estado_siguiente, label=simbolo)

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()

def main():
    root = tk.Tk()
    app = AutomataApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
