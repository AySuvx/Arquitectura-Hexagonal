"""
Puerto de Entrada - Contrato que expone los casos de uso disponibles.
Los adaptadores de entrada (CLI, HTTP, etc.) interactúan SOLO con esta interfaz.
"""

from abc import ABC, abstractmethod
from typing import List

from src.domain.tarea import Tarea


class TareaServicePort(ABC):
    @abstractmethod
    def crear_tarea(self, titulo: str, descripcion: str = "") -> Tarea: ...
    @abstractmethod
    def listar_tareas(self) -> List[Tarea]: ...
    @abstractmethod
    def completar_tarea(self, tarea_id: str) -> Tarea: ...
    @abstractmethod
    def consultar_pendientes(self) -> List[Tarea]: ...
    @abstractmethod
    def eliminar_tarea(self, tarea_id: str) -> bool: ...
