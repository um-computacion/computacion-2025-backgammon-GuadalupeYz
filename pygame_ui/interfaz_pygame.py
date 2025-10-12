import pygame
from codigo.backgammon import BackgammonGame

# --- CONFIGURACION DE COLORES Y DIMENSIONES ---
ANCHO_VENTANA = 900
ALTO_VENTANA = 600
COLOR_FONDO = (200, 170, 120)
COLOR_TABLERO = (150, 110, 70)
COLOR_BLANCO = (245, 245, 245)
COLOR_NEGRO = (20, 20, 20)
COLOR_TEXTO = (10, 10, 10)

pygame.init()
pygame.display.set_caption("Backgammon - Interfaz Gráfica")
fuente = pygame.font.SysFont("Arial", 18)

class InterfazPygame:
    def __init__(self, juego: BackgammonGame):
        self.juego = juego
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.en_ejecucion = True

    def dibujar_tablero(self):
        self.pantalla.fill(COLOR_FONDO)

        # Dibujar base del tablero
        pygame.draw.rect(self.pantalla, COLOR_TABLERO, (50, 50, 800, 500))

        # Líneas divisorias (12 triángulos por lado)
        for i in range(12):
            x = 60 + i * 65
            pygame.draw.polygon(
                self.pantalla,
                (230, 180, 80) if i % 2 == 0 else (90, 50, 30),
                [(x, 50), (x + 32, 250), (x + 65, 50)]
            )
            pygame.draw.polygon(
                self.pantalla,
                (230, 180, 80) if i % 2 == 1 else (90, 50, 30),
                [(x, 550), (x + 32, 350), (x + 65, 550)]
            )

        # Título
        texto = fuente.render("Backgammon", True, COLOR_TEXTO)
        self.pantalla.blit(texto, (ANCHO_VENTANA // 2 - 60, 10))

        # Dibujar fichas iniciales
        self.dibujar_fichas()

    def dibujar_fichas(self):
        puntos = self.juego.get_tablero().get_points()

        for i, pila in enumerate(puntos):
            for j, ficha in enumerate(pila):
                color = COLOR_BLANCO if ficha.get_color() == "blanco" else COLOR_NEGRO

                # Coordenadas de ficha
                if i < 12:
                    x = 70 + i * 65
                    y = 520 - j * 22
                else:
                    x = 70 + (i - 12) * 65
                    y = 80 + j * 22

                pygame.draw.circle(self.pantalla, color, (x, y), 18)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x, y), 18, 2)

    def ejecutar(self):
        reloj = pygame.time.Clock()
        while self.en_ejecucion:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.en_ejecucion = False

            self.dibujar_tablero()
            pygame.display.flip()
            reloj.tick(30)

        pygame.quit()

# --- PRUEBA DIRECTA ---
if __name__ == "__main__":
    juego = BackgammonGame()
    from codigo.jugadores import Jugador
    jugador1 = Jugador("Alice", "blanco")
    jugador2 = Jugador("Bob", "negro")
    juego.agregar_jugador(jugador1)
    juego.agregar_jugador(jugador2)
    juego.setup_inicial()

    interfaz = InterfazPygame(juego)
    interfaz.ejecutar()
