cambios sprint 1

#commit 1
24/08: cree un readme inicial explicando mi primer dia, en donde tengo que estudiar el
juego backgammon. Tmb hice un archivo de codigo y un archivo de test para luego expandir.

#commit 2
25/08: habiendo estudiado el juego cree los archivos q entiendo necesarios y los 
solicitados en el docuemnto, acompañados de una justificacion. 

#commit 3
26/08: agrego codigo en tablero.py , en dados.py y en cli.py ,es inicial, mañana sigo. Tmb agrege carpeta git.

#commit 4
27/08: agrego y modifico codigo en tablero.py, en dados.py y en cli.py. Tmb cambio el README ya que lo estaba usando mal. Agrego archivo test_cli.py. Plantee los primeros test 
para cli, tablero y dados.

#commit 5
28/08: hice codigo inicial de la clase jugador, y su test inicial tmb. 

#commit 6
29/08: agrego un test mas a jugador que me falto probar la funcion obtener_fichas. Tmb la base de la clase ficha, mañana sigo con eso. 

#commit 7
30/08: integre la clase ficha en jugadores, por lo que tmb cambie esto en test jugadores y cree unos test iniciales de ficha. Tmb cambie los test de tablero que tenian un error ya que me olvide de cambiar los atributos. 

#commit 8
31/08: ahora empiezo con clase backgammon y probando ese codigo en sus test iniciales.

#commit 9 
01/09: cmabie en jugadores y dados la implementacion que mencionaron los profesores "Atributos con el prefijo __ delante y la implementación de setter y getter" , por lo que cambie sus test tmb.

#commit 10
02/09: segui con los cambios de getters y setters en fichas, tablero y backgammon. En sus codigo y sus tests.

cambios sprint 2 

#commit 1
04/09: Plantie la primer excepcion de la logica del juego. Y cambie cli agregando set and get y su test. 

#commit 2
07/09: Cambie el codigo tablero para agregar validacion al poner fichas (maximo 15 fichas por punto y rango entre 0 y 23), con getters/setters y cambie los tests 

#commit 3
08/09: Mejore la clase Jugador agregando eliminar_ficha con su validacion. Tamb los tests de Jugador.

#commit 4
09/09: Actualice BackgammonGame para que al iniciar el juego se coloquen las fichas de jugadores en el tablero. Tamb cambie los tests para verificarlo.

#commit 5
10/09: Defini MovimientoInvalidoException en excepciones.py para aplicarlo en jugadores.py y probarlo en sus test. 

#commit 6 
11/09: Hice los test de excepciones para vereficarlas en test_excepciones.py. 

#commit 7
13/09: Agrege en el codigo tablero el set para los get and set, y agrege los test del set. 

#commit 8
14/09: Agregue nuevos metodos en Backgammon para mover la ficha e integre las excepciones MovimientoInvalidoException y FichaInvalidaException dentro del juego

#commit 9
14/09: Ahora añadi sus tests para validar tira dados, movimiento valido de fichas y error al mover fichas 

#commit 10 
15/09: Agrege metodo mover_ficha en Tablero con validaciones usando MovimientoInvalidoException. 
Tamb sus tests para cubrir estos nuevos casos.

cambios sprint 3

#commit 1
23/09: Agregue turnos inciales en BackgammonGame. (turno_actual,get_turno y cambiar_turno). Y los tests para verificar que el turno esta en el jugador 1, cambia al jugador 2 y vuelve al jugador 1

#commit 2 
25/09: Agregue gestion de turnos en Backgammon, para controlar que jugador juega y nuevos metodos de turnos, para que solo el jugador en turno pueda mover. Tamb nuevos tests de esto

#commit 3
25/09: Ahora en BackgammonGame valida que el destino este en el rango 0 a 23. Y los test para comprobar que en un destino invalido use MovimientoInvalidoException. 

#commit 4
25/09: Puse un historial de movimientos en BackgammonGame. Y nuevo test para verificar que los movimientos se registren correctamente 

#commit 5
27/09: Agregue verificacion de victoria en BackgammonGame con metodo chequear_victoria y sus nuevos tests

#commit 6
29/09: Hice la validacion de movimientos con dados en BackgammonGame, agregando dados_disponibles y midiendo la distancia. Y sus test correspondientes

#commit 7 
29/09: Agrege un atributo __bar en BackgammonGame para registrar las fichas capturadas y un nuevo metodo get_bar para acceder al bar. Ademas de nuevos tests

#commit 8
29/09: Nuevo metodo reingresar_ficha para permitir el reingreso de fichas capturadas (cumpliendo con las condiciones de por ejemplo q el lugar no este ocupado) y los test de reingreso desde el bar

#commit 9
30/09: Cree un nuevo metodo mostrar_estado() para saber informacion o estado de la partida, y sus test

#commit 10
30/09: Agrege reinicio de partida en BackgammonGame y sus tests correspondientes
