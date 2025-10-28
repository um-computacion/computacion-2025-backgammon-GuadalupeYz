from typing import List, Tuple, Optional
from codigo.jugadores import Jugador
from codigo.tablero import Tablero
from codigo.dados import Dados
from codigo.fichas import Ficha
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException

class BackgammonGame:
    def __init__(self) -> None:
        self.__jugadores: List[Jugador] = []
        self.__tablero: Tablero = Tablero()
        self.__dados: Dados = Dados()
        self.__turno_actual: int = 0
        self.__historial: List[str] = []
        self.__dados_disponibles: List[int] = []
        self.__bar: dict[str, List[Ficha]] = {"blanco": [], "negro": []}
        self.__ultima_tirada: Tuple[int, int] = (0, 0)

    # -------- Getters básicos --------
    def get_jugadores(self) -> List[Jugador]:
        return self.__jugadores

    def get_tablero(self) -> Tablero:
        return self.__tablero

    def get_dados(self) -> Dados:
        return self.__dados

    def get_historial(self) -> List[str]:
        return self.__historial

    def get_bar(self) -> dict[str, List[Ficha]]:
        return self.__bar

    def get_dados_disponibles(self) -> List[int]:
        """Devuelve una copia de los dados que quedan por usar en el turno actual."""
        return list(self.__dados_disponibles)

    def get_ultima_tirada(self) -> Tuple[int, int]:
        return self.__ultima_tirada

    def get_turno(self) -> Jugador:
        if not self.__jugadores:
            raise ValueError("No hay jugadores en la partida")
        return self.__jugadores[self.__turno_actual]

    def get_ganador(self) -> Optional[Jugador]:
        """Compatibilidad con la UI: devuelve ganador o None."""
        return self.chequear_victoria()

    # -------- Setters básicos --------
    def set_tablero(self, tablero: Tablero) -> None:
        self.__tablero = tablero

    def set_dados(self, dados: Dados) -> None:
        self.__dados = dados

    # -------- Gestión de jugadores / inicio --------
    def agregar_jugador(self, jugador: Jugador) -> None:
        if len(self.__jugadores) < 2:
            self.__jugadores.append(jugador)
        else:
            raise ValueError("Ya hay 2 jugadores en la partida")

    def iniciar_juego(self) -> None:
        if len(self.__jugadores) != 2:
            raise ValueError("Se necesitan 2 jugadores para iniciar el juego")
        print("¡¡Comienza la partida de Backgammon!!")

    def setup_inicial(self) -> None:
     """
     Coloca las fichas en la posición inicial clásica del Backgammon real.
     Blancas se mueven en sentido horario, negras antihorario.
     """
     if len(self.__jugadores) != 2:
        raise ValueError("Se necesitan 2 jugadores para preparar el tablero inicial")

     jugador_blanco, jugador_negro = self.__jugadores
     self.__tablero = Tablero()

    # Limpia las fichas previas de los jugadores
     # Limpia las fichas previas de los jugadores
     jugador_blanco._Jugador__fichas.clear()
     jugador_negro._Jugador__fichas.clear()


    # --- Posiciones iniciales estándar ---
     posiciones_blancas = {23: 2, 12: 5, 7: 3, 5: 5}  # blancas (sentido horario)
     posiciones_negras = {0: 2, 11: 5, 16: 3, 18: 5}  # negras (antihorario)

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

    # Reiniciar barra, historial y dados
     self.__bar = {"blanco": [], "negro": []}
     self.__historial = []
     self.__dados_disponibles = []
     self.__ultima_tirada = (0, 0)

    # -------- Tirada y fin de turno --------
    def tirar_dados(self) -> Tuple[int, int]:
        self.__ultima_tirada = self.__dados.roll()
        a, b = self.__ultima_tirada
        # Si es doble: cuatro movimientos; si no, dos.
        self.__dados_disponibles = [a, a, a, a] if a == b else [a, b]
        return self.__ultima_tirada

    def finalizar_turno(self) -> None:
        """Forzar fin de turno desde la UI."""
        self.__dados_disponibles.clear()
        self.cambiar_turno()

    def cambiar_turno(self) -> None:
     if len(self.__jugadores) != 2:
        raise ValueError("Se necesitan 2 jugadores para cambiar turno")
    # alternar 0 ↔ 1
     self.__turno_actual = 1 - self.__turno_actual
    #  limpiar estado de dados para el nuevo jugador
     self.__dados_disponibles = []
     self.__ultima_tirada = (0, 0)

    # -------- Reglas auxiliares --------
    @staticmethod
    def __direccion(color: str) -> int:
     """
     Devuelve la dirección de movimiento según el color:
     - Blanco: avanza hacia la IZQUIERDA (sentido horario)
     - Negro: avanza hacia la DERECHA (sentido antihorario)
     """
     c = (color or "").strip().lower()
     return -1 if c == "blanco" else 1

   
    def __hay_que_reingresar(self, color: str) -> bool:
        return len(self.__bar[color]) > 0
 
    def __validar_movimiento_basico(self, jugador: Jugador, origen: int, destino: int) -> int:
     puntos = self.__tablero.get_points()

     if not (0 <= origen < 24) or not (0 <= destino < 24):
        raise MovimientoInvalidoException("El punto debe estar entre 0 y 23")

     if not puntos[origen]:
        raise MovimientoInvalidoException("No hay fichas en el punto de origen")

     ficha = puntos[origen][-1]
     if ficha.get_color() != jugador.get_color():
        raise FichaInvalidaException("La ficha no pertenece al jugador")

    #  Usamos la dirección para determinar el sentido correcto
     dir_j = self.__direccion(jugador.get_color())
     delta = destino - origen

