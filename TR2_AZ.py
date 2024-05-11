import subprocess

def cifrar_simetrico(archivo_original, archivo_cifrado):
    try:
        subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-in", archivo_original, "-out", archivo_cifrado, "-pbkdf2"])
        print("Archivo cifrado exitosamente.")
    except Exception as e:
        print(f"Error al cifrar el archivo: {e}")

def descifrar_simetrico(archivo_cifrado, archivo_original):
    try:
        subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-in", archivo_cifrado, "-out", archivo_original, "-pbkdf2"])
        print("Archivo descifrado exitosamente.")
    except Exception as e:
        print(f"Error al descifrar el archivo: {e}")


def generar_claves_asimetrico():
    try:
        ruta_privada = input("Ingrese la ruta donde guardar la clave privada con terminación .pem: ")
        ruta_publica = input("Ingrese la ruta donde guardar la clave pública con terminación .pem: ")
        
        subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", ruta_privada])
        subprocess.run(["openssl", "rsa", "-pubout", "-in", ruta_privada, "-out", ruta_publica])
        
        print("Par de claves pública y privada generadas exitosamente.")
    except Exception as e:
        print(f"Error al generar el par de claves: {e}")

def cifrar_asimetrico(archivo_original, archivo_cifrado):
    try:
        ruta_publica = input("Ingrese la ruta de la clave pública: ")
        subprocess.run(["openssl", "rsautl", "-encrypt", "-pubin", "-inkey", ruta_publica, "-in", archivo_original, "-out", archivo_cifrado])
        print("Archivo cifrado asimétricamente exitosamente.")
    except Exception as e:
        print(f"Error al cifrar asimétricamente el archivo: {e}")

def descifrar_asimetrico(archivo_cifrado, archivo_descifrado, archivo_privada):
    try:
        subprocess.run(["openssl", "rsautl", "-decrypt", "-inkey", archivo_privada, "-in", archivo_cifrado, "-out", archivo_descifrado])
        print("Archivo descifrado asimétricamente exitosamente.")
    except Exception as e:
        print(f"Error al descifrar asimétricamente el archivo: {e}")

def cifrar_hibridamente(archivo_original, archivo_cifrado):
    try:
        # Generar clave simétrica
        ruta_clave_simetrica = input("Ingrese la ruta donde guardar la clave simétrica: ")
        subprocess.run(["openssl", "rand", "-out", ruta_clave_simetrica, "32"])  # 32 bytes = 256 bits
        
        # Cifrar archivo simétricamente
        subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-in", archivo_original, "-out", archivo_cifrado, "-pbkdf2", "-pass", "file:" + ruta_clave_simetrica])

        # Cifrar la clave simétrica con la clave pública RSA
        ruta_publica = input("Ingrese la ruta de la clave pública: ")
        subprocess.run(["openssl", "rsautl", "-encrypt", "-pubin", "-inkey", ruta_publica, "-in", ruta_clave_simetrica, "-out", archivo_cifrado + ".key.enc"])

        print("Archivo cifrado híbridamente exitosamente.")
    except Exception as e:
        print(f"Error al cifrar híbridamente el archivo: {e}")

def descifrar_hibridamente(archivo_cifrado, archivo_descifrado):
    try:
        # Obtener la ruta de la clave privada
        ruta_privada = input("Ingrese la ruta del archivo de clave privada: ")

        # Descifrar la clave simétrica cifrada con la clave pública RSA
        subprocess.run(["openssl", "rsautl", "-decrypt", "-inkey", ruta_privada, "-in", archivo_cifrado + ".key.enc", "-out", archivo_cifrado + ".key"])

        # Descifrar el archivo utilizando la clave simétrica
        subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-in", archivo_cifrado, "-out", archivo_descifrado, "-pbkdf2", "-pass", "file:" + archivo_cifrado + ".key"])

        print("Archivo descifrado híbridamente exitosamente.")
    except Exception as e:
        print(f"Error al descifrar híbridamente el archivo: {e}")



def caratula():
    print("̣̣̣************** TRABAJO FINAL **************")
    print("*ALUMNO: CESAR AZNARAN CABRERA*")
    print("*DOCENTE: ING. JHONATAN ANTONIO URQUIA MUSAYON*")
    print("*CARRERA PROFESIONAL: INGENIERÍA DE LA CIBERSEGURIDAD*")
    print("*CENTRO DE ESTUDIOS: SENATI*")
    print("*CURSO: LENGUAJE DE LA PROGRAMACIÓN*")
    print("̣̣̣************** TRABAJO FINAL **************")

def main():
    caratula()
    while True:
        print("\nMenú principal: ")
        print("1. Cifrar archivo simétricamente")
        print("2. Descifrar archivo simétricamente")
        print("3. Generar par de claves RSA")
        print("4. Cifrar archivo asimétricamente")
        print("5. Descifrar archivo asimétricamente") 
        print("6. Cifrar archivo híbridamente")
        print("7. Descifrar archivo híbridamente")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            archivo_original = input("Ingrese la ruta del archivo original: ")
            archivo_cifrado = input("Ingrese la ruta donde guardar el archivo cifrado: ")
            cifrar_simetrico(archivo_original, archivo_cifrado)
        elif opcion == "2":
            archivo_cifrado = input("Ingrese la ruta del archivo cifrado: ")
            archivo_original = input("Ingrese la ruta donde guardar el archivo descifrado: ")
            descifrar_simetrico(archivo_cifrado, archivo_original)
        elif opcion == "3":
            generar_claves_asimetrico()
        elif opcion == "4":
            archivo_original = input("Ingrese la ruta del archivo original: ")
            archivo_cifrado = input("Ingrese la ruta donde guardar el archivo cifrado: ")
            cifrar_asimetrico(archivo_original, archivo_cifrado)
        elif opcion == "5":
            archivo_cifrado = input("Ingrese la ruta del archivo cifrado: ")
            archivo_descifrado = input("Ingrese la ruta donde guardar el archivo descifrado: ")
            archivo_privada = input("Ingrese la ruta del archivo de clave privada: ")  # Solicitar el archivo de clave privada
            descifrar_asimetrico(archivo_cifrado, archivo_descifrado, archivo_privada)

        elif opcion == "6":
            archivo_original = input("Ingrese la ruta del archivo original: ")
            archivo_cifrado = input("Ingrese la ruta donde guardar el archivo cifrado: ")
            cifrar_hibridamente(archivo_original, archivo_cifrado)

        elif opcion == "7":
            archivo_cifrado = input("Ingrese la ruta del archivo cifrado: ")
            archivo_descifrado = input("Ingrese la ruta donde guardar el archivo descifrado: ")
            descifrar_hibridamente(archivo_cifrado, archivo_descifrado)

        elif opcion == "8":
            print("Saliendo del programa...........")
            break
        else:
            print("Opción no válida. Por favor seleccione una opción del menú.")

if __name__ == "__main__":
    main()
