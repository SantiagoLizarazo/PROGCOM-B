import string # Usaremos esto para la regla 40

print("=== JUEGO DE LA CONTRASEÑA (Versión Extendida) ===")
contrasena = input("Ingresa tu contraseña: ")

# --- INICIALIZACIÓN DE REGLAS ---

# Reglas básicas (5)
tiene_mayus = False
tiene_minus = False
tiene_numero = False
tiene_simbolo = False
longitud_valida = False # (>= 8)

# 40 Nuevas Reglas
# Reglas de longitud (3)
longitud_maxima = False # (<= 50)
longitud_par = False
longitud_no_primo = False # (Longitud NO debe ser 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)

# Reglas de inicio y fin (4)
empieza_con_letra_P_mayus = False
termina_con_letra_a_minus = False
no_empieza_con_numero = False
no_termina_con_simbolo = False

# Reglas de contenido específico (20)
tiene_letra_q = False
tiene_letra_z = False
tiene_letra_j = False
tiene_letra_k = False
tiene_letra_w = False
tiene_letra_A_mayus = False
tiene_letra_Z_mayus = False
tiene_letra_J_mayus = False
tiene_letra_K_mayus = False
tiene_letra_W_mayus = False
tiene_num_0 = False
tiene_num_5 = False
tiene_num_9 = False
tiene_simbolo_arroba = False
tiene_simbolo_gato = False # '#'
tiene_simbolo_dolar = False # '$'
tiene_simbolo_porc = False # '%'
tiene_simbolo_y = False # '&'
tiene_simbolo_guionbajo = False # '_'
tiene_simbolo_mas = False # '+'

# Reglas de "no contenido" (5)
no_tiene_tres_letras_seguidas = True # (Ej: "abc" o "123" o "aaa")
no_tiene_secuencias_faciles = True # (No "123", "abc", "qwerty")
no_contiene_palabra_password = True
no_contiene_palabra_admin = True
no_contiene_palabra_user = True

# Reglas de conteo (3)
al_menos_dos_numeros = False
al_menos_dos_simbolos = False
al_menos_tres_mayusculas = False

# Reglas de posición (2)
tercer_caracter_es_letra = False
penultimo_caracter_es_numero = False

# Reglas misceláneas (3)
tiene_espacio = False
tiene_caracteres_no_ascii = False # (Ej: á, é, ñ, ç)
todos_los_simbolos_son_basicos = True # (No símbolos raros como © ó ™)

# --- Variables de conteo ---
conteo_numeros = 0
conteo_simbolos = 0
conteo_mayusculas = 0
simbolos_definidos = "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~"
simbolos_basicos_ascii = set(string.punctuation)

# --- REVISIÓN DE CADA CARÁCTER ---
for i, c in enumerate(contrasena):
    
    # Revisión general (Reglas 1-4)
    if c.isupper():
        tiene_mayus = True
        conteo_mayusculas += 1
    elif c.islower():
        tiene_minus = True
    elif c.isdigit():
        tiene_numero = True
        conteo_numeros += 1
    elif c in simbolos_definidos:
        tiene_simbolo = True
        conteo_simbolos += 1
        
    # Reglas de contenido específico (20)
    if c == 'q': tiene_letra_q = True
    elif c == 'z': tiene_letra_z = True
    elif c == 'j': tiene_letra_j = True
    elif c == 'k': tiene_letra_k = True
    elif c == 'w': tiene_letra_w = True
    elif c == 'A': tiene_letra_A_mayus = True
    elif c == 'Z': tiene_letra_Z_mayus = True
    elif c == 'J': tiene_letra_J_mayus = True
    elif c == 'K': tiene_letra_K_mayus = True
    elif c == 'W': tiene_letra_W_mayus = True
    elif c == '0': tiene_num_0 = True
    elif c == '5': tiene_num_5 = True
    elif c == '9': tiene_num_9 = True
    elif c == '@': tiene_simbolo_arroba = True
    elif c == '#': tiene_simbolo_gato = True
    elif c == '$': tiene_simbolo_dolar = True
    elif c == '%': tiene_simbolo_porc = True
    elif c == '&': tiene_simbolo_y = True
    elif c == '_': tiene_simbolo_guionbajo = True
    elif c == '+': tiene_simbolo_mas = True
    
    # Regla de espacio
    if c == ' ': tiene_espacio = True

    # Regla de no-ascii
    if not c.isascii():
        tiene_caracteres_no_ascii = True
        
    # Regla de símbolos básicos
    if (not c.isalnum()) and (c not in simbolos_basicos_ascii):
        todos_los_simbolos_son_basicos = False

    # Regla de secuencias (3 seguidas)
    if i > 1:
        c1 = contrasena[i-2]
        c2 = contrasena[i-1]
        c3 = c
        # Secuencia numérica (ej: "123") o alfabética (ej: "abc")
        if ord(c1)+1 == ord(c2) and ord(c2)+1 == ord(c3):
            no_tiene_tres_letras_seguidas = False
        # Secuencia repetida (ej: "aaa")
        if c1 == c2 and c2 == c3:
            no_tiene_tres_letras_seguidas = False

