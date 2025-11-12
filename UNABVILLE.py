import tkinter as tk
from tkinter import messagebox, font
import json
import os 
import random 
import math 

# --- Constantes de Diseño del Menú ---
COLOR_FONDO_MENU = "#000000" # Negro sólido
COLOR_TITULO = "#e67e22" # Naranja calabaza
COLOR_BOTON_MENU = "#4b0082" # Morado oscuro
COLOR_BOTON_MENU_HOVER = "#6a00aa" # Morado más claro
COLOR_TEXTO_MENU = "#ecf0f1" # Blanco

# --- Fuentes del Menú ---
# Cambia "Impact" por "Spicy Sale" si la tienes instalada
FONT_TITULO_MENU = ("Impact", 72, "bold") # Título más grande
FONT_BOTON_TEXTO_MENU = ("Impact", 18, "bold") # Fuente para el texto dentro del botón

# --- Constantes Globales ---
COLOR_FONDO_APP = "#2c3e50" 
COLOR_MARCA_AGUA = "#7f8c8d"
FONT_MARCA_AGUA = ("Arial", 10, "italic")
FONT_NORMAL = ("Comic Sans MS", 14)
FONT_TITULO_MEDIO = ("Comic Sans MS", 24, "bold") # Para sub-menús

# --- Constantes del Juego ---
ARCHIVO_GUARDADO = "partida_guardada.json"
LIMITE_TIEMPO_JUEGO = 120 
GRID_SIZE = 10 
ENEMY_ANIMATION_SPEED = 8 

# Colores del tablero - AHORA MÁS SUAVES
COLOR_PASTO_1 = "#8FBC8F" # Verde Bosque Claro, más suave
COLOR_PASTO_2 = "#6B8E23" # Verde Oliva Oscuro, más suave

# Colores de los Emojis
COLORES_DULCE = ["red", "orange", "violet"]
FONT_JUEGO_DULCE = ("Arial", 30) # <-- DULCES MÁS GRANDES
FONT_JUEGO_ENEMIGO = ("Arial", 36, "bold")
FONT_JUGADOR = ("Arial", 20)

