# Golden Berry

GoldenBerry es una plataforma avanzada diseñada para implementar sistemas multiagente y sistemas expertos. Facilita la creación, gestión y coordinación de agentes autónomos que pueden colaborar o competir en entornos complejos. Integra inteligencia artificial y permite la toma de decisiones basada en conceptos bioinspirados.

GoldenBerry es una innovadora herramienta open-source diseñada para transformar la manera en que las empresas y organizaciones gestionan y desarrollan soluciones basadas en inteligencia artificial. En el corazón de su funcionalidad se encuentra la capacidad de disponibilizar agentes cognitivos avanzados que utilizan una variedad de técnicas de vanguardia, incluyendo Recuperación y Generación (RAG, por sus siglas en inglés). Estos agentes son capaces de operar de manera autónoma o colaborativa, interactuando con otros sistemas y usuarios para resolver problemas complejos, realizar tareas específicas y mejorar la eficiencia operativa.

Una de las características más destacadas de GoldenBerry es su flexibilidad y adaptabilidad a diversos escenarios. Gracias a su arquitectura modular y su enfoque basado en microservicios, la plataforma permite a los desarrolladores y equipos de ingeniería implementar soluciones personalizadas que se ajusten a las necesidades particulares de su organización. Esto facilita la integración de los agentes cognitivos en diferentes entornos, desde aplicaciones empresariales hasta sistemas de control industrial, ofreciendo un amplio espectro de posibilidades.

Además de RAG, GoldenBerry soporta otras técnicas avanzadas de inteligencia artificial, como aprendizaje profundo, redes neuronales, sistemas expertos, y algoritmos bioinspirados, lo que la convierte en una solución integral para la toma de decisiones inteligentes. Estas capacidades permiten a los agentes cognitivos procesar grandes volúmenes de datos, aprender de experiencias previas, y adaptarse a nuevos contextos y desafíos en tiempo real.

En resumen, GoldenBerry es más que una herramienta; es un ecosistema completo para la creación, gestión y despliegue de agentes cognitivos que potencian la innovación y optimizan los procesos de negocio. Con su enfoque en la accesibilidad open-source, GoldenBerry está posicionada para democratizar el acceso a la inteligencia artificial avanzada, brindando a las empresas de todos los tamaños la capacidad de aprovechar el poder transformador de la tecnología cognitiva.

### Estructura

La estructura del proyecto contiene un `.gitignore` para archivos a ignorar, una `LICENSE` para la licencia, y un `README.md` como guía del proyecto. En el directorio `src`, se encuentran ejemplos (`examples/inf.md`) y el módulo principal `uchuva`, que incluye un submódulo `rag` con varios componentes: `commons` para elementos comunes como configuraciones administrativas, controladores de solicitudes, y lógica de trabajadores, además de archivos específicos como `models.py`, `serializers.py`, y pruebas (`tests.py`). También contiene `documents` con configuraciones de Docker (`Dockerfile`, `DockerfileBase`) y Kubernetes (`deployment.yaml`, `service.yaml`), junto a scripts y gestión de modelos en `src`. Por último, el directorio `teams` incluye un archivo informativo (`inf.md`). Esta estructura bien organizada facilita la gestión y el desarrollo del proyecto, cubriendo desde la configuración y administración hasta la ejecución de código y despliegue.

```
├── .gitignore               # Lista de archivos y directorios que Git debe ignorar.
├── LICENSE                  # Archivo que especifica la licencia del proyecto.
├── README.md                # Documento de introducción y guía del proyecto.
└── src                      # Directorio principal del código fuente.
    ├── examples
    │   └── inf.md           # Ejemplo o documentación informativa sobre el proyecto.
    └── uchuva               # Directorio del módulo o componente "uchuva".
        ├── rag              # Subdirectorio relacionado con la implementación de RAG.
        │   ├── commons      # Contiene componentes comunes reutilizables.
        │   │   ├── admin.py             # Configuraciones administrativas.
        │   │   ├── apps.py              # Configuración de aplicaciones.
        │   │   ├── chunkdocument.py     # Manejo de documentos segmentados.
        │   │   ├── dmas                 # Controladores y trabajadores de solicitudes.
        │   │   │   ├── requestcontroller
        │   │   │   │   ├── loadaction.py         # Acciones de carga en el controlador.
        │   │   │   │   └── requestcontroller.py  # Controlador principal de solicitudes.
        │   │   │   └── requestworker
        │   │   │       ├── requesttask.py        # Tareas específicas del trabajador.
        │   │   │       ├── requestworker.py      # Lógica del trabajador de solicitudes.
        │   │   │       └── updateaction.py       # Acciones de actualización en el trabajador.
        │   │   ├── engine.py           # Motor principal del módulo.
        │   │   ├── __init__.py         # Inicializador del paquete.
        │   │   ├── mas                 # Submódulo de agentes múltiples.
        │   │   │   ├── requestcontroller
        │   │   │   │   └── requestcontroller.py  # Controlador de solicitudes para agentes múltiples.
        │   │   │   └── requestworker
        │   │   │       ├── requesttask.py        # Tareas del trabajador en agentes múltiples.
        │   │   │       └── requestworker.py      # Lógica del trabajador en agentes múltiples.
        │   │   ├── models.py           # Definición de modelos de datos.
        │   │   ├── runtime             # Código relacionado con la ejecución en tiempo real.
        │   │   │   ├── ai_engine.py            # Motor de inteligencia artificial.
        │   │   │   ├── exp.py                  # Código experimental.
        │   │   │   ├── program3.py             # Programa específico número 3.
        │   │   │   └── program4.py             # Programa específico número 4.
        │   │   ├── serializers.py     # Serializadores de datos.
        │   │   ├── tests.py           # Pruebas unitarias y de integración.
        │   │   ├── urls.py            # Definición de rutas y URLs.
        │   │   └── views.py           # Controladores de vistas.
        │   └── documents              # Documentos y archivos de configuración.
        │       ├── Dockerfile         # Definición de la imagen Docker para despliegue.
        │       ├── DockerfileBase     # Base para la construcción de imágenes Docker.
        │       ├── k8s                # Configuraciones para Kubernetes.
        │       │   ├── deployment.yaml         # Despliegue de aplicaciones en Kubernetes.
        │       │   └── service.yaml            # Configuración de servicios en Kubernetes.
        │       ├── model              # Archivos de modelos de datos.
        │       │   └── book_normalized.json    # Modelo de datos normalizado en formato JSON.
        │       └── src                # Código fuente del módulo "documents".
        │           ├── app.py                 # Aplicación principal.
        │           ├── cmdsim.py              # Simulador de línea de comandos.
        │           ├── download_nltk.py       # Script para descargar recursos de NLTK.
        │           ├── model_manager.py       # Gestión de modelos.
        │           ├── requirements.txt       # Dependencias del proyecto.
        │           ├── run.sh                 # Script para ejecutar la aplicación.
        │           ├── security_manager.py    # Gestión de seguridad.
        │           └── util.py                # Funciones utilitarias.
        └── teams
            └── inf.md           # Documento informativo relacionado con "teams".

```
