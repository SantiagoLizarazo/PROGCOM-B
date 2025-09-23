import pygame
import sys
import random
import time
import json
import os

# Inicializar pygame
pygame.init()

# Configuración de la pantalla (tamaño similar al HTML)
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Quest - Juego Educativo")

# Colores IDÉNTICOS al HTML
BG_COLOR = (28, 18, 48)       # Azul-morado muy oscuro
CARD_COLOR = (44, 28, 84)     # Morado oscuro para paneles
ACCENT_COLOR = (102, 51, 204) # Morado vibrante para acentos
MUTED_COLOR = (120, 120, 180) # Azul-morado suave para textos secundarios
GOOD_COLOR = (72, 61, 139)    # Azul-morado para correcto
BAD_COLOR = (186, 85, 211)    # Morado claro para error
TEXT_COLOR = (220, 210, 255)  # Blanco con tinte violeta

# Fuentes
def get_font(size, bold=False):
    try:
        # Priorizar fuente compatible con emojis
        font_names = ['Segoe UI Emoji', 'Arial', 'Helvetica', 'Verdana', 'Segoe UI']
        for font_name in font_names:
            try:
                font = pygame.font.SysFont(font_name, size, bold=bold)
                return font
            except:
                continue
        return pygame.font.Font(None, size)
    except:
        return pygame.font.Font(None, size)

font_small = get_font(12)
font_medium = get_font(16)
font_large = get_font(20)
font_xlarge = get_font(28, bold=True)
font_title = get_font(20, bold=True)
font_question = get_font(44, bold=True)

# Estado del juego
class GameState:
    def __init__(self):
        self.difficulty = "medium"
        self.time_per_question = 18
        self.questions_per_game = 10
        self.score = 0
        self.lives = 3
        self.streak = 0
        self.highscore = self.load_highscore()
        self.current_question = 0
        self.active_question = None
        self.waiting_answer = False
        self.game_started = False
        self.game_over = False
        self.time_left = 0
        self.start_time = 0
        self.last_change = "Esperando inicio"
        self.status = "Listo"
        self.explanation = ""
        self.explanation_type = ""
        
    def load_highscore(self):
        try:
            if os.path.exists("mathquest_highscore.json"):
                with open("mathquest_highscore.json", "r") as f:
                    data = json.load(f)
                    return data.get("highscore", 0)
        except:
            pass
        return 0
    
    def save_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            try:
                with open("mathquest_highscore.json", "w") as f:
                    json.dump({"highscore": self.highscore}, f)
            except:
                pass

# Función para dibujar paneles con efecto glass (como en HTML)
def draw_glass_panel(surface, rect, border_radius=12):
    # Crear superficie con alpha para efecto glass
    panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Fondo principal
    pygame.draw.rect(panel_surface, (*CARD_COLOR, 200), (0, 0, rect.width, rect.height), 
                    border_radius=border_radius)
    
    # Borde sutil
    pygame.draw.rect(panel_surface, (255, 255, 255, 30), (0, 0, rect.width, rect.height), 
                    width=1, border_radius=border_radius)
    
    surface.blit(panel_surface, rect)

# Generador de preguntas
def generate_question(difficulty):
    ops = ['+', '-', '×', '÷']
    op = random.choice(ops)
    
    if difficulty == "easy":
        a = random.randint(1, 12)
        b = random.randint(1, 12)
    elif difficulty == "medium":
        a = random.randint(2, 30)
        b = random.randint(2, 20)
    else:  # hard
        a = random.randint(5, 120)
        b = random.randint(2, 40)
    
    if op == '÷':
        b = max(1, b)
        a = a * b
        answer = a // b
        explain = f"{a} ÷ {b} = {answer}"
    elif op == '×':
        answer = a * b
        explain = f"{a} × {b} = {answer}"
    elif op == '+':
        answer = a + b
        explain = f"{a} + {b} = {answer}"
    else:  # -
        if random.random() < 0.2:
            answer = a - b
        else:
            if a < b:
                a, b = b, a
            answer = a - b
        explain = f"{a} - {b} = {answer}"
    
    choices = set()
    choices.add(answer)
    
    while len(choices) < 4:
        perturb = max(1, int(abs(answer) * (0.05 + random.random() * 0.4)))
        sign = -1 if random.random() < 0.5 else 1
        candidate = answer + sign * random.randint(1, max(2, perturb))
        if op == '÷':
            candidate = round(candidate, 2)
        choices.add(candidate)
    
    choices = list(choices)
    random.shuffle(choices)
    
    return {
        'op': op,
        'a': a,
        'b': b,
        'answer': answer,
        'explain': explain,
        'choices': choices,
        'raw': f"{a} {op} {b}"
    }

