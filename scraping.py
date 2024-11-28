import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def scraping_data(lista_csvs, driver_path, archivo_resultante_base):
    """
    Realiza scraping de datos desde una lista de archivos CSV y genera un archivo JSON por cada archivo.
    """
    # Configuración del driver
    options = Options()
    options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    for archivo_csv in lista_csvs:
        # Preguntar al usuario por el tipo de producto
        tipo_producto = input(f"Ingrese el tipo de producto para los enlaces en {archivo_csv}: ").strip()

        # Leer enlaces desde el archivo CSV
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            enlaces = [row[0].strip() for row in reader if row]

        # Preguntar cuántos enlaces analizar
        while True:
            try:
                max_enlaces = int(input(f"Ingrese el número de enlaces a analizar (máximo {len(enlaces)}): ").strip())
                if max_enlaces > 0 and max_enlaces <= len(enlaces):
                    enlaces = enlaces[:max_enlaces]  # Tomar solo los primeros `max_enlaces` enlaces
                    break
                else:
                    print(f"Por favor, ingrese un número válido entre 1 y {len(enlaces)}.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número entero.")

        # Lista para almacenar los datos nutricionales
        datos_nutricionales = []

        # Procesar cada enlace
        for enlace in enlaces:
            url_producto = f'https://www.jumbo.cl{enlace}'  # Construir la URL del producto
            print(f'Accediendo a: {url_producto}')

            try:
                driver.get(url_producto)
                time.sleep(2)  # Espera a que la página cargue

                # Extraer datos del producto
                h1_element = driver.find_element(By.CSS_SELECTOR, 
                                                 'h1.product-name.text-black.text-lg.font-bold.lg\\:text-2xl.lg\\:mb-0\\.5')
                marca = driver.find_element(By.CSS_SELECTOR, 
                                            'span.product-brand.leading-\\[18px\\].text-primary500.text-base.font-semibold.text-black-600.underline.capitalize')
                id_product = driver.find_element(By.CSS_SELECTOR, 
                                                 'span.product-code.text-greyMidDark.text-sm.lg\\:mb-2')
                precio = driver.find_element(By.CSS_SELECTOR, 'span.prices-main-price')

                marca_producto = marca.text.strip()
                nombre_producto = h1_element.text.strip()
                codigo_producto = id_product.text.strip()  # Obtener el id
                precio_producto = precio.text.strip()  # Obtener el precio del producto

                # Información nutricional
                nutrientes = []
                try:
                    informacion_nutricional_tab = driver.find_element(By.XPATH, "//span[contains(text(), 'Información nutricional')]")
                    driver.execute_script("arguments[0].scrollIntoView();", informacion_nutricional_tab)
                    informacion_nutricional_tab.click()
                    time.sleep(2)  # Espera a que se cargue la tabla

                    li_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.nutritional-details-container-data li')

                    for i in range(0, len(li_elements), 3):  # Incrementar de 3 en 3
                        if i + 2 < len(li_elements):
                            nutriente = li_elements[i].text.strip()
                            valor_por_100g = li_elements[i + 1].text.strip()
                            valor_por_porcion = li_elements[i + 2].text.strip()

                            nutrientes.append({
                                'Nutriente': nutriente,
                                'Valor por 100g': valor_por_100g,
                                'Valor por porción': valor_por_porcion
                            })
                except Exception as e:
                    print(f"Información nutricional no disponible: {e}")

                # Ingredientes
                ingredientes_texto = "No disponible"
                try:
                    ingredientes_tab = driver.find_element(By.XPATH, "//span[contains(text(), 'Ingredientes')]")
                    ingredientes_tab.click()
                    time.sleep(1)

                    ingredientes_div = driver.find_element(By.CSS_SELECTOR, 'div.text-base.leading-5')
                    ingredientes_texto = ingredientes_div.text.strip()
                except Exception as e:
                    print(f"No se encontró la pestaña de 'Ingredientes': {e}")

                # Guardar datos del producto
                datos_nutricionales.append({
                    'Tipo Producto': tipo_producto,
                    'Marca': marca_producto,
                    'Nombre Producto': nombre_producto,
                    'Codigo Producto': codigo_producto,
                    'Precio': precio_producto,
                    'Ingredientes': ingredientes_texto,
                    'Nutrientes': nutrientes
                })

            except Exception as e:
                print(f"Error al procesar {url_producto}: {e}")

        # Guardar los datos en un archivo JSON
        archivo_json = f"{archivo_resultante_base}_{tipo_producto.replace(' ', '_')}.json"
        with open(archivo_json, 'w', encoding='utf-8') as file:
            json.dump(datos_nutricionales, file, ensure_ascii=False, indent=4)

        print(f"Datos guardados en {archivo_json}")

    # Cerrar el driver
    driver.quit()
