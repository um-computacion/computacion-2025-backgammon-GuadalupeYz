Modelo utilizado
ChatGPT (GPT-4, versión Octubre 2025)

Prompt 1: desarrollo de la lógica de dados
Mensaje:
Necesito implementar una clase Dados para mi juego de Backgammon.  
Tiene que tirar dos dados, devolver los valores, y si salen dobles (por ej 4 y 4)  
se tienen que duplicar los movimientos disponibles, o sea, quedar como [4, 4, 4, 4].  
Cómo puedo programarlo en python y usando orientación a objetos

Respuesta:
import random

class Dados:
    def __init__(self):
        self.__valores = (0, 0)

    def roll(self):
        """Lanza los dados"""
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        self.__valores = (d1, d2)
        return self.__valores

    def get_valores(self):
        return self.__valores

    def movimientos_disponibles(self):
        """Devuelve los movimientos según los valores"""
        d1, d2 = self.__valores
        if d1 == d2:
            return [d1] * 4
        return [d1, d2]

Prompt 2: lógica del tablero en Pygame

Mensaje:
Estoy haciendo la interfaz Pygame para mi Backgammon.
Quiero mostrar el tablero con 24 puntos, divididos en dos zonas tipo abajo y arriba,
y dibujar fichas blancas y negras según la posición. Digamos estructurarlo para que use las posiciones que tengo en BackgammonGame

Respuesta:

import pygame

class InterfazPygame:
    def __init__(self, juego):
        pygame.init()
        self.juego = juego
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Backgammon")
        self.font = pygame.font.SysFont("Arial", 18)
        self.running = True

    def dibujar_tablero(self):
        self.screen.fill((210, 180, 140))
        puntos = self.juego.get_tablero().get_points()
        for i, pila in enumerate(puntos):
            x = 50 + (i % 12) * 90
            y = 100 if i < 12 else 400
            pygame.draw.polygon(self.screen, (139, 69, 19),
                [(x, y), (x+40, y), (x+20, y+200 if i<12 else y-200)])
            for j, ficha in enumerate(pila):
                color = (255, 255, 255) if ficha.get_color() == "blanco" else (0, 0, 0)
                pos_y = y + (j * 20 if i < 12 else -j * 20)
                pygame.draw.circle(self.screen, color, (x+20, pos_y), 10)
        pygame.display.flip()


Prompt 3: alternancia de turnos

Mensaje:
En el Backgammon tengo dos jugadores, y quiero alternar sus turnos. Como que termine el turno del blanco y pase al negro ¿Cómo puedo hacerlo?

Respuesta:

class BackgammonGame:
    def __init__(self):
        self.__jugadores = []
        self.__turno_actual = 0

    def agregar_jugador(self, jugador):
        self.__jugadores.append(jugador)

    def get_turno(self):
        return self.__jugadores[self.__turno_actual]

    def cambiar_turno(self):
        self.__turno_actual = 1 - self.__turno_actual


Prompt 3: test de excepción por movimiento inválido
Mensaje:
Necesito un test que verifique que si intento mover una ficha a un punto bloqueado,
se lanza una excepción MovimientoInvalidoException.

Respuesta:

def test_movimiento_invalido_lanza_excepcion(self):
    juego = BackgammonGame()
    j1 = Jugador("Guada", "blanco")
    j2 = Jugador("Bruno", "negro")
    juego.agregar_jugador(j1)
    juego.agregar_jugador(j2)
    juego.setup_inicial()
    with self.assertRaises(MovimientoInvalidoException):
        juego.mover_ficha(j1, 7, 18)

        
Prompt 4: manejo de excepciones personalizadas

Mensaje:
Necesito crear lasexcepciones específicas para mi juego Backgammon.Ponele cuando el jugador intenta mover una ficha inválida q no es su turno o a una posición que no puede , etc

Respuesta:

class MovimientoInvalidoException(Exception):
    pass

class FichaInvalidaException(Exception):
    pass


Prompt 5: método para detectar victoria

Mensaje:
Quiero que el juego detecte cuándo un jugador saca todas sus fichas del tablero.
Así puedo mostrar un mensaje de “ganador” en CLI y Pygame.
¿Cómo puedo hacer el método para eso?

Respuesta:

def finalizar_jugada(self):
    for jugador in self.__jugadores:
        if self.__fichas_fuera[jugador.get_color()] == 15:
            return jugador
    return None


Prompt 3: dibujar nombres de jugadores en la interfaz Pygame
Mensaje:
Estoy agregando los textos en la interfaz Pygame.
Quiero que aparezcan los nombres de los jugadores arriba y abajo del tablero
con su color correspondiente (blanco y negro) con Pygame

Respuesta:

def dibujar_nombres(self):
    j1, j2 = self.juego.get_jugadores()
    texto1 = self.font.render(f"{j1.get_nombre()} ({j1.get_color()})", True, (0, 0, 0))
    texto2 = self.font.render(f"{j2.get_nombre()} ({j2.get_color()})", True, (0, 0, 0))
    self.screen.blit(texto1, (50, 30))
    self.screen.blit(texto2, (50, 650))
    pygame.display.update()

