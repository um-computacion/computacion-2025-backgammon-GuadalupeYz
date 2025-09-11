
class BackgammonException(Exception):
    #excepcion base para el juego
    pass


class MovimientoInvalidoException(BackgammonException):      
    #se lanza cuando un movimiento que no es valido en el tablero
    pass


class FichaInvalidaException(BackgammonException):
    #se lanza cuando se intenta usar una ficha que no corresponde al jugador
    pass