# Cálculo de puntos
def calculate_points(time_left, streak):
    base = 100
    time_bonus = max(0, int(time_left * 5))
    streak_mult = 1 + min(0.5, streak * 0.05)
    return int((base + time_bonus) * streak_mult)

# Clase para botones
class Button:
    def __init__(self, x, y, width, height, text, color=MUTED_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        self.disabled = False
    
    def draw(self, surface):
        # Fondo del botón (efecto glass como en HTML)
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (255, 255, 255, 10), (0, 0, self.rect.width, self.rect.height), 
                        border_radius=8)
        pygame.draw.rect(s, (255, 255, 255, 30), (0, 0, self.rect.width, self.rect.height), 
                        width=1, border_radius=8)
        
        # Efecto hover
        if self.hover and not self.disabled:
            pygame.draw.rect(s, (255, 255, 255, 20), (0, 0, self.rect.width, self.rect.height), 
                            border_radius=8)
        
        surface.blit(s, self.rect)
        
        # Texto del botón
        text_color = self.color if not self.disabled else (100, 100, 100)
        text_surf = font_medium.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

# Clase para dropdowns
class Dropdown:
    def __init__(self, x, y, width, height, options, selected_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = selected_index
        self.expanded = False
    
    def draw(self, surface):
        # Fondo del dropdown
        draw_glass_panel(surface, self.rect, 8)
        
        # Texto seleccionado
        text_surf = font_small.render(self.options[self.selected_index], True, MUTED_COLOR)
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)
        
        # Flecha indicadora
        points = [
            (self.rect.right - 20, self.rect.centery - 5),
            (self.rect.right - 10, self.rect.centery - 5),
            (self.rect.right - 15, self.rect.centery + 5)
        ]
        pygame.draw.polygon(surface, MUTED_COLOR, points)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Cambiar opción (simplificado)
                self.selected_index = (self.selected_index + 1) % len(self.options)
                return True
        return False

