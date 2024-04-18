# Guía del Proyecto Integrador # 1 
# Modelo de Recomendacion SteamGameRecommender

## Introducción

Este proyecto se centró en la creación de una api RestFull para un  sistema de recomendación de videojuegos personalizado para la plataforma Steam. El objetivo era ofrecer una herramienta que facilitara a los usuarios el descubrimiento de nuevos juegos que se ajustaran a sus preferencias e intereses Ademas de conocer otras metricas.

 Esta guía está diseñada para ayudarte a comprender la estructura y la organización del proyecto, así como para facilitar tu navegación por los diferentes componentes y recursos disponibles.

## Estructura del Proyecto

El proyecto se organiza en varias carpetas principales, cada una con un propósito específico. A continuación, se describe la estructura básica del proyecto:

### Carpeta ETL

La carpeta `ETL` contiene los Notebooks de Jupyter utilizados para el proceso de Extracción, Transformación y Carga (ETL) de datos. Cada Notebook en esta carpeta está dedicado al procesamiento de un DataFrame particular. El resultado del proceso ETL se guarda en la carpeta `Data_Extracted`.

### Carpeta EDA

La carpeta `EDA` (Análisis Exploratorio de Datos) se utiliza para explorar y analizar los datos previamente procesados por el proceso ETL. Aquí encontrarás Notebooks dedicados a problemas específicos, cada uno utilizando uno o más DataFrames generados por el proceso ETL según sea necesario.

### Carpeta API

La carpeta `API` contiene los archivos relacionados con la API de la aplicación. Incluye los scripts de Python que definen los endpoints de la API, así como cualquier otro archivo necesario para su funcionamiento.

## Uso del Proyecto

Recomiendo que siga en este orden.

1. **Explora la Carpeta ETL:** Comienza revisando los Notebooks en la carpeta `ETL`. Cada uno de estos Notebooks describe el proceso de ETL para un DataFrame específico. Sigue las instrucciones detalladas en cada Notebook para entender cómo se cargan, transforman y extraen los datos.

2. **Analiza los Datos en la Carpeta EDA:** Una vez que los datos han sido procesados por el ETL, puedes explorar y analizar su contenido en la carpeta `EDA`. Aquí encontrarás Notebooks dedicados a problemas específicos, cada uno utilizando los DataFrames generados por el proceso ETL como entrada.

3. **Utiliza los Endpoints de la API:** Además de los análisis realizados en los Notebooks de la carpeta EDA, este proyecto también incluye una API. Cada endpoint de la API tiene su propio script en la carpeta `API`, donde se define su funcionamiento y se muestra cómo utilizarlo.

## Recursos Adicionales

- [Enlace al Repositorio del Proyecto](https://github.com/Antojose93/SteamGameRecommender.git): Encuentra el código fuente, los Notebooks y otros recursos relacionados con este proyecto en nuestro repositorio público.
- [Documentación de la API](https://steam-game-recommender.onrender.com/): Consulta la documentación detallada de la API para obtener más información sobre cómo utilizar sus endpoints.


