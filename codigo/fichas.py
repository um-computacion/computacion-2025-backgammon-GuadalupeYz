class Ficha:
    def __init__(self, color: str) -> None:
        self._color: str = color  # blanco o negro
    
    def obtener_color(self) -> str:
        return self._color

    