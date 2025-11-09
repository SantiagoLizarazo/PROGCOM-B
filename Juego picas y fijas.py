import tkinter as tk
from tkinter import ttk, messagebox
import random
from itertools import permutations

class PicasFijasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Picas y Fijas")
        self.root.geometry("500x600")

        # Estilo para los widgets
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))

        # --- Variables del juego ---
        self.numero_secreto_pc = []
        self.intentos_jugador = 0
        
        # --- Variables de la IA de la máquina ---
        self.soluciones_posibles = []
        self.intento_actual_maquina = ""
        self.intentos_maquina = 0

        # --- Crear la interfaz de pestañas ---
        self.notebook = ttk.Notebook(root)
        
        self.tab_jugador_adivina = ttk.Frame(self.notebook, padding=10)
        self.tab_maquina_adivina = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.tab_jugador_adivina, text="Tú Adivinas")
        self.notebook.add(self.tab_maquina_adivina, text="La Máquina Adivina")
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # --- Construir cada pestaña ---
        self.crear_tab_jugador_adivina()
        self.crear_tab_maquina_adivina()

        # Iniciar el primer juego
        self.iniciar_juego_jugador()

    # ===================================================================
    # PESTAÑA 1: EL JUGADOR ADIVINA
    # ===================================================================

    def crear_tab_jugador_adivina(self):
        frame = self.tab_jugador_adivina
        
        # --- Frame de Entrada ---
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Ingresa 4 dígitos (sin repetir):").pack()
        
        self.entry_frame = ttk.Frame(input_frame)
        self.entry_frame.pack(pady=5)
        
        self.entries_jugador = []
        for i in range(4):
            # Usamos 'validatecommand' para mover el foco automáticamente
            vcmd = (self.root.register(self.auto_tab), '%P', i)
            entry = ttk.Entry(self.entry_frame, width=3, font=('Arial', 24, 'bold'), 
                              justify='center', validate='key', validatecommand=vcmd)
            entry.pack(side="left", padx=5)
            # Bind para borrar y mover foco hacia atrás
            entry.bind("<BackSpace>", lambda e, idx=i: self.on_backspace(e, idx))
            self.entries_jugador.append(entry)

        # --- Frame de Botones ---
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        self.btn_adivinar = ttk.Button(button_frame, text="¡Adivinar!", command=self.revisar_intento_jugador)
        self.btn_adivinar.pack(side="left", padx=10)
        
        self.btn_nuevo_juego_jugador = ttk.Button(button_frame, text="Juego Nuevo", command=self.iniciar_juego_jugador)
        self.btn_nuevo_juego_jugador.pack(side="left", padx=10)

        # --- Frame de Estado ---
        self.status_label_jugador = ttk.Label(frame, text="¡Adivina el número secreto!", font=("Arial", 14, "italic"))
        self.status_label_jugador.pack(pady=10)

        # --- Frame de Historial (con Scrollbar) ---
        hist_container = ttk.Frame(frame)
        hist_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Encabezados del historial
        header_frame = ttk.Frame(hist_container)
        header_frame.pack(fill="x", padx=5)
        ttk.Label(header_frame, text="Intento", width=15, style="Header.TLabel").pack(side="left")
        ttk.Label(header_frame, text="Número", width=15, style="Header.TLabel").pack(side="left")
        ttk.Label(header_frame, text="Picas", width=10, style="Header.TLabel").pack(side="left")
        ttk.Label(header_frame, text="Fijas", width=10, style="Header.TLabel").pack(side="left")
        
        # Área de historial con scroll
        scrollbar = ttk.Scrollbar(hist_container, orient="vertical")
        self.historial_canvas = tk.Canvas(hist_container, yscrollcommand=scrollbar.set, bg="white")
        
        scrollbar.config(command=self.historial_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.historial_canvas.pack(side="left", fill="both", expand=True)

        self.historial_frame_jugador = ttk.Frame(self.historial_canvas)
        self.historial_canvas.create_window((0, 0), window=self.historial_frame_jugador, anchor="nw")

        self.historial_frame_jugador.bind("<Configure>", lambda e: self.historial_canvas.configure(scrollregion=self.historial_canvas.bbox("all")))

    def auto_tab(self, P, i_str):
        """Mueve el foco al siguiente Entry cuando se escribe un dígito."""
        i = int(i_str)
        if len(P) == 1 and P.isdigit():
            if i < 3:
                self.entries_jugador[i+1].focus_set()
            return True
        elif len(P) == 0:
            return True # Permite borrar
        else:
            return False # No permite más de 1 dígito o no dígitos

    def on_backspace(self, event, index):
        """Mueve el foco al Entry anterior al presionar Backspace en un Entry vacío."""
        if index > 0 and len(event.widget.get()) == 0:
            self.entries_jugador[index-1].focus_set()
            # Borra también el anterior por si acaso
            self.entries_jugador[index-1].delete(0, 'end')

    def iniciar_juego_jugador(self):
        """Prepara un nuevo juego para el jugador."""
        digitos = list(range(10))
        random.shuffle(digitos)
        self.numero_secreto_pc = [str(d) for d in digitos[:4]]
        self.intentos_jugador = 0
        
        # Imprimir en consola para depuración
        print(f"Número Secreto (Tú Adivinas): {''.join(self.numero_secreto_pc)}")
        
        self.status_label_jugador.config(text="Nuevo juego. ¡Adivina el número!")
        self.btn_adivinar.config(state="normal")
        
        for entry in self.entries_jugador:
            entry.delete(0, 'end')
        
        # Limpiar historial
        for widget in self.historial_frame_jugador.winfo_children():
            widget.destroy()
            
        self.entries_jugador[0].focus_set()

    def revisar_intento_jugador(self):
        """Comprueba el intento del jugador y da retroalimentación."""
        intento = []
        for entry in self.entries_jugador:
            val = entry.get()
            if not val.isdigit():
                self.status_label_jugador.config(text="Error: Debes ingresar 4 dígitos.")
                return
            intento.append(val)
        
        if len(set(intento)) != 4:
            self.status_label_jugador.config(text="Error: Los dígitos no deben repetirse.")
            return

        self.intentos_jugador += 1
        picas = 0
        fijas = 0

        for i in range(4):
            if intento[i] == self.numero_secreto_pc[i]:
                fijas += 1
            elif intento[i] in self.numero_secreto_pc:
                picas += 1
        
        # Añadir al historial
        self.agregar_historial_jugador("".join(intento), picas, fijas)

        if fijas == 4:
            self.status_label_jugador.config(text=f"¡Ganaste en {self.intentos_jugador} intentos!")
            self.btn_adivinar.config(state="disabled")
        else:
            self.status_label_jugador.config(text="¡Sigue intentando!")
            # Limpiar entries para el siguiente intento
            for entry in self.entries_jugador:
                entry.delete(0, 'end')
            self.entries_jugador[0].focus_set()

    def agregar_historial_jugador(self, intento_str, picas, fijas):
        """Añade una fila al historial del jugador."""
        fila_frame = ttk.Frame(self.historial_frame_jugador)
        fila_frame.pack(fill="x", padx=5, pady=2)
        
        # Estilo para el número de intento
        intento_num_label = ttk.Label(fila_frame, text=f"{self.intentos_jugador}.", width=15)
        intento_num_label.pack(side="left")

        # Estilo para el número (más grande)
        num_label = ttk.Label(fila_frame, text=f" {intento_str[0]} {intento_str[1]} {intento_str[2]} {intento_str[3]}", 
                              width=15, font=("Courier", 14, "bold"))
        num_label.pack(side="left")

        # Estilo Picas (Círculo sin relleno - como en la imagen)
        picas_label = ttk.Label(fila_frame, text=f"{picas}", width=10, 
                                font=("Arial", 14, "bold"))
        picas_label.pack(side="left")

        # Estilo Fijas (Círculo con relleno - como en la imagen)
        fijas_label = ttk.Label(fila_frame, text=f"{fijas}", width=10, 
                                font=("Arial", 14, "bold"), foreground="red")
        fijas_label.pack(side="left")
        
        # Auto-scroll al fondo
        self.historial_canvas.update_idletasks()
        self.historial_canvas.yview_moveto(1.0)

    # ===================================================================
    # PESTAÑA 2: LA MÁQUINA ADIVINA
    # ===================================================================

    def crear_tab_maquina_adivina(self):
        frame = self.tab_maquina_adivina

        ttk.Label(frame, text="Piensa en un número de 4 dígitos únicos.").pack(pady=5)
        ttk.Label(frame, text="La máquina intentará adivinarlo.").pack()

        self.btn_iniciar_maquina = ttk.Button(frame, text="¡Estoy listo! (Empezar a adivinar)", command=self.iniciar_juego_maquina)
        self.btn_iniciar_maquina.pack(pady=10)
        
        # --- Frame del intento de la máquina ---
        intento_frame = ttk.Frame(frame)
        intento_frame.pack(pady=10)
        
        ttk.Label(intento_frame, text="La máquina adivina:", font=("Arial", 14)).pack(side="left")
        self.label_intento_maquina = ttk.Label(intento_frame, text="----", font=("Courier", 24, "bold"))
        self.label_intento_maquina.pack(side="left", padx=10)

        # --- Frame de retroalimentación (Picas y Fijas) ---
        feedback_frame = ttk.Frame(frame)
        feedback_frame.pack(pady=10)

        ttk.Label(feedback_frame, text="Picas:").pack(side="left", padx=5)
        self.spin_picas = ttk.Spinbox(feedback_frame, from_=0, to=4, width=4, font=("Arial", 14), state="disabled")
        self.spin_picas.pack(side="left", padx=5)

        ttk.Label(feedback_frame, text="Fijas:").pack(side="left", padx=5)
        self.spin_fijas = ttk.Spinbox(feedback_frame, from_=0, to=4, width=4, font=("Arial", 14), state="disabled")
        self.spin_fijas.pack(side="left", padx=5)
        
        # Configurar Spinbox para que no se pueda escribir
        self.spin_picas.config(state="readonly")
        self.spin_fijas.config(state="readonly")


        self.btn_confirmar_feedback = ttk.Button(frame, text="Confirmar Picas y Fijas", command=self.procesar_feedback_maquina, state="disabled")
        self.btn_confirmar_feedback.pack(pady=10)

        # --- Estado de la máquina ---
        self.status_label_maquina = ttk.Label(frame, text="Presiona 'Estoy listo' para comenzar.", font=("Arial", 14, "italic"))
        self.status_label_maquina.pack(pady=10)

        # --- Historial de la máquina ---
        self.historial_maquina_text = tk.Text(frame, height=10, width=50, state="disabled", font=("Courier", 12))
        self.historial_maquina_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def iniciar_juego_maquina(self):
        """Prepara la IA de la máquina para empezar a adivinar."""
        # Generar todas las 5040 permutaciones posibles
        todos_los_digitos = '0123456789'
        self.soluciones_posibles = [''.join(p) for p in permutations(todos_los_digitos, 4)]
        self.intentos_maquina = 0
        
        # El primer intento (un clásico es '1234')
        self.intento_actual_maquina = "1234"
        self.soluciones_posibles.remove(self.intento_actual_maquina) # Quitarlo de la lista

        self.label_intento_maquina.config(text="1 2 3 4")
        self.status_label_maquina.config(text=f"Intento 1. Quedan {len(self.soluciones_posibles)} posibilidades.")
        
        self.spin_picas.config(state="readonly")
        self.spin_fijas.config(state="readonly")
        self.spin_picas.set(0)
        self.spin_fijas.set(0)
        
        self.btn_confirmar_feedback.config(state="normal")
        self.btn_iniciar_maquina.config(state="disabled")

        # Limpiar historial
        self.historial_maquina_text.config(state="normal")
        self.historial_maquina_text.delete('1.0', 'end')
        self.historial_maquina_text.insert('1.0', "Intento | Número | P | F \n")
        self.historial_maquina_text.insert('end', "--------------------------\n")
        self.historial_maquina_text.config(state="disabled")

    def procesar_feedback_maquina(self):
        """La IA filtra la lista de soluciones basadas en el feedback."""
        try:
            picas = int(self.spin_picas.get())
            fijas = int(self.spin_fijas.get())
        except ValueError:
            self.status_label_maquina.config(text="Error: Picas y Fijas deben ser números.")
            return

        if picas + fijas > 4:
            self.status_label_maquina.config(text="Error: La suma de Picas y Fijas no puede ser > 4.")
            return
        
        self.intentos_maquina += 1
        
        # Añadir al historial
        self.historial_maquina_text.config(state="normal")
        self.historial_maquina_text.insert('end', f"{self.intentos_maquina: <7} | {' '.join(self.intento_actual_maquina)} | {picas} | {fijas}\n")
        self.historial_maquina_text.config(state="disabled")
        
        if fijas == 4:
            self.status_label_maquina.config(text=f"¡Adiviné tu número en {self.intentos_maquina} intentos!")
            self.btn_confirmar_feedback.config(state="disabled")
            self.btn_iniciar_maquina.config(state="normal")
            return

        # --- El núcleo de la IA: Filtrar la lista de posibilidades ---
        nuevo_set_soluciones = []
        for solucion_hipotetica in self.soluciones_posibles:
            # Comparamos el intento actual de la máquina ('1234')
            # con cada una de las otras soluciones ('5678', '1256', etc.)
            p, f = self.calcular_pf(self.intento_actual_maquina, solucion_hipotetica)
            
            # Si una solución hipotética ('1256') hubiera dado las mismas picas y fijas
            # que el usuario nos dio, entonces es una candidata válida.
            if p == picas and f == fijas:
                nuevo_set_soluciones.append(solucion_hipotetica)
        
        self.soluciones_posibles = nuevo_set_soluciones

        if not self.soluciones_posibles:
            self.status_label_maquina.config(text="Error: Me diste información contradictoria.")
            self.btn_confirmar_feedback.config(state="disabled")
            self.btn_iniciar_maquina.config(state="normal")
            return

        # Elegir el siguiente intento (el primero de la lista filtrada)
        self.intento_actual_maquina = self.soluciones_posibles.pop(0) # Tomar y quitar
        
        self.label_intento_maquina.config(text=" ".join(self.intento_actual_maquina))
        self.status_label_maquina.config(text=f"Intento {self.intentos_maquina + 1}. Quedan {len(self.soluciones_posibles)} posibilidades.")
        self.spin_picas.set(0)
        self.spin_fijas.set(0)

    def calcular_pf(self, intento, secreto):
        """Función helper para la IA: calcula picas y fijas entre dos números."""
        p = 0
        f = 0
        for i in range(4):
            if intento[i] == secreto[i]:
                f += 1
            elif intento[i] in secreto:
                p += 1
        return p, f


# --- Bloque principal para ejecutar la aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PicasFijasApp(root)
    root.mainloop()
    