Aca pondre la justificacion del codigo elegido como dice en el docuemnto:

Archivo obligatorio: JUSTIFICACION.md (Solo se aceptaran archivos en formato markdown).
Contenido mínimo:
Resumen del diseño general.
Justificación de las clases elegidas (por qué, responsabilidades).
Justificación de atributos (por qué se eligieron).
Decisiones de diseño relevantes
Excepciones y manejo de errores (qué excepciones definidas y por qué).
Estrategias de testing y cobertura (qué se probó y por qué).
Referencias a requisitos SOLID y cómo se cumplen.
Anexos: diagramas UML(ej: diagrama de clases).

Empiezo con lo puesto en los archivo:

Backgammon:
#representa el juego de backgammon.
#justificacion: esta clase es para manejar la logica general del juego, como
#el turno de los jugadores, el estado del juego (en curso, terminado), etc.
#ademas de contener las demas clases que representan los componentes del juego.

CLI:
#interfaz de texto para jugar al backgammon.
#justificacion: esta interfaz es para que el usuario pueda interactuar con el juego
#de manera sencilla, mostrando el estado del tablero, las fichas, los turnos, etc.

Dados:
#representa los dados del backgammon.
#justificacion: esta clase es porque en el backgammon los turnos se dan en tirar 
#los dos dados. Entonces en esta clase dado pongo esa lógica de tirarlos y devolver 
#el resultado. 

Excepciones:
#representa las excepciones personalizadas del backgammon.
#justificacion: esta clase es para manejar errores del juego, como pueden ser
#movimientos no validos(por ej cuando se llega a una casilla ocupada por 2 o mas 
#fichas del oponente), mover la ficha encapsulada y no otra, etc. 

Fichas:
#representa las fichas del backgammon.
#justificacion: esta clase es para que cada ficha tenga su color, posicion, jugador 
#al que pertenece, etc.

Jugadores:
#representa a los jugadores del backgammon.
#justificacion: esta clase es para separar la logica de los jugadores
#del juego en general, para q cada uno tenga su nombre, sus propias fichas, estado, etc.

Tablero:
#representa el tablero del backgammon.
#justificacion: separo el tablero para que el manejo de las fichas,los
#movimientos,etc no se mezcle con la logica general del juego.
    