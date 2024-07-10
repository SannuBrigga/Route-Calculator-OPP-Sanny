import heapq
import random

# Inicializar la matriz 5x5
class Mapa (): #clase mapa para el molde de mi matriz
    def __init__(self, tamanho = 5): 
        self.tamanho = tamanho
        self.matriz =  [["🔳" for _ in range(tamanho)] for _ in range(tamanho)]



    # Función para imprimir la matriz con guía visual
    def imprimir_laberinto(self):
        print("   0  1  2  3  4")  # Encabezado de las columnas
        for i in range(5):
            fila_str = str(i) + " "  # Encabezado de las filas
            fila_str += " ".join(self.matriz[i])
            print(fila_str)

    # Función para agregar entrada, salida y obstáculos
    def agregar_entrada_salida_obstaculos(self):
        entrada = input("Introduce la coordenada de entrada (x y): ")
        entrada_x, entrada_y = map(int, entrada.split())
        self.matriz[entrada_x][entrada_y] = "🔽"
        
        salida = input("Introduce la coordenada de salida (x y): ")
        salida_x, salida_y = map(int, salida.split())
        self.matriz[salida_x][salida_y] = '🏁'
        
        num_obstaculos = int(input("Introduce el número de obstáculos: "))
        for _ in range(num_obstaculos):
            while True:
                obstaculo = input("Introduce la coordenada del obstáculo (x y): ")
                obstaculo_x, obstaculo_y = map(int, obstaculo.split())
                if (0 <= obstaculo_x < self.tamanho) and (0 <= obstaculo_y < self.tamanho): # Verificar si está dentro de los límites
                    if (obstaculo_x, obstaculo_y) != (entrada_x, entrada_y) and (obstaculo_x, obstaculo_y) != (salida_x, salida_y):
                        self.matriz[obstaculo_x][obstaculo_y] = '🏢'
                        break
                    else:
                        print("No se puede colocar un obstáculo en la coordenada de entrada o salida. Intenta de nuevo.")
                else:
                    print("Coordenadas fuera de los límites de la matriz. Intenta de nuevo.")
        
        for _ in range(3):
            while True:
                bache_x = random.randint(0, 4)
                bache_y = random.randint(0, 4)
                if self.matriz[bache_x][bache_y] == "🔳":
                    self.matriz[bache_x][bache_y] = '🗻'
                    break


class Astar():

    def __init__(self, mapa):
        self.mapa = mapa
        self.tamanho = mapa.tamanho
# Heurística Manhattan
    def distancia_manhattan(self,a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Algoritmo A*
    def a_estrella(self, inicio, fin): #funcion A* que toma como parametro mi matriz, mi entrada y salida
        entrada_x, entrada_y = inicio # me guarda mi entrada en coordenadas x y
        salida_x, salida_y = fin #me guarda mi salida en coordenadas x y
        openset = [] # genera una variable con valor de una lista vacia
        heapq.heappush(openset, (0, entrada_x, entrada_y))#genera mi cola de prioridad, y emete dentro de mi lista vacia mi primer elementp de la cola de prioridad y entrada_x y entrada_y representa que estoy dentro de las oordenadas de mi inicio
        #(open_set,(f_score,(posicion x y)))
        viene_de = {}# se guarda en un diccionario las coordenadas que recorri
        g_score = { (i, j): float('inf') for i in range(self.tamanho) for j in range(self.tamanho) } #guarda todas mis filas y columnas con un valor inf.
        g_score[(entrada_x, entrada_y)] = 0 # le digo q vale 0, g score serria como mi costo, como ese paso o pasos a realizar ES G
        f_score = { (i, j): float('inf') for i in range(self.tamanho) for j in range(self.tamanho) } #guarda todas mis filas y columnas con un valor inf. ES F
        f_score[(entrada_x, entrada_y)] = self.distancia_manhattan(inicio, fin)

        while openset: # en el whilw se crea la variable esta, y sirve para crear una tipo lista para guardar valores//SE EJECUTA SIEMPRE MIENTRAS SEA TRUE, empiezo desde mi punto inicial
            _, x, y = heapq.heappop(openset)#toma la coordenada de menor valor de la cola openset // mientras mi conjunto abierto no este vacio

            if (x, y) == (salida_x, salida_y):# si x y que son mis valores recorridos son == al las coordenadas del final
                return self.reconstruir_camino(viene_de, (x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # son las direcciones en las cuales me puedo ir, van iterando
                nueva_x, nueva_y = x + dx, y + dy #nueva_x, nueva_y son las nuevas posiciones, que son la suma de la direccion y la coordenada actual, para ir moviendose
                #para verificar que se esta usando dentro de mi laberinto
                if 0 <= nueva_x < self.tamanho and 0 <= nueva_y < self.tamanho: #evalua que el movimiento que hago esta dentro de las coordenadas de mi laberinto
                    if self.mapa.matriz[nueva_x][nueva_y] == '🏢': # si la nueva cordenada es igual a la posicion de un edificio que ignore ese y continue calculando los otros nodos
                        continue

                    # Paso 1: Obtener el g_score del nodo actual
                    g_score_actual = g_score[(x, y)]

                    # Paso 2: Determinar el costo del movimiento al nodo vecino
                    if self.mapa.matriz[nueva_x][nueva_y] == '🗻':
                        costo_movimiento = 2
                    else:
                        costo_movimiento = 1

                    # Paso 3: Calcular el g_score tentativo para el nodo vecino
                    tentative_g_score = g_score_actual + costo_movimiento 

                    if tentative_g_score < g_score[(nueva_x, nueva_y)]:# esta condicion si se cumple porque el valor tentativo sempre es menor que el valor inf
                        viene_de[(nueva_x, nueva_y)] = (x, y)
                        g_score[(nueva_x, nueva_y)] = tentative_g_score
                        h_score=self.distancia_manhattan((nueva_x, nueva_y), fin)
                        f_score[(nueva_x, nueva_y)] = tentative_g_score + h_score
                        heapq.heappush(openset, (f_score[(nueva_x, nueva_y)], nueva_x, nueva_y))

        return None

    # Reconstrucción del camino
    def reconstruir_camino(self,viene_de, actual):
        camino = []
        while actual in viene_de:
            camino.append(actual)
            actual = viene_de[actual]
        camino.reverse()
        return camino

# Ejemplo de uso
mapa = Mapa()

print("Matriz inicial:")
mapa.imprimir_laberinto()

mapa.agregar_entrada_salida_obstaculos()

print("\nMatriz final con entrada, salida, obstáculos y baches:")
mapa.imprimir_laberinto()

# Determinar las coordenadas de inicio y fin
inicio = [(i, fila.index("🔽")) for i, fila in enumerate(mapa.matriz) if "🔽" in fila][0]
fin = [(i, fila.index('🏁')) for i, fila in enumerate(mapa.matriz) if '🏁' in fila][0]

# Encontrar el camino usando A*
a_estrella=Astar(mapa)
camino = a_estrella.a_estrella(inicio,fin)

# Marcar el camino en la matriz
if camino:
    for x, y in camino:
        if  mapa.matriz[x][y] == "🔳":
            mapa.matriz[x][y] = '🔸'
else:
    print("No se encontró un camino.")

# Mostrar la matriz resultante
print("\nMatriz con el camino encontrado:")
mapa.imprimir_laberinto()