#  Blancas (-1) deben moverse hacia índices menores
#  Negras (+1) deben moverse hacia índices mayores
     if dir_j == -1 and delta >= 0:
      raise MovimientoInvalidoException("Solo se puede avanzar hacia la izquierda (blancas)")
     if dir_j == 1 and delta <= 0:
      raise MovimientoInvalidoException("Solo se puede avanzar hacia la derecha (negras)")

     distancia = abs(delta)
     if distancia not in self.__dados_disponibles:
        raise MovimientoInvalidoException("El movimiento no coincide con los dados disponibles")

     return distancia

    # -------- Movimiento normal --------
    def mover_ficha(self, jugador: Jugador, origen: int, destino: int) -> None:
        # Turno correcto
        if jugador != self.get_turno():
            raise MovimientoInvalidoException("No es el turno de este jugador")

        # Si hay fichas en la barra, primero hay que reingresar
        if self.__hay_que_reingresar(jugador.get_color()):
            raise MovimientoInvalidoException("Debes reingresar desde la barra antes de mover")

        if not self.__dados_disponibles:
            raise MovimientoInvalidoException("Aún no tiraste los dados")

        puntos = self.__tablero.get_points()
        # Validaciones básicas y distancia en dirección correcta
        distancia = self.__validar_movimiento_basico(jugador, origen, destino)

        if distancia not in self.__dados_disponibles:
            raise MovimientoInvalidoException("El movimiento no coincide con los dados disponibles")

        # Bloqueo por punto rival con 2+ fichas
        if puntos[destino] and puntos[destino][-1].get_color() != jugador.get_color() and len(puntos[destino]) > 1:
            raise MovimientoInvalidoException("Punto bloqueado por el rival")

        # Captura (blot)
        if puntos[destino] and puntos[destino][-1].get_color() != jugador.get_color() and len(puntos[destino]) == 1:
            ficha_capturada = puntos[destino].pop()
            self.__bar[ficha_capturada.get_color()].append(ficha_capturada)
            self.__historial.append(
                f"{jugador.get_nombre()} capturó una ficha de color {ficha_capturada.get_color()} en {destino}"
            )

        # Mover la ficha
        ficha = puntos[origen].pop()
        self.__tablero.colocar_ficha(destino, ficha)

        # Consumir dado usado
        self.__dados_disponibles.remove(distancia)
        self.__historial.append(f"{jugador.get_nombre()} movió una ficha de {origen} a {destino}")

        # Si ya no quedan dados, cambiar turno
        if not self.__dados_disponibles:
            self.cambiar_turno()

    # -------- Reingreso desde la barra --------
    def reingresar_ficha(self, jugador: Jugador, punto: int) -> None:
     color = jugador.get_color()
     if not self.__bar[color]:
        raise MovimientoInvalidoException("El jugador no tiene fichas en el bar")
     if not (0 <= punto < 24):
        raise MovimientoInvalidoException("El punto de reingreso debe estar entre 0 y 23")
     if not self.__dados_disponibles:
        raise MovimientoInvalidoException("Aún no tiraste los dados")

     destino_fichas = self.__tablero.get_points()[punto]
     if destino_fichas and destino_fichas[0].get_color() != color and len(destino_fichas) > 1:
        raise MovimientoInvalidoException("No se puede reingresar en un punto ocupado por más de una ficha rival")

    # Puntos de entrada reales:
    # - blancas entran en 23..18 según dado d -> punto = 24 - d ; distancia usada = 24 - punto
    # - negras  entran en 0..5  según dado d -> punto = d - 1   ; distancia usada = punto + 1
     if color == "blanco":
        distancia = 24 - punto
     else:
        distancia = punto + 1

     if distancia not in self.__dados_disponibles:
        raise MovimientoInvalidoException("El reingreso no coincide con los dados disponibles")
 
     ficha = self.__bar[color].pop()
     self.__tablero.colocar_ficha(punto, ficha)
     self.__historial.append(f"{jugador.get_nombre()} reingresó una ficha en {punto}")

     self.__dados_disponibles.remove(distancia)
     if not self.__dados_disponibles:
        self.cambiar_turno()

    # -------- Estado / victoria / reinicio --------
    def chequear_victoria(self) -> Optional[Jugador]:
        for jugador in self.__jugadores:
            if jugador.cantidad_fichas() == 0:
                return jugador
        return None

    def mostrar_estado(self) -> str:
        turno = self.get_turno().get_nombre() if self.__jugadores else "Ninguno"
        estado = f"Turno actual: {turno}\n"
        estado += f"Dados disponibles: {self.__dados_disponibles}\n"
        estado += f"Bar: {{blanco: {len(self.__bar['blanco'])}, negro: {len(self.__bar['negro'])}}}\n"
        estado += f"Historial (últimos 5): {self.__historial[-5:]}\n"
        return estado

    def reiniciar_partida(self) -> None:
        self.__tablero = Tablero()
        self.__dados = Dados()
        self.__turno_actual = 0
        self.__historial = []
        self.__dados_disponibles = []
        self.__bar = {"blanco": [], "negro": []}

    def finalizar_jugada(self) -> Optional[Jugador]:
        ganador = self.chequear_victoria()
        if ganador:
            print(f"🎉 ¡{ganador.get_nombre()} ganó la partida! 🎉")
            return ganador
        return None
