#!/bin/bash

# Recorre todos los archivos en el directorio actual
for file in *; do
    # Si el archivo es un archivo (no un directorio), realiza el commit
    if [ -f "$file" ]; then
        # Añadir el archivo al área de staging
        git add "$file"
        
        # Crear un commit con el nombre del archivo como mensaje
        git commit -m "Subida de archivo: $file"
        
        # Empujar los cambios al repositorio remoto
        git push origin main
    fi
done
