JUSTIFICACION DEL DISEÑO PROYECTO BACKGAMMON

Guadalupe Yañez
Materia: Computación 
Año: 2025

1. Resumen del diseño general

El proyecto implementa el juego Backgammon utilizando Python y una arquitectura orientada a objetos.
Se diseñó un núcleo lógico (en la carpeta codigo/) independiente de las interfaces de usuario (CLI y Pygame), de modo que ambas compartan la misma lógica de juego.

El sistema se estructura según los principios de responsabilidad única y encapsulamiento, separando la lógica de negocio (movimientos, turnos, validaciones) de la visualización (interfaz de texto o gráfica).

2. Justificación de las clases elegidas

BackgammonGame: Representa la lógica principal del juego.
Responsabilidades:
Coordinar el flujo de la partida.
Controlar los turnos de los jugadores.
Verificar condiciones de victoria.
Gestionar el tablero, los dados y las fichas.
Se eligió como clase central para mantener el control general del sistema y contener las demás entidades (jugadores, tablero, dados, excepciones).

CLI: Implementa la interfaz de texto del juego.
Responsabilidades:
Permitir la interacción del usuario por consola.
Mostrar el estado del tablero, los dados y el historial de movimientos.
Capturar entradas y validar opciones.
Se separa de la lógica del juego para seguir el principio MVC (Modelo-Vista-Controlador), donde la CLI actúa como “vista”.

Dados: Modela los dados del Backgammon.
Responsabilidades:
Generar tiradas aleatorias válidas entre 1 y 6.
Controlar los valores disponibles por turno.
Se creó como clase independiente para facilitar las pruebas unitarias y reutilización en ambas interfaces.

Excepciones: Define errores personalizados del juego.
Responsabilidades:
Distinguir errores de lógica propios del Backgammon de errores de Python.
Manejar casos como:
Movimiento inválido.
Ficha incorrecta.
Reingreso imposible.
Turno incorrecto.
Permite mantener el código limpio y comprensible, separando los flujos normales de los errores.

Fichas: Representa cada ficha del tablero.
Responsabilidades:
Almacenar el color (blanco o negro).
Identificar a qué jugador pertenece.
Permitir operaciones básicas como agregar o quitar fichas.
Su separación mejora la claridad y permite manipularlas sin acoplarlas al jugador o al tablero directamente.

Jugadores: Modela los jugadores del juego.
Responsabilidades:
Almacenar nombre, color y sus fichas.
Calcular la cantidad de fichas restantes.
Permitir agregar o eliminar fichas de su lista.
Esta separación facilita gestionar turnos, identificar ganadores y aplicar reglas individuales.

Tablero: Representa los 24 puntos del Backgammon.
Responsabilidades:
Almacenar las pilas de fichas en cada punto.
Permitir colocar o retirar fichas.
Exponer el estado actual del tablero para las interfaces.
Se mantiene separada del juego principal para cumplir con el principio SRP (Single Responsibility Principle): el tablero solo conoce las posiciones, no las reglas.

3. Justificación de los atributos
__jugadores: lista de objetos Jugador para mantener referencia directa a los participantes.
__tablero: objeto Tablero, facilita modificar posiciones sin mezclar reglas.
__dados: instancia de Dados, aislada para probar tiradas.
__bar: diccionario con fichas capturadas de cada color.
__fichas_fuera_blanco / __fichas_fuera_negro: control del “bear-off” (fase de sacar fichas).
__historial: lista de strings que documenta los movimientos realizados.
__dados_disponibles y __ultima_tirada: controlan los movimientos válidos por turno.

Cada atributo cumple una función específica y ayuda a mantener el encapsulamiento y la legibilidad.

4. Decisiones de diseño relevantes

Se eligió programación orientada a objetos para modelar las entidades del juego de forma modular.
La lógica del juego (BackgammonGame) se separó de las interfaces (CLI y Pygame) para facilitar pruebas, mantenimiento y reuso.
Se implementaron métodos auxiliares como puede_sacar_fichas() y chequear_victoria() para aislar las reglas del Backgammon.
Se implementó el patrón de diseño MVC en sentido práctico:

Modelo: codigo/ (toda la lógica).
Vista: cli/ y pygame_ui/.
Controlador: BackgammonGame (coordina la interacción).

5. Excepciones y manejo de errores

Excepciones personalizadas definidas en codigo/excepciones.py:

MovimientoInvalidoException	Se lanza cuando el jugador intenta un movimiento no permitido.
FichaInvalidaException	Se lanza cuando la ficha elegida no pertenece al jugador actual.

El manejo de errores en CLI y Pygame evita que el juego se interrumpa ante un error de entrada o movimiento inválido.
Cada excepción se captura y muestra un mensaje descriptivo para el usuario.

6. Estrategia de testing y cobertura

Se usó unittest para realizar pruebas unitarias.
Se probaron todos los módulos de la lógica central:
Movimientos válidos e inválidos.
Reingreso desde la barra.
Fase de “bear-off”.
Cambio de turnos.
Condición de victoria.
Se crearon tests específicos para las interfaces (CLI y Pygame) con unittest.mock.
Se alcanzó una cobertura superior al 90%, medida con coverage.
La integración continua (GitHub Actions) ejecuta los tests automáticamente en cada push o PR hacia main.

7. Cumplimiento de principios SOLID

S – Single Responsibility	Cada clase tiene una única función (por ejemplo, Tablero solo gestiona posiciones).
O – Open/Closed	  El sistema puede ampliarse con nuevas interfaces sin modificar la lógica central.
L – Liskov Substitution 	Las clases se usan a través de interfaces bien definidas (ej. fichas y jugadores).
I – Interface Segregation	Cada clase expone solo los métodos que necesita.
D – Dependency Inversion	Las interfaces (CLI y Pygame) dependen de la lógica abstracta del juego, no de implementaciones concretas.