"""
Puerto de Salida - Contrato para el repositorio de tareas.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.tarea import Tarea


class TareaRepositoryPort(ABC):
    @abstractmethod
    def guardar(self, tarea: Tarea) -> Tarea: ...
    @abstractmethod
    def buscar_por_id(self, tarea_id: str) -> Optional[Tarea]: ...
    @abstractmethod
    def listar_todas(self) -> List[Tarea]: ...
    @abstractmethod
    def listar_pendientes(self) -> List[Tarea]: ...
    @abstractmethod
    def eliminar(self, tarea_id: str) -> bool: ...
