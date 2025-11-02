"""Módulo con las excepciones personalizadas del juego Backgammon."""


class BackgammonException(Exception):
    """Excepción base para el juego."""
    # excepción base para el juego


class MovimientoInvalidoException(BackgammonException):
    """Se lanza cuando se intenta hacer un movimiento no válido."""
    # se lanza cuando un movimiento no es válido en el tablero


class FichaInvalidaException(BackgammonException):
    """Se lanza cuando se intenta usar una ficha que no pertenece al jugador."""
    # se lanza cuando se intenta usar una ficha que no corresponde al jugador
