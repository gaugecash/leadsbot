import csv

def count_emails(archivo_entrada, archivo_salida):
    correos = {}

    with open(archivo_entrada, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        
        for fila in lector_csv:
            correo = fila[0]  # Suponiendo que el correo electrónico está en la primera columna
            
            if correo in correos:
                correos[correo] += 1
            else:
                correos[correo] = 1
    
    with open(archivo_salida, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        for correo, repeticiones in correos.items():
            escritor_csv.writerow([correo, repeticiones])

    print(f"Se han eliminado los correos duplicados y se ha guardado el resultado en '{archivo_salida}'.")


# Uso del script
archivo_entrada = "results.csv"  
archivo_salida = "results-count.csv" 

count_emails(archivo_entrada, archivo_salida)
