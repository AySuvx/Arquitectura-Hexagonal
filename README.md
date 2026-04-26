# Gestor de Tareas Academicas — Arquitectura Hexagonal

## Descripcion del problema

Los estudiantes universitarios enfrentan el reto constante de organizar multiples actividades academicas de forma simultanea: entregas, parciales, lecturas, laboratorios y proyectos. Sin un sistema estructurado, es facil perder el seguimiento de que tareas estan pendientes, cuales ya fueron completadas y cuales dejaron de ser relevantes.

Esta aplicacion resuelve ese problema proporcionando una herramienta de consola simple y funcional que permite registrar actividades academicas, consultarlas por estado, marcarlas como completadas y archivarlas cuando ya no son necesarias. El estado de cada tarea se guarda automaticamente en un archivo JSON local, de modo que la informacion persiste entre sesiones.

El proposito tecnico del proyecto va mas alla de la funcionalidad: el verdadero objetivo es demostrar la aplicacion correcta de la arquitectura hexagonal (Ports and Adapters) en un sistema real, separando de forma clara el nucleo del negocio de los mecanismos de entrada y salida.

---

## Estructura del proyecto

```
academic_tasks/
|
|-- src/
|   |
|   |-- domain/                              # Nucleo del negocio (independiente de frameworks)
|   |   |-- __init__.py
|   |   |-- tarea.py                         # Entidad principal: Tarea, EstadoTarea
|   |   +-- exceptions.py                    # Excepciones del dominio
|   |
|   |-- application/                         # Casos de uso y contratos (puertos)
|   |   |-- __init__.py
|   |   |-- ports/
|   |   |   |-- __init__.py
|   |   |   |-- input/
|   |   |   |   |-- __init__.py
|   |   |   |   +-- tarea_service_port.py    # Puerto de entrada (interfaz ABC)
|   |   |   +-- output/
|   |   |       |-- __init__.py
|   |   |       +-- tarea_repository_port.py # Puerto de salida (interfaz ABC)
|   |   +-- use_cases/
|   |       |-- __init__.py
|   |       +-- tarea_service.py             # Implementacion de los 5 casos de uso
|   |
|   +-- infrastructure/                      # Adaptadores de entrada y salida
|       |-- __init__.py
|       +-- adapters/
|           |-- __init__.py
|           |-- input/
|           |   |-- __init__.py
|           |   +-- cli_adapter.py           # Adaptador de entrada: interfaz de consola
|           +-- output/
|               |-- __init__.py
|               +-- json_tarea_repository.py # Adaptador de salida: persistencia en JSON
|
|-- tests/
|   |-- __init__.py
|   +-- test_tareas.py                       # 15 pruebas unitarias (pytest)
|
|-- data/
|   +-- tareas.json                          # Archivo generado automaticamente en ejecucion
|
|-- main.py                                  # Punto de entrada e inyeccion de dependencias
|-- requirements.txt                         # Dependencias del proyecto
+-- README.md
```

### Descripcion de cada capa

