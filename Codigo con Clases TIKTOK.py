class Coreografia:
    """
    Esta clase agrupa todos los pasos de la secuencia de baile como métodos.
    """
    
    def __init__(self):
        pass

    def paso_1(self, q):
      for posición_b1 in range(q):
        print("Manos en la cintura")
      for posición_b1 in range(q):
        print("Mano izquierda en la frente")
         
    def paso_2(self, x):
      for posición_b2 in range(x):
        print("Mano izquierda pasa por detras de la cabeza")
      for posición_b2 in range(x):
        print("Mano izquierda vuelve a la cintura junto con un movimineto de cadera hacía la derecha")
         
    def paso_3(self, a, b):
      for y in range(b):
        for posición_b3 in range(a):
          print("Movimiento de cintura hacía la derecha")
        for posición_b3 in range(a):
         print("Movimiento de cintura hacía la izquierda")
        for posición_b3 in range(a):
          print("Movimiento de manos ascendente con movimiento hasta la altura de la cabeza")
         
    def paso_4(self, a, b):
      for t in range(b):
        for i in range(a):
          print("Movimiento de manos con puño cerrado perpendicular a los hombros hacía afuera, y a su vez movimiento de cadera alineado con las piernas hacía la derecha")
        for i in range(a):
          print("Movimiento de manos con puño cerrado perpendicular a los hombros hacía adentro, y a su vez movimiento de cadera alineado con las piernas hacía la izquierda")
         
    def paso_5(self, a, b):
      for y in range(b):
        for i in range(a):
          print("Baja los brazos, luego extiende el brazo izquierdo levantando el dedo indice")
        for i in range(a):
          print("Luego extiende el brazo derecho levantando el dedo indice y junta los dedos de forma lineal y baja los brazos")
         
    def paso_6(self, x):
      for posición_b2 in range(x):
        print("Mano izquierda pasa por detras de la cabeza")
      for posición_b2 in range(x):
        print("Mano iquierda vuelve a la cintura junto con un movimineto de pierna izquierda hacía la izquierda")
         
    def paso_7(self, a):
      for i in range(a):
        print("Baja los brasos y extiende su mano izquierda con el puño cerrado y la mano derecha en la cintura")
         
    def paso_8(self, a, b):
      for y in range(b):
        for i in range(a):
          print("Junta sus piernas y comienza a moverlas de forma parabolica hacía la derecha")
        for i in range(a):
          print("Y luego comienza a moverlas de forma parabolica hacía la izquierda")
         
    def paso_9(self, a, b):
      for y in range(b):
        for i in range(a):
          print("Levanta los brazos y los coloca en posición de cruz detras de la nuca, para posteriormente moverse con sus piernas de forma parabolica hacia la derecha")
        for i in range(a):
          print("Y luego comienza a moverlas de forma parabolica hacía la izquierda, manteniendo la posición de sus brazos")
         
    def paso_10(self, a, b):
      for y in range (b):
        for y in range(a): # Nota: tu código original reutiliza 'y' aquí, lo cual es válido
          print("Comienza a dar una vuelta sobre su propio eje manteniendo la posición de sus brazos")
        for y in range(a): # Y aquí también
          print("Baja los brazos y termina el baile")

mi_baile = Coreografia()

print("¡Que comience el baile!")

mi_baile.paso_1(1)
mi_baile.paso_2(1)
mi_baile.paso_3(1,1)
mi_baile.paso_4(1,2)
mi_baile.paso_5(1,1)
mi_baile.paso_2(1)  
mi_baile.paso_6(1)
mi_baile.paso_3(1,1)  
mi_baile.paso_4(1,2)  
mi_baile.paso_5(1,1)  
mi_baile.paso_6(1)  
mi_baile.paso_7(1)
mi_baile.paso_8(1,2)
mi_baile.paso_9(1,2)

print("¡Fin de la secuencia!")