# Gestor de Tareas Académicas — Arquitectura Hexagonal

Aplicación de consola desarrollada en Python para la gestión de tareas académicas, implementando el patrón **Hexagonal (Ports & Adapters)**, lo que garantiza desacoplamiento, testabilidad y facilidad de extensión.

---

## Descripción

Este sistema permite a estudiantes:

- Crear tareas académicas
- Listar tareas (todas / pendientes / completadas)
- Marcar tareas como completadas
- Eliminar tareas
- Persistir información en almacenamiento local (JSON)

El diseño se centra en separar claramente la lógica de negocio del resto de la aplicación.

---

## Estructura del Proyecto (Optimizada)

```bash
academic_tasks/
│
├── src/
│   ├── domain/
│   │   ├── tarea.py
│   │   └── exceptions.py
│   │
│   ├── application/
│   │   ├── ports/
│   │   │   ├── input/
│   │   │   │   └── tarea_service_port.py
│   │   │   └── output/
│   │   │       └── tarea_repository_port.py
│   │   │
│   │   └── use_cases/
│   │       └── tarea_service.py
│   │
│   └── infrastructure/
│       └── adapters/
│           ├── input/
│           │   └── cli_adapter.py
│           └── output/
│               └── json_tarea_repository.py
│
├── tests/
│   └── test_tareas.py
│
├── data/
│   └── tareas.json
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Ejecución

```bash
git clone https://github.com/tu-usuario/academic_tasks.git
cd academic_tasks
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Tecnologías

- Python 3.10+
- Arquitectura Hexagonal
- JSON
- pytest

---

classDiagram

%% =====================
%% Dominio
%% =====================
class Tarea
class DomainException

%% =====================
%% Aplicación
%% =====================
class TareaService {
}
class TareaServicePort
class TareaRepositoryPort

%% =====================
%% Infraestructura
%% =====================
class CLIAdapter
class JsonTareaRepository

%% =====================
%% Relaciones
%% =====================

TareaService ..|> TareaServicePort
TareaService --> TareaRepositoryPort

CLIAdapter --> TareaServicePort
JsonTareaRepository --> TareaRepositoryPort

Tarea --> DomainException