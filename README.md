## NLP - Proyecto: Instrucciones de instalación y uso

Breve guía para instalar dependencias y ejecutar el script `analyze_files.py` en Windows (PowerShell).

### Requisitos
- Python (`3.13.5`)
- Git (opcional)
- Conexión a Internet para descargar paquetes y modelos spaCy

### 1) Abrir PowerShell

Abre PowerShell en la carpeta del proyecto (por ejemplo `d:\User\NLP---Proyecto`).

### 2) Crear y activar un entorno virtual

1. Crear el virtualenv:

```powershell
python -m venv .venv
```

2. Si aparece una restricción de ejecución al activar, ejecuta (solo en la sesión actual):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
```

3. Activar el entorno (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

> Alternativa para CMD: `.venv\Scripts\activate`.

### 3) Actualizar pip e instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

El archivo `requirements.txt` incluido contiene:

- `spacy==3.8.7`
- `rich>=13.7`

### 4) Descargar un modelo spaCy

El script `analyze_files.py` requiere que pases un modelo spaCy instalado. Ejemplos comunes:

```powershell
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm
```

Usa el nombre del modelo descargado como valor para la opción `--model` (por ejemplo `es_core_news_sm`).

### 5) Ejecutar el analizador

Para listar los modelos instalados:

```powershell
python analyze_files.py --list-models
```

Para analizar los textos en la carpeta `samples` usando, por ejemplo, el modelo en español:

```powershell
python analyze_files.py --model es_core_news_sm --folder samples
```

Notas:
- El script busca archivos con extensiones `.txt` y `.c` dentro de la carpeta indicada.
- Por defecto `--folder` está en `samples`.

### 6) Ejemplo rápido (paso a paso)

```powershell
# Desde la raíz del proyecto
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download es_core_news_sm
python analyze_files.py --model es_core_news_sm
```

### 7) Solución de problemas
- Si el script indica que el modelo no está instalado, ejecuta `python -m spacy download <modelo>` con el mismo intérprete de Python/entorno virtual activado.
