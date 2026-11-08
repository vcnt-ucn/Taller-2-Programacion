MAX_POKEMON = 100
MAX_ZONAS = 10

nombres = [""] * MAX_POKEMON # nombres de Pokémon
tipos = [""] * MAX_POKEMON # tipo de cada Pokémon
zonas = [""] * MAX_ZONAS # nombres de zonas
climas = [""] * MAX_ZONAS # clima de cada zona
avist = [None] * MAX_POKEMON # avist[i][j] => veces que el Pokémon i fue visto en la zona j
for i in range(MAX_POKEMON):
    avist[i] = [0] * MAX_ZONAS

np = 0 # cantidad de Pokémon en la Pokédex
nz = 0 # cantidad de zonas

error = False
ignoradas = 0

entrenador = input("Ingrese su nombre de entrenador: ")

# === Lectura de zonas.txt ===
archivo = open("zonas.txt", "r", encoding="utf-8")
for linea in archivo:
    linea = linea.strip()
    if linea != "":
        partes = linea.split(",")
        if len(partes) != 2:
            error = True
        elif nz < MAX_ZONAS:
            zonas[nz] = partes[0]
            climas[nz] = partes[1]
            nz += 1
archivo.close()
# === Lectura de pokemon.txt ===
if not error:
    archivo = open("pokemon.txt", "r", encoding="utf-8")
    for linea in archivo:
        linea = linea.strip()
        if linea != "":
            partes = linea.split(",")
            if len(partes) != 2:
                error = True
            elif np < MAX_POKEMON:
                nombres[np] = partes[0]
                tipos[np] = partes[1]
                np += 1
    archivo.close()
# === Lectura de avistamientos.txt ===
if not error:
    archivo = open("avistamientos.txt", "r", encoding="utf-8")
    for linea in archivo:
        linea = linea.strip()
        if linea != "":
            partes = linea.split(",")
            if len(partes) != 2:
                error = True
            else:
                nom = partes[0] # nombre del Pokémon
                zon = partes[1] # zona donde fue visto
                # buscar zona
                z = -1
                for j in range(nz):
                    if zonas[j] == zon:
                        z = j
                # buscar pokémon
                p = -1
                for i in range(np):
                    if nombres[i] == nom:
                        p = i
                if z == -1:
                    ignoradas += 1
                elif p == -1:
                    if np < MAX_POKEMON:
                        nombres[np] = nom
                        tipos[np] = "Desconocido"
                        avist[np][z] += 1
                        np += 1
                    else:
                        ignoradas += 1
                else:
                    avist[p][z] += 1
    archivo.close()
if error:
    print("Error: una línea de un archivo no cumple la estructura requerida.")
