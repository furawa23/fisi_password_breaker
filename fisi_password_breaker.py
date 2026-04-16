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
    # Limitamos la generación a 100 variaciones máximas por palabra para evitar sobrecarga
    variaciones = [''.join(comb) for comb in itertools.islice(itertools.product(*opciones), 100)]
    return variaciones

def recopilar_datos():
    print(f"{G}[+] FASE 1: Recolección de Datos (Deje en blanco si desconoce el dato){W}")
    datos_base = {
        'nombre': input(" Nombre de la víctima: ").strip().lower(),
        'apellido': input(" Apellido: ").strip().lower(),
        'fecha_nac': input(" Año de nacimiento (ej. 1985): ").strip(),
        'fecha_grad': input(" Año importante (ej. boda, graduación): ").strip(),
        'color': input(" Color favorito: ").strip().lower(),
        'animal': input(" Mascota / Animal favorito: ").strip().lower(),
        'lugar': input(" Ciudad / Lugar favorito: ").strip().lower(),
        'empresa': input(" Empresa actual (¡No lo subestimes!): ").strip().lower()
    }
    
    print(f"\n{G}[+] FASE 2: Limitadores del Diccionario{W}")
    try:
        min_len = int(input(" Longitud mínima de contraseña (ej. 8): ") or 8)
        max_len = int(input(" Longitud máxima de contraseña (ej. 16): ") or 16)
    except ValueError:
        print(f"{R}[!] Error de entrada. Se usarán valores por defecto (8-16).{W}")
        min_len, max_len = 8, 16
        
    semillas = [v for k, v in datos_base.items() if v and not k.startswith('fecha')]
    fechas = [v for k, v in datos_base.items() if v and k.startswith('fecha')]
    
    return semillas, fechas, min_len, max_len

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
    for r in range(1, 3): 
        for permutacion in itertools.permutations(semillas_expandidas, r):
            for delim in delimitadores:
                base_word = delim.join(permutacion)
                
                # 3. Aplicar sufijos (Años importantes + Símbolos)
                # Si no hay fechas, añadimos una cadena vacía para que el bucle corra al menos una vez
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
    semillas, fechas, min_len, max_len = recopilar_datos()
    
    if not semillas:
        print(f"{R}[-] No se ingresaron semillas base. Saliendo...{W}")
        return

    passwords = generar_diccionario(semillas, fechas, min_len, max_len)
    archivo_salida = "diccionario_fisi.txt"

    with open(archivo_salida, "w", encoding="utf-8") as f:
        for pw in passwords:
            f.write(pw + "\n")

    print(f"\n{G}[+] ¡Proceso Completado Exitosamente!{W}")
    print(f"{C}[*] Se han generado {len(passwords)} contraseñas únicas bajo los parámetros establecidos.{W}")
    print(f"{C}[*] Archivo guardado en: {os.path.abspath(archivo_salida)}{W}")

if __name__ == "__main__":
    principal()