# Función principal del juego
def main():
    game = GameState()
    clock = pygame.time.Clock()
    
    # Elementos de la interfaz
    difficulty_dropdown = Dropdown(700, 20, 120, 30, ["Fácil", "Media", "Difícil"])
    time_dropdown = Dropdown(830, 20, 80, 30, ["12s", "18s", "25s"])
    questions_dropdown = Dropdown(700, 550, 60, 30, ["5", "10", "15"])
    
    start_button = Button(920, 20, 70, 30, "Iniciar")
    hint_button = Button(700, 450, 120, 40, "💡 Pista")
    skip_button = Button(830, 450, 120, 40, "⏭ Saltar")

    # Cuadrículas de respuesta más pequeñas
    answer_buttons = [
        Button(0, 0, 160, 40, ""),
        Button(0, 0, 160, 40, ""),
        Button(0, 0, 160, 40, ""),
        Button(0, 0, 160, 40, "")
    ]
    
    running = True
    while running:
        current_time = time.time()
        
        # Actualizar temporizador
        if game.game_started and not game.game_over and game.waiting_answer:
            elapsed = current_time - game.start_time
            game.time_left = max(0, game.time_per_question - elapsed)
            
            if game.time_left <= 0:
                # Tiempo agotado
                game.lives -= 1
                game.streak = 0
                game.last_change = "Tiempo agotado"
                game.explanation = f"Se agotó el tiempo. La respuesta correcta era {game.active_question['answer']}. {game.active_question['explain']}"
                game.explanation_type = "bad"
                game.current_question += 1
                game.waiting_answer = False
                
                if game.lives <= 0 or game.current_question >= game.questions_per_game:
                    game.game_over = True
                    game.status = "Terminado"
                    game.save_highscore()
                else:
                    # Siguiente pregunta después de un delay
                    pygame.time.delay(1600)
                    next_question(game)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Manejo de dropdowns
            if difficulty_dropdown.handle_event(event):
                game.difficulty = ["easy", "medium", "hard"][difficulty_dropdown.selected_index]
            
            if time_dropdown.handle_event(event):
                game.time_per_question = [12, 18, 25][time_dropdown.selected_index]
            
            if questions_dropdown.handle_event(event):
                game.questions_per_game = [5, 10, 15][questions_dropdown.selected_index]
            
            # Clicks del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Botón de inicio
                if start_button.rect.collidepoint(event.pos) and not game.game_started:
                    start_game(game)
                
                # Botones de respuesta
                if game.waiting_answer and not game.game_over:
                    for i, btn in enumerate(answer_buttons):
                        if btn.rect.collidepoint(event.pos) and not btn.disabled:
                            handle_answer(game, i, btn)
                
                # Botón de pista
                if hint_button.rect.collidepoint(event.pos) and game.waiting_answer and not game.game_over:
                    use_hint(game)
                
                # Botón de saltar
                if skip_button.rect.collidepoint(event.pos) and game.waiting_answer and not game.game_over:
                    skip_question(game)
            
            # Atajos de teclado
            if event.type == pygame.KEYDOWN:
                if not game.game_started and event.key == pygame.K_r:
                    start_game(game)
                
                if game.waiting_answer and not game.game_over:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        idx = event.key - pygame.K_1
                        if idx < len(answer_buttons) and not answer_buttons[idx].disabled:
                            handle_answer(game, idx, answer_buttons[idx])
                    elif event.key == pygame.K_h:
                        use_hint(game)
                    elif event.key == pygame.K_r:
                        start_game(game)
        
        # Actualizar estado de hover
        mouse_pos = pygame.mouse.get_pos()
        start_button.hover = start_button.rect.collidepoint(mouse_pos)
        hint_button.hover = hint_button.rect.collidepoint(mouse_pos)
        skip_button.hover = skip_button.rect.collidepoint(mouse_pos)
        
        for btn in answer_buttons:
            btn.hover = btn.rect.collidepoint(mouse_pos)
        
        # DIBUJAR INTERFAZ
        # Fondo
        screen.fill(BG_COLOR)

        # Panel principal (container)
        main_rect = pygame.Rect(50, 50, WIDTH-100, HEIGHT-100)
        draw_glass_panel(screen, main_rect, 14)

        # Encabezado centrado
        title_text = font_title.render("🧠 Math Quest — Practica aritmética rápido", True, TEXT_COLOR)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 70))

        # Controles de dificultad y tiempo (alineados a la derecha)
        diff_label = font_small.render("Dificultad", True, MUTED_COLOR)
        screen.blit(diff_label, (WIDTH-320, 5))
        difficulty_dropdown.draw(screen)

        time_label = font_small.render("Tiempo/pregunta", True, MUTED_COLOR)
        screen.blit(time_label, (WIDTH-190, 5))
        time_dropdown.draw(screen)

        start_button.draw(screen)

        # Panel lateral izquierdo (estadísticas)
        left_panel = pygame.Rect(70, 120, 300, 500)
        draw_glass_panel(screen, left_panel, 12)

        # Estadísticas (centradas en el panel)
        stats_data = [
            ("Puntuación", str(game.score), 160),
            ("Vidas", str(game.lives), 220),
            ("Racha", str(game.streak), 280)
        ]
        for label, value, y in stats_data:
            label_text = font_small.render(label, True, MUTED_COLOR)
            screen.blit(label_text, (left_panel.centerx - label_text.get_width()//2, y))
            value_text = font_xlarge.render(value, True, TEXT_COLOR)
            screen.blit(value_text, (left_panel.centerx - value_text.get_width()//2, y+18))

        # Récord
        record_label = font_small.render("Récord", True, MUTED_COLOR)
        screen.blit(record_label, (left_panel.centerx - record_label.get_width()//2, 340))
        record_value = font_large.render(str(game.highscore), True, TEXT_COLOR)
        screen.blit(record_value, (left_panel.centerx - record_value.get_width()//2, 360))
        record_note = font_small.render("Guarda tu récord localmente", True, MUTED_COLOR)
        screen.blit(record_note, (left_panel.centerx - record_note.get_width()//2, 390))

        # Progreso
        progress_label = font_small.render("Progreso", True, MUTED_COLOR)
        screen.blit(progress_label, (left_panel.centerx - progress_label.get_width()//2, 430))
        progress_text = font_small.render(f"{game.current_question}/{game.questions_per_game}", True, MUTED_COLOR)
        screen.blit(progress_text, (left_panel.centerx - progress_text.get_width()//2, 450))

        # Barra de progreso
        progress_bg = pygame.Rect(left_panel.left+20, 470, left_panel.width-40, 10)
        pygame.draw.rect(screen, (255, 255, 255, 30), progress_bg, border_radius=5)
        if game.questions_per_game > 0:
            progress_width = (left_panel.width-40) * (game.current_question / game.questions_per_game)
            progress_fg = pygame.Rect(left_panel.left+20, 470, progress_width, 10)
            pygame.draw.rect(screen, ACCENT_COLOR, progress_fg, border_radius=5)

        # Panel central (pregunta y respuestas)
        center_panel = pygame.Rect(400, 120, 520, 500)
        draw_glass_panel(screen, center_panel, 12)

        # Pregunta
        if game.game_started and not game.game_over and game.active_question:
            question_bg = pygame.Rect(center_panel.left+20, 140, center_panel.width-40, 100)
            pygame.draw.rect(screen, (30, 30, 40, 230), question_bg, border_radius=10)

            # Pregunta centrada y grande
            question_text = font_question.render(game.active_question['raw'], True, (255,255,255))
            screen.blit(question_text, (center_panel.centerx - question_text.get_width()//2, 170))

            # Temporizador
            timer_text = font_large.render(f"{int(game.time_left)}s", True, ACCENT_COLOR)
            screen.blit(timer_text, (center_panel.left+40, 250))
            timer_label = font_small.render("Tiempo restante", True, MUTED_COLOR)
            screen.blit(timer_label, (center_panel.left+90, 255))

            # Botones de pista y saltar (centrados abajo)
            hint_button.rect.topleft = (center_panel.left+60, 450)
            skip_button.rect.topleft = (center_panel.left+200, 450)
            hint_button.draw(screen)
            skip_button.draw(screen)

            # Respuestas (centradas, más pequeñas y con fondo oscuro)
            if game.active_question and game.waiting_answer:
                # Espaciado y centrado
                btn_w, btn_h = 160, 40
                gap_x, gap_y = 40, 20
                start_x = center_panel.centerx - btn_w - gap_x//2
                start_y = 340
                emoji_list = ['1️⃣','2️⃣','3️⃣','4️⃣']
                for i, choice in enumerate(game.active_question['choices']):
                    answer_buttons[i].text = f"{emoji_list[i]} {choice}"
                    x = start_x + (i%2)*(btn_w + gap_x)
                    y = start_y + (i//2)*(btn_h + gap_y)
                    answer_buttons[i].rect.topleft = (x, y)
                    answer_buttons[i].draw(screen)
        else:
            if game.game_over:
                question_text = font_question.render("Juego terminado", True, TEXT_COLOR)
                screen.blit(question_text, (center_panel.centerx - question_text.get_width()//2, 170))
                
                score_text = font_medium.render(f"Puntuación final: {game.score}", True, MUTED_COLOR)
                screen.blit(score_text, (center_panel.centerx - score_text.get_width()//2, 220))
            else:
                question_text = font_question.render("Pulsa Iniciar para comenzar", True, TEXT_COLOR)
                screen.blit(question_text, (center_panel.centerx - question_text.get_width()//2, 170))
        
        # Explicación (centrada y con fondo más visible)
        if game.explanation:
            explanation_bg = pygame.Rect(center_panel.left+20, 500, center_panel.width-40, 60)
            pygame.draw.rect(screen, (30, 30, 40, 230), explanation_bg, border_radius=8)
            explanation_color = GOOD_COLOR if game.explanation_type == "good" else BAD_COLOR
            explanation_text = font_small.render(game.explanation, True, explanation_color)
            screen.blit(explanation_text, (center_panel.centerx - explanation_text.get_width()//2, 520))
        
        # Configuración extra
        extra_label = font_small.render("Preguntas por partida", True, MUTED_COLOR)
        screen.blit(extra_label, (700, 530))
        questions_dropdown.draw(screen)
        
        # Estado del juego
        status_text = font_small.render(f"Estado: {game.status}", True, MUTED_COLOR)
        screen.blit(status_text, (420, 580))
        
        last_change_text = font_small.render(f"Último cambio: {game.last_change}", True, MUTED_COLOR)
        screen.blit(last_change_text, (420, 600))
        
        # Pie de página
        footer_text = font_small.render("Math Quest — Hecho con ❤️ — Versión Pygame 1.0", True, MUTED_COLOR)
        screen.blit(footer_text, (WIDTH//2 - footer_text.get_width()//2, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

# Funciones del juego
def start_game(game):
    game.game_started = True
    game.game_over = False
    game.score = 0
    game.lives = 3
    game.streak = 0
    game.current_question = 0
    game.status = "Jugando"
    game.last_change = "Comenzó el juego"
    game.explanation = ""
    next_question(game)

def next_question(game):
    if game.current_question >= game.questions_per_game:
        end_game(game, "Todas las preguntas respondidas")
        return
    
    game.active_question = generate_question(game.difficulty)
    game.waiting_answer = True
    game.start_time = time.time()
    game.explanation = ""

def handle_answer(game, choice_idx, button):
    if not game.waiting_answer:
        return
    
    game.waiting_answer = False
    choice = game.active_question['choices'][choice_idx]
    correct = abs(choice - game.active_question['answer']) < 0.001
    
    if correct:
        pts = calculate_points(game.time_left, game.streak)
        game.score += pts
        game.streak += 1
        game.last_change = f"Respuesta correcta (+{pts} pts)"
        game.explanation = f"{game.active_question['explain']} — Ganaste {pts} puntos."
        game.explanation_type = "good"
    else:
        game.lives -= 1
        game.streak = 0
        game.last_change = "Respuesta incorrecta"
        game.explanation = f"Incorrecto. La respuesta correcta era {game.active_question['answer']}. {game.active_question['explain']}"
        game.explanation_type = "bad"
    
    game.current_question += 1
    
    if game.lives <= 0 or game.current_question >= game.questions_per_game:
        game.game_over = True
        game.status = "Terminado"
        game.save_highscore()
    else:
        pygame.time.delay(1400)
        next_question(game)

def use_hint(game):
    if not game.waiting_answer:
        return
    # Eliminar una opción incorrecta (si hay más de 2 opciones)
    wrong_choices = [c for c in game.active_question['choices'] if c != game.active_question['answer']]
    if len(wrong_choices) > 1:
        to_remove = random.choice(wrong_choices)
        game.active_question['choices'].remove(to_remove)
        game.last_change = "Pista usada: opción incorrecta eliminada"
        game.explanation = "Se eliminó una opción incorrecta."
        game.explanation_type = "good"
    else:
        game.last_change = "No hay suficientes opciones para eliminar"
        game.explanation = "Ya solo quedan dos opciones."
        game.explanation_type = "bad"

def skip_question(game):
    if not game.waiting_answer:
        return
    
    game.waiting_answer = False
    game.lives -= 1
    game.streak = 0
    game.last_change = "Pregunta saltada (-1 vida)"
    game.explanation = f"Saltaste la pregunta. La respuesta correcta era {game.active_question['answer']}."
    game.explanation_type = "bad"
    game.current_question += 1
    
    if game.lives <= 0 or game.current_question >= game.questions_per_game:
        game.game_over = True
        game.status = "Terminado"
        game.save_highscore()
    else:
        pygame.time.delay(1300)
        next_question(game)

def end_game(game, reason):
    game.game_over = True
    game.status = "Terminado"
    game.last_change = reason
    game.save_highscore()

if __name__ == "__main__":
    main()