# --- REVISIÓN GLOBAL (DESPUÉS DEL LOOP) ---

# Reglas de longitud (3 + 1 original)
if len(contrasena) >= 8:
    longitud_valida = True
if len(contrasena) <= 50:
    longitud_maxima = True
if len(contrasena) % 2 == 0:
    longitud_par = True
if len(contrasena) not in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    longitud_no_primo = True

# Reglas de conteo (3)
if conteo_numeros >= 2:
    al_menos_dos_numeros = True
if conteo_simbolos >= 2:
    al_menos_dos_simbolos = True
if conteo_mayusculas >= 3:
    al_menos_tres_mayusculas = True

# Reglas de "no contenido" (3)
if "password" in contrasena.lower():
    no_contiene_palabra_password = False
if "admin" in contrasena.lower():
    no_contiene_palabra_admin = False
if "user" in contrasena.lower():
    no_contiene_palabra_user = False
    
# Reglas de secuencias fáciles (2)
if "123" in contrasena or "abc" in contrasena.lower() or "qwerty" in contrasena.lower():
    no_tiene_secuencias_faciles = False

# Reglas de inicio y fin (4)
if len(contrasena) > 0:
    if contrasena.startswith('P'):
        empieza_con_letra_P_mayus = True
    if contrasena.endswith('a'):
        termina_con_letra_a_minus = True
        
    if not contrasena[0].isdigit():
        no_empieza_con_numero = True
        
    if contrasena[-1] not in simbolos_definidos:
        no_termina_con_simbolo = True
else:
    # Si está vacía, falla automáticamente las reglas de inicio/fin
    no_empieza_con_numero = False
    no_termina_con_simbolo = False

# Reglas de posición (2)
if len(contrasena) >= 3:
    if contrasena[2].isalpha():
        tercer_caracter_es_letra = True
if len(contrasena) >= 2:
    if contrasena[-2].isdigit():
        penultimo_caracter_es_numero = True

# --- VERIFICACIÓN FINAL ---

# Se combinan las 5 originales + 40 nuevas
if (tiene_mayus and tiene_minus and tiene_numero and tiene_simbolo and longitud_valida and
    longitud_maxima and longitud_par and longitud_no_primo and
    empieza_con_letra_P_mayus and termina_con_letra_a_minus and no_empieza_con_numero and no_termina_con_simbolo and
    tiene_letra_q and tiene_letra_z and tiene_letra_j and tiene_letra_k and tiene_letra_w and
    tiene_letra_A_mayus and tiene_letra_Z_mayus and tiene_letra_J_mayus and tiene_letra_K_mayus and tiene_letra_W_mayus and
    tiene_num_0 and tiene_num_5 and tiene_num_9 and
    tiene_simbolo_arroba and tiene_simbolo_gato and tiene_simbolo_dolar and tiene_simbolo_porc and tiene_simbolo_y and tiene_simbolo_guionbajo and tiene_simbolo_mas and
    no_tiene_tres_letras_seguidas and no_tiene_secuencias_faciles and no_contiene_palabra_password and no_contiene_palabra_admin and no_contiene_palabra_user and
    al_menos_dos_numeros and al_menos_dos_simbolos and al_menos_tres_mayusculas and
    tercer_caracter_es_letra and penultimo_caracter_es_numero and
    tiene_espacio and tiene_caracteres_no_ascii and todos_los_simbolos_son_basicos):
    
    print("✅ Contraseña aceptada, cumple las 45 reglas.")
