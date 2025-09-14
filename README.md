# Generador de historias de usuario

## Pasos para poder ejecutar

### Correr Ollama local con Docker
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama-app ollama/ollama

### Descargar el modelo llama3.2
docker exec -it ollama-app ollama pull llama3.2

### Crear entorno de Python
python -m venv stories

### Activar entorno de Python
source stories/bin/activate

### Instalar dependencias
pip install -r requirements.txt

### Correr aplicación
python historias.py

### Ayuda de la aplicación
python historias.py --help

### Para desactivar el entorno de Python
deactivate