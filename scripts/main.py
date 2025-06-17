from scraping import scraping_data
from limpieza import limpiar_datos_productos
import pandas as pd
import glob

def main():
    print("Ejecutando main.py")
    # 1. Archivos de entrada
    csvs = ["enlaces_legumbres_arroz.csv", "enlaces_pastas_salsas.csv"]
    driver_path = r"C:\Users\SIMON\Desktop\Kaggle\scraping\chromedriver.exe"
    archivo_resultante_base = "datos_scrapeados"

    # 2. Ejecutar el scraping
    print("Ejecutando scraping...")
    scraping_data(csvs, driver_path, archivo_resultante_base)
    print("Scraping completado.")

    # 3. Procesar los archivos JSON generados
    print("Procesando archivos JSON resultantes...")
    json_files = glob.glob("datos_scrapeados_*.json")  # Buscar todos los archivos JSON generados
    dataframes_limpios = []

    for file in json_files:
        print(f"Limpieza del archivo: {file}")
        df_limpio = limpiar_datos_productos(file)  # Limpiar los datos
        dataframes_limpios.append(df_limpio)

    # 4. Combinar todos los DataFrames limpios en uno solo
    df_final = pd.concat(dataframes_limpios, ignore_index=True)
    print("Todos los datos han sido limpiados y combinados.")

    # 5. Guardar el DataFrame final en un archivo CSV
    df_final.to_csv("datos_limpios.csv", index=False)
    print("Datos limpios guardados en 'datos_limpios.csv'.")

if __name__ == "__main__":
    main()