"""
Dominio - Entidad Tarea
Contiene la lógica de negocio pura, sin dependencias externas.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class EstadoTarea(Enum):
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
    ARCHIVADA = "archivada"


@dataclass
class Tarea:
    """
    Entidad principal del dominio.
    Encapsula las reglas de negocio relacionadas con una tarea académica.
    """
    titulo: str
    descripcion: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    estado: EstadoTarea = field(default=EstadoTarea.PENDIENTE)
    fecha_creacion: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    fecha_completado: Optional[str] = None

    def __post_init__(self):
        # Regla de negocio: el título no puede estar vacío
        if not self.titulo or not self.titulo.strip():
            raise ValueError("El título de la tarea no puede estar vacío.")
        self.titulo = self.titulo.strip()

    def completar(self) -> None:
        """Regla de negocio: solo se puede completar una tarea pendiente."""
        if self.estado == EstadoTarea.COMPLETADA:
            raise ValueError(f"La tarea '{self.titulo}' ya está completada.")
        if self.estado == EstadoTarea.ARCHIVADA:
            raise ValueError(f"La tarea '{self.titulo}' está archivada y no puede completarse.")
        self.estado = EstadoTarea.COMPLETADA
        self.fecha_completado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def archivar(self) -> None:
        """Regla de negocio: se puede archivar cualquier tarea no archivada."""
        if self.estado == EstadoTarea.ARCHIVADA:
            raise ValueError(f"La tarea '{self.titulo}' ya está archivada.")
        self.estado = EstadoTarea.ARCHIVADA

    def esta_pendiente(self) -> bool:
        return self.estado == EstadoTarea.PENDIENTE

    def esta_completada(self) -> bool:
        return self.estado == EstadoTarea.COMPLETADA

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado.value,
            "fecha_creacion": self.fecha_creacion,
            "fecha_completado": self.fecha_completado,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tarea":
        tarea = cls(
            titulo=data["titulo"],
            descripcion=data.get("descripcion", ""),
            id=data["id"],
            estado=EstadoTarea(data["estado"]),
            fecha_creacion=data["fecha_creacion"],
        )
        tarea.fecha_completado = data.get("fecha_completado")
        return tarea

    def __repr__(self) -> str:
        estado_icon = {"pendiente": "⏳", "completada": "✅", "archivada": "📦"}
        icon = estado_icon.get(self.estado.value, "?")
        return f"[{self.id}] {icon} {self.titulo} ({self.estado.value})"
