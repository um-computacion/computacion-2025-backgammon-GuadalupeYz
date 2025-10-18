import pygame
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException

# --- CONFIGURACION DE COLORES Y DIMENSIONES ---
ANCHO_VENTANA = 900
ALTO_VENTANA = 600
COLOR_FONDO = (200, 170, 120)
COLOR_TABLERO = (150, 110, 70)
COLOR_BLANCO = (245, 245, 245)
COLOR_NEGRO = (20, 20, 20)
COLOR_TEXTO = (10, 10, 10)
COLOR_SELECCION = (255, 0, 0)  #para marcar punto seleccionado

pygame.init()
pygame.display.set_caption("Backgammon - Interfaz Gráfica")
fuente = pygame.font.SysFont("Arial", 18)
fuente_grande = pygame.font.SysFont("Arial", 28) 

class InterfazPygame:
    def __init__(self, juego: BackgammonGame):
        self.juego = juego
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.en_ejecucion = True
        self.punto_seleccionado = None
        self.hitmap = {}   #guarda las coordenadas de cada punto
        self.dados = (0, 0)  #guarda los valores actuales de los dados
        self.mensaje = ""    #para mostrar mensajes


    def dibujar_tablero(self):
        self.pantalla.fill(COLOR_FONDO)
        self.hitmap.clear()  #se limpia y vuelve a generar en cada frame

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

        #registrar las coordenadas del punto superior (0-11)
            self.hitmap[i] = pygame.Rect(x, 50, 65, 250)
            # y del inferior (12-23)
            self.hitmap[23 - i] = pygame.Rect(x, 300, 65, 250)

        # Título
        texto = fuente.render("Backgammon", True, COLOR_TEXTO)
        self.pantalla.blit(texto, (ANCHO_VENTANA // 2 - 60, 10))

        # Dibujar fichas iniciales
        self.dibujar_fichas()

        #resaltar punto seleccionado
        if self.punto_seleccionado is not None:
            self.resaltar_punto(self.punto_seleccionado)

        self.dibujar_info()

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

def resaltar_punto(self, punto: int):
         if punto in self.hitmap:
            rect = self.hitmap[punto]
            pygame.draw.rect(self.pantalla, COLOR_SELECCION, rect, 3)

def dibujar_info(self):     #Muestra turno, dados y mensajes
        jugador = self.juego.get_turno()
        texto_turno = fuente_grande.render(
            f"Turno: {jugador.get_nombre()} ({jugador.get_color()})",
            True,
            COLOR_TEXTO,
        )
        self.pantalla.blit(texto_turno, (100, 560))

        # Mostrar dados
        texto_dados = fuente.render(f"Dados: {self.dados[0]} - {self.dados[1]}", True, COLOR_TEXTO)
        self.pantalla.blit(texto_dados, (600, 560))

        # Mensajes de juego
        if self.mensaje:
            texto_msg = fuente.render(self.mensaje, True, (200, 0, 0))
            self.pantalla.blit(texto_msg, (ANCHO_VENTANA // 2 - 100, 30))

def manejar_click(self, posicion: tuple[int, int]):
        for punto, area in self.hitmap.items():
            if area.collidepoint(posicion):
                if self.punto_seleccionado is None:
                    self.punto_seleccionado = punto
                else:
                    try:
                        jugador = self.juego.get_turno()
                        self.juego.mover_ficha(jugador, self.punto_seleccionado, punto)
                        print(f"Ficha movida de {self.punto_seleccionado} a {punto}")
                    except (MovimientoInvalidoException, FichaInvalidaException) as e:
                        print(f"Error: {e}")
                    self.punto_seleccionado = None
                break

def ejecutar(self):
        reloj = pygame.time.Clock()
        while self.en_ejecucion:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.en_ejecucion = False
             #manejar clic del mouse
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.manejar_click(evento.pos)

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
