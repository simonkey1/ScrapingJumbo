

# Scraping Jumbo

Este proyecto tiene como objetivo extraer datos nutricionales de productos desde un sitio web de Jumbo, limpiarlos y cargarlos en un repositorio para su posterior análisis. El flujo de trabajo se describe a continuación, desde la extracción de datos hasta la carga final en el repositorio.

## Flujo del Proyecto

### 1. **Extracción de Datos:**
La extracción de los datos se realiza a través de un proceso de **web scraping**, que obtiene información de productos de Jumbo, como:
- Nombre del producto
- Código del producto
- Marca
- Ingredientes
- Precio
- Información nutricional (azúcares, grasas, colesterol, etc.)

Los datos son extraídos en formato JSON, los cuales contienen información estructurada sobre los productos.

### 2. **Limpieza de Datos:**
Una vez obtenidos los datos, se procede a limpiarlos y transformarlos para su análisis. La limpieza incluye los siguientes pasos:
- **Normalización**: El JSON de cada producto se normaliza en un DataFrame de Pandas para facilitar su manejo.
- **Pivotado**: Se organiza la información en formato ancho para que cada nutriente sea una columna, tanto para el valor por 100g como para el valor por porción.
- **Renombrado de columnas**: Se realizan cambios en los nombres de las columnas para que sean más comprensibles y consistentes, además de aplicar abreviaciones para facilitar su uso en análisis futuros.
- **Extracción de tamaño**: El tamaño del producto (en gramos, litros, etc.) es extraído de la columna de nombre del producto y se separa en dos columnas: `valor` y `unidad`.
- **Ajustes adicionales**: Se corrigen valores específicos como los precios (eliminando caracteres innecesarios) y se rellenan los valores nulos con 0 para asegurar que no haya errores en el análisis posterior.

### 3. **Carga de Datos en GitHub:**
Los datos limpios se cargan en un repositorio de GitHub para mantener un registro versionado de los mismos. El proceso de carga sigue los pasos estándar de Git:
- **Inicialización de repositorio**: Se crea un repositorio vacío en GitHub y se conecta al repositorio local mediante `git remote`.
- **Commit y Push**: Los cambios en los archivos se guardan localmente y luego se suben al repositorio remoto en GitHub para mantener un registro histórico de los datos extraídos y limpiados.

### 4. **Elementos a Mejorar / Futuras Mejoras:**
- **Visualización de Datos**: Actualmente, no se han incluido visualizaciones en el proyecto, pero sería útil agregar gráficos para ilustrar las tendencias y comparaciones de los nutrientes a lo largo del tiempo o entre productos.
- **Automatización de la Extracción**: Una futura mejora sería automatizar el proceso de extracción periódica de datos, para mantener el repositorio actualizado sin intervención manual. Se planea utilizar airflow como orquestador.

## Requisitos

- Python 3.x
- Pandas
- Requests
- Selenium
- BeautifulSoup4 (si se requiere scraping)
- Git

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/simonkey1/ScrapingJumbo.git
