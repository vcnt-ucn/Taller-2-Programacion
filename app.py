MAX_POKEMON = 100
MAX_ZONAS = 10

nombres = [] # nombres de Pokémon
tipos = [] # tipo de cada Pokémon
zonas = [] # nombres de zonas
climas = [] # clima de cada zona
avist = [] # avist[i][j] => veces que el Pokémon i fue visto en la zona j

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
        elif len(zonas) < MAX_ZONAS:
            zonas.append(partes[0])
            climas.append(partes[1])
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
            elif len(nombres) < MAX_POKEMON:
                nombres.append(partes[0])
                tipos.append(partes[1])
                avist.append([0] * len(zonas))
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
                for j in range(len(zonas)):
                    if zonas[j] == zon:
                        z = j

                # buscar pokémon
                p = -1
                for i in range(len(nombres)):
                    if nombres[i] == nom:
                        p = i

                if z == -1:
                    ignoradas += 1
                elif p == -1:
                    if len(nombres) < MAX_POKEMON:
                        nombres.append(nom)
                        tipos.append("Desconocido")
                        avist.append([0] * len(zonas))
                        avist[len(nombres) - 1][z] += 1
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
            texto = input("Seleccione una opción: ")
            if not texto.isdigit():
                print("Error: debe ingresar un número.")
            elif int(texto) < 1 or int(texto) > 8:
                print("Error: la opción debe estar entre 1 y 8.")
            else:
                opcion = int(texto)
        match opcion:
            # === 1. Registrar avistamiento ===
            case 1:
                nom = input("Nombre del Pokémon: ")
                zon = input("Nombre de la zona: ")

                z = -1
                for j in range(len(zonas)):
                    if zonas[j] == zon:
                        z = j

                p = -1
                for i in range(len(nombres)):
                    if nombres[i] == nom:
                        p = i

                if z == -1:
                    print("La zona ingresada no existe")
                elif p == -1:
                    if len(nombres) >= MAX_POKEMON:
                        print("La Pokédex está llena")
                    else:
                        tipo = input("El Pokémon es nuevo. Ingrese su tipo: ")
                        nombres.append(nom)
                        tipos.append(tipo)
                        avist.append([0] * len(zonas))
                        avist[len(nombres) - 1][z] += 1
                        print("Avistamiento registrado")
                else:
                    avist[p][z] += 1
                    print("Avistamiento registrado")

            # === 2. Eliminar Pokémon ===
            case 2:
                nom = input("Nombre del Pokémon a eliminar: ")
                p = -1
                for i in range(len(nombres)):
                    if nombres[i] == nom:
                        p = i
                if p == -1:
                    print("El Pokémon no está registrado en la Pokédex")
                else:
                    nombres.pop(p)
                    tipos.pop(p)
                    avist.pop(p)
                    print("Pokémon eliminado")

            # === 3. Ranking ===
            case 3:
                totales = []
                orden = []
                for i in range(len(nombres)):
                    suma = 0
                    for j in range(len(zonas)):
                        suma += avist[i][j]
                    totales.append(suma)
                    orden.append(i)

                # burbuja descendente sobre los índices
                for a in range(len(orden) - 1):
                    for b in range(len(orden) - 1 - a):
                        if totales[orden[b]] < totales[orden[b + 1]]:
                            aux = orden[b]
                            orden[b] = orden[b + 1]
                            orden[b + 1] = aux

                for k in range(len(orden)):
                    i = orden[k]
                    print(str(k + 1) + ".", nombres[i], "-", totales[i], "avistamientos")

            # === 4. Zona con menos avistamientos ===
            case 4:
                mejor = -1
                menor = 0
                for j in range(len(zonas)):
                    suma = 0
                    for i in range(len(nombres)):
                        suma += avist[i][j]
                    if mejor == -1 or suma < menor:
                        mejor = j
                        menor = suma
                print("La zona con menos avistamientos es " + zonas[mejor] +
                    " (" + climas[mejor] + "), con " + str(menor) + " avistamientos")

            # === 5. Avistamientos de un Pokémon ===
            case 5:
                nom = input("Nombre del Pokémon: ")
                p = -1
                for i in range(len(nombres)):
                    if nombres[i] == nom:
                        p = i
                if p == -1:
                    print("El Pokémon no está registrado en la Pokédex")
                else:
                    total = 0
                    zmax = 0
                    for j in range(len(zonas)):
                        total += avist[p][j]
                        if avist[p][j] > avist[p][zmax]:
                            zmax = j
                    if total == 0:
                        print("Este Pokémon no tiene avistamientos")
                    else:
                        for j in range(len(zonas)):
                            print(zonas[j] + ":", avist[p][j])
                        print("Zona donde más aparece:", zonas[zmax])

            # === 6. Buscar por tipo ===
            case 6:
                tipo = input("Tipo a buscar: ")
                encontrados = 0
                for i in range(len(nombres)):
                    if tipos[i] == tipo:
                        suma = 0
                        for j in range(len(zonas)):
                            suma += avist[i][j]
                        print(nombres[i], "-", suma, "avistamientos")
                        encontrados += 1
                if encontrados == 0:
                    print("No hay Pokémon registrados de ese tipo")

            # === 7. Pokémon más común en una zona ===
            case 7:
                zon = input("Nombre de la zona: ")
                z = -1
                for j in range(len(zonas)):
                    if zonas[j] == zon:
                        z = j
                if z == -1:
                    print("La zona ingresada no existe")
                else:
                    total = 0
                    pmax = -1
                    for i in range(len(nombres)):
                        total += avist[i][z]
                        if pmax == -1 or avist[i][z] > avist[pmax][z]:
                            pmax = i
                    if total == 0:
                        print("No hay avistamientos en esta zona")
                    else:
                        print(nombres[pmax] + " es el Pokémon más común en " + zon +
                            ", con " + str(avist[pmax][z]) + " avistamientos")

            # === 8. Guardar y salir ===
            case 8:
                archivo = open("pokemon.txt", "w", encoding="utf-8")
                for i in range(len(nombres)):
                    archivo.write(nombres[i] + "," + tipos[i] + "\n")
                archivo.close()

                archivo = open("avistamientos.txt", "w", encoding="utf-8")
                for i in range(len(nombres)):
                    for j in range(len(zonas)):
                        for veces in range(avist[i][j]):
                            archivo.write(nombres[i] + "," + zonas[j] + "\n")
                archivo.close()

                archivo = open("estadisticas.txt", "w", encoding="utf-8")
                for j in range(len(zonas)):
                    suma = 0
                    for i in range(len(nombres)):
                        suma += avist[i][j]
                    archivo.write(zonas[j] + "," + climas[j] + "," + str(suma) + "\n")
                archivo.close()

                print("Hasta pronto,", entrenador)
                salir = True