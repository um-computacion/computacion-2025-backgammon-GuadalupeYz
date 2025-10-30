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

# --- Clase principal de interfaz ---
class InterfazPygame:
    def __init__(self, juego: BackgammonGame):
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
        self.dados_tirados = False  # 🔹 bandera nueva
        self.puntos_destino_validos = []

    def dibujar_tablero(self):
     self.pantalla.fill(COLOR_FONDO)
     self.hitmap.clear()

    # --- Tablero base ---
     pygame.draw.rect(self.pantalla, COLOR_TABLERO, (50, 50, 800, 500))

    # --- Triángulos ---
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

        # hitmap (0..11 arriba, 23..12 abajo)
        self.hitmap[i] = pygame.Rect(x, 50, 65, 250)
        self.hitmap[23 - i] = pygame.Rect(x, 300, 65, 250)

    # --- BAR central ---
     pygame.draw.rect(self.pantalla, (90, 50, 30), (440, 50, 20, 500))
     texto_bar = fuente.render("BAR", True, (255, 255, 255))
     self.pantalla.blit(texto_bar, (445, 260))

    # --- Fichas en el BAR ---
     bar = self.juego.get_bar()
     x_centro = 450  # centro exacto del BAR
     for color_str, fichas in bar.items():
        if not fichas:
            continue
        # desplazamiento para que no se solapen
        x = x_centro - 15 if color_str == "blanco" else x_centro + 15
        for j, _ in enumerate(fichas):
            # apiladas verticalmente en el centro
            y = 270 + j * 22
            color = COLOR_BLANCO if color_str == "blanco" else COLOR_NEGRO
            pygame.draw.circle(self.pantalla, color, (x, y), 18)
            pygame.draw.circle(self.pantalla, (40, 40, 40), (x, y), 18, 2)


    # --- Zonas de salida (Bear-off) ---
    #  Zona izquierda inferior: fichas blancas retiradas
            pygame.draw.rect(self.pantalla, (230, 230, 230), (10, 400, 35, 140))  # recuadro blanco
            texto_out_blanco = fuente.render("OUT", True, (50, 50, 50))
            self.pantalla.blit(texto_out_blanco, (12, 380))

    #  Zona derecha superior: fichas negras retiradas
            pygame.draw.rect(self.pantalla, (50, 50, 50), (860, 60, 35, 140))  # recuadro negro
            texto_out_negro = fuente.render("OUT", True, (255, 255, 255))
            self.pantalla.blit(texto_out_negro, (862, 40))


    # --- Fichas ---
     self.dibujar_fichas()

    # --- Selección y destinos válidos ---
     if self.punto_seleccionado is not None:
        self.resaltar_punto(self.punto_seleccionado)

     if hasattr(self, "puntos_destino_validos"):
        for destino in self.puntos_destino_validos:
            if destino in self.hitmap:
                pygame.draw.rect(self.pantalla, (0, 255, 0), self.hitmap[destino], 3)

    # --- Info del juego ---
     self.dibujar_info()
     self.dibujar_boton_dados()
 
     if self.juego_terminado:
        self.mostrar_victoria()


    def dibujar_fichas(self):
     """Dibuja las fichas en el tablero y las retiradas (bear-off)."""
     puntos = self.juego.get_tablero().get_points()

    # --- Fichas en el tablero ---
     for punto_idx, pila in enumerate(puntos):
        if not pila:
            continue

        for j, ficha in enumerate(pila):
            color = COLOR_BLANCO if ficha.get_color() == "blanco" else COLOR_NEGRO

            # Coordenadas según el punto (arriba o abajo)
            if punto_idx <= 11:  # Puntos 0–11 (arriba)
                x = 60 + punto_idx * 65 + 32
                y = 80 + j * 22
            else:  # Puntos 12–23 (abajo)
                col = 23 - punto_idx
                x = 60 + col * 65 + 32
                y = 520 - j * 22

            pygame.draw.circle(self.pantalla, color, (x, y), 18)
            pygame.draw.circle(self.pantalla, (50, 50, 50), (x, y), 18, 2)

    # --- Fichas fuera del tablero (bear-off) ---
     fuera_blancas = self.juego.get_fichas_fuera("blanco")
     fuera_negras = self.juego.get_fichas_fuera("negro")

    # Blancas → arriba a la derecha
     for i, ficha in enumerate(fuera_blancas):
        x = 880
        y = 70 + i * 20
        pygame.draw.circle(self.pantalla, COLOR_BLANCO, (x, y), 10)
        pygame.draw.circle(self.pantalla, (50, 50, 50), (x, y), 10, 2)

    # Negras → abajo a la derecha
     for i, ficha in enumerate(fuera_negras):
        x = 880
        y = 530 - i * 20
        pygame.draw.circle(self.pantalla, COLOR_NEGRO, (x, y), 10)
        pygame.draw.circle(self.pantalla, (255, 255, 255), (x, y), 10, 2)


    def resaltar_punto(self, punto: int):
        if punto in self.hitmap:
            rect = self.hitmap[punto]
            pygame.draw.rect(self.pantalla, (0, 150, 255), rect, 3)  # celeste

    def dibujar_info(self):
     jugador = self.juego.get_turno()

    # --- Texto de turno ---
     texto_turno = fuente_grande.render(
        f"Turno: {jugador.get_nombre()} ({jugador.get_color()})",
        True,
        COLOR_TEXTO,
    )
     self.pantalla.blit(texto_turno, (100, 560))

    # --- Resultado de los dados ---
     texto_dados = fuente.render(
         f"Dados: {self.dados[0]} - {self.dados[1]}",
        True,
        COLOR_TEXTO,
    )
     self.pantalla.blit(texto_dados, (700, 640))  # más abajo y a la derecha
