import json
import re
import pandas as pd


def limpiar_datos_productos(json_data):
    """
    Limpia y transforma los datos extraídos de un archivo JSON, eliminando duplicados según el código del producto.
    
    Args:
        json_data (str or dict): Ruta al archivo JSON o un diccionario con datos extraídos.
    
    Returns:
        pd.DataFrame: DataFrame limpio con las columnas transformadas y sin duplicados.
    """
    # Cargar los datos desde un archivo o diccionario
    if isinstance(json_data, str):  # Si se pasa una ruta
        with open(json_data, 'r', encoding='utf-8') as file:
            datos = json.load(file)
    elif isinstance(json_data, dict):  # Si es un diccionario ya cargado
        datos = json_data
    else:
        raise ValueError("El input debe ser una ruta a un archivo JSON o un diccionario.")

    # Normalizar el JSON para obtener un DataFrame
    df = pd.json_normalize(
        datos,
        'Nutrientes',
        ['Marca', 'Codigo Producto', 'Nombre Producto', 'Precio', 'Ingredientes', 'Tipo Producto'], 
        errors='ignore'
    )
    
    # Pivotar para obtener formato ancho
    df_ancho = df.pivot_table(
        index=['Nombre Producto', 'Precio', 'Codigo Producto', 'Marca', 'Ingredientes', 'Tipo Producto'], 
        columns='Nutriente', 
        values=['Valor por 100g', 'Valor por porción'], 
        aggfunc='first'
    )

    # Aplanar columnas
    df_ancho.columns = [f'{nutriente} {valor}' for valor, nutriente in df_ancho.columns]
    df_ancho.reset_index(inplace=True)

    # Limpiar nombres de columnas
    df_ancho.columns = df_ancho.columns.str.strip().str.lower()
    df_ancho.columns = df_ancho.columns.str.replace(' ', '_')

    # Diccionario de abreviaciones (igual que antes)
    abbreviations = {
        'azúcares_totales_(g)_valor_por_100g': 'total_sugars_100g',
        'colesterol_(mg)_valor_por_100g': 'cholesterol_100g',
        'energía_(kcal)_valor_por_100g': 'energy_100g',
        'fibra_(g)_valor_por_100g': 'fiber_100g',
        'grasas_monoinsaturadas_(g)_valor_por_100g': 'mono_fats_100g',
        'grasas_poliinsaturadas_(g)_valor_por_100g': 'poly_fats_100g',
        'fibra_(g)_valor_por_porción': 'fiber_serving',
        'grasas_monoinsaturadas_(g)_valor_por_porción': 'mono_fats_serving',
        'grasas_poliinsaturadas_(g)_valor_por_porción': 'poly_fats_serving',
        'grasas_saturadas_(g)_valor_por_porción': 'sat_fats_serving',
        'grasas_totales_(g)_valor_por_porción': 'total_fats_serving',
        'grasas_trans_(g)_valor_por_porción': 'trans_fats_serving',
        'hidratos_de_carbono_disponibles_(g)_valor_por_porción': 'available_carbs_serving',
        'proteínas_(g)_valor_por_porción': 'proteins_serving',
        'sodio_(mg)_valor_por_porción': 'sodium_serving',
    }
    df_ancho.rename(columns=abbreviations, inplace=True)

    # Extraer tamaño y separarlo en valor y unidad
    df_ancho['tamaño'] = df_ancho['nombre_producto'].str.extract(r'(\d+(?:\.\d+)?\s*[a-zA-Z]+)$')

    def separate_size(size):
        match = re.match(r'(\d+(?:\.\d+)?)\s*(L|ml|g|kg|cc)', size)
        if match:
            value, unit = match.groups()
            return pd.Series([value, unit])
        return pd.Series([None, None])

    df_ancho['tamaño'] = df_ancho['tamaño'].astype(str)
    df_ancho[['valor', 'unidad']] = df_ancho['tamaño'].apply(separate_size)
    df_ancho.drop(columns=['tamaño'], inplace=True)

    # Ajustar valores específicos
    df_ancho['marca'] = df_ancho['marca'].replace('Frutas Y Verduras Propias', 'Jumbo')
    df_ancho['precio'] = df_ancho['precio'].str.replace('$', '', regex=False)
    df_ancho['precio'] = df_ancho['precio'].str.replace('.', '', regex=False)
    df_ancho['precio'] = df_ancho['precio'].replace('', '0').astype(int)
    df_ancho['codigo_producto'] = df_ancho['codigo_producto'].str.replace('Código: ', '', regex=False)

    # Rellenar nulos con 0
    df_ancho.fillna(0, inplace=True)

    # Convertir columnas numéricas
    cols_to_convert = [
        "total_sugars_100g", "cholesterol_100g", "energy_100g", "fiber_100g",
        "mono_fats_100g", "poly_fats_100g", "fiber_serving", "mono_fats_serving",
        "poly_fats_serving", "sat_fats_serving", "total_fats_serving",
        "trans_fats_serving", "available_carbs_serving", "proteins_serving", "sodium_serving"
    ]
    existing_columns = df_ancho.columns
    cols_to_convert = [col for col in cols_to_convert if col in existing_columns]

    for col in cols_to_convert:
        df_ancho[col] = df_ancho[col].astype(str).str.replace(r'[^\d]', '', regex=True)
        df_ancho[col] = pd.to_numeric(df_ancho[col])

    # Rellenar nulos tras conversión
    df_ancho.fillna(0, inplace=True)

    # **Eliminar duplicados basados en código_producto**
    df_ancho.drop_duplicates(subset=['codigo_producto'], inplace=True)

    return df_ancho
