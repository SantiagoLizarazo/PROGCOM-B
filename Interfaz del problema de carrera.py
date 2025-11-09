import tkinter as tk
from tkinter import ttk, messagebox
import math # NUEVO: Necesitamos la librería 'math' para cos, sin y radianes

class RobotTorqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Torque - Brazo Robótico 2-GDL")
        
        # --- Configuración de Estilo (igual que antes) ---
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 11))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("TButton", font=("Arial", 11, "bold"))
        style.configure("TEntry", font=("Arial", 11))
        style.configure("Result.TLabel", font=("Arial", 12, "bold"), foreground="blue")
        style.configure("TFrame", padding=10)
        style.configure("TLabelframe", padding=10)
        style.configure("TLabelframe.Label", font=("Arial", 11, "bold"))

        # --- Constante de Gravedad ---
        self.G = 9.81  # m/s^2

        # --- Frames Principales ---
        control_frame = ttk.Frame(root)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        diagram_frame = ttk.Frame(root, relief="sunken", borderwidth=2)
        diagram_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # --- Widgets de Parámetros del Brazo (igual que antes) ---
        params_frame = ttk.Labelframe(control_frame, text="Parámetros del Brazo")
        params_frame.pack(fill="x", pady=5)

        ttk.Label(params_frame, text="Masa Eslabón 1 (kg):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_masa1 = ttk.Entry(params_frame, width=10)
        self.entry_masa1.grid(row=0, column=1, padx=5, pady=5)
        self.entry_masa1.insert(0, "2.0")

        ttk.Label(params_frame, text="Longitud Eslabón 1 (m):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_long1 = ttk.Entry(params_frame, width=10)
        self.entry_long1.grid(row=1, column=1, padx=5, pady=5)
        self.entry_long1.insert(0, "0.5")

        ttk.Label(params_frame, text="Masa Eslabón 2 (kg):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_masa2 = ttk.Entry(params_frame, width=10)
        self.entry_masa2.grid(row=2, column=1, padx=5, pady=5)
        self.entry_masa2.insert(0, "1.0")

        ttk.Label(params_frame, text="Longitud Eslabón 2 (m):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_long2 = ttk.Entry(params_frame, width=10)
        self.entry_long2.grid(row=3, column=1, padx=5, pady=5)
        self.entry_long2.insert(0, "0.4")
        
        # --- Widgets de Carga (igual que antes) ---
        load_frame = ttk.Labelframe(control_frame, text="Carga")
        load_frame.pack(fill="x", pady=10)

        ttk.Label(load_frame, text="Masa de la Carga (kg):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_carga = ttk.Entry(load_frame, width=10)
        self.entry_carga.grid(row=0, column=1, padx=5, pady=5)
        self.entry_carga.insert(0, "5.0")
        
        # --- NUEVO: Sliders para los Ángulos ---
        angle_frame = ttk.Labelframe(control_frame, text="Control de Ángulos")
        angle_frame.pack(fill="x", pady=10)
        
        # Variable para mostrar el valor del slider
        self.theta1_val = tk.StringVar(value="45.0°")
        ttk.Label(angle_frame, text="Ángulo Base (θ1):").grid(row=0, column=0, sticky="w")
        self.slider_theta1 = ttk.Scale(angle_frame, from_=0, to=180, orient="horizontal",
                                       command=self.actualizar_interfaz)
        self.slider_theta1.set(45) # Valor inicial
        self.slider_theta1.grid(row=1, column=0, sticky="ew", padx=5)
        ttk.Label(angle_frame, textvariable=self.theta1_val).grid(row=1, column=1, padx=5)

        self.theta2_val = tk.StringVar(value="30.0°")
        ttk.Label(angle_frame, text="Ángulo Codo (θ2):").grid(row=2, column=0, sticky="w")
        self.slider_theta2 = ttk.Scale(angle_frame, from_=-180, to=180, orient="horizontal",
                                       command=self.actualizar_interfaz)
        self.slider_theta2.set(30) # Valor inicial
        self.slider_theta2.grid(row=3, column=0, sticky="ew", padx=5)
        ttk.Label(angle_frame, textvariable=self.theta2_val).grid(row=3, column=1, padx=5)

        # --- Widgets de Resultados (igual que antes) ---
        results_frame = ttk.Labelframe(control_frame, text="Resultados (Torque Estático)")
        results_frame.pack(fill="x", pady=5)
        
        ttk.Label(results_frame, text="Torque Articulación 2 (Codo):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.label_resultado_t2 = ttk.Label(results_frame, text="--- Nm", style="Result.TLabel")
        self.label_resultado_t2.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(results_frame, text="Torque Articulación 1 (Base):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.label_resultado_t1 = ttk.Label(results_frame, text="--- Nm", style="Result.TLabel")
        self.label_resultado_t1.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # --- Canvas para el Diagrama ---
        self.canvas = tk.Canvas(diagram_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)
        # Bindeamos el evento <Configure> para que redibuje si cambia el tamaño
        self.canvas.bind("<Configure>", self.actualizar_interfaz)
        
        # NUEVO: Forzamos una actualización inicial
        self.root.after(100, self.actualizar_interfaz)

    
    # --- NUEVO: Función de control principal ---
    def actualizar_interfaz(self, event=None):
        """Función central que se llama cada vez que un slider se mueve."""
        
        # 1. Actualizar las etiquetas de los ángulos
        self.theta1_val.set(f"{self.slider_theta1.get():.1f}°")
        self.theta2_val.set(f"{self.slider_theta2.get():.1f}°")
        
        # 2. Calcular los torques Y las posiciones
        try:
            coords = self.calcular_torques_y_posiciones()
            # 3. Si el cálculo fue exitoso, dibujar el brazo
            if coords:
                self.dibujar_diagrama(coords)
        except ValueError:
            # Manejo de error si el usuario ingresa texto en las masas/longitudes
            messagebox.showerror("Error de Entrada", 
                                 "Por favor, ingrese solo números válidos en los campos de parámetros.")
            self.label_resultado_t2.config(text="Error")
            self.label_resultado_t1.config(text="Error")
        except Exception as e:
            # Captura de cualquier otro error (ej. división por cero si L=0)
            print(f"Error inesperado: {e}")


    # --- MODIFICADO: Ahora calcula física Y cinemática ---
    def calcular_torques_y_posiciones(self):
        """Calcula los torques y las coordenadas (x,y) del brazo."""
        
        # --- Recolección de Datos (como float) ---
        masa1 = float(self.entry_masa1.get())
        long1 = float(self.entry_long1.get())
        masa2 = float(self.entry_masa2.get())
        long2 = float(self.entry_long2.get())
        masaCarga = float(self.entry_carga.get())
        
        # --- NUEVO: Recolectar Ángulos ---
        # Convertimos los grados de los sliders a radianes para los cálculos
        theta1 = math.radians(self.slider_theta1.get())
        theta2 = math.radians(self.slider_theta2.get())
        
        # --- Cálculo de Fuerzas (Peso) ---
        fuerza1 = masa1 * self.G
        fuerza2 = masa2 * self.G
        fuerzaCarga = masaCarga * self.G

        # --- NUEVO: Cálculo de Torque Dinámico (Estático) ---
        # El torque es Fuerza * Brazo de Palanca (distancia horizontal)
        # Brazo de palanca = L * cos(angulo_total)
        # 
        
        # Distancias horizontales (Brazos de palanca)
        d1_cm = (long1 / 2) * math.cos(theta1) # Dist. horizontal al centro de masa del eslabón 1
        d2_cm = long1 * math.cos(theta1) + (long2 / 2) * math.cos(theta1 + theta2) # Dist. hor. al C.M. del eslabón 2
        d_carga = long1 * math.cos(theta1) + long2 * math.cos(theta1 + theta2) # Dist. hor. a la carga

        # Torque en Articulación 1 (Base)
        # Es la suma de todos los torques generados por cada componente
        torque1 = (fuerza1 * d1_cm) + (fuerza2 * d2_cm) + (fuerzaCarga * d_carga)

        # Torque en Articulación 2 (Codo)
        # Se calcula relativo a la articulación 2
        d2_cm_rel = (long2 / 2) * math.cos(theta1 + theta2)
        d_carga_rel = long2 * math.cos(theta1 + theta2)
        torque2 = (fuerza2 * d2_cm_rel) + (fuerzaCarga * d_carga_rel)

        # --- Actualización de Resultados en la GUI ---
        self.label_resultado_t1.config(text=f"{torque1:.2f} Nm")
        self.label_resultado_t2.config(text=f"{torque2:.2f} Nm")
        
        # --- NUEVO: Cálculo de Cinemática Directa (Posiciones x,y) ---
        # Definimos el origen (x_base, y_base) en el canvas
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        x_base = w * 0.2  # Dejamos un margen izquierdo
        y_base = h * 0.8  # Ponemos la base abajo
        
        # Calculamos las posiciones del codo y el efector final
        # NOTA: En canvas, Y aumenta hacia abajo, por eso restamos el seno.
        x_codo = x_base + long1 * math.cos(theta1)
        y_codo = y_base - long1 * math.sin(theta1) # Restamos para que suba
        
        x_efector = x_codo + long2 * math.cos(theta1 + theta2)
        y_efector = y_codo - long2 * math.sin(theta1 + theta2)
        
        # Devolvemos las coordenadas para que la función de dibujo las use
        return {
            "x_base": x_base, "y_base": y_base,
            "x_codo": x_codo, "y_codo": y_codo,
            "x_efector": x_efector, "y_efector": y_efector
        }


    # --- MODIFICADO: Ahora dibuja basado en coordenadas ---
    def dibujar_diagrama(self, coords):
        """Dibuja el esquema del brazo robótico usando las coordenadas calculadas."""
        self.canvas.delete("all")
        
        # Obtenemos las coordenadas
        x_base = coords["x_base"]
        y_base = coords["y_base"]
        x_codo = coords["x_codo"]
        y_codo = coords["y_codo"]
        x_efector = coords["x_efector"]
        y_efector = coords["y_efector"]

        # --- NUEVO: Escalado ---
        # Para que el brazo no se salga de la pantalla, escalamos todo.
        # Encontramos la longitud total máxima
        try:
            long1 = float(self.entry_long1.get())
            long2 = float(self.entry_long2.get())
            long_total = long1 + long2
            if long_total == 0: long_total = 1 # Evitar división por cero
        except:
            long_total = 1
        
        # Hacemos que la longitud total del brazo ocupe el 75% del ancho del canvas
        escala = (self.canvas.winfo_width() * 0.75) / long_total
        
        # Aplicamos la escala a las coordenadas (relativas a la base)
        x_codo = x_base + (x_codo - x_base) * escala
        y_codo = y_base - (y_base - y_codo) * escala # Y se invierte
        x_efector = x_base + (x_efector - x_base) * escala
        y_efector = y_base - (y_base - y_efector) * escala

        # Dibujar Eslabón 1
        self.canvas.create_line(x_base, y_base, x_codo, y_codo, width=8, fill="gray")
        
        # Dibujar Eslabón 2
        self.canvas.create_line(x_codo, y_codo, x_efector, y_efector, width=6, fill="gray")

        # Dibujar Articulación 1 (Base)
        self.canvas.create_oval(x_base - 10, y_base - 10, x_base + 10, y_base + 10, fill="black")
        self.canvas.create_text(x_base, y_base + 15, text="Base (T1)", anchor="n")
        
        # Dibujar Articulación 2 (Codo)
        self.canvas.create_oval(x_codo - 8, y_codo - 8, x_codo + 8, y_codo + 8, fill="gray50")
        
        # Dibujar Carga
        self.canvas.create_rectangle(x_efector - 10, y_efector - 10, x_efector + 10, y_efector + 10, fill="red")
        
        # Dibujar el "piso"
        self.canvas.create_line(0, y_base, self.canvas.winfo_width(), y_base, fill="black", dash=(4, 2))


# --- Bloque principal para ejecutar la aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotTorqueApp(root)
    root.geometry("900x600") # Hacemos la ventana más grande
    root.mainloop()