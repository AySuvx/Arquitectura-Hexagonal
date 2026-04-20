"""
Punto de entrada de la aplicación.
Aquí se realiza la inyección de dependencias: se conectan
los adaptadores con los puertos para ensamblar la aplicación.
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.application.use_cases.tarea_service import TareaService
from src.infrastructure.adapters.input.cli_adapter import CLIAdapter
from src.infrastructure.adapters.output.json_tarea_repository import JsonTareaRepository


def main():
    # Ruta del JSON relativa al directorio del proyecto (no al CWD)
    data_path = os.path.join(PROJECT_ROOT, "data", "tareas.json")

    # 1. Crear el adaptador de salida (repositorio JSON)
    repositorio = JsonTareaRepository(ruta_archivo=data_path)

    # 2. Inyectar el repositorio en el servicio (casos de uso)
    servicio = TareaService(repositorio=repositorio)

    # 3. Inyectar el servicio en el adaptador de entrada (CLI)
    cli = CLIAdapter(servicio=servicio)

    # 4. Ejecutar la aplicación
    cli.ejecutar()


if __name__ == "__main__":
    main()
