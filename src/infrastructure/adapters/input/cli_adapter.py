"""
Adaptador de Entrada - CLI.
"""

from typing import List

from src.application.ports.input.tarea_service_port import TareaServicePort
from src.domain.tarea import EstadoTarea, Tarea

SEPARADOR = "─" * 52


class CLIAdapter:
    def __init__(self, servicio: TareaServicePort):
        self._servicio = servicio

    def _header(self, texto: str) -> None:
        print(f"\n{SEPARADOR}\n  {texto}\n{SEPARADOR}")

    def _imprimir_tarea(self, t: Tarea) -> None:
        desc = f" — {t.descripcion}" if t.descripcion else ""
        print(f"  {t}{desc}")
        print(f"      Creada : {t.fecha_creacion}")
        if t.fecha_completado:
            print(f"      Completada: {t.fecha_completado}")

    def _mostrar_tareas_agrupadas(self, tareas: List[Tarea]) -> None:
        """
        Requisito: el listado debe distinguir tareas pendientes y completadas.
        Se muestran agrupadas por estado en secciones separadas.
        """
        pendientes  = [t for t in tareas if t.estado == EstadoTarea.PENDIENTE]
        completadas = [t for t in tareas if t.estado == EstadoTarea.COMPLETADA]
        archivadas  = [t for t in tareas if t.estado == EstadoTarea.ARCHIVADA]

        print(f"\n  ⏳ PENDIENTES ({len(pendientes)})")
        print(f"  {'·'*48}")
        if pendientes:
            for t in pendientes:
                self._imprimir_tarea(t)
        else:
            print("  (ninguna)")

        print(f"\n  COMPLETADAS ({len(completadas)})")
        print(f"  {'·'*48}")
        if completadas:
            for t in completadas:
                self._imprimir_tarea(t)
        else:
            print("  (ninguna)")

        print(f"\n  ARCHIVADAS ({len(archivadas)})")
        print(f"  {'·'*48}")
        if archivadas:
            for t in archivadas:
                self._imprimir_tarea(t)
        else:
            print("  (ninguna)")
        print()

    def _mostrar_tareas(self, tareas: List[Tarea], titulo: str) -> None:
        self._header(titulo)
        if not tareas:
            print("  (Sin resultados)\n")
            return
        for t in tareas:
            self._imprimir_tarea(t)
        print()

    def _menu(self) -> None:
        print(f"\n{'═'*52}")
        print("  GESTOR DE TAREAS ACADÉMICAS")
        print(f"{'═'*52}")
        print("  1. Registrar nueva tarea")
        print("  2. Listar todas las tareas")
        print("  3. Marcar tarea como completada")
        print("  4. Consultar tareas pendientes")
        print("  5. Archivar/Eliminar tarea")
        print("  6. Salir")
        print(f"{'═'*52}")

    # ── Acciones ─────────────────────────────────────────────────────────────

    def _accion_crear(self) -> None:
        titulo = input("\n  Título de la tarea: ").strip()
        if not titulo:
            print("\n  Error: El título no puede estar vacío.")
            return
        descripcion = input("  Descripción (opcional): ").strip()
        try:
            tarea = self._servicio.crear_tarea(titulo, descripcion)
            print(f"\n  Tarea registrada  ID:[{tarea.id}]  '{tarea.titulo}'")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _accion_listar(self) -> None:
        """Lista todas las tareas distinguiendo pendientes y completadas."""
        self._header("TODAS LAS TAREAS")
        tareas = self._servicio.listar_tareas()
        if not tareas:
            print("  (No hay tareas registradas)\n")
            return
        self._mostrar_tareas_agrupadas(tareas)

    def _accion_completar(self) -> None:
        self._header("MARCAR TAREA COMO COMPLETADA")
        tareas = self._servicio.consultar_pendientes()
        if not tareas:
            print("  (No hay tareas pendientes)\n")
            return
        print("  Tareas pendientes:")
        for t in tareas:
            print(f"    [{t.id}] {t.titulo}")
        tarea_id = input("\n  ID de la tarea a completar: ").strip()
        try:
            tarea = self._servicio.completar_tarea(tarea_id)
            print(f"\n  Tarea [{tarea.id}] '{tarea.titulo}' marcada como completada.")
        except Exception as e:
            print(f"\n  Error: {e}")

    def _accion_pendientes(self) -> None:
        tareas = self._servicio.consultar_pendientes()
        self._mostrar_tareas(tareas, f"TAREAS PENDIENTES — {len(tareas)} encontrada(s)")

    def _accion_eliminar(self) -> None:
        self._header("ARCHIVAR / ELIMINAR TAREA")
        tareas = self._servicio.listar_tareas()
        activas = [t for t in tareas if t.estado != EstadoTarea.ARCHIVADA]
        if not activas:
            print("  (No hay tareas para archivar)\n")
            return
        print("  Tareas disponibles:")
        for t in activas:
            print(f"    [{t.id}] {t.titulo}  ({t.estado.value})")
        tarea_id = input("\n  ID de la tarea a archivar: ").strip()
        try:
            self._servicio.eliminar_tarea(tarea_id)
            print(f"\n  Tarea [{tarea_id}] archivada correctamente.")
        except Exception as e:
            print(f"\n  Error: {e}")

    # ── Bucle principal ───────────────────────────────────────────────────────

    def ejecutar(self) -> None:
        acciones = {
            "1": self._accion_crear,
            "2": self._accion_listar,
            "3": self._accion_completar,
            "4": self._accion_pendientes,
            "5": self._accion_eliminar,
        }
        while True:
            self._menu()
            opcion = input("  Selecciona una opción: ").strip()
            if opcion == "6":
                print("\n ¡Hasta pronto!\n")
                break
            accion = acciones.get(opcion)
            if accion:
                accion()
            else:
                print("\n  Opción no válida. Elige entre 1 y 6.")
