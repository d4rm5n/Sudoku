
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