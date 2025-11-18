import re

# --- REGLAS ---
# Lista de 100 reglas para la contraseña
reglas = [
 # Reglas Originales (1-20)
 "1. La contraseña debe tener mínimo 8 caracteres.",
 "2. Debe contener al menos una letra mayúscula.",
 "3. Debe contener al menos un número.",
 "4. Debe contener al menos un símbolo como *, #, $, %, &.",
 "5. No puede contener espacios.",
 "6. Debe contener al menos una palabra (ej: sol, blue, casa, cat...).",
 "7. No puede comenzar con un número.",
 "8. Debe incluir al menos una vocal.",
 "9. No puede repetir el mismo carácter más de 3 veces seguidas.",
 "10. Debe terminar con una letra.",
 "11. No puede tener secuencias como '123' o 'abc'.",
 "12. Debe tener al menos una letra doble (como 'll', 'ss', 'oo').",
 "13. Debe tener al menos una letra minúscula.",
 "14. No puede tener el nombre del jugador (si lo tiene).",
 "15. Debe tener al menos una consonante.",
 "16. No puede tener más de 2 símbolos seguidos.",
 "17. No puede contener la palabra 'password' ni 'contraseña'.",
 "18. Debe tener letras en diferentes posiciones (no todas juntas).",
 "19. No puede tener más de 5 números en total.",
 "20. Debe incluir al menos una letra de las siguientes: X, Y o Z.",
 "21. La longitud máxima de la contraseña es 32 caracteres.",
 "22. Debe tener al menos 2 letras mayúsculas.",
 "23. Debe tener al menos 2 letras minúsculas.",
 "24. Debe tener al menos 2 números.",
 "25. Debe tener al menos 2 símbolos de la lista (*, #, $, %, &).",
 "26. El número total de letras debe ser mayor que el de números.",
 "27. El número total de símbolos (*, #, $, %, &) debe ser 3 o menos.",
 "28. La longitud total de la contraseña debe ser un número impar.",
 "29. El número total de vocales debe ser un número par.",
 "30. El número de consonantes debe ser mayor que el de vocales.",
 "31. Debe tener más de 5 caracteres únicos.",
 "32. El número de mayúsculas y minúsculas debe ser diferente.",
 "33. Debe tener un número par de números pares (0, 2, 4, 6, 8).",
 "34. Debe tener un número impar de números impares (1, 3, 5, 7, 9).",
 "35. El número total de caracteres debe ser un número primo (ej: 11, 13, 17, 19, 23, 29, 31).",
 "36. No puede terminar con un número.",
 "37. No puede terminar con un símbolo (*, #, $, %, &).",
 "38. El segundo carácter debe ser una letra minúscula.",
 "39. El tercer carácter debe ser un número.",
 "40. El penúltimo carácter no puede ser una letra mayúscula.",
 "41. Debe tener un número en los primeros 4 caracteres.",
 "42. Debe tener un símbolo (*, #, $, %, &) en los últimos 4 caracteres.",
 "43. El primer y último carácter no pueden ser iguales.",
 "44. El primer y último carácter deben ser de tipo diferente (letra/número/símbolo).",
 "45. No puede tener un número y un símbolo juntos (en cualquier orden).",
 "46. Debe tener una letra mayúscula junto a una minúscula.",
 "47. La primera letra 'A' (si existe) debe ser mayúscula 'A'.",
 "48. El primer número (si existe) debe ir antes de la primera mayúscula (si existe).",
 "49. El primer símbolo (si existe) debe ir después de la primera minúscula (si existe).",
 "50. Todos los números (si existen) deben estar agrupados.",
 "51. Debe incluir al menos un símbolo de puntuación ( . , ; ).",
 "52. No puede contener paréntesis ( ) ni corchetes [ ].",
 "53. Debe incluir un guion - o un guion bajo _.",
 "54. No puede contener tildes (á, é, í, ó, ú) ni la letra 'ñ'.",
 "55. Debe incluir una letra 'poco común' (K, Q, W).",
 "56. No puede incluir más de 3 vocales seguidas.",
 "57. No puede incluir más de 3 consonantes seguidas.",
 "58. Debe incluir al menos un número par (0, 2, 4, 6, 8).",
 "59. Debe incluir al menos un número impar (1, 3, 5, 7, 9).",
 "60. La suma de todos los dígitos debe ser mayor a 5.",
 "61. No puede contener la letra 'O' (mayúscula) y el número '0' (cero) a la vez.",
 "62. No puede contener la letra 'l' (minúscula) y el número '1' a la vez.",
 "63. Debe incluir un símbolo matemático (+ o =).",
 "64. No puede contener la barra inclinada / o \\.",
 "65. La primera vocal de la contraseña debe ser 'A' o 'E' (may/min).",
 "66. No puede contener el símbolo '@' (arroba).",
 "67. No puede contener el símbolo '!' (admiración).",
 "68. Debe contener un número mayor a 5 (6, 7, 8, 9).",
 "69. Debe contener un número menor a 5 (0, 1, 2, 3, 4).",
 "70. Debe incluir un símbolo de llaves { }.",
 "71. No puede tener secuencias numéricas inversas (ej: 321, 987).",
 "72. No puede tener secuencias comunes del teclado (ej: qwerty, asdf, zxcv).",
 "73. No puede tener secuencias de letras inversas (ej: cba, zyx).",
 "74. No puede repetir un par de caracteres (ej: 'blabla' o '1212').",
 "75. No puede tener más de 2 letras mayúsculas consecutivas.",
 "76. No puede tener más de 2 letras minúsculas consecutivas.",
 "77. No puede ser un palíndromo (ignorando mayúsculas/minúsculas).",
 "78. No puede tener un número que sea un año común (1990-2029).",
 "79. Los números (si hay más de uno) no pueden estar en orden ascendente (ej: a1b5c9).",
 "80. El primer carácter no puede repetirse en el resto de la contraseña.",
 "81. El último carácter no puede repetirse en el resto de la contraseña.",
 "82. No puede tener la misma letra 3 veces, aunque no sea seguida.",
 "83. No puede tener el mismo número 3 veces, aunque no sea seguido.",
 "84. No puede tener el mismo símbolo (*, #, $, %, &) 3 veces, aunque no sea seguido.",
 "85. La 'palabra' (regla 6) no puede ser un palíndromo (ej: 'oso', 'radar').",
 "86. No puede contener 'admin', 'root' o '1234'.",
 "87. No puede contener meses del año (3 primeras letras, ej: 'ene', 'feb', 'jan', 'sep').",
 "88. No puede contener días de la semana (3 primeras letras, ej: 'lun', 'mar', 'mon', 'tue').",
 "89. No puede contener palabras del juego ('tic', 'tac', 'toe').",
 "90. La 'palabra' (regla 6) debe estar toda en MAYÚSCULAS.",
 "91. La 'palabra' (regla 6) no puede ser la primera parte de la contraseña.",
 "92. No puede contener 'hola' o 'hello'.",
 "93. Si se usa el nombre (regla 14), tampoco puede usarse al revés.",
 "94. No puede contener las 3 primeras letras del nombre (si nombre > 3).",
 "95. No puede contener las 3 últimas letras del nombre (si nombre > 3).",
 "96. No puede contener un color común (ej: 'rojo', 'verde', 'azul', 'red', 'blue').",
 "97. No puede contener 'juego' o 'game'.",
 "98. No puede contener 'sol' o 'luna'.",
 "99. No puede contener un nombre de planeta (ej: 'marte', 'venus', 'tierra').",
 "100. La contraseña no puede contener el número '100'."
]

