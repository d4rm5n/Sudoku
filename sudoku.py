
import random
import sys
import os

class nXzq:
    """Clase principal que controla la lógica del juego y almacena el estado del tablero"""
    
    def __init__(self):
        # Matriz del tablero visible: cada celda es un diccionario con:
        # 'v': valor numérico (0 = vacío)
        # 'f': bandera de celda fija (pista inicial)
        # 'e': bandera de error
        self.n_vb = [[{'v':0,'f':False,'e':False} for _ in range(9)] for _ in range(9)]
        
        # Matriz de solución completa (para comparación y función de rendirse)
        self.n_qa = [[0]*9 for _ in range(9)]
        
    def n_cl(self):
        """Limpia la pantalla de la terminal de forma multiplataforma"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def n_p(self, n_r, n_c, n_v):
        """
        Valida si un número puede colocarse en una posición específica según las reglas del Sudoku
        Args:
            n_r (int): Fila (0-8)
            n_c (int): Columna (0-8)
            n_v (int): Valor a validar (1-9)
        Returns:
            bool: True si el movimiento es válido, False si hay conflicto
        """
        # Validación de fila
        for n_i in range(9):
            if self.n_qa[n_r][n_i] == n_v and n_i != n_c: return False
        
        # Validación de columna
        for n_i in range(9):
            if self.n_qa[n_i][n_c] == n_v and n_i != n_r: return False
        
        # Validación de cuadrante 3x3
        n_sr, n_sc = 3*(n_r//3), 3*(n_c//3)  # Calcula esquina superior izquierda del cuadrante
        for n_i in range(n_sr, n_sr+3):
            for n_j in range(n_sc, n_sc+3):
                if self.n_qa[n_i][n_j] == n_v and (n_i,n_j) != (n_r,n_c): return False
        return True
    
    def n_tg(self):
        """Genera las 17 pistas iniciales requeridas para un Sudoku válido"""
        # Crea lista de todas las posiciones y las mezcla
        n_l = [(i,j) for i in range(9) for j in range(9)]
        random.shuffle(n_l)
        
        # Inserta 17 números válidos en posiciones aleatorias
        for n_k in range(17):
            n_r,n_c = n_l[n_k]
            n_v = random.randint(1,9)
            # Busca un número que cumpla las reglas del Sudoku
            while not self.n_p(n_r,n_c,n_v): n_v = random.randint(1,9)
            # Actualiza ambas matrices (visible y solución)
            self.n_qa[n_r][n_c] = n_v
            self.n_vb[n_r][n_c]['v'] = n_v
            self.n_vb[n_r][n_c]['f'] = True  # Marca como pista fija
            
    def n_rs(self):
        """
        Resuelve el Sudoku usando algoritmo recursivo con backtracking
        Returns:
            bool: True si encuentra solución, False si no hay solución
        """
        # Lista de celdas vacías
        n_e = [(i,j) for i in range(9) for j in range(9) if self.n_qa[i][j]==0]
        if not n_e: return True  # Sudoku resuelto
        
        n_r,n_c = n_e[0]  # Toma la primera celda vacía
        
        # Prueba números en orden aleatorio para variedad de soluciones
        for n_v in random.sample(range(1,10),9):
            if self.n_p(n_r,n_c,n_v):
                self.n_qa[n_r][n_c] = n_v
                # Llamada recursiva para siguiente celda
                if self.n_rs(): return True
                # Backtrack si no lleva a solución
                self.n_qa[n_r][n_c] = 0
        return False
    
    def n_ui(self):
        """Muestra el tablero en la terminal con formato y colores"""
        print("\n\033[94mTablero Actual:\033[0m")
        for n_i in range(9):
            # Línea divisoria horizontal cada 3 filas
            if n_i%3 == 0 and n_i!=0: print("\033[93m" + "-"*23 + "\033[0m")
            for n_j in range(9):
                # Obtiene valor y color según estado de la celda
                n_d = self.n_vb[n_i][n_j]['v']
                n_c = '\033[91m' if self.n_vb[n_i][n_j]['e'] else (  # Rojo para errores
                    '\033[94m' if self.n_vb[n_i][n_j]['f'] else '\033[0m'  # Azul para pistas
                )
                # Formato visual con separadores verticales
                sep = " | " if (n_j+1)%3==0 and n_j!=8 else "  "
                print(f"{n_c}{n_d if n_d!=0 else ' '}\033[0m", end=sep)
            print()
    
    def n_uv(self):
        """
        Actualiza el estado de errores y verifica si el juego está completo
        Returns:
            bool: True si el tablero está completo y sin errores, False en caso contrario
        """
        n_g = True  # Supone que el juego está completo inicialmente
        for n_i in range(9):
            for n_j in range(9):
                self.n_vb[n_i][n_j]['e'] = False  # Reinicia errores
                
                # Detecta celdas vacías
                if self.n_vb[n_i][n_j]['v'] == 0: n_g = False
                
                # Marca errores de conflicto
                elif not self.n_p(n_i,n_j,self.n_vb[n_i][n_j]['v']):
                    self.n_vb[n_i][n_j]['e'] = True
        
        # Verifica victoria: sin vacíos y sin errores
        return n_g and not any(self.n_vb[n_i][n_j]['e'] for n_i in range(9) for n_j in range(9))
    
    def n_vn(self, mensaje, rango):
        """
        Valida entrada numérica estricta
        Args:
            mensaje (str): Texto a mostrar al usuario
            rango (tuple): Tupla con (mínimo, máximo) permitido
        Returns:
            int: Número validado dentro del rango
        """
        while True:
            try:
                entrada = input(mensaje)
                # Valida que sea solo dígitos
                if not entrada.isdigit(): raise ValueError
                valor = int(entrada)
                # Valida rango numérico
                if not (rango[0] <= valor <= rango[1]): raise ValueError
                return valor
            except ValueError:
                print(f"\033[91mError: Debe ingresar un número entre {rango[0]} y {rango[1]}\033[0m")
                self.n_cl()
                self.n_ui()

    def n_ug(self):
        """Método principal que controla el flujo completo del juego"""
        self.n_cl()
        print("\n\033[95mBienvenido al Sudoku!\033[0m")
        
        # Inicialización del juego
        self.n_tg()  # Genera pistas iniciales
        self.n_qa = [[celda['v'] for celda in fila] for fila in self.n_vb]  # Copia pistas
        self.n_rs()  # Genera solución completa
        
        # Bucle principal del juego
        while True:
            self.n_cl()
            self.n_ui()  # Muestra el tablero
            
            # Verifica condición de victoria
            if self.n_uv():
                print("\033[92m¡Sudoku completado!\033[0m")
                break
            
            # Menú de opciones con validación
            op = None
            while op not in {'1','2','3'}:
                op = input("\n1. Ingresar número\n2. Borrar número\n3. Rendirse\nOpción: ").strip()
                if op not in {'1','2','3'}:
                    print("\033[91mOpción inválida! Use 1, 2 o 3\033[0m")
                    self.n_cl()
                    self.n_ui()
            
            # Manejo de opción "Rendirse"
            if op == '3':
                self.n_cl()
                print("\n\033[91mSolución del Sudoku:\033[0m")
                # Muestra solución completa con colores:
                # - Azul: pistas originales
                # - Verde: números correctos del usuario
                # - Amarillo: números incorrectos del usuario
                for i in range(9):
                    for j in range(9):
                        sol_val = self.n_qa[i][j]
                        usu_val = self.n_vb[i][j]['v']
                        
                        if self.n_vb[i][j]['f']:
                            color = '\033[94m'  # Pistas originales
                        else:
                            color = '\033[92m' if usu_val == sol_val else '\033[93m'  # Correcto/Incorrecto
                        
                        print(f"{color}{sol_val}\033[0m", end=' ')
                    print()
                input("\nPresione Enter para salir...")
                sys.exit()
            
            # Captura de posición válida
            while True:
                try:
                    n_r = self.n_vn("Fila (1-9): ", (1,9)) - 1  # Ajuste a índice 0-based
                    n_c = self.n_vn("Columna (1-9): ", (1,9)) - 1
                    
                    # Valida que no sea posición bloqueada (pista)
                    if self.n_vb[n_r][n_c]['f']:
                        print("\033[91m¡Posición bloqueada!\033[0m")
                        self.n_cl()
                        self.n_ui()
                        continue
                    break
                except: pass  # Maneja errores en conversión numérica
            
            # Manejo de acciones del usuario
            if op == '2':  # Borrar número
                self.n_vb[n_r][n_c]['v'] = 0
            elif op == '1':  # Ingresar número
                n_v = self.n_vn("Número (1-9): ", (1,9))
                self.n_vb[n_r][n_c]['v'] = n_v

if __name__ == "__main__":
    n_app = nXzq()
    n_app.n_ug()