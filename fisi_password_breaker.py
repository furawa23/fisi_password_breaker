#!/usr/bin/env python3
import itertools
import os

# Códigos ANSI para diseño en terminal
C = '\033[96m'  # Cyan
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
R = '\033[91m'  # Red
W = '\033[0m'   # Reset/White

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{C}===================================================={W}")
    print(f"{C}      ███████╗██╗███████╗██╗{W}")
    print(f"{C}      ██╔════╝██║██╔════╝██║{W}")
    print(f"{C}      █████╗  ██║███████╗██║{W}")
    print(f"{C}      ██╔══╝  ██║╚════██║██║{W}")
    print(f"{C}      ██║     ██║███████║██║{W}")
    print(f"{C}      ╚═╝     ╚═╝╚══════╝╚═╝{W}")
    print(f"{R}   F I S I   P A S S W O R D   B R E A K E R{W}")
    print(f"{C}===================================================={W}")
    print(f"{Y}[*] Generador de Diccionarios OSINT Optimizado{W}\n")

def leet_speak(word):
    """Aplica mutaciones Leet Speak básicas pero limitadas para no saturar."""
    subs = {'a': ['a', '4', '@'], 'e': ['e', '3'], 'i': ['i', '1'], 'o': ['o', '0'], 's': ['s', '$']}
    opciones = [subs.get(char.lower(), [char]) for char in word]
    # Limitamos a 100 variaciones máximas por palabra para evitar sobrecarga
    variaciones = [''.join(comb) for comb in itertools.islice(itertools.product(*opciones), 100)]
    return variaciones

def recopilar_datos():
    print(f"{G}[+] FASE 1: Recolección de Datos (Deje en blanco si desconoce el dato){W}")
    
    nombre_raw = input(" Nombre (completo o solo uno): ").strip().lower()
    # Si ingresa nombre completo, lo separamos en palabras
    nombres = nombre_raw.split() if nombre_raw else []
    
    anio_nac = input(" Año de nacimiento (YYYY): ").strip()
    mes_nac = input(" Mes de nacimiento (MM): ").strip()
    dia_nac = input(" Día de nacimiento (DD): ").strip()
    
    color = input(" Color favorito: ").strip().lower()
    anio_imp = input(" Año importante (ej. boda, graduación): ").strip()
    ciudad = input(" Ciudad: ").strip().lower()
    
    print(f"\n{G}[+] FASE 2: Configuración del Diccionario{W}")
    archivo_salida = input(" Nombre del diccionario a generar (ej. dict_profesor.txt): ").strip()
    if not archivo_salida:
        archivo_salida = "diccionario_fisi.txt"
    if not archivo_salida.endswith(".txt"):
        archivo_salida += ".txt"

    try:
        min_len = int(input(" Longitud mínima de contraseña (ej. 8): ") or 8)
        max_len = int(input(" Longitud máxima de contraseña (ej. 16): ") or 16)
    except ValueError:
        print(f"{R}[!] Error de entrada. Se usarán valores por defecto (8-16).{W}")
        min_len, max_len = 8, 16
        
    # Agrupamos las palabras base
    semillas = nombres + [x for x in [color, ciudad] if x]
    
    # Agrupamos las fechas (individuales y combinadas como DDMM o DDMMAAAA)
    fechas_base = [x for x in [anio_nac, mes_nac, dia_nac, anio_imp] if x]
    if dia_nac y mes_nac:
        fechas_base.append(f"{dia_nac}{mes_nac}")
    if dia_nac y mes_nac y anio_nac:
        fechas_base.append(f"{dia_nac}{mes_nac}{anio_nac}")
        fechas_base.append(f"{dia_nac}{mes_nac}{anio_nac[-2:]}") # Ej: 120590 en vez de 12051990

    # Quitamos duplicados de las fechas
    fechas = list(set(fechas_base))
    
    return semillas, fechas, min_len, max_len, archivo_salida

def generar_diccionario(semillas, fechas, min_len, max_len):
    print(f"\n{Y}[*] Aplicando combinatoria, permutación y limitadores...{W}")
    diccionario = set()
    delimitadores = ['', '.', '_']
    simbolos = ['', '!', '*']

    # 1. Expandir semillas (Capitalización)
    semillas_expandidas = []
    for s in semillas:
        semillas_expandidas.extend([s, s.capitalize()])

    # 2. Permutaciones limitadas a un máximo de 2 palabras juntas
    for r in range(1, min(3, len(semillas_expandidas) + 1)): 
        for permutacion in itertools.permutations(semillas_expandidas, r):
            for delim in delimitadores:
                base_word = delim.join(permutacion)
                
                # 3. Aplicar sufijos (Fechas + Símbolos)
                sufijos_fecha = fechas + [''] 
                
                for fecha in sufijos_fecha:
                    for sim in simbolos:
                        pw_candidata = f"{base_word}{fecha}{sim}"
                        
                        # 4. Filtro de Límite de Longitud
                        if min_len <= len(pw_candidata) <= max_len:
                            diccionario.add(pw_candidata)
                            
                        # 5. Aplicar Leet Speak a contraseñas que pasen el filtro
                        if len(base_word) > 3:
                            for leet_word in leet_speak(pw_candidata):
                                if min_len <= len(leet_word) <= max_len:
                                    diccionario.add(leet_word)

    return sorted(list(diccionario))

def principal():
    banner()
    semillas, fechas, min_len, max_len, archivo_salida = recopilar_datos()
    
    if not semillas:
        print(f"{R}[-] No se ingresaron nombres ni palabras clave. Saliendo...{W}")
        return

    passwords = generar_diccionario(semillas, fechas, min_len, max_len)

    with open(archivo_salida, "w", encoding="utf-8") as f:
        for pw in passwords:
            f.write(pw + "\n")

    print(f"\n{G}[+] ¡Proceso Completado Exitosamente!{W}")
    print(f"{C}[*] Se han generado {len(passwords)} contraseñas únicas.{W}")
    print(f"{C}[*] Archivo guardado en: {os.path.abspath(archivo_salida)}{W}")

if __name__ == "__main__":
    principal()