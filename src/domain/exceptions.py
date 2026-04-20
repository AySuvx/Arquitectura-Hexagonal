"""
Dominio - Excepciones personalizadas del dominio.
"""


class TareaNoEncontradaError(Exception):
    def __init__(self, tarea_id: str):
        super().__init__(f"No se encontró ninguna tarea con id '{tarea_id}'.")


class TareaDuplicadaError(Exception):
    def __init__(self, titulo: str):
        super().__init__(f"Ya existe una tarea con el título '{titulo}'.")


class TituloVacioError(ValueError):
    def __init__(self):
        super().__init__("El título de la tarea no puede estar vacío.")
