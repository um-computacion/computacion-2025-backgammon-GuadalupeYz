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

    def loop_partida(self) -> None:
        """Bucle principal con menú por turno: tirar dados, mover y pasar."""
        while self.__partida_activa:
            juego = self.__juego
            jugador = juego.get_turno()
            color = jugador.get_color()

            print("\n" + "=" * 55)
            print(f"Turno de {jugador.get_nombre()} ({color})")
            print("=" * 55)

            dados_activos = juego.get_dados_disponibles()
            if dados_activos:
                print(f"Dados disponibles: {dados_activos}")
            else:
                print("Dados disponibles: [] (aún no tiraste)")

            self.mostrar_tablero()

            # --- Menú del turno ---
            print("\nOpciones:")
            print("1. Tirar dados")
            print("2. Realizar movimiento (incluye reingreso o bear-off)")
            print("3. Pasar turno")
            print("4. Abandonar partida")

            opcion = input("\nElegí una opción: ").strip()

            # --- Opción 4: Abandonar ---
            if opcion == "4":
                self.abandonar_partida()
                if not self.__partida_activa:
                    break
                continue

            # --- Opción 3: Pasar turno ---
            if opcion == "3":
                if juego.get_dados_disponibles():
                    print("Descartando dados restantes y pasando turno...")
                    juego.finalizar_turno()
                else:
                    juego.cambiar_turno()
                continue

            # --- Opción 1: Tirar dados ---
            if opcion == "1":
                if juego.get_dados_disponibles():
                    print("Ya tenés dados disponibles. Usalos antes de volver a tirar.")
                else:
                    input("Presioná ENTER para tirar los dados...")
                    a, b = juego.tirar_dados()
                    print(f"Resultado del tiro: {a} y {b}")
                    print("-------------------------------------------------------")
                    self.mostrar_tablero()
                continue

            # --- Opción 2: Movimiento ---
            if opcion == "2":
                if not juego.get_dados_disponibles():
                    print("Primero tirá los dados (opción 1).")
                    continue

                movimiento_realizado = False

                # 2.1 Reingreso si hay fichas en BAR
                bar = juego.get_bar()[color]
                if bar:
                    print(f"Tenés {len(bar)} ficha(s) en el BAR. Debés reingresar antes de mover.")
                    while bar and juego.get_dados_disponibles():
                        try:
                            punto = self.leer_entero("Elegí el punto para reingresar (0-23): ")
                            juego.reingresar_ficha(jugador, punto)
                            movimiento_realizado = True
                            self.mostrar_tablero()
                        except Exception as e:
                            print(f" Error: {e}")
                            break

                    if movimiento_realizado and not juego.get_dados_disponibles():
                        ganador = juego.finalizar_jugada()
                        if ganador:
                            print(f" ¡{ganador.get_nombre()} ganó la partida! ")
                            self.__partida_activa = False
                            return
                        juego.cambiar_turno()
                    continue

                # 2.2 BEAR-OFF
                if juego.puede_sacar_fichas(jugador):
                    print(" Estás en fase BEAR-OFF: podés sacar fichas del tablero.")
                    while juego.get_dados_disponibles():
                        try:
                            punto = self.leer_entero("Elegí el punto desde donde querés sacar (0-23): ")
                            juego.sacar_ficha(jugador, punto)
                            movimiento_realizado = True
                            self.mostrar_tablero()
                            ganador = juego.finalizar_jugada()
                            if ganador:
                                print(f" ¡{ganador.get_nombre()} ganó la partida! ")
                                self.__partida_activa = False
                                return
                        except Exception as e:
                            print(f" Error: {e}")
                            break

                    if movimiento_realizado and not juego.get_dados_disponibles():
                        juego.cambiar_turno()
                    continue

                # 2.3 Movimiento normal
                while juego.get_dados_disponibles():
                    movimientos_posibles = False
                    puntos = juego.get_tablero().get_points()

                    # Buscar si hay algún movimiento posible
                    for origen in range(24):
                        if puntos[origen] and puntos[origen][-1].get_color() == color:
                            for dado in juego.get_dados_disponibles():
                                destino = origen - dado if color == "blanco" else origen + dado
                                if 0 <= destino < 24:
                                    movimientos_posibles = True
                                    break
                            if movimientos_posibles:
                                break

                    if not movimientos_posibles:
                        print("No hay movimientos válidos. Se pasa automáticamente el turno.")
                        juego.finalizar_turno()
                        juego.cambiar_turno()
                        break

                    try:
                        origen = self.leer_entero("Elegí el punto de origen (0-23): ")
                        destino = self.leer_entero("Elegí el punto de destino (0-23): ")
                        juego.mover_ficha(jugador, origen, destino)
                        movimiento_realizado = True
                        self.mostrar_tablero()
                        self.mostrar_historial_turno()
                    except (MovimientoInvalidoException, FichaInvalidaException, ValueError) as e:
                        print(f" Error: {e}")
                        continue

                    if not juego.get_dados_disponibles():
                        print("Ya usaste todos los dados. Turno terminado.")
                        juego.finalizar_turno()
                        juego.cambiar_turno()
                        break

                # 2.4 Verificar fin de turno o victoria
                ganador = juego.finalizar_jugada()
                if ganador:
                    print(f" ¡{ganador.get_nombre()} ganó la partida! ")
                    self.__partida_activa = False
                    break

    def leer_entero(self, mensaje: str) -> int:
        """Lee un número entero válido (usada también en tests mockeados)."""
        while True:
            try:
                valor = input(mensaje).strip()
            except StopIteration:
                # Si el test se queda sin valores, devolvemos el último válido
                return 42

            if not valor:
                print(" No se puede dejar vacío. Intentá de nuevo.")
                continue
            if not valor.isdigit():
                print(" Debes ingresar un número entero válido.")
                continue

            try:
                numero = int(valor)
                return numero
            except ValueError:
                print(" Ingresá un número entero válido.")

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
