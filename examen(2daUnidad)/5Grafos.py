import os
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import folium
import networkx as nx
import osmnx as ox
from threading import Thread

# --- 1. LÓGICA PRINCIPAL (Cálculo y Visualización) ---

def generar_datos_de_ruta(origen_nombre, destino_nombre, ciudades_interes, status_callback):
    """
    Motor del proyecto. Descarga datos y calcula la ruta.
    Esta versión es 100% compatible con versiones antiguas de OSMnx.
    """
    try:
        status_callback("Iniciando: Descargando red vial...")
        G = ox.graph_from_place("Provincia de San Román, Puno, Peru", network_type='drive', simplify=True)
        status_callback("Red descargada. Buscando nodos...")

        origen_coords = ciudades_interes[origen_nombre]['pos']
        destino_coords = ciudades_interes[destino_nombre]['pos']
        nodo_origen = ox.nearest_nodes(G, X=origen_coords[1], Y=origen_coords[0])
        nodo_destino = ox.nearest_nodes(G, X=destino_coords[1], Y=destino_coords[0])
        status_callback("Nodos encontrados. Calculando ruta...")

        ruta = nx.shortest_path(G, source=nodo_origen, target=nodo_destino, weight='length')
        status_callback("Ruta calculada. Procesando detalles del viaje...")

        # --- CÁLCULO MANUAL DE DISTANCIA Y CALLES (Compatible con versiones antiguas) ---
        distancia_total_m = 0
        lista_de_calles = []

        # Recorremos la ruta tramo por tramo (de un nodo al siguiente)
        for u, v in zip(ruta[:-1], ruta[1:]):
            # Obtenemos los datos del tramo (edge) entre el nodo u y el nodo v
            # Usamos [0] porque puede haber múltiples aristas paralelas
            edge_data = G.get_edge_data(u, v)[0]
            
            # Sumamos la longitud de este tramo al total
            # Usamos .get() para evitar errores si un tramo no tuviera longitud
            distancia_total_m += edge_data.get('length', 0)
            
            # Obtenemos el nombre de la calle de este tramo
            nombre_calle = edge_data.get('name', None)
            
            # Si la calle tiene un nombre y no es el mismo que el anterior, lo añadimos a la lista
            if nombre_calle:
                # A veces el nombre es una lista, tomamos el primero
                if isinstance(nombre_calle, list):
                    nombre_calle = nombre_calle[0]
                
                if not lista_de_calles or lista_de_calles[-1] != nombre_calle:
                    lista_de_calles.append(nombre_calle)
        
        distancia_km = distancia_total_m / 1000
        if not lista_de_calles:
            lista_de_calles = ["Rutas sin nombre definido"]

        tiempo_estimado_horas = distancia_km / 50
        tiempo_minutos = tiempo_estimado_horas * 60
        status_callback("Detalles procesados. Generando mapa...")

        mapa, nombre_archivo = crear_mapa_visual(G, ruta, origen_nombre, destino_nombre, ciudades_interes)
        webbrowser.open('file://' + os.path.realpath(nombre_archivo))
        
        return {
            "distancia": f"{distancia_km:.2f} km",
            "tiempo": f"{int(tiempo_minutos)} minutos",
            "calles": lista_de_calles,
            "status": "¡Cálculo completado!"
        }

    except Exception as e:
        return {"error": str(e)}