# --- Mensaje principal (rojo) ---
     
     if self.mensaje:
       texto_msg = fuente.render(self.mensaje, True, (200, 0, 0))
       self.pantalla.blit(texto_msg, (100, 590))  # más arriba y centrado
       pygame.draw.rect(self.pantalla, (230, 210, 180), (90, 620, 500, 70))

    # --- Instrucciones de colores ---
     ayuda1 = fuente.render(" Verde: puntos donde podés mover la ficha", True, (0, 180, 0))
     ayuda2 = fuente.render(" Azul: punto de llegada", True, (0, 120, 255))
     #ayuda3 = fuente.render(" Celeste: ficha seleccionada", True, (0, 160, 255))

    # ahora con separación visual más grande
     self.pantalla.blit(ayuda1, (100, 630))
     self.pantalla.blit(ayuda2, (100, 650))
     #self.pantalla.blit(ayuda3, (100, 670))

    def dibujar_boton_dados(self):
     """Dibuja el botón para tirar los dados."""
     mouse_pos = pygame.mouse.get_pos()
     color = COLOR_BOTON_HOVER if self.boton_dados.collidepoint(mouse_pos) else COLOR_BOTON

     # mover el botón un poco a la derecha y más abajo
     self.boton_dados = pygame.Rect(730, 600, 120, 45)


     pygame.draw.rect(self.pantalla, color, self.boton_dados, border_radius=8)
     texto_boton = fuente.render("Tirar dados", True, (0, 0, 0))
     self.pantalla.blit(texto_boton, (self.boton_dados.x + 10, self.boton_dados.y + 10))

    def mostrar_victoria(self):
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
     destinos = []
     dados = self.juego.get_dados_disponibles() or []
     if not dados:
        return destinos

     jugador = self.juego.get_turno()
     color = (jugador.get_color() or "").strip().lower()
     puntos = self.juego.get_tablero().get_points()

     for d in dados:
        # Blancas van hacia índices MENORES (→ 0..5)
        # Negras  van hacia índices MAYORES (→ 18..23)
        destino = punto_origen - d if color == "blanco" else punto_origen + d

        if 0 <= destino < 24:
            pila_destino = puntos[destino]
            if pila_destino and pila_destino[-1].get_color() != color and len(pila_destino) > 1:
                continue
            destinos.append(destino)

     return sorted(set(destinos))

    def manejar_click(self, posicion: tuple[int, int]):
     if self.juego_terminado:
        return

     jugador = self.juego.get_turno()
     color = jugador.get_color()
     dados = self.juego.get_dados_disponibles() or []
     print("DEBUG puede_sacar_fichas:", self.juego.puede_sacar_fichas(jugador))


    # --- Click en botón "Tirar dados" ---
     if self.boton_dados.collidepoint(posicion):
        if not self.dados_tirados:
            self.dados = self.juego.tirar_dados()
            self.dados_tirados = True
            self.mensaje = f"Dados: {self.dados[0]} - {self.dados[1]}"
        else:
            self.mensaje = "Ya tiraste los dados."
        return

    # --- Reingreso desde la barra ---
     bar_color = jugador.get_color()
     en_barra = self.juego.get_bar()[bar_color]

     if en_barra:  # 🔹 Solo si hay fichas en el BAR
        if not dados:
            self.mensaje = "Debes tirar los dados para reingresar desde el BAR."
            return

        # Puntos válidos según color y dados
        if bar_color == "blanco":
            posibles = [24 - d for d in dados]   # 1→23, 2→22, ..., 6→18
        else:
            posibles = [d - 1 for d in dados]    # 1→0,  2→1,  ..., 6→5

        puntos = self.juego.get_tablero().get_points()
        posibles = [
            p for p in posibles
            if 0 <= p < 24 and not (
                puntos[p] and puntos[p][-1].get_color() != bar_color and len(puntos[p]) > 1
            )
        ]

        # Si NO hay posibles casillas de entrada
        if not posibles:
            self.mensaje = "No hay movimientos válidos, se pasa el turno."
            self.juego.finalizar_turno()
            self.dados_tirados = False
            self.dados = (0, 0)
            turno = self.juego.get_turno()
            self.mensaje = f"Turno de {turno.get_nombre()} ({turno.get_color()})."
            pygame.display.flip()
            return

        # Mostrar opciones de reingreso
        self.punto_seleccionado = None
        self.puntos_destino_validos = posibles
        self.mensaje = "Reingresá una ficha desde el BAR."

        # --- Click sobre casillas válidas ---
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
                # Si no puede sacar ficha, simplemente muestra el mensaje y deja intentar mover
                  self.mensaje = str(e)
                # No bloquea el juego: no borres los dados ni cambies turno
                  return


        return  # Salir si el jugador tenía fichas en el BAR
            # --- Verificar si el jugador tiene movimientos posibles ---
     puntos = self.juego.get_tablero().get_points()
     color = jugador.get_color()
     dados = self.juego.get_dados_disponibles() or []

     movimientos_posibles = False
     for i, pila in enumerate(puntos):
        if pila and pila[-1].get_color() == color:
            destinos = self.calcular_destinos_validos(i)
            if destinos:
                movimientos_posibles = True
                break

    # Si no hay movimientos posibles, pasar turno automáticamente
     if not movimientos_posibles and self.dados_tirados:
        self.mensaje = "No hay movimientos posibles, se pasa el turno."
        self.juego.cambiar_turno()
        self.dados_tirados = False
        self.dados = (0, 0)
        turno = self.juego.get_turno()
        self.mensaje = f"Turno de {turno.get_nombre()} ({turno.get_color()})."
        pygame.display.flip()
        return
    
        # --- Intentar sacar ficha (fase Bear-Off) ---
     if self.juego.puede_sacar_fichas(jugador):
      puntos = self.juego.get_tablero().get_points()
     for punto, area in self.hitmap.items():
        if area.collidepoint(posicion):
            # Solo puede sacar si hay una ficha propia en ese punto
            if not puntos[punto] or puntos[punto][-1].get_color() != color:
                continue

            try:
                # Intenta sacar la ficha del tablero
                self.juego.sacar_ficha(jugador, punto)
                self.mensaje = f"Sacaste una ficha desde el punto {punto}."

                # Chequear si la jugada terminó en victoria
                ganador = self.juego.finalizar_jugada()
                if ganador:
                    self.juego_terminado = True
                    self.mensaje = f"🎉 ¡{ganador.get_nombre()} ganó la partida! 🎉"

                    # Mostrar el cartel de victoria en grande
                    self.pantalla.fill((0, 0, 0))
                    texto = fuente_victoria.render(self.mensaje, True, (255, 255, 255))
                    rect_texto = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
                    self.pantalla.blit(texto, rect_texto)
                    pygame.display.flip()

                    # Esperar unos segundos antes de cerrar la partida
                    pygame.time.wait(4000)
                    return

                # Si no ganó todavía, sigue el turno normal
                if not self.juego.get_dados_disponibles():
                    self.dados_tirados = False
                    self.dados = (0, 0)
                    turno = self.juego.get_turno()
                    self.mensaje = f"Turno de {turno.get_nombre()} ({turno.get_color()})."

                return

            except (MovimientoInvalidoException, FichaInvalidaException) as e:
                self.mensaje = str(e)
                return


     # --- Movimiento normal sobre el tablero ---
     for punto, area in self.hitmap.items():
        if area.collidepoint(posicion):
            puntos = self.juego.get_tablero().get_points()

            # Seleccionar una ficha
            if self.punto_seleccionado is None:
                if puntos[punto] and puntos[punto][-1].get_color() == jugador.get_color():
                    self.punto_seleccionado = punto
                    self.puntos_destino_validos = self.calcular_destinos_validos(punto)
                    self.mensaje = f"Ficha seleccionada en punto {punto}."
                else:
                    self.mensaje = "Debes seleccionar una ficha tuya."
                return

            # Intentar mover la ficha seleccionada
            else:
                if not self.juego.get_dados_disponibles():
                    self.mensaje = "Primero tirá los dados."
                    self.punto_seleccionado = None
                    self.puntos_destino_validos = []
                    return

                try:
                    self.juego.mover_ficha(jugador, self.punto_seleccionado, punto)
                    ganador = self.juego.finalizar_jugada()

                    if ganador:
                        self.juego_terminado = True
                        self.mensaje = f"🎉 ¡{ganador.get_nombre()} ganó!"
                    else:
                        if not self.juego.get_dados_disponibles():
                            self.dados_tirados = False
                            self.dados = (0, 0)
                            turno = self.juego.get_turno()
                            self.mensaje = f"Turno de {turno.get_nombre()} ({turno.get_color()})."
                        else:
                            self.mensaje = "Movimiento exitoso."

                    self.punto_seleccionado = None
                    self.puntos_destino_validos = []
                    self.dibujar_tablero()
                    pygame.display.flip()
                    return

                except (MovimientoInvalidoException, FichaInvalidaException) as e:
                    self.mensaje = str(e)
                    self.punto_seleccionado = None
                    self.puntos_destino_validos = []
                    return

    def ejecutar(self):
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

    # --- Bear-off (fase de sacar fichas) ---
    def dibujar_bear_off(self):
        """
        Área reservada para mostrar las fichas que ya fueron retiradas del tablero.
        Por ahora solo se dibuja un rectángulo placeholder (no funcional).
        """
        pygame.draw.rect(self.pantalla, (180, 160, 120), (870, 100, 40, 400))
        texto = fuente.render("Bear-off", True, (0, 0, 0))
        self.pantalla.blit(texto, (865, 70))

        #  En el futuro: se dibujarán las fichas sacadas del tablero.
        # Ejemplo:
        # for i, ficha in enumerate(self.juego.get_fichas_sacadas("blanco")):
        #     y = 500 - i * 25
        #     pygame.draw.circle(self.pantalla, COLOR_BLANCO, (890, y), 12)

# --- PRUEBA DIRECTA ---
# --- PRUEBA DIRECTA ---
if __name__ == "__main__":
    from codigo.jugadores import Jugador

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

