class Ficha:
    def __init__(self, color: str) -> None:
        self.__color: str = color  # blanco o negro

    def get_color(self) -> str:
        return self.__color

    def set_color(self, nuevo_color: str) -> None:
        self.__color = nuevo_color