else:
    print("Líneas ignoradas:", ignoradas)
    print("Bienvenido/a,", entrenador)
    salir = False
    while not salir:
        print()
        print("1. Registrar avistamiento")
        print("2. Eliminar Pokémon")
        print("3. Ranking de Pokémon más vistos")
        print("4. Zona con menos avistamientos")
        print("5. Avistamientos de un Pokémon")
        print("6. Buscar por tipo")
        print("7. Pokémon más común en una zona")
        print("8. Guardar y salir")
        # validación de opción
        opcion = 0
        while opcion == 0:
            try:
                texto = input("Seleccione una opción: ")
                if int(texto) < 1 or int(texto) > 8:
                    print("Error: la opción debe estar entre 1 y 8.")
                else:
                    opcion = int(texto)
            except ValueError:
                print("Error: debe ingresar un número.")
        match opcion:
            # === 1. Registrar avistamiento ===
            case 1:
                nom = input("Nombre del Pokémon: ")
                zon = input("Nombre de la zona: ")
                z = -1
                for j in range(nz):
                    if zonas[j] == zon:
                        z = j
                p = -1
                for i in range(np):
                    if nombres[i] == nom:
                        p = i
                if z == -1:
                    print("La zona ingresada no existe")
                elif p == -1:
                    if np >= MAX_POKEMON:
                        print("La Pokédex está llena")
                    else:
                        tipo = input("El Pokémon es nuevo. Ingrese su tipo: ")
                        nombres[np] = nom
                        tipos[np] = tipo
                        avist[np][z] += 1
                        np += 1
                        print("Avistamiento registrado")
                else:
                    avist[p][z] += 1
                    print("Avistamiento registrado")
            # === 2. Eliminar Pokémon ===
            case 2:
                nom = input("Nombre del Pokémon a eliminar: ")
                p = -1
                for i in range(np):
                    if nombres[i] == nom:
                        p = i
                if p == -1:
                    print("El Pokémon no está registrado en la Pokédex")
                else:
                    for i in range(p, np - 1):
                        nombres[i] = nombres[i + 1]
                        tipos[i] = tipos[i + 1]
                        for j in range(MAX_ZONAS):
                            avist[i][j] = avist[i + 1][j]
                    nombres[np - 1] = ""
                    tipos[np - 1] = ""
                    for j in range(MAX_ZONAS):
                        avist[np - 1][j] = 0
                    np -= 1
                    print("Pokémon eliminado")
            # === 3. Ranking ===
            case 3:
                totales = [0] * MAX_POKEMON
                orden = [0] * MAX_POKEMON
                for i in range(np):
                    suma = 0
                    for j in range(nz):
                        suma += avist[i][j]
                    totales[i] = suma
                    orden[i] = i
                # burbuja descendente sobre los índices
                for a in range(np - 1):
                    for b in range(np - 1 - a):
                        if totales[orden[b]] < totales[orden[b + 1]]:
                            aux = orden[b]
                            orden[b] = orden[b + 1]
                            orden[b + 1] = aux
                for k in range(np):
                    i = orden[k]
                    print(f"{k + 1}. {nombres[i]} - {totales[i]} avistamientos")
            # === 4. Zona con menos avistamientos ===
            case 4:
                mejor = -1
                menor = 0
                for j in range(nz):
                    suma = 0
                    for i in range(np):
                        suma += avist[i][j]
                    if mejor == -1 or suma < menor:
                        mejor = j
                        menor = suma
                print(f"La zona con menos avistamientos es {zonas[mejor]} ({climas[mejor]}), con {menor} avistamientos")
            # === 5. Avistamientos de un Pokémon ===
            case 5:
                nom = input("Nombre del Pokémon: ")
                p = -1
                for i in range(np):
                    if nombres[i] == nom:
                        p = i
                if p == -1:
                    print("El Pokémon no está registrado en la Pokédex")
                else:
                    total = 0
                    zmax = 0
                    for j in range(nz):
                        total += avist[p][j]
                        if avist[p][j] > avist[p][zmax]:
                            zmax = j
                    if total == 0:
                        print("Este Pokémon no tiene avistamientos")
                    else:
                        for j in range(nz):
                            print(f"{zonas[j]}: {avist[p][j]}")
                        print("Zona donde más aparece:", zonas[zmax])
            # === 6. Buscar por tipo ===
            case 6:
                tipo = input("Tipo a buscar: ")
                encontrados = 0
                for i in range(np):
                    if tipos[i] == tipo:
                        suma = 0
                        for j in range(nz):
                            suma += avist[i][j]
                        print(nombres[i], "-", suma, "avistamientos")
                        encontrados += 1
                if encontrados == 0:
                    print("No hay Pokémon registrados de ese tipo")
            # === 7. Pokémon más común en una zona ===
            case 7:
                zon = input("Nombre de la zona: ")
                z = -1
                for j in range(nz):
                    if zonas[j] == zon:
                        z = j
                if z == -1:
                    print("La zona ingresada no existe")
                else:
                    total = 0
                    pmax = -1
                    for i in range(np):
                        total += avist[i][z]
                        if pmax == -1 or avist[i][z] > avist[pmax][z]:
                            pmax = i
                    if total == 0:
                        print("No hay avistamientos en esta zona")
                    else:
                        print(f"{nombres[pmax]} es el Pokémon más común en {zon}, con {avist[pmax][z]} avistamientos")
            # === 8. Guardar y salir ===
            case 8:
                archivo = open("pokemon.txt", "w", encoding="utf-8")
                for i in range(np):
                    archivo.write(f"{nombres[i]},{tipos[i]}\n")
                archivo.close()
                archivo = open("avistamientos.txt", "w", encoding="utf-8")
                for i in range(np):
                    for j in range(nz):
                        for veces in range(avist[i][j]):
                            archivo.write(f"{nombres[i]},{zonas[j]}\n")
                archivo.close()
                archivo = open("estadisticas.txt", "w", encoding="utf-8")
                for j in range(nz):
                    suma = 0
                    for i in range(np):
                        suma += avist[i][j]
                    archivo.write(f"{zonas[j]},{climas[j]},{suma}\n")
                archivo.close()
                print("Hasta pronto,", entrenador)
                salir = True