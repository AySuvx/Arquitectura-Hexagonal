"""
Adaptador de Salida - Repositorio JSON.
"""

import json
import os
from typing import List, Optional

from src.application.ports.output.tarea_repository_port import TareaRepositoryPort
from src.domain.tarea import EstadoTarea, Tarea


class JsonTareaRepository(TareaRepositoryPort):
    def __init__(self, ruta_archivo: str):
        self._ruta = ruta_archivo
        self._asegurar_archivo()

    def _asegurar_archivo(self) -> None:
        os.makedirs(os.path.dirname(self._ruta), exist_ok=True)
        if not os.path.exists(self._ruta):
            self._escribir([])

    def _leer(self) -> List[dict]:
        with open(self._ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def _escribir(self, datos: List[dict]) -> None:
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def guardar(self, tarea: Tarea) -> Tarea:
        datos = self._leer()
        indice = next((i for i, t in enumerate(datos) if t["id"] == tarea.id), None)
        if indice is not None:
            datos[indice] = tarea.to_dict()
        else:
            datos.append(tarea.to_dict())
        self._escribir(datos)
        return tarea

    def buscar_por_id(self, tarea_id: str) -> Optional[Tarea]:
        for item in self._leer():
            if item["id"] == tarea_id:
                return Tarea.from_dict(item)
        return None

    def listar_todas(self) -> List[Tarea]:
        return [Tarea.from_dict(item) for item in self._leer()]

    def listar_pendientes(self) -> List[Tarea]:
        return [Tarea.from_dict(item) for item in self._leer()
                if item["estado"] == EstadoTarea.PENDIENTE.value]

    def eliminar(self, tarea_id: str) -> bool:
        datos = self._leer()
        nuevos = [t for t in datos if t["id"] != tarea_id]
        if len(nuevos) == len(datos):
            return False
        self._escribir(nuevos)
        return True
