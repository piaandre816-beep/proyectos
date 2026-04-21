# Análisis de Uso de Herramientas de IA en Educación

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)

Proyecto completo que despliega un dashboard analítico para explorar el impacto y el uso de herramientas de Inteligencia Artificial en el sector educativo. Utiliza un conjunto de datos obtenidos directamente de Kaggle mediante el paquete `kagglehub`.

## Estructura del Proyecto

```text
PROYECTOS/
├── README.md               # Este archivo
├── requirements.txt        # Dependencias de Python necesarias
├── index.html              # Landing Page para GitHub Pages (Despliegue estático)
├── app.py                  # Aplicación de Streamlit con gráficos y tarjetas dinámicas
└── analysis.ipynb          # Cuaderno de análisis de datos e ingesta principal
```

## Instalación y Ejecución Local

1. Abre tu terminal en el directorio `PROYECTOS`.
2. Instala las dependencias: 
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el dashboard:
   ```bash
   streamlit run app.py
   ```
La aplicación se abrirá automáticamente en tu navegador por defecto mostrando los análisis en tiempo real.

## Landing Page
Abre el archivo `index.html` en tu navegador para ver la página de inicio, o súbelo a un repositorio de GitHub y activa **GitHub Pages** para compartir públicamente la presentación del proyecto.
