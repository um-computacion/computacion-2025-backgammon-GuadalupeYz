"""Lógica principal del juego Backgammon: manejo de tablero, jugadores, dados y reglas."""

from typing import List, Tuple, Optional
from codigo.jugadores import Jugador
from codigo.tablero import Tablero
from codigo.dados import Dados
from codigo.fichas import Ficha
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException


class BackgammonGame:
    """Controla toda la lógica del juego Backgammon."""

    def __init__(self) -> None:
        """Inicializa los componentes básicos del juego."""
        self.__jugadores: List[Jugador] = []
        self.__tablero: Tablero = Tablero()
        self.__dados: Dados = Dados()
        self.__turno_actual: int = 0
        self.__historial: List[str] = []
        self.__dados_disponibles: List[int] = []
        self.__bar: dict[str, List[Ficha]] = {"blanco": [], "negro": []}
        self.__ultima_tirada: Tuple[int, int] = (0, 0)
        self.__fichas_fuera_blanco: List[Ficha] = []
        self.__fichas_fuera_negro: List[Ficha] = []

    # -------- Getters --------
    def get_jugadores(self) -> List[Jugador]:
        """Devuelve la lista de jugadores."""
        return self.__jugadores

    def get_tablero(self) -> Tablero:
        """Devuelve el tablero actual."""
        return self.__tablero

    def get_fichas_fuera(self, color: str) -> List[Ficha]:
        """Devuelve las fichas fuera del tablero según el color."""
        return self.__fichas_fuera_blanco if color == "blanco" else self.__fichas_fuera_negro

    def get_dados(self) -> Dados:
        """Devuelve el objeto dados."""
        return self.__dados

    def get_historial(self) -> List[str]:
        """Devuelve el historial de movimientos."""
        return self.__historial

    def get_bar(self) -> dict[str, List[Ficha]]:
        """Devuelve el diccionario con las fichas en la barra."""
        return self.__bar

    def get_dados_disponibles(self) -> List[int]:
        """Devuelve los dados disponibles en el turno actual."""
        return list(self.__dados_disponibles)

    def get_ultima_tirada(self) -> Tuple[int, int]:
        """Devuelve la última tirada realizada."""
        return self.__ultima_tirada

    def get_turno(self) -> Jugador:
        """Devuelve el jugador del turno actual."""
        if not self.__jugadores:
            raise ValueError("No hay jugadores en la partida")
        return self.__jugadores[self.__turno_actual]

    def get_ganador(self) -> Optional[Jugador]:
        """Devuelve el jugador ganador si hay uno."""
        return self.chequear_victoria()

    # -------- Setters --------
    def set_tablero(self, tablero: Tablero) -> None:
        """Permite establecer un tablero nuevo."""
        self.__tablero = tablero

    def set_dados(self, dados: Dados) -> None:
        """Permite establecer un nuevo conjunto de dados."""
        self.__dados = dados

    # -------- Jugadores --------
    def agregar_jugador(self, jugador: Jugador) -> None:
        """Agrega un jugador a la partida."""
        if len(self.__jugadores) < 2:
            self.__jugadores.append(jugador)
        else:
            raise ValueError("Ya hay 2 jugadores en la partida")

    def iniciar_juego(self) -> None:
        """Inicia la partida si hay dos jugadores."""
        if len(self.__jugadores) != 2:
            raise ValueError("Se necesitan 2 jugadores para iniciar el juego")
        print("¡¡Comienza la partida de Backgammon!!")

    def setup_inicial(self) -> None:
        """Coloca las fichas en la posición inicial clásica del Backgammon real."""
        if len(self.__jugadores) != 2:
            raise ValueError("Se necesitan 2 jugadores para preparar el tablero inicial")

        jugador_blanco, jugador_negro = self.__jugadores
        self.__tablero = Tablero()

        # Limpia las fichas previas
        jugador_blanco._Jugador__fichas.clear()
        jugador_negro._Jugador__fichas.clear()

        # Posiciones iniciales
        posiciones_blancas = {23: 2, 12: 5, 7: 3, 5: 5}
        posiciones_negras = {0: 2, 11: 5, 16: 3, 18: 5}

        # Colocar fichas blancas
        for punto, cantidad in posiciones_blancas.items():
            for _ in range(cantidad):
                ficha = Ficha("blanco")
                jugador_blanco.agregar_ficha(ficha)
                self.__tablero.colocar_ficha(punto, ficha)

        # Colocar fichas negras
        for punto, cantidad in posiciones_negras.items():
            for _ in range(cantidad):
                ficha = Ficha("negro")
                jugador_negro.agregar_ficha(ficha)
                self.__tablero.colocar_ficha(punto, ficha)

        # Reiniciar estado
        self.__bar = {"blanco": [], "negro": []}
        self.__historial = []
        self.__dados_disponibles = []
        self.__ultima_tirada = (0, 0)

    # -------- Dados y turnos --------
    def tirar_dados(self) -> Tuple[int, int]:
        """Lanza los dados y actualiza los disponibles."""
        self.__ultima_tirada = self.__dados.roll()
        a, b = self.__ultima_tirada
        self.__dados_disponibles = [a, a, a, a] if a == b else [a, b]
        return self.__ultima_tirada

    def finalizar_turno(self) -> None:
        """Finaliza el turno actual."""
        self.__dados_disponibles.clear()
        self.cambiar_turno()

    def cambiar_turno(self) -> None:
        """Cambia al otro jugador."""
        if len(self.__jugadores) != 2:
            raise ValueError("Se necesitan 2 jugadores para cambiar turno")
        self.__turno_actual = 1 - self.__turno_actual
        self.__dados_disponibles = []
        self.__ultima_tirada = (0, 0)

    # -------- Reglas --------
    @staticmethod
    def __direccion(color: str) -> int:
        """Devuelve la dirección de movimiento según el color."""
        c = (color or "").strip().lower()
        return -1 if c == "blanco" else 1

    def __hay_que_reingresar(self, color: str) -> bool:
        """Devuelve True si hay fichas en la barra de ese color."""
        return len(self.__bar[color]) > 0

    def __validar_movimiento_basico(self, jugador: Jugador, origen: int, destino: int) -> int:
        """Valida si un movimiento es legal según el dado."""
        puntos = self.__tablero.get_points()

        if not (0 <= origen < 24) or not (0 <= destino < 24):
            raise MovimientoInvalidoException("El punto debe estar entre 0 y 23")

        if not puntos[origen]:
            raise MovimientoInvalidoException("No hay fichas en el punto de origen")

        ficha = puntos[origen][-1]
        if ficha.get_color() != jugador.get_color():
            raise FichaInvalidaException("La ficha no pertenece al jugador")

        dir_j = self.__direccion(jugador.get_color())
        delta = destino - origen

        if dir_j == -1 and delta >= 0:
            raise MovimientoInvalidoException("Solo se puede avanzar hacia la izquierda (blancas)")
        if dir_j == 1 and delta <= 0:
            raise MovimientoInvalidoException("Solo se puede avanzar hacia la derecha (negras)")

        distancia = abs(delta)
        if distancia not in self.__dados_disponibles:
            raise MovimientoInvalidoException("El movimiento no coincide con los dados disponibles")

        return distancia

    # -------- Movimiento --------
    def mover_ficha(self, jugador: Jugador, origen: int, destino: int) -> None:
        """Realiza el movimiento de una ficha si es válido."""
        if jugador != self.get_turno():
            raise MovimientoInvalidoException("No es el turno de este jugador")

        if self.__hay_que_reingresar(jugador.get_color()):
            raise MovimientoInvalidoException("Debes reingresar desde la barra antes de mover")

        if not self.__dados_disponibles:
            raise MovimientoInvalidoException("Aún no tiraste los dados")

        puntos = self.__tablero.get_points()
        distancia = self.__validar_movimiento_basico(jugador, origen, destino)

        if puntos[destino] and puntos[destino][-1].get_color() != jugador.get_color() and len(puntos[destino]) > 1:
            raise MovimientoInvalidoException("Punto bloqueado por el rival")

        if puntos[destino] and puntos[destino][-1].get_color() != jugador.get_color() and len(puntos[destino]) == 1:
            ficha_capturada = puntos[destino].pop()
            self.__bar[ficha_capturada.get_color()].append(ficha_capturada)
            self.__historial.append(
                f"{jugador.get_nombre()} capturó una ficha de color {ficha_capturada.get_color()} en {destino}"
            )

        ficha = puntos[origen].pop()
        self.__tablero.colocar_ficha(destino, ficha)
        self.__dados_disponibles.remove(distancia)
        self.__historial.append(f"{jugador.get_nombre()} movió una ficha de {origen} a {destino}")

        if not self.__dados_disponibles:
            self.cambiar_turno()

    def puede_sacar_fichas(self, jugador: Jugador) -> bool:
        """Devuelve True si el jugador puede empezar a sacar fichas."""
        color = jugador.get_color()
        puntos = self.__tablero.get_points()

        if color == "blanco":
            casa = range(0, 6)
        else:
            casa = range(18, 24)

        for i, pila in enumerate(puntos):
            for ficha in pila:
                if ficha.get_color() == color and i not in casa:
                    return False
        return True

    def chequear_victoria(self) -> Optional[Jugador]:
        """Devuelve el jugador que ganó (si no le quedan fichas en ningún lado)."""
        puntos = self.__tablero.get_points()

        for jugador in self.__jugadores:
            color = jugador.get_color()
            en_tablero = any(
                any(f.get_color() == color for f in pila)
                for pila in puntos
            )
            en_barra = len(self.__bar[color]) > 0
            en_lista = len(jugador.get_fichas()) > 0

            if not (en_tablero or en_barra or en_lista):
                return jugador
        return None

    def mostrar_estado(self) -> str:
        """Devuelve una cadena con el estado actual de la partida."""
        turno = self.get_turno().get_nombre() if self.__jugadores else "Ninguno"
        estado = f"Turno actual: {turno}\n"
        estado += f"Dados disponibles: {self.__dados_disponibles}\n"
        estado += f"Bar: {{blanco: {len(self.__bar['blanco'])}, negro: {len(self.__bar['negro'])}}}\n"
        estado += f"Historial (últimos 5): {self.__historial[-5:]}\n"
        return estado

    def reiniciar_partida(self) -> None:
        """Reinicia todo el estado del juego sin eliminar jugadores."""
        self.__tablero = Tablero()
        self.__dados = Dados()
        self.__turno_actual = 0
        self.__historial = []
        self.__dados_disponibles = []
        self.__bar = {"blanco": [], "negro": []}

    def sacar_ficha(self, jugador: Jugador, punto: int) -> None:
        """Permite sacar una ficha del tablero si las condiciones son válidas."""
        color = jugador.get_color()
        puntos = self.__tablero.get_points()

        if not self.puede_sacar_fichas(jugador):
            raise MovimientoInvalidoException("No podés sacar fichas hasta que todas estén en tu casa")
        if not puntos[punto]:
            raise MovimientoInvalidoException("No hay fichas en ese punto")

        ficha = puntos[punto][-1]
        if ficha.get_color() != color:
            raise FichaInvalidaException("La ficha no pertenece a este jugador")

        if not self.__dados_disponibles:
            raise MovimientoInvalidoException("Aún no tiraste los dados")

        # Distancia real de bear-off (regla estándar):
        # blancas (0..5) necesitan dado = punto + 1
        # negras  (18..23) necesitan dado = 24 - punto
        if color == "blanco":
            distancia = punto + 1
        else:
            distancia = 24 - punto

        dados = self.__dados_disponibles
        dado_a_usar = None

        if distancia in dados:
            dado_a_usar = distancia
        else:
            # Se permite usar un dado mayor SOLO si no hay fichas "más lejos" en la casa
            dados_mayores = sorted(d for d in dados if d > distancia)
            if dados_mayores:
                if color == "blanco":
                    # ¿hay blancas en puntos de índice mayor (más lejos de salir)?
                    hay_mas_lejos = any(
                        any(f.get_color() == "blanco" for f in puntos[i])
                        for i in range(punto + 1, 6)
                    )
                else:
                    # ¿hay negras en puntos de índice menor (más lejos de salir)?
                    hay_mas_lejos = any(
                        any(f.get_color() == "negro" for f in puntos[i])
                        for i in range(18, punto)
                    )
                if not hay_mas_lejos:
                    dado_a_usar = dados_mayores[0]
                else:
                    raise MovimientoInvalidoException(
                        "No podés sacar esta ficha aún (hay fichas más lejos)."
                    )
            else:
                raise MovimientoInvalidoException(
                    "El movimiento no coincide con los dados disponibles."
                )

        # Efectivizar bear-off
        puntos[punto].pop()
        if ficha in jugador.get_fichas():
            jugador.eliminar_ficha(ficha)

        if color == "blanco":
            self.__fichas_fuera_blanco.append(ficha)
        else:
            self.__fichas_fuera_negro.append(ficha)

        self.__dados_disponibles.remove(dado_a_usar)
        self.__historial.append(
            f"{jugador.get_nombre()} sacó una ficha del punto {punto} con dado {dado_a_usar}"
        )

        if not self.__dados_disponibles:
            self.cambiar_turno()

    def reingresar_ficha(self, jugador: Jugador, punto: int) -> None:
        """Permite reingresar una ficha desde la barra si es posible."""
        color = jugador.get_color()
        if not self.__bar[color]:
            raise MovimientoInvalidoException("El jugador no tiene fichas en el BAR")
        if not (0 <= punto < 24):
            raise MovimientoInvalidoException("El punto de reingreso debe estar entre 0 y 23")
        if not self.__dados_disponibles:
            raise MovimientoInvalidoException("Aún no tiraste los dados")

        puntos = self.__tablero.get_points()
        destino_fichas = puntos[punto]

        if destino_fichas and destino_fichas[-1].get_color() != color and len(destino_fichas) > 1:
            raise MovimientoInvalidoException("No se puede reingresar en un punto ocupado por más de una ficha rival")

        if destino_fichas and destino_fichas[-1].get_color() != color and len(destino_fichas) == 1:
            ficha_capturada = destino_fichas.pop()
            self.__bar[ficha_capturada.get_color()].append(ficha_capturada)
            self.__historial.append(
                f"{jugador.get_nombre()} capturó una ficha de color {ficha_capturada.get_color()} al reingresar en {punto}"
            )

        if color == "blanco":
            distancia = 24 - punto
        else:
            distancia = punto + 1

        if distancia not in self.__dados_disponibles:
            raise MovimientoInvalidoException("El reingreso no coincide con los dados disponibles")

        ficha = self.__bar[color].pop()
        self.__tablero.colocar_ficha(punto, ficha)
        self.__historial.append(f"{jugador.get_nombre()} reingresó una ficha en el punto {punto}")

        if distancia in self.__dados_disponibles:
            self.__dados_disponibles.remove(distancia)

        if self.__bar[color] and self.__dados_disponibles:
            return
        if not self.__dados_disponibles:
            self.cambiar_turno()

    def finalizar_jugada(self) -> Optional[Jugador]:
        """Chequea al final del turno si hay un ganador."""
        ganador = self.chequear_victoria()
        if ganador:
            print(f"{ganador.get_nombre()} ganó la partida.")
            return ganador
        return None
