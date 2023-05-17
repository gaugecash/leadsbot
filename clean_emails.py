import csv

def eliminar_correos_duplicados(archivo_entrada, archivo_salida):
    correos_duplicados = set()
    correos_unicos = []

    with open(archivo_entrada, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        
        for fila in lector_csv:
            correo = fila[0]  # Suponiendo que el correo electrónico está en la primera columna
            
            if correo in correos_duplicados:
                continue

            correos_duplicados.add(correo)
            correos_unicos.append(fila)
    
    with open(archivo_salida, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerows(correos_unicos)

    print(f"Se han eliminado los correos duplicados y se ha guardado el resultado en '{archivo_salida}'.")

# Uso del script
archivo_entrada = "leads-IG-05-17.csv"  
archivo_salida = "final.csv" 

eliminar_correos_duplicados(archivo_entrada, archivo_salida)