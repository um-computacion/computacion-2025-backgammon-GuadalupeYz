"""Interfaz gráfica del juego Backgammon usando Pygame."""

import pygame
from codigo.backgammon import BackgammonGame
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException

# --- Colores y configuración ---
ANCHO_VENTANA, ALTO_VENTANA = 900, 600
COLOR_FONDO = (190, 150, 100)
COLOR_TABLERO = (160, 110, 60)
COLOR_TEXTO = (0, 0, 0)
COLOR_SELECCION = (255, 0, 0)
COLOR_BOTON = (100, 200, 100)
COLOR_BOTON_HOVER = (150, 255, 150)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)

pygame.init()
fuente = pygame.font.SysFont("Arial", 20)
fuente_grande = pygame.font.SysFont("Arial", 24, bold=True)
fuente_victoria = pygame.font.SysFont("Arial", 32, bold=True)


class InterfazPygame:
    """Clase que maneja toda la interfaz gráfica del juego Backgammon."""

    def __init__(self, juego: BackgammonGame):
        """Inicializa la interfaz, las variables y los botones."""
        self.juego = juego
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA + 100))
        pygame.display.set_caption("Backgammon - Interfaz Gráfica")
        self.en_ejecucion = True
        self.punto_seleccionado = None
        self.hitmap = {}
        self.dados = (0, 0)
        self.mensaje = ""
        self.boton_dados = pygame.Rect(700, 590, 130, 45)
        self.juego_terminado = False
        self.dados_tirados = False  # bandera para saber si ya tiró
        self.puntos_destino_validos = []

    def dibujar_tablero(self):
        """Dibuja el tablero completo: triángulos, barra, fichas, botones e info."""
        self.pantalla.fill(COLOR_FONDO)
        self.hitmap.clear()

        # --- Tablero base ---
        pygame.draw.rect(self.pantalla, COLOR_TABLERO, (50, 50, 800, 500))

        # --- Triángulos superiores e inferiores ---
        for i in range(12):
            x = 60 + i * 65
            # superiores
            pygame.draw.polygon(
                self.pantalla,
                (230, 180, 80) if i % 2 == 0 else (90, 50, 30),
                [(x, 50), (x + 32, 250), (x + 65, 50)]
            )
            # inferiores
            pygame.draw.polygon(
                self.pantalla,
                (230, 180, 80) if i % 2 == 1 else (90, 50, 30),
                [(x, 550), (x + 32, 350), (x + 65, 550)]
            )

            # hitmap para clicks
            self.hitmap[i] = pygame.Rect(x, 50, 65, 250)
            self.hitmap[23 - i] = pygame.Rect(x, 300, 65, 250)

        # --- BAR central ---
        pygame.draw.rect(self.pantalla, (90, 50, 30), (440, 50, 20, 500))
        texto_bar = fuente.render("BAR", True, (255, 255, 255))
        self.pantalla.blit(texto_bar, (445, 260))

        # --- Fichas en el BAR ---
        bar = self.juego.get_bar()
        x_centro = 450
        for color_str, fichas in bar.items():
            if not fichas:
                continue
            x = x_centro - 15 if color_str == "blanco" else x_centro + 15
            for j, _ in enumerate(fichas):
                y = 270 + j * 22
                color = COLOR_BLANCO if color_str == "blanco" else COLOR_NEGRO
                pygame.draw.circle(self.pantalla, color, (x, y), 18)
                pygame.draw.circle(self.pantalla, (40, 40, 40), (x, y), 18, 2)

        # --- Zonas de salida ---
        pygame.draw.rect(self.pantalla, (230, 230, 230), (10, 400, 35, 140))
        texto_out_blanco = fuente.render("OUT", True, (50, 50, 50))
        self.pantalla.blit(texto_out_blanco, (12, 380))

        pygame.draw.rect(self.pantalla, (50, 50, 50), (860, 60, 35, 140))
        texto_out_negro = fuente.render("OUT", True, (255, 255, 255))
        self.pantalla.blit(texto_out_negro, (862, 40))

        # --- Fichas y marcadores ---
        self.dibujar_fichas()
        if self.punto_seleccionado is not None:
            self.resaltar_punto(self.punto_seleccionado)

        if hasattr(self, "puntos_destino_validos"):
            for destino in self.puntos_destino_validos:
                if destino in self.hitmap:
                    pygame.draw.rect(self.pantalla, (0, 255, 0), self.hitmap[destino], 3)

        # --- Info y botón ---
        self.dibujar_info()
        self.dibujar_boton_dados()

        if self.juego_terminado:
            self.mostrar_victoria()

    def dibujar_fichas(self):
        """Dibuja todas las fichas del tablero y las fichas retiradas."""
        puntos = self.juego.get_tablero().get_points()

        for punto_idx, pila in enumerate(puntos):
            if not pila:
                continue
            for j, ficha in enumerate(pila):
                color = COLOR_BLANCO if ficha.get_color() == "blanco" else COLOR_NEGRO
                if punto_idx <= 11:
                    x = 60 + punto_idx * 65 + 32
                    y = 80 + j * 22
                else:
                    col = 23 - punto_idx
                    x = 60 + col * 65 + 32
                    y = 520 - j * 22
                pygame.draw.circle(self.pantalla, color, (x, y), 18)
                pygame.draw.circle(self.pantalla, (50, 50, 50), (x, y), 18, 2)

        # fichas fuera del tablero
        fuera_blancas = self.juego.get_fichas_fuera("blanco")
        fuera_negras = self.juego.get_fichas_fuera("negro")
        for i, _ in enumerate(fuera_blancas):
            x = 880
            y = 70 + i * 20
            pygame.draw.circle(self.pantalla, COLOR_BLANCO, (x, y), 10)
            pygame.draw.circle(self.pantalla, (50, 50, 50), (x, y), 10, 2)

        # Negras → abajo a la izquierda (rectángulo OUT)
        for i, ficha in enumerate(fuera_negras):
            x = 30
            y = 520 - i * 20
            pygame.draw.circle(self.pantalla, COLOR_NEGRO, (x, y), 10)
            pygame.draw.circle(self.pantalla, (255, 255, 255), (x, y), 10, 2)

    def resaltar_punto(self, punto: int):
        """Resalta un punto del tablero con un borde celeste."""
        if punto in self.hitmap:
            rect = self.hitmap[punto]
            pygame.draw.rect(self.pantalla, (0, 150, 255), rect, 3)

    def dibujar_info(self):
        """Muestra en pantalla el turno, los dados y los mensajes."""
        jugador = self.juego.get_turno()
        texto_turno = fuente_grande.render(
            f"Turno: {jugador.get_nombre()} ({jugador.get_color()})", True, COLOR_TEXTO
        )
        self.pantalla.blit(texto_turno, (100, 560))

        texto_dados = fuente.render(f"Dados: {self.dados[0]} - {self.dados[1]}", True, COLOR_TEXTO)
        self.pantalla.blit(texto_dados, (700, 640))

        if self.mensaje:
            texto_msg = fuente.render(self.mensaje, True, (200, 0, 0))
            self.pantalla.blit(texto_msg, (100, 590))
            pygame.draw.rect(self.pantalla, (230, 210, 180), (90, 620, 500, 70))

        ayuda1 = fuente.render(" Verde: puntos donde podés mover la ficha", True, (0, 180, 0))
        ayuda2 = fuente.render(" Azul: punto de llegada", True, (0, 120, 255))
        self.pantalla.blit(ayuda1, (100, 630))
        self.pantalla.blit(ayuda2, (100, 650))

    def dibujar_boton_dados(self):
        """Dibuja el botón de tirar dados y detecta hover."""
        mouse_pos = pygame.mouse.get_pos()
        color = COLOR_BOTON_HOVER if self.boton_dados.collidepoint(mouse_pos) else COLOR_BOTON
        self.boton_dados = pygame.Rect(730, 600, 120, 45)
        pygame.draw.rect(self.pantalla, color, self.boton_dados, border_radius=8)
        texto_boton = fuente.render("Tirar dados", True, (0, 0, 0))
        self.pantalla.blit(texto_boton, (self.boton_dados.x + 10, self.boton_dados.y + 10))

    def mostrar_victoria(self):
        """Muestra el mensaje de victoria del jugador ganador."""
        ganador = getattr(self.juego, "get_ganador", lambda: None)()
        if not ganador:
            return
        texto_victoria = fuente_victoria.render(
            f" ¡{ganador.get_nombre()} ganó la partida! ",
            True, (255, 255, 255)
        )
        rect_texto = texto_victoria.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        pygame.draw.rect(self.pantalla, (0, 0, 0), rect_texto.inflate(40, 20))
        self.pantalla.blit(texto_victoria, rect_texto)

    def calcular_destinos_validos(self, punto_origen):
        """
        Calcula destinos válidos desde un punto.
        Devuelve índices 0..23 para movimientos internos y:
          -1  (blancas) cuando puede sacar,
          24  (negras)  cuando puede sacar.
        """
        destinos = []
        dados = list(self.juego.get_dados_disponibles() or [])
        if not dados:
            return destinos

        jugador = self.juego.get_turno()
        color = (jugador.get_color() or "").strip().lower()
        puntos = self.juego.get_tablero().get_points()

        def blanco_hay_mas_lejos(desde):
            # en casa blanca (0..5), más lejos de salir = índices mayores a 'desde'
            return any(any(f.get_color() == "blanco" for f in puntos[i]) for i in range(desde + 1, 6))

        def negro_hay_mas_lejos(desde):
            # en casa negra (18..23), más lejos de salir = índices menores a 'desde'
            return any(any(f.get_color() == "negro" for f in puntos[i]) for i in range(18, desde))

        for d in dados:
            if color == "blanco":
                destino = punto_origen - d
                if destino >= 0:
                    pila = puntos[destino]
                    if not (pila and pila[-1].get_color() != color and len(pila) > 1):
                        destinos.append(destino)
                else:
                    # candidato a bear-off con este dado
                    if 0 <= punto_origen <= 5 and not blanco_hay_mas_lejos(punto_origen):
                        destinos.append(-1)
            else:
                destino = punto_origen + d
                if destino <= 23:
                    pila = puntos[destino]
                    if not (pila and pila[-1].get_color() != color and len(pila) > 1):
                        destinos.append(destino)
                else:
                    # candidato a bear-off con este dado
                    if 18 <= punto_origen <= 23 and not negro_hay_mas_lejos(punto_origen):
                        destinos.append(24)

        return sorted(set(destinos))

    def manejar_click(self, posicion: tuple[int, int]):
        """Maneja clics: tirar dados, mover fichas, sacar o reingresar."""
        if self.juego_terminado:
            return

        jugador = self.juego.get_turno()
        color = jugador.get_color()
        dados = self.juego.get_dados_disponibles() or []

        # --- Botón tirar dados ---
        if self.boton_dados.collidepoint(posicion):
            if not self.dados_tirados:
                self.dados = self.juego.tirar_dados()
                self.dados_tirados = True
                self.mensaje = f"Dados: {self.dados[0]} - {self.dados[1]}"
            else:
                self.mensaje = "Ya tiraste los dados."
            return

        # --- Reingreso desde BAR ---
        bar_color = jugador.get_color()
        en_barra = self.juego.get_bar()[bar_color]
        if en_barra:
            if not dados:
                self.mensaje = "Debes tirar los dados para reingresar desde el BAR."
                return

            if bar_color == "blanco":
                posibles = [24 - d for d in dados]
            else:
                posibles = [d - 1 for d in dados]

            puntos = self.juego.get_tablero().get_points()
            posibles = [
                p for p in posibles
                if 0 <= p < 24 and not (
                    puntos[p] and puntos[p][-1].get_color() != bar_color and len(puntos[p]) > 1
                )
            ]

            if not posibles:
                self.mensaje = "No hay movimientos válidos, se pasa el turno."
                self.juego.finalizar_turno()
                self.dados_tirados = False
                self.dados = (0, 0)
                turno = self.juego.get_turno()
                self.mensaje = f"Turno de {turno.get_nombre()} ({turno.get_color()})."
                pygame.display.flip()
                return

            self.punto_seleccionado = None
            self.puntos_destino_validos = posibles
            self.mensaje = "Reingresá una ficha desde el BAR."

            for punto, area in self.hitmap.items():
                if area.collidepoint(posicion) and punto in posibles:
                    try:
                        self.juego.reingresar_ficha(jugador, punto)
                        if not self.juego.get_dados_disponibles():
                            self.dados_tirados = False
                            self.dados = (0, 0)
                            turno = self.juego.get_turno()
                            self.mensaje = f"Turno de {turno.get_nombre()} ({turno.get_color()})."
                            pygame.display.flip()
                            return
                        self.mensaje = f"Reingresaste en {punto}."
                        self.puntos_destino_validos = []
                        return
                    except (MovimientoInvalidoException, FichaInvalidaException) as e:
                        self.mensaje = str(e)
                        return
            return

        # --- Movimiento normal / Bear-off ---
        puntos = self.juego.get_tablero().get_points()
        for punto, area in self.hitmap.items():
            if area.collidepoint(posicion):
                # primer click: seleccionar ficha propia
                if self.punto_seleccionado is None:
                    if puntos[punto] and puntos[punto][-1].get_color() == jugador.get_color():
                        self.punto_seleccionado = punto
                        self.puntos_destino_validos = self.calcular_destinos_validos(punto)
                        self.mensaje = f"Ficha seleccionada en punto {punto}."
                    else:
                        self.mensaje = "Debes seleccionar una ficha tuya."
                    return

                # segundo click: intentar mover o sacar
                if not self.juego.get_dados_disponibles():
                    self.mensaje = "Primero tirá los dados."
                    self.punto_seleccionado = None
                    self.puntos_destino_validos = []
                    return
                try:
                    origen = self.punto_seleccionado
                    destinos = self.calcular_destinos_validos(origen)

                    # BEAR-OFF: si el jugador hace click sobre la MISMA casilla y el destino especial está habilitado
                    if punto == origen and (
                        (color == "blanco" and -1 in destinos) or
                        (color == "negro" and 24 in destinos)
                    ):
                        self.juego.sacar_ficha(jugador, origen)
                        self.mensaje = f"Sacaste una ficha desde el punto {origen}."
                    else:
                        # Movimiento normal: el destino clickeado debe estar en 'destinos'
                        if punto not in destinos:
                            self.mensaje = "Movimiento inválido."
                            self.punto_seleccionado = None
                            self.puntos_destino_validos = []
                            return
                        self.juego.mover_ficha(jugador, origen, punto)
                        self.mensaje = f"Movimiento de {origen} → {punto}."

                    ganador = self.juego.finalizar_jugada()
                    if ganador:
                        self.juego_terminado = True
                        self.mensaje = f" ¡{ganador.get_nombre()} ganó!"
                    elif not self.juego.get_dados_disponibles():
                        self.dados_tirados = False
                        self.dados = (0, 0)
                        turno = self.juego.get_turno()
                        self.mensaje = f"Turno de {turno.get_nombre()} ({turno.get_color()})."

                    self.punto_seleccionado = None
                    self.puntos_destino_validos = []
                    self.dibujar_tablero()
                    pygame.display.flip()
                    return

                except (MovimientoInvalidoException, FichaInvalidaException) as e:
                    # No forzamos cambio de turno si falló; solo informamos y limpiamos selección
                    self.mensaje = str(e)
                    self.punto_seleccionado = None
                    self.puntos_destino_validos = []
                    pygame.display.flip()
                    return

    def ejecutar(self):
        """Bucle principal de la interfaz: actualiza y dibuja todo."""
        reloj = pygame.time.Clock()
        while self.en_ejecucion:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.en_ejecucion = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.manejar_click(evento.pos)

            self.dibujar_tablero()
            pygame.display.flip()
            reloj.tick(30)
        pygame.quit()

    def dibujar_bear_off(self):
        """Dibuja la zona lateral donde se mostrarán fichas retiradas."""
        pygame.draw.rect(self.pantalla, (180, 160, 120), (870, 100, 40, 400))
        texto = fuente.render("Bear-off", True, (0, 0, 0))
        self.pantalla.blit(texto, (865, 70))

# --- PRUEBA DIRECTA ---
if __name__ == "__main__":
    from codigo.jugadores import Jugador
    from codigo.backgammon import BackgammonGame

    print("=== CONFIGURACIÓN DE JUGADORES ===")
    nombre_blanco = input("Nombre del jugador blancas: ")
    nombre_negro = input("Nombre del jugador negras: ")

    juego = BackgammonGame()
    jugador_blanco = Jugador(nombre_blanco, "blanco")
    jugador_negro = Jugador(nombre_negro, "negro")

    juego.agregar_jugador(jugador_blanco)
    juego.agregar_jugador(jugador_negro)
    juego.setup_inicial()

    interfaz = InterfazPygame(juego)
    interfaz.ejecutar()