**domain/**
Contiene la logica de negocio pura. La entidad `Tarea` define los atributos (id, titulo, descripcion, estado, fechas) y encapsula las reglas de negocio en sus metodos: `completar()` y `archivar()`. El enum `EstadoTarea` define los tres estados posibles: PENDIENTE, COMPLETADA y ARCHIVADA. Esta capa no importa ningun framework ni libreria externa.

**application/ports/**
Define los contratos mediante clases abstractas (ABC). El puerto de entrada `TareaServicePort` declara las operaciones que el exterior puede solicitar. El puerto de salida `TareaRepositoryPort` declara las operaciones de persistencia que la aplicacion necesita. Ninguna capa interna conoce las implementaciones concretas.

**application/use_cases/**
`TareaService` implementa el puerto de entrada y recibe el repositorio mediante inyeccion de dependencias. Aqui viven los cinco casos de uso: crear tarea, listar tareas, completar tarea, consultar pendientes y archivar tarea.

**infrastructure/adapters/input/**
`CLIAdapter` es el adaptador de entrada. Traduce las interacciones del usuario (seleccion de menu, ingreso de datos) en llamadas al puerto de entrada. No contiene logica de negocio.

**infrastructure/adapters/output/**
`JsonTareaRepository` es el adaptador de salida. Implementa el puerto de salida usando un archivo JSON como mecanismo de persistencia. Serializa y deserializa entidades `Tarea` usando los metodos `to_dict()` y `from_dict()`.

**main.py**
Es el unico punto del sistema donde todas las capas se conocen entre si. Instancia el repositorio JSON, lo inyecta en el servicio, e inyecta el servicio en el adaptador CLI. Tambien agrega el directorio raiz del proyecto al `sys.path` para que los imports funcionen correctamente en cualquier sistema operativo.

---

## Pasos para ejecutar

### Requisitos previos

- Python 3.10 o superior instalado
- pip disponible en el sistema

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/tu-usuario/academic_tasks.git
cd academic_tasks
```

### 2. Crear y activar un entorno virtual (recomendado)

En Linux o macOS:
```bash
python -m venv venv
source venv/bin/activate
```

En Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene unicamente `pytest`, que se usa para las pruebas. La aplicacion principal no tiene dependencias externas.

### 4. Ejecutar la aplicacion

Desde la carpeta raiz del proyecto (`academic_tasks/`):

```bash
python main.py
```

Se desplegara el menu principal en consola. El archivo `data/tareas.json` se crea automaticamente en el primer uso.

### 5. Ejecutar las pruebas unitarias

```bash
python -m pytest tests/ -v
```

Resultado esperado: 15 pruebas pasando, 0 errores.

### Uso basico del menu

```
1. Registrar nueva tarea       -> Ingresa titulo y descripcion opcional
2. Listar todas las tareas     -> Muestra tareas agrupadas por estado
3. Marcar tarea como completada-> Muestra tareas pendientes, pide el ID
4. Consultar tareas pendientes -> Muestra unicamente las tareas en estado PENDIENTE
5. Archivar/Eliminar tarea     -> Muestra tareas activas, pide el ID a archivar
6. Salir
```

Nota: las opciones 3 y 5 muestran primero las tareas disponibles con sus IDs para facilitar la seleccion.

---

## Tecnologias usadas

| Componente         | Tecnologia              | Version minima |
|--------------------|-------------------------|----------------|
| Lenguaje           | Python                  | 3.10           |
| Persistencia       | JSON (modulo estandar)  | incluido       |
| Pruebas unitarias  | pytest                  | 7.0            |
| Identificadores    | uuid (modulo estandar)  | incluido       |
| Entidades          | dataclasses (estandar)  | incluido       |
| Contratos          | abc (estandar)          | incluido       |

No se usan frameworks web, ORMs ni bases de datos externas. Todas las dependencias de la aplicacion principal forman parte de la biblioteca estandar de Python. El unico paquete externo es `pytest`, usado exclusivamente para las pruebas.

---

## Explicacion de puertos y adaptadores

La arquitectura hexagonal organiza el sistema en tres zonas concentrinas: el dominio en el centro, los casos de uso alrededor, y los adaptadores en el exterior. La comunicacion entre zonas se realiza exclusivamente a traves de puertos, que son interfaces abstractas.

### Puertos de entrada

Un puerto de entrada define las operaciones que el mundo exterior puede solicitar a la aplicacion. En este proyecto, la interfaz `TareaServicePort` (ubicada en `application/ports/input/`) declara cinco metodos: `crear_tarea`, `listar_tareas`, `completar_tarea`, `consultar_pendientes` y `eliminar_tarea`.

Cualquier mecanismo de interaccion con el usuario (consola, API REST, interfaz grafica) debe comunicarse con la aplicacion unicamente a traves de esta interfaz. El adaptador de entrada `CLIAdapter` la implementa para el caso de la consola. Si en el futuro se quisiera agregar una API REST, bastaria con crear un nuevo adaptador que implemente la misma interfaz, sin modificar ninguna linea del dominio ni de los casos de uso.

### Puertos de salida

Un puerto de salida define lo que la aplicacion necesita del exterior, en este caso, operaciones de persistencia. La interfaz `TareaRepositoryPort` (ubicada en `application/ports/output/`) declara: `guardar`, `buscar_por_id`, `listar_todas`, `listar_pendientes` y `eliminar`.

Los casos de uso (en `TareaService`) llaman a estos metodos sin saber como estan implementados. El adaptador de salida `JsonTareaRepository` implementa este contrato usando un archivo JSON. Si se quisiera cambiar a SQLite o PostgreSQL, bastaria con crear un nuevo adaptador que implemente `TareaRepositoryPort`. El dominio y los casos de uso no cambiarian en absoluto.

### Inyeccion de dependencias

La conexion entre puertos y adaptadores ocurre en `main.py`, que es el unico lugar del sistema donde todas las capas se conocen. Este patron se llama inyeccion de dependencias:

```
JsonTareaRepository  -->  inyectado en  -->  TareaService  -->  inyectado en  -->  CLIAdapter
(adaptador salida)                      (casos de uso)                         (adaptador entrada)
```

Esto garantiza que el dominio y los casos de uso no dependen de ninguna implementacion concreta, lo que los hace completamente testeables de forma aislada usando un repositorio en memoria, como se demuestra en `tests/test_tareas.py`.