# --- Funciones auxiliares para validaciones complejas ---

def _get_vowels(pwd):
 return re.findall(r"[aeiouAEIOU]", pwd)

def _get_consonants(pwd):
 return re.findall(r"[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]", pwd)

def _get_numbers(pwd):
 return re.findall(r"[0-9]", pwd)

def _get_symbols(pwd, symbol_set=r"[\*\#$\%\&]"):
 return re.findall(symbol_set, pwd)

def _get_letters(pwd):
 return re.findall(r"[a-zA-Z]", pwd)

def _is_prime(n):
 if n < 2: return False
 for i in range(2, int(n**0.5) + 1):
  if n % i == 0:
   return False
 return True

def _check_char_types(c1, c2):
 c1_type = 'letter' if c1.isalpha() else 'number' if c1.isdigit() else 'symbol'
 c2_type = 'letter' if c2.isalpha() else 'number' if c2.isdigit() else 'symbol'
 return c1_type != c2_type

# --- Funciones del Juego ---

def mostrar_reglas():
 print("\nREGLAS ACTUALES (100):")
 for r in reglas:
  print(r)
 print()

def validar_contraseña(pwd, nombre=""):
 # Funciones auxiliares internas para limpieza
 def _find_first(pattern, s):
  search = re.search(pattern, s)
  return search.start() if search else -1

 def _sum_digits(s):
  return sum(int(d) for d in _get_numbers(s))
 
 def _get_word(s):
  search = re.search(r"[a-zA-Z]{3,}", s)
  return search

 # Diccionarios para chequeos de palabras prohibidas
 common_words = {
  "months": r"ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic|jan|aug|sun", # "sun" colisiona
  "days": r"lun|mar|mie|jue|vie|sab|dom|mon|tue|wed|thu|fri|sat",
  "colors": r"rojo|verde|azul|blue|red|green|yellow|black|white",
  "planets": r"mercurio|venus|tierra|marte|jupiter|saturno|urano|neptuno",
  "simple": r"admin|root|1234|hola|hello|juego|game|sol|luna|sun|moon|tic|tac|toe"
 }
 
 # --- LISTA DE 100 VALIDACIONES ---
 validaciones = [
  # Reglas Originales (1-20)
  len(pwd) >= 8, # 1
  re.search(r"[A-Z]", pwd) != None, # 2
  re.search(r"[0-9]", pwd) != None, # 3
  re.search(r"[\*\#$\%\&]", pwd) != None, # 4
  " " not in pwd, # 5
  re.search(r"[a-zA-Z]{3,}", pwd) != None, # 6
  not re.match(r"^[0-9]", pwd), # 7
  re.search(r"[aeiouAEIOU]", pwd) != None, # 8
  not re.search(r"(.)\1{3,}", pwd), # 9
  re.search(r"[a-zA-Z]$", pwd) != None, # 10
  not re.search(r"123|abc|ABC", pwd), # 11
  re.search(r"([a-zA-Z])\1", pwd) != None, # 12
  re.search(r"[a-z]", pwd) != None, # 13
  (nombre.lower() not in pwd.lower()) if nombre else True, # 14
  re.search(r"[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]", pwd) != None, # 15
  not re.search(r"[\*\#$\%\&]{3,}", pwd), # 16
  not re.search(r"password|contraseña", pwd.lower()), # 17
  re.search(r"[a-zA-Z].*[\*\#$\%\&0-9].*[a-zA-Z]", pwd) != None, # 18 (Interpretación: letras no todas juntas)
  len(_get_numbers(pwd)) <= 5, # 19
  re.search(r"[XYZxyz]", pwd) != None, # 20
  
  # Nuevas Reglas: Conteo y Longitud (21-35)
  len(pwd) <= 32, # 21
  len(re.findall(r"[A-Z]", pwd)) >= 2, # 22
  len(re.findall(r"[a-z]", pwd)) >= 2, # 23
  len(_get_numbers(pwd)) >= 2, # 24
  len(_get_symbols(pwd)) >= 2, # 25
  len(_get_letters(pwd)) > len(_get_numbers(pwd)), # 26
  len(_get_symbols(pwd)) <= 3, # 27
  len(pwd) % 2 != 0, # 28
  len(_get_vowels(pwd)) % 2 == 0, # 29
  len(_get_consonants(pwd)) > len(_get_vowels(pwd)), # 30
  len(set(pwd)) > 5, # 31
  len(re.findall(r"[A-Z]", pwd)) != len(re.findall(r"[a-z]", pwd)), # 32
  len(re.findall(r"[02468]", pwd)) % 2 == 0, # 33
  len(re.findall(r"[13579]", pwd)) % 2 != 0, # 34
  _is_prime(len(pwd)), # 35
  
  # Nuevas Reglas: Posicionamiento (36-50)
  not re.search(r"[0-9]$", pwd), # 36
  not re.search(r"[\*\#$\%\&]$", pwd), # 37
  re.match(r"^.[a-z]", pwd) != None, # 38
  re.match(r"^..[0-9]", pwd) != None, # 39
  (len(pwd) < 2 or not pwd[-2].isupper()), # 40
  re.search(r"[0-9]", pwd[:4]) != None, # 41
  re.search(r"[\*\#$\%\&]", pwd[-4:]) != None, # 42
  (len(pwd) < 2 or pwd[0] != pwd[-1]), # 43
  (len(pwd) < 2 or _check_char_types(pwd[0], pwd[-1])), # 44
  not re.search(r"([0-9][\*\#$\%\&])|([\*\#$\%\&][0-9])", pwd), # 45
  re.search(r"([a-z][A-Z])|([A-Z][a-z])", pwd) != None, # 46
  not ('a' in pwd and ('A' not in pwd or pwd.find('a') < pwd.find('A'))), # 47
  not (_find_first(r"[0-9]", pwd) > _find_first(r"[A-Z]", pwd) > -1), # 48
  not (_find_first(r"[\*\#$\%\&]", pwd) < _find_first(r"[a-z]", pwd) > -1), # 49
  not re.search(r"[0-9].*[^0-9].*[0-9]", pwd), # 50
  
  # Nuevas Reglas: Caracteres Específicos (51-70)
  re.search(r"[\.,;]", pwd) != None, # 51
  not re.search(r"[\(\)\[\]]", pwd), # 52
  re.search(r"[\-_]", pwd) != None, # 53
  not re.search(r"[ñáéíóúÁÉÍÓÚ]", pwd), # 54
  re.search(r"[kqwKQW]", pwd) != None, # 55
  not re.search(r"[aeiouAEIOU]{4,}", pwd), # 56
  not re.search(r"[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]{4,}", pwd), # 57
  re.search(r"[02468]", pwd) != None, # 58
  re.search(r"[13579]", pwd) != None, # 59
  _sum_digits(pwd) > 5, # 60
  not ('O' in pwd and '0' in pwd), # 61
  not ('l' in pwd and '1' in pwd), # 62
  re.search(r"[\+=]", pwd) != None, # 63
  not re.search(r"[/\\]", pwd), # 64
  (_v := re.search(r"[aeiouAEIOU]", pwd)) and _v.group().lower() in ['a', 'e'], # 65
  not re.search(r"@", pwd), # 66
  not re.search(r"!", pwd), # 67
  re.search(r"[6-9]", pwd) != None, # 68
  re.search(r"[0-4]", pwd) != None, # 69
  re.search(r"[\{\}]", pwd) != None, # 70
  
  # Nuevas Reglas: Secuencias y Repeticiones (71-85)
  not re.search(r"321|432|543|654|765|876|987", pwd), # 71
  not re.search(r"qwerty|asdf|zxcv", pwd.lower()), # 72
  not re.search(r"cba|zyx", pwd.lower()), # 73
  not re.search(r"(.{2,}).*\1", pwd), # 74
  not re.search(r"[A-Z]{3,}", pwd), # 75
  not re.search(r"[a-z]{3,}", pwd), # 76
  pwd.lower() != pwd.lower()[::-1], # 77
  not re.search(r"199[0-9]|20[0-2][0-9]", pwd), # 78
  (nums := _get_numbers(pwd)) and not (len(nums) > 1 and all(nums[i] <= nums[i+1] for i in range(len(nums)-1))), # 79
  (len(pwd) < 2 or pwd[0] not in pwd[1:]), # 80
  (len(pwd) < 2 or pwd[-1] not in pwd[:-1]), # 81
  not any(pwd.lower().count(c) >= 3 for c in "abcdefghijklmnopqrstuvwxyz"), # 82
  not any(pwd.count(n) >= 3 for n in "0123456789"), # 83
  not any(pwd.count(s) >= 3 for s in "*#$%&"), # 84
  (_w := _get_word(pwd)) and _w.group().lower() != _w.group().lower()[::-1], # 85
  
  # Nuevas Reglas: Palabras Prohibidas y Contexto (86-100)
  not re.search(common_words["simple"], pwd.lower()), # 86
  not re.search(common_words["months"], pwd.lower()), # 87
  not re.search(common_words["days"], pwd.lower()), # 88
  not re.search(r"tic|tac|toe", pwd.lower()), # 89 (duplicado de 86, pero mantiene tu lista)
  (_w := _get_word(pwd)) and _w.group().isupper(), # 90
  (_w := _get_word(pwd)) and _w.start() > 0, # 91
  not re.search(r"hola|hello", pwd.lower()), # 92 (duplicado de 86)
  (nombre.lower()[::-1] not in pwd.lower()) if nombre else True, # 93
  (nombre.lower()[:3] not in pwd.lower()) if nombre and len(nombre) >= 3 else True, # 94
  (nombre.lower()[-3:] not in pwd.lower()) if nombre and len(nombre) >= 3 else True, # 95
  not re.search(common_words["colors"], pwd.lower()), # 96
  not re.search(r"juego|game", pwd.lower()), # 97 (duplicado de 86)
  not re.search(r"sol|luna|sun|moon", pwd.lower()), # 98 (duplicado de 86)
  not re.search(common_words["planets"], pwd.lower()), # 99
  not re.search(r"100", pwd), # 100
 ]

 # Imprimir el estado de cada regla
 for i, ok in enumerate(validaciones, 1):
  # Manejar casos donde la regla no aplica (ej: no hay números) y da un Falso Negativo
  # Regla 79: Falla si no hay números, pero la regla es "si hay, que no estén ordenados"
  if i == 79 and not _get_numbers(pwd):
   ok = True
  # Regla 85, 90, 91: Requieren una palabra
  if i in [85, 90, 91] and not _get_word(pwd):
   ok = False # Falla porque no hay palabra (regla 6)
  
  print(f"Regla {i}: {'Cumple ✅' if ok else 'No cumple ❌'}")
 print()
 return all(validaciones)

