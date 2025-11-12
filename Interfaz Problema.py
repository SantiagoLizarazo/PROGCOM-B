import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import Scrollbar, Text  # NUEVO: Importar Text y Scrollbar
import math

class RobotTorqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Torque - Brazo Robótico 2-GDL")
        
        # --- Configuración de Estilo ---
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
        
        # --- Widgets de Parámetros del Brazo ---
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
        
        # --- Widgets de Carga ---
        load_frame = ttk.Labelframe(control_frame, text="Carga")
        load_frame.pack(fill="x", pady=10)

        ttk.Label(load_frame, text="Masa de la Carga (kg):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_carga = ttk.Entry(load_frame, width=10)
        self.entry_carga.grid(row=0, column=1, padx=5, pady=5)
        self.entry_carga.insert(0, "5.0")
        
        # --- Sliders para los Ángulos ---
        angle_frame = ttk.Labelframe(control_frame, text="Control de Ángulos")
        angle_frame.pack(fill="x", pady=10)
        
        self.theta1_val = tk.StringVar(value="45.0°")
        ttk.Label(angle_frame, text="Ángulo Base (θ1):").grid(row=0, column=0, sticky="w")
        self.slider_theta1 = ttk.Scale(angle_frame, from_=0, to=180, orient="horizontal",
                                       command=self.actualizar_interfaz)
        self.slider_theta1.set(45)
        self.slider_theta1.grid(row=1, column=0, sticky="ew", padx=5)
        ttk.Label(angle_frame, textvariable=self.theta1_val).grid(row=1, column=1, padx=5)

        self.theta2_val = tk.StringVar(value="30.0°")
        ttk.Label(angle_frame, text="Ángulo Codo (θ2):").grid(row=2, column=0, sticky="w")
        self.slider_theta2 = ttk.Scale(angle_frame, from_=-180, to=180, orient="horizontal",
                                       command=self.actualizar_interfaz)
        self.slider_theta2.set(30)
        self.slider_theta2.grid(row=3, column=0, sticky="ew", padx=5)
        ttk.Label(angle_frame, textvariable=self.theta2_val).grid(row=3, column=1, padx=5)

        # --- Widgets de Resultados ---
        results_frame = ttk.Labelframe(control_frame, text="Resultados (Torque Estático)")
        results_frame.pack(fill="x", pady=5)
        
        ttk.Label(results_frame, text="Torque Articulación 2 (Codo):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.label_resultado_t2 = ttk.Label(results_frame, text="--- Nm", style="Result.TLabel")
        self.label_resultado_t2.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(results_frame, text="Torque Articulación 1 (Base):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.label_resultado_t1 = ttk.Label(results_frame, text="--- Nm", style="Result.TLabel")
        self.label_resultado_t1.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # --- Botón de Generar Reporte ---
        report_button = ttk.Button(control_frame, text="Generar Reporte", 
                                   command=self.generar_reporte)
        report_button.pack(fill="x", ipady=5, pady=10)


        # --- Canvas para el Diagrama ---
        self.canvas = tk.Canvas(diagram_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.actualizar_interfaz)
        
        # Forzamos una actualización inicial
        self.root.after(100, self.actualizar_interfaz)

    
    def actualizar_interfaz(self, event=None):
        """Función central que se llama cada vez que un slider se mueve."""
        
        self.theta1_val.set(f"{self.slider_theta1.get():.1f}°")
        self.theta2_val.set(f"{self.slider_theta2.get():.1f}°")
        
        try:
            resultados = self.calcular_torques_y_posiciones()
            
            if resultados:
                self.label_resultado_t1.config(text=f"{resultados['torque1']:.2f} Nm")
                self.label_resultado_t2.config(text=f"{resultados['torque2']:.2f} Nm")
                self.dibujar_diagrama(resultados['coords'], 
                                      resultados['l1'], 
                                      resultados['l2'])
                                      
        except ValueError:
            messagebox.showerror("Error de Entrada", 
                                 "Por favor, ingrese solo números válidos en los campos de parámetros.")
            self.label_resultado_t2.config(text="Error")
            self.label_resultado_t1.config(text="Error")
        except Exception as e:
            print(f"Error inesperado: {e}")


    def calcular_torques_y_posiciones(self):
        """Calcula los torques y las coordenadas (x,y) del brazo."""
        
        try:
            masa1 = float(self.entry_masa1.get())
            long1 = float(self.entry_long1.get())
            masa2 = float(self.entry_masa2.get())
            long2 = float(self.entry_long2.get())
            masaCarga = float(self.entry_carga.get())
            theta1_deg = self.slider_theta1.get()
            theta2_deg = self.slider_theta2.get()
            
            theta1 = math.radians(theta1_deg)
            theta2 = math.radians(theta2_deg)
        except ValueError:
            raise ValueError("Datos de entrada no son numéricos")
        
        fuerza1 = masa1 * self.G
        fuerza2 = masa2 * self.G
        fuerzaCarga = masaCarga * self.G

        d1_cm = (long1 / 2) * math.cos(theta1)
        d2_cm = long1 * math.cos(theta1) + (long2 / 2) * math.cos(theta1 + theta2)
        d_carga = long1 * math.cos(theta1) + long2 * math.cos(theta1 + theta2)

        torque1 = (fuerza1 * d1_cm) + (fuerza2 * d2_cm) + (fuerzaCarga * d_carga)

        d2_cm_rel = (long2 / 2) * math.cos(theta1 + theta2)
        d_carga_rel = long2 * math.cos(theta1 + theta2)
        torque2 = (fuerza2 * d2_cm_rel) + (fuerzaCarga * d_carga_rel)
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        x_base = w * 0.2
        y_base = h * 0.8
        
        x_codo = x_base + long1 * math.cos(theta1)
        y_codo = y_base - long1 * math.sin(theta1)
        
        x_efector = x_codo + long2 * math.cos(theta1 + theta2)
        y_efector = y_codo - long2 * math.sin(theta1 + theta2)
        
        return {
            "m1": masa1, "l1": long1,
            "m2": masa2, "l2": long2,
            "mc": masaCarga,
            "theta1_deg": theta1_deg, "theta2_deg": theta2_deg,
            "torque1": torque1, "torque2": torque2,
            "coords": {
                "x_base": x_base, "y_base": y_base,
                "x_codo": x_codo, "y_codo": y_codo,
                "x_efector": x_efector, "y_efector": y_efector
            }
        }

    def dibujar_diagrama(self, coords, long1, long2):
        """Dibuja el esquema del brazo robótico."""
        self.canvas.delete("all")
        
        x_base = coords["x_base"]
        y_base = coords["y_base"]
        x_codo = coords["x_codo"]
        y_codo = coords["y_codo"]
        x_efector = coords["x_efector"]
        y_efector = coords["y_efector"]

        long_total = long1 + long2
        if long_total == 0: long_total = 1
        
        escala = (self.canvas.winfo_width() * 0.75) / long_total
        
        x_codo = x_base + (x_codo - x_base) * escala
        y_codo = y_base - (y_base - y_codo) * escala
        x_efector = x_base + (x_efector - x_base) * escala
        y_efector = y_base - (y_base - y_efector) * escala

        self.canvas.create_line(x_base, y_base, x_codo, y_codo, width=8, fill="gray")
        self.canvas.create_line(x_codo, y_codo, x_efector, y_efector, width=6, fill="gray")
        self.canvas.create_oval(x_base - 10, y_base - 10, x_base + 10, y_base + 10, fill="black")
        self.canvas.create_text(x_base, y_base + 15, text="Base (T1)", anchor="n")
        self.canvas.create_oval(x_codo - 8, y_codo - 8, x_codo + 8, y_codo + 8, fill="gray50")
        self.canvas.create_rectangle(x_efector - 10, y_efector - 10, x_efector + 10, y_efector + 10, fill="red")
        self.canvas.create_line(0, y_base, self.canvas.winfo_width(), y_base, fill="black", dash=(4, 2))


    # --- FUNCIÓN MODIFICADA ---
    def generar_reporte(self):
        """Crea y MUESTRA un archivo de reporte en una ventana emergente."""
        
        # 1. Obtener los datos actuales
        try:
            datos = self.calcular_torques_y_posiciones()
            if not datos:
                return
        except ValueError:
            messagebox.showerror("Error", "Datos de entrada inválidos. No se puede generar el reporte.")
            return

        # 2. Definir el contenido del reporte (igual que antes)
        contenido = f"""# Análisis del Simulador de Torque Robótico

## 1. Resumen de Parámetros de Simulación

Estos son los datos de entrada utilizados para este cálculo:

* **Masa Eslabón 1 (m1):** {datos['m1']} kg
* **Longitud Eslabón 1 (l1):** {datos['l1']} m
* **Masa Eslabón 2 (m2):** {datos['m2']} kg
* **Longitud Eslabón 2 (l2):** {datos['l2']} m
* **Masa de la Carga (mc):** {datos['mc']} kg
* **Ángulo Base (θ1):** {datos['theta1_deg']:.1f}°
* **Ángulo Codo (θ2):** {datos['theta2_deg']:.1f}°

---

## 2. Resultados y Análisis de Comportamiento

Los cálculos de torque estático (la fuerza para *sostener* la carga contra la gravedad) para esta posición específica son:

* **Torque Articulación 1 (Base):** {datos['torque1']:.2f} Nm
* **Torque Articulación 2 (Codo):** {datos['torque2']:.2f} Nm

### Cómo Actuaría la Máquina

Con esta configuración, la máquina (el robot) debe ejercer {datos['torque1']:.2f} Nm en su base y {datos['torque2']:.2f} Nm en el codo solo para *mantenerse quieto*.

**Análisis Crítico:**
Estos valores de torque son **altamente dependientes** de los ángulos. El torque máximo (el peor escenario para sus motores) casi siempre ocurre cuando el brazo está extendido horizontalmente (ángulos θ1 y θ2 cercanos a 0°), ya que el "brazo de palanca" de la gravedad es máximo.

---

## 3. Gráfico Conceptual y "Margen de Error"

### Gráfico (Conceptual)

Un gráfico de **Torque vs. Ángulo del Brazo** (para esta carga) no es lineal. Seguiría una curva de Coseno. El torque sería MÁXIMO en 0° (horizontal) y caería a CERO en 90° (vertical). Sus {datos['theta1_deg']:.1f}° actuales se encuentran en algún punto de esa curva.

### Margen de Error (Factor de Seguridad)

¡IMPORTANTE! Los valores calculados son **estáticos**. No incluyen la fuerza necesaria para *acelerar* el brazo (torque dinámico), que es mucho mayor.

En ingeniería, nunca se usa el valor exacto. Se aplica un **Factor de Seguridad (FdS)**.

* **Motor Base (T1) Recomendado (con FdS 1.5x):** {datos['torque1']:.2f} Nm * 1.5 = **{datos['torque1'] * 1.5:.2f} Nm**
* **Motor Codo (T2) Recomendado (con FdS 1.5x):** {datos['torque2']:.2f} Nm * 1.5 = **{datos['torque2'] * 1.5:.2f} Nm**

Este "margen" asegura que el motor pueda manejar la aceleración, el frenado y cualquier imprecisión en las masas o longitudes de los componentes.
"""
        
        # 3. --- NUEVO: Crear la ventana emergente ---
        reporte_window = tk.Toplevel(self.root)
        reporte_window.title("Visor de Reporte de Simulación")
        reporte_window.geometry("650x700") # Tamaño de la ventana emergente
        reporte_window.transient(self.root) # Mantenerla al frente
        reporte_window.grab_set() # Bloquear la ventana principal

        # 4. Crear un Frame para el texto y el scrollbar
        text_frame = ttk.Frame(reporte_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 5. Añadir Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
        
        # 6. Añadir Widget de Texto
        # Usamos una fuente monoespaciada para que se vea como "código"
        texto_reporte = tk.Text(text_frame, wrap="word", 
                                font=("Courier New", 10), 
                                yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=texto_reporte.yview)
        
        scrollbar.pack(side="right", fill="y")
        texto_reporte.pack(side="left", fill="both", expand=True)
        
        # 7. Insertar el contenido y hacerlo de solo lectura
        texto_reporte.insert("1.0", contenido)
        texto_reporte.config(state="disabled") # Para que no se pueda editar

        # --- Función interna para el botón de guardar ---
        def guardar_contenido():
            try:
                filepath = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[
                        ("Archivos de Texto", "*.txt"),
                        ("Documentos Markdown", "*.md"),
                        ("Todos los Archivos", "*.*")
                    ],
                    title="Guardar Reporte de Simulación"
                )

                if not filepath:
                    return # El usuario canceló

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(contenido) # "contenido" viene de la función exterior
                
                messagebox.showinfo("Éxito", f"Reporte guardado exitosamente en:\n{filepath}",
                                    parent=reporte_window) # Mostrar mensaje sobre la ventana emergente

            except Exception as e:
                messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo.\nError: {e}",
                                     parent=reporte_window)

        # 8. Añadir el botón de "Guardar" DENTRO de la ventana emergente
        boton_guardar = ttk.Button(reporte_window, 
                                   text="Guardar Reporte como...", 
                                   command=guardar_contenido)
        boton_guardar.pack(pady=10, padx=10, fill="x")


# --- Bloque principal para ejecutar la aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotTorqueApp(root)
    root.geometry("900x600")
    root.mainloop()