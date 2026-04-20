"""
Casos de Uso - Orquesta la lógica de aplicación.
"""

from typing import List

from src.application.ports.input.tarea_service_port import TareaServicePort
from src.application.ports.output.tarea_repository_port import TareaRepositoryPort
from src.domain.exceptions import TareaNoEncontradaError
from src.domain.tarea import Tarea


class TareaService(TareaServicePort):
    def __init__(self, repositorio: TareaRepositoryPort):
        self._repositorio = repositorio

    def crear_tarea(self, titulo: str, descripcion: str = "") -> Tarea:
        tarea = Tarea(titulo=titulo, descripcion=descripcion)
        return self._repositorio.guardar(tarea)

    def listar_tareas(self) -> List[Tarea]:
        return self._repositorio.listar_todas()

    def completar_tarea(self, tarea_id: str) -> Tarea:
        tarea = self._repositorio.buscar_por_id(tarea_id)
        if tarea is None:
            raise TareaNoEncontradaError(tarea_id)
        tarea.completar()
        return self._repositorio.guardar(tarea)

    def consultar_pendientes(self) -> List[Tarea]:
        return self._repositorio.listar_pendientes()

    def eliminar_tarea(self, tarea_id: str) -> bool:
        tarea = self._repositorio.buscar_por_id(tarea_id)
        if tarea is None:
            raise TareaNoEncontradaError(tarea_id)
        tarea.archivar()
        self._repositorio.guardar(tarea)
        return True
