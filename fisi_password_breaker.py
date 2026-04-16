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
    print(f"{R}   F I S I   P A S S W O R D   B R E A K E R   P R O{W}")
    print(f"{C}===================================================={W}")
    print(f"{Y}[*] Generador Avanzado de Diccionarios OSINT{W}\n")

def leet_speak(word):
    """Aplica mutaciones Leet Speak comunes."""
    subs = {'a': ['a', '4', '@'], 'e': ['e', '3'], 'i': ['i', '1', '!'], 'o': ['o', '0'], 's': ['s', '$', '5']}
    opciones = [subs.get(char.lower(), [char]) for char in word]
    return [''.join(comb) for comb in itertools.islice(itertools.product(*opciones), 50)]

def recopilar_datos():
    print(f"{G}[+] FASE 1: Recolección de Datos Sociales{W}")
    print(f"{Y}(Presiona ENTER para omitir un dato si lo desconoces){W}\n")
    
    nombre_raw = input(f" {C}[?]{W} Nombres (ej. Juan Carlos): ").strip().lower()
    apellido_raw = input(f" {C}[?]{W} Apellidos (ej. Perez Gomez): ").strip().lower()
    
    print(f"\n {C}[?]{W} Fecha de Nacimiento:")
    dia_nac = input("     - Día (DD): ").strip()
    mes_nac = input("     - Mes (MM): ").strip()
    anio_nac = input("     - Año (YYYY): ").strip()
    
    color = input(f"\n {C}[?]{W} Color favorito: ").strip().lower()
    animal = input(f" {C}[?]{W} Animal favorito / Mascota: ").strip().lower()
    lugar = input(f" {C}[?]{W} Ciudad o lugar favorito: ").strip().lower()
    empresa = input(f" {C}[?]{W} Empresa o Universidad actual: ").strip().lower()
    anio_imp = input(f" {C}[?]{W} Otro año importante (ej. Boda, Graduación): ").strip()
    
    print(f"\n{G}[+] FASE 2: Configuración del Diccionario{W}")
    archivo_salida = input(f" {C}[?]{W} Nombre del archivo de salida (ej. dict_pro.txt): ").strip()
    if not archivo_salida:
        archivo_salida = "diccionario_fisi.txt"
    if not archivo_salida.endswith(".txt"):
        archivo_salida += ".txt"

    try:
        min_len = int(input(f" {C}[?]{W} Longitud mínima de contraseña [Default 8]: ") or 8)
        max_len = int(input(f" {C}[?]{W} Longitud máxima de contraseña [Default 16]: ") or 16)
    except ValueError:
        print(f"{R}[!] Error. Se usarán valores por defecto (8-16).{W}")
        min_len, max_len = 8, 16
        
    # Procesamiento de Semillas (Palabras)
    palabras_base = nombre_raw.split() + apellido_raw.split() + [color, animal, lugar, empresa]
    palabras_base = [p for p in palabras_base if p] 
    
    # Procesamiento de Fechas (Números)
    numeros_base = set()
    if anio_nac: 
        numeros_base.update([anio_nac, anio_nac[-2:]])
    if anio_imp:
        numeros_base.update([anio_imp, anio_imp[-2:]])
    
    # Aislamiento de Fechas Individuales
    if dia_nac:
        numeros_base.add(dia_nac)
    if mes_nac:
        numeros_base.add(mes_nac)
        
    if dia_nac and mes_nac:
        numeros_base.add(f"{dia_nac}{mes_nac}")
        numeros_base.add(f"{mes_nac}{dia_nac}")
    if dia_nac and mes_nac and anio_nac:
        numeros_base.add(f"{dia_nac}{mes_nac}{anio_nac}")
        numeros_base.add(f"{dia_nac}{mes_nac}{anio_nac[-2:]}")
        
    return list(set(palabras_base)), list(numeros_base), min_len, max_len, archivo_salida

def generar_diccionario(palabras, numeros, min_len, max_len):
    print(f"\n{Y}[*] Procesando combinaciones bidireccionales y mutaciones...{W}")
    diccionario = set()
    delimitadores = ['', '.', '_', '-']
    simbolos = ['', '!', '*', '$']

    # 1. Capitalización Predictiva
    palabras_exp = []
    for p in palabras:
        palabras_exp.extend([p.lower(), p.capitalize()])
        
    # 2. Combinaciones Básicas y Bidireccionales (Sufijos y Prefijos)
    for palabra in palabras_exp:
        if min_len <= len(palabra) <= max_len:
            diccionario.add(palabra)
            
        for num in numeros + ['']:
            for delim in delimitadores:
                for sim in simbolos:
                    candidato_suf = f"{palabra}{delim}{num}{sim}"
                    if min_len <= len(candidato_suf) <= max_len:
                        diccionario.add(candidato_suf)
                    
                    if num: 
                        candidato_pref = f"{num}{delim}{palabra}{sim}"
                        if min_len <= len(candidato_pref) <= max_len:
                            diccionario.add(candidato_pref)

    # 3. Permutación Limitada de 2 palabras juntas
    for r in itertools.permutations(palabras_exp, 2):
        for delim in delimitadores:
            base_compuesta = delim.join(r)
            for num in [''] + numeros: 
                candidato_comp = f"{base_compuesta}{num}"
                if min_len <= len(candidato_comp) <= max_len:
                    diccionario.add(candidato_comp)

    # 4. NUEVO: Envoltura Numérica (Fecha + Palabra + Fecha)
    print(f"{Y}[*] Generando envolturas numéricas avanzadas...{W}")
    for palabra in palabras_exp:
        for num_pref in numeros:
            for num_suf in numeros:
                # Filtro anti-duplicados lógicos
                if num_pref and num_suf and num_pref != num_suf:
                    for delim in delimitadores:
                        # Patrón: Fecha + Delimitador + Palabra + Delimitador + Fecha
                        candidato_env = f"{num_pref}{delim}{palabra}{delim}{num_suf}"
                        if min_len <= len(candidato_env) <= max_len:
                            diccionario.add(candidato_env)

    # 5. Fase de Leet Speak
    diccionario_final = set(diccionario)
    print(f"{Y}[*] Aplicando Leet Speak a las combinaciones generadas...{W}")
    for cand in diccionario:
        if len(cand) >= min_len:
            for leet_word in leet_speak(cand):
                if min_len <= len(leet_word) <= max_len:
                    diccionario_final.add(leet_word)

    return sorted(list(diccionario_final))

def principal():
    banner()
    palabras, numeros, min_len, max_len, archivo_salida = recopilar_datos()
    
    if not palabras:
        print(f"\n{R}[-] No se ingresaron suficientes palabras clave. Saliendo...{W}")
        return

    passwords = generar_diccionario(palabras, numeros, min_len, max_len)

    try:
        with open(archivo_salida, "w", encoding="utf-8") as f:
            for pw in passwords:
                f.write(pw + "\n")
                
        print(f"\n{G}[+] ¡Diccionario Generado Exitosamente!{W}")
        print(f"{C}[*] Total de combinaciones lógicas: {len(passwords)}{W}")
        print(f"{C}[*] Guardado en: {os.path.abspath(archivo_salida)}{W}")
    except IOError as e:
        print(f"\n{R}[!] Error al escribir el archivo: {e}{W}")

if __name__ == "__main__":
    try:
        principal()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Proceso cancelado por el usuario.{W}")