else:
    print("❌ Contraseña rechazada. Faltan las siguientes reglas:")
    
    # Originales
    if not longitud_valida: print("- Debe tener al menos 8 caracteres")
    if not tiene_mayus: print("- Debe tener al menos una letra mayúscula")
    if not tiene_minus: print("- Debe tener al menos una letra minúscula")
    if not tiene_numero: print("- Debe tener al menos un número")
    if not tiene_simbolo: print("- Debe tener al menos un símbolo (!, @, #, $, %, etc.)")
    
    # Nuevas
    if not longitud_maxima: print("- Debe tener 50 caracteres o menos")
    if not longitud_par: print("- La longitud debe ser un número par")
    if not longitud_no_primo: print("- La longitud no puede ser un número primo problemático (11, 13, 17...)")
    if not empieza_con_letra_P_mayus: print("- Debe empezar con la letra 'P' mayúscula")
    if not termina_con_letra_a_minus: print("- Debe terminar con la letra 'a' minúscula")
    if not no_empieza_con_numero: print("- No debe empezar con un número")
    if not no_termina_con_simbolo: print("- No debe terminar con un símbolo")
    
    if not tiene_letra_q: print("- Debe contener la letra 'q'")
    if not tiene_letra_z: print("- Debe contener la letra 'z'")
    if not tiene_letra_j: print("- Debe contener la letra 'j'")
    if not tiene_letra_k: print("- Debe contener la letra 'k'")
    if not tiene_letra_w: print("- Debe contener la letra 'w'")
    if not tiene_letra_A_mayus: print("- Debe contener la letra 'A' mayúscula")
    if not tiene_letra_Z_mayus: print("- Debe contener la letra 'Z' mayúscula")
    if not tiene_letra_J_mayus: print("- Debe contener la letra 'J' mayúscula")
    if not tiene_letra_K_mayus: print("- Debe contener la letra 'K' mayúscula")
    if not tiene_letra_W_mayus: print("- Debe contener la letra 'W' mayúscula")
    
    if not tiene_num_0: print("- Debe contener el número '0'")
    if not tiene_num_5: print("- Debe contener el número '5'")
    if not tiene_num_9: print("- Debe contener el número '9'")
    
    if not tiene_simbolo_arroba: print("- Debe contener el símbolo '@'")
    if not tiene_simbolo_gato: print("- Debe contener el símbolo '#'")
    if not tiene_simbolo_dolar: print("- Debe contener el símbolo '$'")
    if not tiene_simbolo_porc: print("- Debe contener el símbolo '%'")
    if not tiene_simbolo_y: print("- Debe contener el símbolo '&'")
    if not tiene_simbolo_guionbajo: print("- Debe contener el símbolo '_'")
    if not tiene_simbolo_mas: print("- Debe contener el símbolo '+'")
    
    if not no_tiene_tres_letras_seguidas: print("- No debe tener 3 caracteres idénticos o secuenciales seguidos (ej: 'aaa' o '123')")
    if not no_tiene_secuencias_faciles: print("- No debe contener '123', 'abc' o 'qwerty'")
    if not no_contiene_palabra_password: print("- No debe contener la palabra 'password'")
    if not no_contiene_palabra_admin: print("- No debe contener la palabra 'admin'")
    if not no_contiene_palabra_user: print("- No debe contener la palabra 'user'")
    
    if not al_menos_dos_numeros: print("- Debe tener al menos dos números")
    if not al_menos_dos_simbolos: print("- Debe tener al menos dos símbolos")
    if not al_menos_tres_mayusculas: print("- Debe tener al menos tres mayúsculas")
    
    if not tercer_caracter_es_letra: print("- El tercer carácter debe ser una letra")
    if not penultimo_caracter_es_numero: print("- El penúltimo carácter debe ser un número")
    
    if not tiene_espacio: print("- Debe contener al menos un espacio en blanco")
    if not tiene_caracteres_no_ascii: print("- Debe contener al menos un carácter no ASCII (ej: ñ, á, ç)")
    if not todos_los_simbolos_son_basicos: print("- No debe usar símbolos extraños (ej: ©, ™, µ)")