def agregar_reglas():
 print("\nAgregar una nueva regla personalizada:")
 print("(Nota: La lógica de validación no se agregará, solo el texto de la regla)")
 nueva = input("Escribe la nueva regla: ")
 reglas.append(nueva)
 print(f"Regla {len(reglas)} agregada exitosamente!\n")

def jugar():
 print("=== JUEGO DE LA CONTRASEÑA (VERSIÓN 100 REGLAS) ===")
 nombre = input("Ingresa tu nombre (opcional): ")
 mostrar_reglas()

 while True:
  print("Elige una opción:")
  print("1. Intentar crear contraseña")
  print("2. Agregar una regla (solo texto)")
  print("3. Ver reglas")
  print("4. Salir")
  op = input("> ")

  if op == "1":
   pwd = input("Escribe tu contraseña: ")
   print("\nVerificando...")
   if validar_contraseña(pwd, nombre):
    print("✅ ¡IMPOSIBLE! ¡Contraseña válida! Has ganado.\n")
    break # El juego termina si ganas
   else:
    print("❌ No cumple todas las reglas. Intenta otra vez.\n")

  elif op == "2":
   agregar_reglas()

  elif op == "3":
   mostrar_reglas()

  elif op == "4":
   print("Gracias por jugar. ¡Hasta la próxima!\n")
   break

  else:
   print("Opción no válida, intenta de nuevo.\n")

# --- Iniciar el juego ---
if __name__ == "__main__":
    jugar()
  