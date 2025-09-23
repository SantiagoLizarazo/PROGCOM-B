import tkinter as tk
import random
from tkinter import messagebox

# Reglas del juego
# spock vence a tijeras y a piedra
# tijeras vence a papel y a lagarto
# papel vence a piedra y a spock
# piedra vence a lagarto y a tijeras
# lagarto vence a spock y a papel

rules = {
    "tijeras": ["papel", "lagarto"],
    "papel": ["piedra", "spock"],
    "piedra": ["lagarto", "tijeras"],
    "lagarto": ["spock", "papel"],
    "spock": ["tijeras", "piedra"]
}

# Mapeo de opciones a emojis
emojis = {
    "piedra": "🗿",
    "papel": "📄",
    "tijeras": "✂️",
    "lagarto": "🦎",
    "spock": "🖖"
}

# Opciones para el juego
opciones = ["piedra", "papel", "tijeras", "lagarto", "spock"]

def jugar(eleccion_jugador):
    """
    Función principal para manejar la lógica del juego.
    """
    eleccion_pc = random.choice(opciones)
    
    # Mostrar las elecciones en la interfaz
    lbl_eleccion_jugador.config(text=f"Tu elección: {emojis[eleccion_jugador]}")
    lbl_eleccion_pc.config(text=f"Elección de la PC: {emojis[eleccion_pc]}")
    
    resultado = determinar_ganador(eleccion_jugador, eleccion_pc)
    
    lbl_resultado.config(text=resultado)
    
    # Mensaje de victoria/derrota
    if "¡Ganaste!" in resultado:
        messagebox.showinfo("Resultado", "🎉 ¡Felicidades, ganaste! 🎉")
    elif "¡Perdiste!" in resultado:
        messagebox.showinfo("Resultado", "😢 Lo siento, perdiste. 😢")
    else:
        messagebox.showinfo("Resultado", "🤝 ¡Es un empate! 🤝")

def determinar_ganador(jugador, pc):
    """
    Determina quién gana según las reglas.
    """
    if jugador == pc:
        return "¡Empate!"
    elif pc in rules[jugador]:
        return "¡Ganaste!"
    else:
        return "¡Perdiste!"

# Configuración de la ventana principal de tkinter
root = tk.Tk()
root.title("Piedra, Papel, Tijera, Lagarto, Spock")
root.geometry("400x350")
root.configure(bg="#f0f0f0")

# --- Creación de los widgets ---

# Título del juego
lbl_titulo = tk.Label(root, text="Elige tu jugada:", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
lbl_titulo.pack(pady=10)

# Contenedor para los botones
frame_botones = tk.Frame(root, bg="#f0f0f0")
frame_botones.pack(pady=10)

# Botones con emojis
for opcion, emoji in emojis.items():
    tk.Button(
        frame_botones, 
        text=emoji, 
        font=("Helvetica", 30), 
        width=3,
        height=1,
        command=lambda o=opcion: jugar(o)
    ).pack(side=tk.LEFT, padx=5)

# Separador visual
tk.Frame(root, height=2, bg="gray").pack(fill=tk.X, padx=20, pady=10)

# Etiquetas para mostrar las elecciones y el resultado
lbl_eleccion_jugador = tk.Label(root, text="Tu elección: ", font=("Helvetica", 14), bg="#f0f0f0")
lbl_eleccion_jugador.pack(pady=5)

lbl_eleccion_pc = tk.Label(root, text="Elección de la PC: ", font=("Helvetica", 14), bg="#f0f0f0")
lbl_eleccion_pc.pack(pady=5)

lbl_resultado = tk.Label(root, text="¡A jugar! 🎲", font=("Helvetica", 18, "bold"), fg="#333", bg="#f0f0f0")
lbl_resultado.pack(pady=10)

# Bucle principal de la interfaz
root.mainloop()