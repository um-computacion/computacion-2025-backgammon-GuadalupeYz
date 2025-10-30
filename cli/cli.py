from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException

class CLI:
    def __init__(self) -> None:
        self.__juego: BackgammonGame | None = None
        self.__partida_activa: bool = False

    # ---------------- MENÚ PRINCIPAL ----------------
    def start(self) -> None:
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Iniciar partida")
            print("2. Ver historial de movimientos")
            print("3. Salir")
            print("4. Abandonar partida")

            opcion = input("Elegí una opción: ").strip()
            if opcion == "1":
                self.iniciar_partida()
            elif opcion == "2":
                self.mostrar_historial()
            elif opcion == "3":
                print("Saliendo del juego...")
                break
            elif opcion == "4":
                self.abandonar_partida()
            else:
                print("Opción inválida.")

    # ---------------- CONFIGURACIÓN DE PARTIDA ----------------
    def iniciar_partida(self) -> None:
        self.__juego = BackgammonGame()
        self.__partida_activa = True

        print("\nCargando jugadores...")
        nombre1 = input("Nombre del jugador 1 (blanco): ")
        nombre2 = input("Nombre del jugador 2 (negro): ")

        jugador1 = Jugador(nombre1, "blanco")
        jugador2 = Jugador(nombre2, "negro")

        self.__juego.agregar_jugador(jugador1)
        self.__juego.agregar_jugador(jugador2)
        self.__juego.iniciar_juego()
        self.__juego.setup_inicial()

        print(f"\nPartida iniciada entre {nombre1} y {nombre2}. ¡A jugar!\n")

        self.loop_partida()

    # ---------------- LOOP PRINCIPAL DE JUEGO ----------------
    def loop_partida(self) -> None:
        while self.__partida_activa:
            jugador = self.__juego.get_turno()
            color = jugador.get_color()

            print(f"\nTurno de {jugador.get_nombre()} ({color})")
            input("Presioná ENTER para tirar los dados...")
            dados = self.__juego.tirar_dados()
            print(f"Resultado del tiro: {dados[0]} y {dados[1]}")
            print("-------------------------------------------------------")

            self.mostrar_tablero()

            # 1️⃣ Si hay fichas en el BAR → reingreso
            bar = self.__juego.get_bar()[color]
            if bar:
                print(f"Tienes {len(bar)} ficha(s) en el BAR. Debes reingresar antes de mover.")
                while bar and self.__juego.get_dados_disponibles():
                    try:
                        punto = int(input("Elegí el punto para reingresar: "))
                        self.__juego.reingresar_ficha(jugador, punto)
                        self.mostrar_tablero()
                    except Exception as e:
                        print(f" Error: {e}")
                continue

            # 2️⃣ Si puede sacar fichas (fase Bear-Off)
            if self.__juego.puede_sacar_fichas(jugador):
                print("⚪ Estás en fase de BEAR-OFF: podés sacar fichas del tablero.")
                while self.__juego.get_dados_disponibles():
                    try:
                        punto = int(input("Elegí el punto desde donde querés sacar ficha: "))
                        self.__juego.sacar_ficha(jugador, punto)
                        self.mostrar_tablero()
                        ganador = self.__juego.finalizar_jugada()
                        if ganador:
                            print(f"🎉 ¡{ganador.get_nombre()} ganó la partida! 🎉")
                            self.__partida_activa = False
                            return
                    except Exception as e:
                        print(f" Error: {e}")
                        break
                continue

            # 3️⃣ Movimiento normal
            while self.__juego.get_dados_disponibles():
                try:
                    origen = int(input("Elegí el punto de origen: "))
                    destino = int(input("Elegí el punto de destino: "))
                    self.__juego.mover_ficha(jugador, origen, destino)
                    self.mostrar_tablero()
                    self.mostrar_historial_turno()
                except (MovimientoInvalidoException, FichaInvalidaException, ValueError) as e:
                    print(f" Error: {e}")

                if not self.__juego.get_dados_disponibles():
                    print("No te quedan dados disponibles.")
                    break

                continuar = input("¿Querés mover otra ficha con el dado restante? (s/n): ")
                if continuar.lower() != "s":
                    break

            # 4️⃣ Chequear victoria o pasar turno
            ganador = self.__juego.finalizar_jugada()
            if ganador:
                print(f"🎉 ¡{ganador.get_nombre()} ganó la partida! 🎉")
                self.__partida_activa = False
                break

    def leer_entero(self, mensaje: str) -> int:
        """Pide un número y valida que sea entero."""
        while True:
            valor = input(mensaje).strip()
            if not valor:
                print(" No se puede dejar vacío. Intentá de nuevo.")
                continue
            if not valor.isdigit():
                print(" Debes ingresar un número entero válido.")
                continue
            return int(valor)

    # ---------------- MOSTRAR TABLERO ----------------
    def mostrar_tablero(self) -> None:
        puntos = self.__juego.get_tablero().get_points()

        print("\n" + "=" * 70)
        print(" " * 25 + "TABLERO DE BACKGAMMON")
        print("=" * 70)

        print("\nZona superior (puntos 23→12):")
        fila_superior = ""
        for i in range(23, 11, -1):
            if puntos[i]:
                color = puntos[i][-1].get_color()[0].upper()
                cantidad = len(puntos[i])
                fila_superior += f"{i:2d}[{color}{cantidad}] "
            else:
                fila_superior += f"{i:2d}[  ] "
        print(fila_superior)

        print("\nZona inferior (puntos 0→11):")
        fila_inferior = ""
        for i in range(0, 12):
            if puntos[i]:
                color = puntos[i][-1].get_color()[0].upper()
                cantidad = len(puntos[i])
                fila_inferior += f"{i:2d}[{color}{cantidad}] "
            else:
                fila_inferior += f"{i:2d}[  ] "
        print(fila_inferior)
        print("=" * 70)

    # ---------------- HISTORIAL ----------------
    def mostrar_historial_turno(self) -> None:
        historial = self.__juego.get_historial()
        if historial:
            print("\nÚltimos movimientos:")
            for linea in historial[-3:]:
                print("-", linea)
        print("-------------------------------------------------------")

    def mostrar_historial(self) -> None:
        if not self.__juego:
            print("Todavía no hay partida iniciada.")
            return
        historial = self.__juego.get_historial()
        if not historial:
            print("No hay movimientos registrados.")
        else:
            print("\nHistorial completo:")
            for mov in historial:
                print("-", mov)
        print("-------------------------------------------------------")

    # ---------------- ABANDONAR ----------------
    def abandonar_partida(self) -> None:
        if not self.__partida_activa:
            print("No hay partida en curso.")
            return
        confirm = input("¿Seguro que querés abandonar la partida? (s/n): ").strip().lower()
        if confirm == "s":
            print("Partida abandonada. Volviendo al menú principal.")
            self.__partida_activa = False
            self.__juego = None

# ---------------- MAIN ----------------
if __name__ == "__main__":
    cli = CLI()
    cli.start()