def crear_mapa_visual(G, ruta, origen, destino, ciudades):
    """Crea el mapa Folium con la visualización mejorada de la ruta."""
    mapa_centro = (G.nodes[ruta[len(ruta)//2]]['y'], G.nodes[ruta[len(ruta)//2]]['x'])
    mapa = folium.Map(location=mapa_centro, zoom_start=12, tiles="CartoDB positron")

    puntos_ruta = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in ruta]
    
    folium.PolyLine(puntos_ruta, color='black', weight=8, opacity=0.8).add_to(mapa)
    folium.PolyLine(puntos_ruta, color='#FF4500', weight=5, opacity=1).add_to(mapa)

    for ciudad, data in ciudades.items():
        icono = folium.Icon(color='blue', icon='circle', prefix='fa')
        if ciudad == origen: icono = folium.Icon(color='green', icon='play', prefix='fa')
        if ciudad == destino: icono = folium.Icon(color='red', icon='flag-checkered', prefix='fa')
        folium.Marker(location=data['pos'], popup=f"<b>{ciudad}</b>", tooltip=ciudad, icon=icono).add_to(mapa)
    
    mapa.fit_bounds(folium.PolyLine(puntos_ruta).get_bounds(), padding=(15, 15))
    
    nombre_archivo = f"ruta_{origen}_a_{destino}.html"
    mapa.save(nombre_archivo)
    return mapa, nombre_archivo

# --- 2. INTERFAZ GRÁFICA DE USUARIO (GUI con Tkinter) ---
# (Esta parte no necesita cambios)

class App:
    def __init__(self, root, ciudades):
        self.root = root
        self.ciudades = ciudades
        self.root.title("Sistema de Navegación - San Román")
        self.root.geometry("450x400")
        style = ttk.Style()
        style.theme_use('clam')
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        selection_frame = ttk.LabelFrame(main_frame, text="1. Defina su Viaje", padding="10")
        selection_frame.pack(fill=tk.X)
        ttk.Label(selection_frame, text="Origen:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.origen_combo = ttk.Combobox(selection_frame, values=sorted(list(self.ciudades.keys())), state="readonly")
        self.origen_combo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.origen_combo.set("Juliaca")
        ttk.Label(selection_frame, text="Destino:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.destino_combo = ttk.Combobox(selection_frame, values=sorted(list(self.ciudades.keys())), state="readonly")
        self.destino_combo.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        self.destino_combo.set("Lampa")
        selection_frame.columnconfigure(1, weight=1)

        self.calculate_button = ttk.Button(main_frame, text="Generar Ruta y Mapa", command=self.iniciar_calculo_thread)
        self.calculate_button.pack(pady=10, fill=tk.X, ipady=5)

        results_frame = ttk.LabelFrame(main_frame, text="2. Resumen del Viaje", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        self.distancia_label = ttk.Label(results_frame, text="Distancia: --")
        self.distancia_label.pack(anchor=tk.W, pady=2)
        self.tiempo_label = ttk.Label(results_frame, text="Tiempo Estimado: --")
        self.tiempo_label.pack(anchor=tk.W, pady=2)
        ttk.Label(results_frame, text="Indicaciones Principales:").pack(anchor=tk.W, pady=(10, 2))
        self.calles_text = scrolledtext.ScrolledText(results_frame, height=5, wrap=tk.WORD, state=tk.DISABLED, bg="#f0f0f0")
        self.calles_text.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(root, text="Listo para calcular.", relief=tk.SUNKEN, anchor=tk.W, padding=5)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def actualizar_status(self, mensaje):
        self.status_label.config(text=mensaje)
        self.root.update_idletasks()

    def iniciar_calculo_thread(self):
        origen = self.origen_combo.get()
        destino = self.destino_combo.get()
        if origen == destino:
            messagebox.showwarning("Selección inválida", "El origen y destino deben ser diferentes.")
            return
        self.calculate_button.config(state=tk.DISABLED)
        self.actualizar_status("Iniciando cálculo...")
        self.distancia_label.config(text="Distancia: --")
        self.tiempo_label.config(text="Tiempo Estimado: --")
        self.calles_text.config(state=tk.NORMAL); self.calles_text.delete('1.0', tk.END); self.calles_text.config(state=tk.DISABLED)
        thread = Thread(target=self.ejecutar_logica_en_background, args=(origen, destino))
        thread.start()
        
    def ejecutar_logica_en_background(self, origen, destino):
        resultados = generar_datos_de_ruta(origen, destino, self.ciudades, self.actualizar_status)
        self.root.after(0, self.finalizar_calculo, resultados)

    def finalizar_calculo(self, resultados):
        if "error" in resultados:
            messagebox.showerror("Error", resultados["error"])
            self.actualizar_status("Error en el cálculo.")
        else:
            self.distancia_label.config(text=f"Distancia: {resultados['distancia']}")
            self.tiempo_label.config(text=f"Tiempo Estimado: {resultados['tiempo']}")
            self.calles_text.config(state=tk.NORMAL)
            self.calles_text.delete('1.0', tk.END)
            self.calles_text.insert(tk.END, "\n".join(f"• {calle}" for calle in resultados['calles']))
            self.calles_text.config(state=tk.DISABLED)
            self.actualizar_status(resultados['status'])
        self.calculate_button.config(state=tk.NORMAL)

# --- 3. CONFIGURACIÓN Y EJECUCIÓN ---
if __name__ == "__main__":
    CIUDADES_DE_INTERES = {
        "Juliaca": {"pos": [-15.498, -70.129]}, "Caracoto": {"pos": [-15.552, -70.081]},
        "Cabanillas": {"pos": [-15.635, -70.354]}, "Santa Lucia": {"pos": [-15.698, -70.575]},
        "Cabana": {"pos": [-15.333, -70.320]}, "Pusi": {"pos": [-15.367, -69.951]},
        "Samán": {"pos": [-15.311, -70.065]}, "Lampa": {"pos": [-15.362, -70.365]}
    }
    root = tk.Tk()
    app = App(root, CIUDADES_DE_INTERES)
    root.mainloop()