class UnabvilleApp(tk.Tk):
    """Clase principal de la aplicación del juego UNABVILLE."""

    def __init__(self):
        super().__init__()
        
        self.title("UNABVILLE")
        self.geometry("1024x768")
        self.config(bg=COLOR_FONDO_APP)
        
        self.mapa_seleccionado = tk.StringVar(value="circo")
        self.dificultad_seleccionada = tk.StringVar(value="noob")
        self.volumen = tk.DoubleVar(value=75)
        self.es_pantalla_completa = tk.BooleanVar(value=False)

        self.vida_actual = 3
        self.dulces_actuales = 0
        self.nivel_actual = 1
        self.meta_dulces = 20

        self.tiempo_restante = LIMITE_TIEMPO_JUEGO
        
        self._frame_actual = None
        
        self.game_running = False
        self.game_paused = False # <-- NUEVA VARIABLE DE PAUSA
        self.canvas_juego = None
        self.label_vida = None
        self.label_dulces = None
        self.label_tiempo = None
        self.game_items = []
        self.dificultad_settings = {}

        self.player_id = None
        self.player_row = 0
        self.player_col = 0
        
        self.cell_width = 0
        self.cell_height = 0
        
        self._animate_title_id = None # Inicializar la variable de animación

        self.crear_marca_de_agua()
        self.crear_boton_configuracion()
        
        # Vincular la tecla ESCAPE a la función de pausa
        self.bind_all("<Escape>", self.on_escape_press)
        
        self.mostrar_menu_principal()

    def limpiar_frame_actual(self):
        """Destruye el frame activo actual."""
        self.game_running = False 
        self.game_paused = False # Asegurarse de resetear la pausa
        
        if self._frame_actual:
            if self.canvas_juego:
                self.canvas_juego.unbind("<KeyPress-w>")
                self.canvas_juego.unbind("<KeyPress-s>")
                self.canvas_juego.unbind("<KeyPress-a>")
                self.canvas_juego.unbind("<KeyPress-d>")
            self._frame_actual.destroy()
        
        self.canvas_juego = None
        self.label_vida = None
        self.label_dulces = None
        self.label_tiempo = None
        self.game_items = []
        self.player_id = None

        # Detener la animación del título si existe
        if self._animate_title_id:
            try:
                self.after_cancel(self._animate_title_id)
            except ValueError:
                pass # Ignorar error si el 'after' ya se ejecutó
            self._animate_title_id = None

    def crear_marca_de_agua(self):
        """Crea la etiqueta de la marca de agua."""
        marca_agua = tk.Label(
            self, 
            text="Como Taja Entertaiment ©",
            font=FONT_MARCA_AGUA,
            bg=COLOR_FONDO_APP,
            fg=COLOR_MARCA_AGUA
        )
        marca_agua.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    def crear_boton_configuracion(self):
        """Crea el botón de engranaje para la configuración."""
        config_button = tk.Button(
            self,
            text="\u2699", 
            font=("Arial", 20, "bold"),
            fg=COLOR_TEXTO_MENU,
            bg=COLOR_FONDO_APP,
            activebackground=COLOR_FONDO_APP,
            activeforeground=COLOR_BOTON_MENU_HOVER,
            bd=0,
            relief="flat",
            command=self.mostrar_menu_configuracion
        )
        config_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    # --- 1. MENÚ PRINCIPAL (REDiseñado con Canvas para botones redondeados y animación) ---

    def mostrar_menu_principal(self):
        """Crea y muestra la pantalla del menú principal con Canvas y elementos personalizados."""
        self.limpiar_frame_actual()
        
        # Usamos un Canvas como frame actual para dibujar los elementos
        self._frame_actual = tk.Canvas(self, bg=COLOR_FONDO_MENU, highlightthickness=0)
        self._frame_actual.pack(expand=True, fill="both")
        
        # Necesitamos 'actualizar' el canvas para obtener su tamaño
        self._frame_actual.update_idletasks() 

        # Posición central para el título
        center_x = self._frame_actual.winfo_width() / 2
        
        # Título "UNABVILLE"
        self.title_text_id = self._frame_actual.create_text(
            center_x, 150, # Posición Y fija, pero X al centro
            text="UNABVILLE",
            font=FONT_TITULO_MENU,
            fill=COLOR_TITULO,
            tags="game_title"
        )
        # Guardar la posición original para la animación
        self._title_original_x, self._title_original_y = self._frame_actual.coords(self.title_text_id)

        # Iniciar animación del título
        self.animate_title()

        # Posiciones de los botones
        button_y_start = 350
        button_spacing = 80
        button_width = 300 # Ancho para los textos largos
        button_height = 60
        button_radius = 25 # <<-- CORRECCIÓN: Radio reducido para que quepa
        
        self.create_rounded_button(
            self._frame_actual,
            center_x - button_width / 2, button_y_start,
            center_x + button_width / 2, button_y_start + button_height,
            button_radius, 
            COLOR_BOTON_MENU, COLOR_BOTON_MENU_HOVER, COLOR_TEXTO_MENU,
            "New Game", FONT_BOTON_TEXTO_MENU,
            self.mostrar_menu_nuevo_juego
        )
        
        self.create_rounded_button(
            self._frame_actual,
            center_x - button_width / 2, button_y_start + button_spacing,
            center_x + button_width / 2, button_y_start + button_spacing + button_height,
            button_radius, 
            COLOR_BOTON_MENU, COLOR_BOTON_MENU_HOVER, COLOR_TEXTO_MENU,
            "Load a Game", FONT_BOTON_TEXTO_MENU,
            self.cargar_juego
        )
        
        self.create_rounded_button(
            self._frame_actual,
            center_x - button_width / 2, button_y_start + (2 * button_spacing),
            center_x + button_width / 2, button_y_start + (2 * button_spacing) + button_height,
            button_radius, 
            COLOR_BOTON_MENU, COLOR_BOTON_MENU_HOVER, COLOR_TEXTO_MENU,
            "Exit to Desktop", FONT_BOTON_TEXTO_MENU,
            self.salir_del_juego
        )

    def animate_title(self):
        """Aplica un efecto de 'vibración' al título del juego."""
        # Comprobar si el frame actual sigue siendo un Canvas (estamos en el menú)
        if not self.game_running and isinstance(self._frame_actual, tk.Canvas): 
            try:
                # Pequeño desplazamiento aleatorio
                dx = random.randint(-2, 2)
                dy = random.randint(-2, 2)
                
                # Mover
                self._frame_actual.coords(self.title_text_id, self._title_original_x + dx, self._title_original_y + dy)
                
                # Volver a la posición original después de un corto tiempo
                self.after(50, lambda: self._frame_actual.coords(self.title_text_id, self._title_original_x, self._title_original_y))
                
                # Programar la próxima vibración
                self._animate_title_id = self.after(random.randint(200, 400), self.animate_title)
            except (tk.TclError, AttributeError):
                # El canvas ya no existe o el título fue borrado
                self._animate_title_id = None

    def create_rounded_button(self, canvas, x1, y1, x2, y2, radius, 
                              fill_color, hover_color, text_color, 
                              text, font_config, command):
        """Dibuja un botón con esquinas redondeadas en un canvas."""
        
        # Dibujar el rectángulo redondeado
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2-radius,
                  x1, y1+radius]
        
        button_body = canvas.create_polygon(points, smooth=True, fill=fill_color, outline=fill_color)
        
        # Añadir el texto del botón
        button_text = canvas.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2,
            text=text,
            font=font_config,
            fill=text_color
        )
        
        # Crear un grupo de tags para el botón
        button_tag = f"button_{text.replace(' ', '_').lower()}"
        canvas.addtag_withtag(button_tag, button_body)
        canvas.addtag_withtag(button_tag, button_text)
        
        # --- Eventos de Hover y Click ---
        def on_enter(event):
            canvas.itemconfig(button_body, fill=hover_color)

        def on_leave(event):
            canvas.itemconfig(button_body, fill=fill_color)
            
        def on_click(event):
            command()

        canvas.tag_bind(button_tag, "<Enter>", on_enter)
        canvas.tag_bind(button_tag, "<Leave>", on_leave)
        canvas.tag_bind(button_tag, "<Button-1>", on_click)
        
        return button_tag

    # --- 2. MENÚ NUEVO JUEGO ---

    def mostrar_menu_nuevo_juego(self):
        """Crea y muestra la pantalla de selección de nueva partida."""
        self.limpiar_frame_actual()
        
        self._frame_actual = tk.Frame(self, bg=COLOR_FONDO_APP)
        self._frame_actual.pack(expand=True, fill="both")

        contenedor = tk.Frame(self._frame_actual, bg=COLOR_FONDO_APP)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        label_mapa = tk.Label(contenedor, text="Seleccionar Mapa", font=FONT_TITULO_MEDIO, fg=COLOR_TEXTO_MENU, bg=COLOR_FONDO_APP)
        label_mapa.pack(pady=(0, 15))

        self.crear_radio_boton_estilo(contenedor, "Circo", self.mapa_seleccionado, "circo")
        self.crear_radio_boton_estilo(contenedor, "Cementerio", self.mapa_seleccionado, "cementerio")

        label_dificultad = tk.Label(contenedor, text="Seleccionar Dificultad", font=FONT_TITULO_MEDIO, fg=COLOR_TEXTO_MENU, bg=COLOR_FONDO_APP)
        label_dificultad.pack(pady=(30, 15))

        self.crear_radio_boton_estilo(contenedor, "Noob", self.dificultad_seleccionada, "noob")
        self.crear_radio_boton_estilo(contenedor, "Pro", self.dificultad_seleccionada, "pro")
        self.crear_radio_boton_estilo(contenedor, "God", self.dificultad_seleccionada, "god")

        contenedor_botones = tk.Frame(contenedor, bg=COLOR_FONDO_APP)
        contenedor_botones.pack(pady=40)

        # Aquí usamos el estilo de botón tk.Button estándar
        self.crear_boton_estilo(contenedor_botones, "Iniciar Juego", self.iniciar_juego_nuevo)
        self.crear_boton_estilo(contenedor_botones, "Volver", self.mostrar_menu_principal)

    def crear_radio_boton_estilo(self, master, texto, variable, valor):
        """Función helper para crear Radiobuttons con estilo."""
        rb = tk.Radiobutton(
            master,
            text=texto,
            variable=variable,
            value=valor,
            font=FONT_NORMAL,
            bg=COLOR_FONDO_APP,
            fg=COLOR_TEXTO_MENU,
            selectcolor="#7f8c8d",
            activebackground=COLOR_FONDO_APP,
            activeforeground=COLOR_TEXTO_MENU,
            indicatoron=0,
            width=20,
            pady=8,
            bd=0
        )
        rb.pack(pady=5)
        
        rb.config(
            selectcolor=COLOR_BOTON_MENU,
            indicatoron=False
        )
        return rb
        
    # --- 3. MENÚ CONFIGURACIÓN (Pop-up) ---

    def on_escape_press(self, event=None):
        """Pausa el juego si está corriendo y no está pausado."""
        if self.game_running and not self.game_paused:
            self.game_paused = True
            print("Juego Pausado")
            # Mostrar el menú de configuración actúa como pantalla de pausa
            self.mostrar_menu_configuracion()
            
    def mostrar_menu_configuracion(self):
        """Muestra la ventana emergente de configuración."""
        
        # Si el juego está corriendo, esto es una pausa
        is_pause_menu = self.game_running
        
        config_window = tk.Toplevel(self)
        config_window.title("Configuración")
        config_window.geometry("400x450")
        config_window.config(bg=COLOR_FONDO_APP)
        config_window.transient(self)
        config_window.grab_set()

        # --- Función para reanudar el juego al cerrar ---
        def on_close_config():
            if is_pause_menu and self.game_paused:
                self.game_paused = False
                print("Juego Reanudado")
                # Devolver el foco al canvas del juego para que las teclas WASD funcionen
                if self.canvas_juego:
                    self.canvas_juego.focus_set()
            config_window.destroy()

        # Asignar la función al botón "Cerrar" y a la 'X' de la ventana
        config_window.protocol("WM_DELETE_WINDOW", on_close_config)

        contenedor = tk.Frame(config_window, bg=COLOR_FONDO_APP, padX=20, padY=20)
        contenedor.pack(expand=True, fill="both")

        label_volumen = tk.Label(contenedor, text="Volumen", font=FONT_TITULO_MEDIO, fg=COLOR_TEXTO_MENU, bg=COLOR_FONDO_APP)
        label_volumen.pack(pady=10)

        slider_volumen = tk.Scale(
            contenedor,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.volumen,
            font=FONT_NORMAL,
            bg=COLOR_FONDO_APP,
            fg=COLOR_TEXTO_MENU,
            troughcolor=COLOR_BOTON_MENU,
            activebackground=COLOR_BOTON_MENU_HOVER,
            highlightthickness=0,
            bd=0
        )
        slider_volumen.pack(fill="x", padx=10, pady=5)
        
        label_pantalla = tk.Label(contenedor, text="Pantalla", font=FONT_TITULO_MEDIO, fg=COLOR_TEXTO_MENU, bg=COLOR_FONDO_APP)
        label_pantalla.pack(pady=20)

        check_pantalla = tk.Checkbutton(
            contenedor,
            text="Pantalla Completa",
            variable=self.es_pantalla_completa,
            command=self.alternar_pantalla_completa,
            font=FONT_NORMAL,
            bg=COLOR_FONDO_APP,
            fg=COLOR_TEXTO_MENU,
            selectcolor="#7f8c8d",
            activebackground=COLOR_FONDO_APP,
            activeforeground=COLOR_TEXTO_MENU,
            bd=0
        )
        check_pantalla.pack()

        self.crear_boton_estilo(contenedor, "Créditos", self.mostrar_creditos)
        
        # Cambiar el texto del botón si es un menú de pausa
        close_text = "Reanudar" if is_pause_menu else "Cerrar"
        self.crear_boton_estilo(contenedor, close_text, on_close_config)
        
    def alternar_pantalla_completa(self):
        """Activa o desactiva el modo de pantalla completa."""
        self.attributes("-fullscreen", self.es_pantalla_completa.get())

    def mostrar_creditos(self):
        """Muestra una ventana emergente con los créditos."""
        creditos_texto = """
        Juego programado en:
        Python 3 con tkinter
        
        Desarrollado por:
        - Santiago Lizarazo
        - Hames Escorcia
        - Harry Gutierrez
        - Juan David Rodriguez
        
        Como Taja Entertaiment ©
        """
        
        messagebox.showinfo(
            "Créditos",
            creditos_texto,
            parent=self.winfo_children()[-1] # Mostrar sobre la ventana de config
        )

    # --- Función genérica para botones tk.Button (para no-menú principal) ---
    def crear_boton_estilo(self, master, texto, comando):
        """Función helper para crear botones tk.Button con el estilo deseado."""
        btn = tk.Button(
            master,
            text=texto,
            font=FONT_BOTON_TEXTO_MENU,
            fg=COLOR_TEXTO_MENU,
            bg=COLOR_BOTON_MENU,
            activebackground=COLOR_BOTON_MENU_HOVER,
            activeforeground=COLOR_TEXTO_MENU,
            width=20,
            pady=10,
            bd=0,
            relief="flat",
            command=comando
        )
        btn.pack(pady=10)
        
        btn.bind("<Enter>", lambda e: e.widget.config(bg=COLOR_BOTON_MENU_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=COLOR_BOTON_MENU))
        return btn

    # --- 4. ACCIONES DEL JUEGO (Lógica principal sin cambios) ---

    def iniciar_juego_nuevo(self):
        """Inicia un juego desde cero, reseteando estadísticas."""
        print("Iniciando juego NUEVO.")
        self.vida_actual = 3
        self.dulces_actuales = 0
        self.nivel_actual = 1
        self.meta_dulces = 20 * self.nivel_actual
        self.tiempo_restante = LIMITE_TIEMPO_JUEGO
        self.game_paused = False
        
        self.mostrar_pantalla_de_juego()

    def iniciar_juego_cargado(self, datos_guardados):
        """Inicia un juego cargando datos de un archivo."""
        print("Cargando juego desde archivo.")
        
        try:
            self.mapa_seleccionado.set(datos_guardados.get("mapa", "circo"))
            self.dificultad_seleccionada.set(datos_guardados.get("dificultad", "noob"))
            self.vida_actual = datos_guardados.get("vida", 3)
            self.dulces_actuales = datos_guardados.get("dulces", 0)
            self.nivel_actual = datos_guardados.get("nivel", 1)
            self.meta_dulces = 20 * self.nivel_actual
            self.tiempo_restante = LIMITE_TIEMPO_JUEGO
            self.game_paused = False
            
            self.mostrar_pantalla_de_juego()
            
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            messagebox.showerror("Error de carga", "El archivo de guardado está corrupto.")
            self.mostrar_menu_principal()


    def mostrar_pantalla_de_juego(self):
        """Prepara e inicia la pantalla principal del juego."""
        dificultad = self.dificultad_seleccionada.get()
        
        print(f"Mostrando pantalla de juego: Dificultad={dificultad}")

        self.limpiar_frame_actual()
        
        self._frame_actual = tk.Frame(self, bg=COLOR_FONDO_APP)
        self._frame_actual.pack(expand=True, fill="both")

        self.dificultad_settings = {
            "noob": {"e_move_delay": 1200, "e_spawn": 3000, "d_spawn": 1500},
            "pro": {"e_move_delay": 850, "e_spawn": 2000, "d_spawn": 2000},
            "god": {"e_move_delay": 500, "e_spawn": 1000, "d_spawn": 3000}
        }[dificultad]

        self.canvas_juego = tk.Canvas(self._frame_actual, bg="white", highlightthickness=0)
        self.canvas_juego.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.canvas_juego.update_idletasks()

        self.draw_board()

        ui_frame = tk.Frame(self._frame_actual, bg=COLOR_FONDO_APP)
        ui_frame.place(relx=0.0, rely=0.0, anchor='nw', relwidth=1.0)
        
        self.label_vida = tk.Label(ui_frame, text="", font=FONT_NORMAL, fg="red", bg=COLOR_FONDO_APP)
        self.label_vida.pack(side="left", padx=20, pady=10)
        
        self.label_dulces = tk.Label(ui_frame, text="", font=FONT_NORMAL, fg="yellow", bg=COLOR_FONDO_APP)
        self.label_dulces.pack(side="right", padx=20, pady=10)

        self.label_tiempo = tk.Label(ui_frame, text="", font=FONT_NORMAL, fg="cyan", bg=COLOR_FONDO_APP)
        self.label_tiempo.pack(side="right", padx=20, pady=10)
        
        self.actualizar_ui()

        # Usar el estilo de botón estándar para el juego
        self.crear_boton_estilo(self._frame_actual, "Guardar y Salir", self.guardar_y_salir)
        
        self.player_row = GRID_SIZE // 2
        self.player_col = GRID_SIZE // 2
        
        center_x = (self.player_col + 0.5) * self.cell_width
        center_y = (self.player_row + 0.5) * self.cell_height
        
        self.player_id = self.canvas_juego.create_text(
            center_x, center_y,
            text="⚫",
            font=FONT_JUGADOR,
            tags="player"
        )
        
        self.game_running = True
        
        self.canvas_juego.focus_set()
        self.canvas_juego.bind("<KeyPress-w>", self.move_player_event)
        self.canvas_juego.bind("<KeyPress-s>", self.move_player_event)
        self.canvas_juego.bind("<KeyPress-a>", self.move_player_event)
        self.canvas_juego.bind("<KeyPress-d>", self.move_player_event)
        
        self.spawn_enemigo_loop()
        self.spawn_dulce_loop()
        self.monster_ai_loop()
        self.game_loop()
        self.temporizador_loop()
        
    # --- BUCLES DEL JUEGO ---

    def draw_board(self):
        """Dibuja el fondo de tablero de ajedrez verde."""
        canvas_width = self.canvas_juego.winfo_width()
        canvas_height = self.canvas_juego.winfo_height()
        
        self.cell_width = canvas_width / GRID_SIZE
        self.cell_height = canvas_height / GRID_SIZE
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1 = col * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                
                if (row + col) % 2 == 0:
                    color = COLOR_PASTO_1
                else:
                    color = COLOR_PASTO_2
                    
                self.canvas_juego.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
        self.canvas_juego.tag_lower("all")

    def temporizador_loop(self):
        """Bucle de 1 segundo para el contador de tiempo."""
        if not self.game_running:
            return
            
        if self.game_paused:
            self.after(1000, self.temporizador_loop) # Esperar pero no descontar
            return

        self.tiempo_restante -= 1
        self.actualizar_ui()

        if self.tiempo_restante <= 0:
            self.game_over(causa="tiempo") 
        else:
            self.after(1000, self.temporizador_loop)

    def spawn_enemigo_loop(self):
        """Bucle para crear enemigos."""
        if not self.game_running:
            return
        
        if not self.game_paused:
            self.spawn_entidad(tipo="enemigo")
        
        spawn_time = self.dificultad_settings['e_spawn']
        self.after(random.randint(spawn_time - 500, spawn_time + 500), self.spawn_enemigo_loop)

    def spawn_dulce_loop(self):
        """Bucle para crear dulces en el tablero."""
        if not self.game_running:
            return
        
        if not self.game_paused:
            self.spawn_entidad(tipo="dulce")
        
        spawn_time = self.dificultad_settings['d_spawn']
        self.after(random.randint(spawn_time - 500, spawn_time + 500), self.spawn_dulce_loop)

    def spawn_entidad(self, tipo):
        """Crea un objeto (enemigo o dulce) en el canvas."""
        if not self.canvas_juego or not self.game_running or self.cell_width == 0:
            return

        if tipo == "enemigo":
            edge = random.choice(["top", "bottom", "left", "right"])
            if edge == "top":
                row, col = 0, random.randint(0, GRID_SIZE - 1)
            elif edge == "bottom":
                row, col = GRID_SIZE - 1, random.randint(0, GRID_SIZE - 1)
            elif edge == "left":
                row, col = random.randint(0, GRID_SIZE - 1), 0
            else: # "right"
                row, col = random.randint(0, GRID_SIZE - 1), GRID_SIZE - 1
            
            texto_emoji = random.choice(["👻", "🧟"])
            tag = "enemigo"
            font_to_use = FONT_JUEGO_ENEMIGO
            
            # Ambos fantasmas y zombies serán blancos
            color = "white"
            
        else: # "dulce"
            while True:
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - 1)
                if row == self.player_row and col == self.player_col:
                    continue
                is_occupied = False
                for item in self.game_items:
                    if item["tipo"] == "dulce" and item["row"] == row and item["col"] == col:
                        is_occupied = True
                        break
                if not is_occupied:
                    break
            
            texto_emoji = "🍬"
            tag = "dulce"
            font_to_use = FONT_JUEGO_DULCE
            color = random.choice(COLORES_DULCE)
        
        x_pos = (col + 0.5) * self.cell_width
        y_pos = (row + 0.5) * self.cell_height

        item_id = self.canvas_juego.create_text(
            x_pos, y_pos,
            text=texto_emoji,
            font=font_to_use,
            tags=(tag),
            fill=color
        )
        
        is_moving = False if tipo == "enemigo" else None
        
        self.game_items.append({
            "id": item_id, 
            "tipo": tipo, 
            "tag": tag, 
            "row": row, 
            "col": col, 
            "is_moving": is_moving
        })
        
        if tipo == "enemigo":
            self.check_collisions()

    # --- Lógica de Movimiento y Colisión ---

    def game_loop(self):
        """Bucle de animación (rápido) para deslizar a los enemigos."""
        if not self.game_running:
            return
        
        if not self.game_paused:
            self.update_enemy_visuals()
        
        self.after(33, self.game_loop) # ~30 FPS

    def update_enemy_visuals(self):
        """Mueve suavemente a los enemigos hacia su casilla de destino."""
        if not self.game_running:
            return
            
        for item in self.game_items:
            if item["tipo"] == "enemigo" and item["is_moving"]:
                try:
                    target_x = (item["col"] + 0.5) * self.cell_width
                    target_y = (item["row"] + 0.5) * self.cell_height
                    
                    current_coords = self.canvas_juego.coords(item["id"])
                    if not current_coords: continue
                    
                    current_x, current_y = current_coords[0], current_coords[1]
                    
                    dx = target_x - current_x
                    dy = target_y - current_y
                    
                    dist = math.sqrt(dx**2 + dy**2)
                    
                    if dist < ENEMY_ANIMATION_SPEED:
                        self.canvas_juego.coords(item["id"], target_x, target_y)
                        item["is_moving"] = False
                        self.check_collisions()
                    else:
                        vx = (dx / dist) * ENEMY_ANIMATION_SPEED
                        vy = (dy / dist) * ENEMY_ANIMATION_SPEED
                        self.canvas_juego.move(item["id"], vx, vy)
                
                except tk.TclError:
                    continue

    def move_player_event(self, event):
        """Maneja el evento de tecla para mover al jugador una casilla."""
        if not self.game_running or self.game_paused: # No moverse si está pausado
            return
            
        key = event.keysym.lower()
        new_row, new_col = self.player_row, self.player_col
        
        if key == 'w' and self.player_row > 0:
            new_row -= 1
        elif key == 's' and self.player_row < GRID_SIZE - 1:
            new_row += 1
        elif key == 'a' and self.player_col > 0:
            new_col -= 1
        elif key == 'd' and self.player_col < GRID_SIZE - 1:
            new_col += 1
        
        if new_row != self.player_row or new_col != self.player_col:
            self.move_player_to_tile(new_row, new_col)

    def move_player_to_tile(self, row, col):
        """Mueve el sprite del jugador a la nueva casilla y comprueba colisiones."""
        self.player_row = row
        self.player_col = col
        
        x = (col + 0.5) * self.cell_width
        y = (row + 0.5) * self.cell_height
        
        try:
            self.canvas_juego.coords(self.player_id, x, y)
            self.check_collisions()
        except tk.TclError:
            print("Error: El jugador no se pudo mover (probablemente el juego terminó).")


    def monster_ai_loop(self):
        """Bucle de IA (lento) que le dice a cada monstruo a dónde moverse."""
        if not self.game_running:
            return
        
        if not self.game_paused:
            for item in self.game_items[:]:
                if item["tipo"] == "enemigo":
                    self.move_one_enemy(item)
        
        delay = self.dificultad_settings['e_move_delay']
        self.after(delay, self.monster_ai_loop)

    def move_one_enemy(self, item):
        """Calcula y actualiza el *destino* de un enemigo."""
        if not self.game_running or item["is_moving"]:
            return

        e_row, e_col = item["row"], item["col"]
        
        d_row = self.player_row - e_row
        d_col = self.player_col - e_col
        
        if d_row == 0 and d_col == 0:
            self.check_collisions()
            return
        
        new_row, new_col = e_row, e_col
        
        if abs(d_row) > abs(d_col):
            new_row += 1 if d_row > 0 else -1
        elif abs(d_row) == abs(d_col) and d_row != 0:
             new_row += 1 if d_row > 0 else -1
        elif d_col != 0:
            new_col += 1 if d_col > 0 else -1
        
        if new_row != e_row or new_col != e_col:
            item["row"] = new_row
            item["col"] = new_col
            item["is_moving"] = True
            
            self.check_collisions()
            

    def check_collisions(self):
        """Comprueba si el jugador está en la misma casilla que un item."""
        if not self.game_running:
            return
            
        for item in self.game_items[:]:
            if item["tipo"] == "enemigo" and not item["is_moving"]:
                if item["row"] == self.player_row and item["col"] == self.player_col:
                    self.perder_vida()
                    self.canvas_juego.delete(item["id"])
                    self.game_items.remove(item)
                    if not self.game_running: return
        
        for item in self.game_items[:]:
            if item["tipo"] == "dulce":
                if item["row"] == self.player_row and item["col"] == self.player_col:
                    self.dulces_actuales += 1
                    print("¡Dulce recogido!")
                    self.canvas_juego.delete(item["id"])
                    self.game_items.remove(item)
                    self.actualizar_ui()
                    if not self.game_running: return


    def perder_vida(self):
        """Resta una vida y actualiza la UI. Comprueba Game Over."""
        if not self.game_running:
            return
            
        self.vida_actual -= 1
        print("¡Vida perdida!")
        self.actualizar_ui()
        
        if self.vida_actual <= 0:
            self.game_over(causa="vida")

    def actualizar_ui(self):
        """Actualiza todas las etiquetas (Vida, Dulces, Tiempo)."""
        if not self.label_vida or not self.label_dulces or not self.label_tiempo:
            return
            
        vida_texto = "Vida: " + "❤️" * max(0, self.vida_actual)
        self.label_vida.config(text=vida_texto)
        
        dulces_texto = f"Dulces: {self.dulces_actuales} / {self.meta_dulces}"
        self.label_dulces.config(text=dulces_texto)
        
        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60
        tiempo_texto = f"Tiempo: {minutos:02d}:{segundos:02d}"
        self.label_tiempo.config(text=tiempo_texto)
        
        if self.tiempo_restante <= 10:
            self.label_tiempo.config(fg="red")
        else:
            self.label_tiempo.config(fg="cyan")

        if self.game_running and self.dulces_actuales >= self.meta_dulces:
            self.ganar_nivel()

    def game_over(self, causa="vida"):
        """Detiene el juego y muestra el mensaje de Game Over."""
        if not self.game_running:
            return
            
        print("Game Over")
        self.game_running = False
        
        if causa == "tiempo":
            messagebox.showinfo("Game Over", "¡Se acabó el tiempo!\nTodos tus dulces se han perdido.")
        else: # "vida"
            messagebox.showinfo("Game Over", "¡Te has quedado sin vidas!\nTodos tus dulces se han perdido.")
        
        self.vida_actual = 3
        self.dulces_actuales = 0
        self.nivel_actual = 1
        self.meta_dulces = 20 * self.nivel_actual
        self.tiempo_restante = LIMITE_TIEMPO_JUEGO
        
        self.mostrar_menu_principal()

    def ganar_nivel(self):
        """Detiene el juego y muestra el mensaje de victoria."""
        if not self.game_running:
            return

        print("¡Nivel ganado!")
        self.game_running = False
        
        self.nivel_actual += 1
        self.dulces_actuales = 0
        self.vida_actual = 3
        self.meta_dulces = 20 * self.nivel_actual
        self.tiempo_restante = LIMITE_TIEMPO_JUEGO
        
        messagebox.showinfo("¡Nivel Completado!", f"¡Felicidades! Has completado el nivel.\n\nAhora estás en el Nivel {self.nivel_actual}.\n\nPara guardar tu progreso, haz clic en 'Guardar y Salir'.")
        
        # El juego se detiene. El usuario debe guardar.

    # --- 5. SISTEMA DE GUARDADO/CARGA ---

    def cargar_juego(self):
        """Carga una partida guardada."""
        print("Buscando partida...")
        self.limpiar_frame_actual()
        
        self._frame_actual = tk.Frame(self, bg=COLOR_FONDO_APP)
        self._frame_actual.pack(expand=True, fill="both")
        
        label_carga = tk.Label(self._frame_actual, text="Seleccionar Partida Guardada", font=FONT_TITULO_MEDIO, fg=COLOR_TEXTO_MENU, bg=COLOR_FONDO_APP)
        label_carga.pack(pady=50)

        if os.path.exists(ARCHIVO_GUARDADO):
            print("Archivo de guardado encontrado.")
            try:
                with open(ARCHIVO_GUARDADO, 'r') as f:
                    datos_guardados = json.load(f)
                
                info = f"Nivel: {datos_guardados.get('nivel', 1)} | " \
                       f"Mapa: {datos_guardados.get('mapa', 'N/A').capitalize()} | " \
                       f"Dulces: {datos_guardados.get('dulces', 0)}"
                
                label_partida = tk.Label(self._frame_actual, text=info, font=FONT_NORMAL, fg=COLOR_TEXTO_MENU, bg=COLOR_FONDO_APP)
                label_partida.pack(pady=10)
                
                self.crear_boton_estilo(self._frame_actual, "Cargar Partida", lambda: self.iniciar_juego_cargado(datos_guardados))

            except Exception as e:
                print(f"Error leyendo archivo de guardado: {e}")
                label_placeholder = tk.Label(self._frame_actual, text="[Error al leer partida]", font=FONT_NORMAL, fg="red", bg=COLOR_FONDO_APP)
                label_placeholder.pack(pady=20)
        
        else:
            print("No se encontró archivo de guardado.")
            label_placeholder = tk.Label(self._frame_actual, text="[No hay partidas guardadas]", font=FONT_NORMAL, fg=COLOR_MARCA_AGUA, bg=COLOR_FONDO_APP)
            label_placeholder.pack(pady=20)
        
        self.crear_boton_estilo(self._frame_actual, "Volver", self.mostrar_menu_principal)

    def guardar_y_salir(self):
        """Guarda el estado actual del juego en un archivo JSON y vuelve al menú."""
        
        self.game_running = False
        
        print("Guardando el estado del juego...")
        
        datos_a_guardar = {
            "mapa": self.mapa_seleccionado.get(),
            "dificultad": self.dificultad_seleccionada.get(),
            "vida": self.vida_actual,
            "dulces": self.dulces_actuales,
            "nivel": self.nivel_actual
        }
        
        try:
            with open(ARCHIVO_GUARDADO, 'w') as f:
                json.dump(datos_a_guardar, f, indent=4)
            
            print(f"Guardado exitoso en {ARCHIVO_GUARDADO}")
            messagebox.showinfo("Guardado", "¡Partida guardada exitosamente!")
        
        except Exception as e:
            print(f"Error al guardar el juego: {e}")
            messagebox.showerror("Error", "No se pudo guardar la partida.")
            return 
        
        self.mostrar_menu_principal()


    def salir_del_juego(self):
        """Muestra confirmación antes de salir."""
        
        es_pantalla_de_juego = False
        if self._frame_actual:
            for widget in self._frame_actual.winfo_children():
                if isinstance(widget, tk.Canvas):
                    es_pantalla_de_juego = True
                    break

        if es_pantalla_de_juego:
            # Pausar el juego para que el messagebox no quede detrás
            self.game_paused = True
            if messagebox.askyesno("Salir", "¿Quieres guardar tu progreso antes de salir?"):
                self.guardar_y_salir() # Esta función ya vuelve al menú
                self.destroy()
            else:
                self.game_paused = False # Reanudar si cancela
                self.canvas_juego.focus_set() # Devolver foco
                self.destroy() # Salir sin guardar
        else:
            if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir de UNABVILLE?"):
                self.destroy()

# --- Punto de entrada de la aplicación ---
if __name__ == "__main__":
    app = UnabvilleApp()
    app.mainloop()