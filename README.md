# Generador de Historias de Usuario con LLM

Este proyecto permite generar historias de usuario enriquecidas siguiendo metodologías ágiles, utilizando modelos de lenguaje (LLM) a través de Ollama. El resultado puede obtenerse en diferentes formatos y guardarse automáticamente.

## Características

- Generación automática de historias de usuario en formato JSON, Markdown o texto.
- Integración con modelos LLM locales vía Ollama.
- Opcionalmente guarda los resultados en archivos.
- Interfaz de línea de comandos interactiva y fácil de usar.

## Requisitos

- [Docker](https://www.docker.com/) (para ejecutar Ollama)
- [Python 3.8+](https://www.python.org/)
- Acceso a un modelo compatible con Ollama (por ejemplo, `llama3.2`)

## Instalación

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/aleluis79/historias.git
   cd stories
   ```

2. **Crear y activar un entorno virtual de Python**  
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

## Configuración de Ollama

1. **Ejecutar Ollama con Docker**  
   ```bash
   docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama-app ollama/ollama
   ```

2. **Descargar el modelo `llama3.1`**  
   ```bash
   docker exec -it ollama-app ollama pull llama3.1
   ```

## Uso

Ejecuta la aplicación desde la terminal:

```bash
python historias.py
```

Sigue las instrucciones interactivas para ingresar el rol, la funcionalidad y el beneficio.

### Opciones principales

- `--output [console|markdown|json]`  
  Formato de salida (por defecto: markdown).
- `--save`  
  Guarda el resultado en un archivo.
- `--outdir <directorio>`  
  Directorio donde se guardarán los archivos (por defecto: `historias`).
- `--ollama-url <url>`  
  URL de la API de Ollama (por defecto: `http://localhost:11434/api/generate`).
- `--model <modelo>`  
  Modelo de Ollama a utilizar (por defecto: `llama3.2`).

### Ejemplo de uso

```bash
python historias.py --output markdown --save
```

### Ayuda

Para ver todas las opciones disponibles:

```bash
python historias.py --help
```

## Desactivar el entorno virtual

```bash
deactivate
```

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

---