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
    os.system('clear')
    print(f"{C}===================================================={W}")
    print(f"{C}      ███████╗██╗███████╗██╗{W}")
    print(f"{C}      ██╔════╝██║██╔════╝██║{W}")
    print(f"{C}      █████╗  ██║███████╗██║{W}")
    print(f"{C}      ██╔══╝  ██║╚════██║██║{W}")
    print(f"{C}      ██║     ██║███████║██║{W}")
    print(f"{C}      ╚═╝     ╚═╝╚══════╝╚═╝{W}")
    print(f"{R}   P A S S W O R D   B R E A K E R{W}")
    print(f"{C}===================================================={W}")
    print(f"{Y}[*] Herramienta Avanzada de Perfilamiento OSINT{W}\n")

def leet_speak(word):
    """Aplica mutaciones Leet Speak básicas a una palabra."""
    subs = {'a': ['a', '4', '@'], 'e': ['e', '3'], 'i': ['i', '1', '!'], 
            'o': ['o', '0'], 's': ['s', '5', '$']}
    
    opciones = [subs.get(char.lower(), [char]) for char in word]
    # Genera todas las combinaciones posibles de caracteres
    return [''.join(comb) for comb in itertools.product(*opciones)]

def recopilar_datos():
    print(f"{G}[+] Ingrese los datos de la víctima (deje en blanco si no aplica):{W}")
    datos = {
        'nombre': input(" Nombre: ").strip().lower(),
        'apellido': input(" Apellido: ").strip().lower(),
        'fecha': input(" Año relevante (ej. 2024): ").strip(),
        'empresa': input(" Entorno/Empresa: ").strip().lower(),
        'keyword': input(" Palabra clave (ej. python): ").strip().lower()
    }
    # Filtramos campos vacíos
    return [v for v in datos.values() if v]

def generar_diccionario(semillas):
    print(f"\n{Y}[*] Iniciando combinatoria y permutación...{W}")
    diccionario = set()
    delimitadores = ['', '.', '-', '_']
    simbolos_finales = ['', '!', '*']

    # 1. Expandir las semillas con capitalización
    semillas_expandidas = []
    for s in semillas:
        semillas_expandidas.extend([s, s.capitalize(), s.upper()])

    # 2. Permutaciones de 1 a 2 elementos (ej. Nombre, NombreApellido, EmpresaAño)
    for r in range(1, 3):
        for permutacion in itertools.permutations(semillas_expandidas, r):
            for delim in delimitadores:
                base_word = delim.join(permutacion)
                
                # 3. Aplicar Leet Speak a la palabra base
                variaciones_leet = leet_speak(base_word)
                
                # 4. Añadir símbolos finales
                for var in variaciones_leet:
                    for sim in simbolos_finales:
                        diccionario.add(var + sim)

    return sorted(list(diccionario))

def principal():
    banner()
    semillas = recopilar_datos()
    
    if not semillas:
        print(f"{R}[-] No se ingresaron datos. Saliendo...{W}")
        return

    passwords = generar_diccionario(semillas)
    archivo_salida = "diccionario_fisi.txt"

    with open(archivo_salida, "w", encoding="utf-8") as f:
        for pw in passwords:
            f.write(pw + "\n")

    print(f"{G}[+] ¡Proceso Completado!{W}")
    print(f"{C}[*] Se han generado {len(passwords)} contraseñas.{W}")
    print(f"{C}[*] Guardado en: {archivo_salida}{W}")

if __name__ == "__main__":
    principal()