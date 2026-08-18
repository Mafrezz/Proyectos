# ============================================================
# SISTEMA DE ANALITICA ACADEMICA
# PYTHON + POSTGRESQL
# ============================================================

import os
import re
import psycopg2
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURACION
# ============================================================

MAX_TAREAS = 25
MAX_PARCIAL1 = 16
MAX_PARCIAL2 = 17
MAX_PARCIAL3 = 17
MAX_EXAMEN = 25

NOTA_APROBACION = 61


# ============================================================
# ARCHIVO NOTAS.TXT
# ============================================================

# Siempre utiliza el notas.txt que esta en la misma carpeta
# que este archivo Parcial1.py

CARPETA_PROGRAMA = os.path.dirname(
    os.path.abspath(__file__)
)

ARCHIVO = os.path.join(
    CARPETA_PROGRAMA,
    "notas.txt"
)


# ============================================================
# CONEXION A POSTGRESQL
# ============================================================

def conectar_bd():

    try:

        conn = psycopg2.connect(
            dbname="postgres",
            host="localhost",
            port="5432",
            user="postgres",
            password="mafer123"
        )

        print(
            "\nConexion con PostgreSQL establecida."
        )

        return conn

    except Exception:

        print(
            "\nPostgreSQL no disponible."
        )

        print(
            "Los registros se almacenaran en notas.txt."
        )

        return None


# ============================================================
# CREAR TABLA
# ============================================================

def crear_tabla(conn):

    if conn is None:
        return

    try:

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas_academicas (
                id SERIAL PRIMARY KEY,
                carnet VARCHAR(30),
                nombre VARCHAR(100),
                tareas NUMERIC(5,2),
                parcial1 NUMERIC(5,2),
                parcial2 NUMERIC(5,2),
                parcial3 NUMERIC(5,2),
                examen_final NUMERIC(5,2),
                nota_exacta NUMERIC(6,2),
                nota_final INTEGER,
                estado VARCHAR(20)
            );
        """)

        conn.commit()

        cursor.close()

    except Exception:

        conn.rollback()

        print(
            "Advertencia: no se pudo verificar la tabla."
        )


# ============================================================
# VALIDAR CARNET
# ============================================================

def pedir_carnet():

    while True:

        carnet = input(
            "Ingrese el carnet: "
        ).strip()

        if re.fullmatch(
            r"[0-9]{9}",
            carnet
        ):

            return carnet

        print(
            "ERROR: El carnet debe contener exactamente 9 numeros."
        )


# ============================================================
# VALIDAR NOMBRE
# ============================================================

def pedir_nombre():

    while True:

        nombre = input(
            "Ingrese el nombre: "
        ).strip()

        if (
            nombre
            and re.fullmatch(
                r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+",
                nombre
            )
        ):

            return nombre

        print(
            "ERROR: El nombre solo puede contener letras y espacios."
        )


# ============================================================
# VALIDAR NOTAS
# ============================================================

def pedir_nota(mensaje, maximo):

    while True:

        entrada = input(
            mensaje
        ).strip()

        try:

            valor = float(entrada)

        except ValueError:

            print(
                "ERROR: Debe ingresar un valor numerico."
            )

            continue

        if valor < 0 or valor > maximo:

            print(
                f"ERROR: La nota debe estar entre 0 y {maximo:.2f}."
            )

        else:

            return valor


# ============================================================
# REDONDEO DE INGENIERIA
# ============================================================

def redondeo_ingenieria(valor):

    parte_entera = int(valor)

    parte_decimal = valor - parte_entera

    if parte_decimal >= 0.5:

        return parte_entera + 1

    else:

        return parte_entera


# ============================================================
# GUARDAR EN NOTAS.TXT
# ============================================================

def guardar_archivo(
    carnet,
    nombre,
    tareas,
    parcial1,
    parcial2,
    parcial3,
    examen_final,
    nota_exacta,
    nota_final,
    estado
):

    try:

        with open(
            ARCHIVO,
            "a",
            encoding="utf-8"
        ) as archivo:

            archivo.write(
                "========================================\n"
            )

            archivo.write(
                "REGISTRO ACADEMICO\n"
            )

            archivo.write(
                "========================================\n"
            )

            archivo.write(
                f"Carnet: {carnet}\n"
            )

            archivo.write(
                f"Nombre: {nombre}\n"
            )

            archivo.write(
                f"Tareas: {tareas:.2f}\n"
            )

            archivo.write(
                f"Parcial 1: {parcial1:.2f}\n"
            )

            archivo.write(
                f"Parcial 2: {parcial2:.2f}\n"
            )

            archivo.write(
                f"Parcial 3: {parcial3:.2f}\n"
            )

            archivo.write(
                f"Examen Final: {examen_final:.2f}\n"
            )

            archivo.write(
                f"Nota exacta: {nota_exacta:.2f}\n"
            )

            archivo.write(
                f"Nota final: {nota_final}\n"
            )

            archivo.write(
                f"Estado: {estado}\n"
            )

            archivo.write(
                "========================================\n\n"
            )

        print(
            "Registro guardado en notas.txt."
        )

        return True

    except Exception as error:

        print(
            "ERROR: No se pudo guardar en notas.txt."
        )

        print(error)

        return False


# ============================================================
# GUARDAR EN POSTGRESQL
# ============================================================

def guardar_bd(
    conn,
    carnet,
    nombre,
    tareas,
    parcial1,
    parcial2,
    parcial3,
    examen_final,
    nota_exacta,
    nota_final,
    estado
):

    if conn is None:

        print(
            "PostgreSQL no esta disponible."
        )

        return

    try:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notas_academicas
            (
                carnet,
                nombre,
                tareas,
                parcial1,
                parcial2,
                parcial3,
                examen_final,
                nota_exacta,
                nota_final,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            carnet,
            nombre,
            tareas,
            parcial1,
            parcial2,
            parcial3,
            examen_final,
            nota_exacta,
            nota_final,
            estado
        ))

        conn.commit()

        cursor.close()

        print(
            "Registro guardado en PostgreSQL."
        )

    except Exception as error:

        conn.rollback()

        print(
            "Advertencia: no se pudo guardar en PostgreSQL."
        )

        print(error)


# ============================================================
# INGRESAR DATOS
# ============================================================

def ingresar_datos(conn):

    print(
        "\n============= INGRESO DE DATOS ============="
    )

    carnet = pedir_carnet()

    nombre = pedir_nombre()

    tareas = pedir_nota(
        "Tareas (0-25): ",
        MAX_TAREAS
    )

    parcial1 = pedir_nota(
        "Parcial 1 (0-16): ",
        MAX_PARCIAL1
    )

    parcial2 = pedir_nota(
        "Parcial 2 (0-17): ",
        MAX_PARCIAL2
    )

    parcial3 = pedir_nota(
        "Parcial 3 (0-17): ",
        MAX_PARCIAL3
    )

    examen_final = pedir_nota(
        "Examen Final (0-25): ",
        MAX_EXAMEN
    )

    # ========================================================
    # CALCULAR NOTA
    # ========================================================

    nota_exacta = (
        tareas
        + parcial1
        + parcial2
        + parcial3
        + examen_final
    )

    nota_final = redondeo_ingenieria(
        nota_exacta
    )

    # ========================================================
    # ESTADO
    # ========================================================

    if nota_final >= NOTA_APROBACION:

        estado = "Aprobado"

    else:

        estado = "Reprobado"

    # ========================================================
    # MOSTRAR RESULTADO
    # ========================================================

    print(
        "\n=============================================="
    )

    print(
        "              RESULTADO ACADEMICO"
    )

    print(
        "=============================================="
    )

    print(
        f"Carnet:       {carnet}"
    )

    print(
        f"Nombre:       {nombre}"
    )

    print(
        f"Tareas:       {tareas:.2f} / 25"
    )

    print(
        f"Parcial 1:    {parcial1:.2f} / 16"
    )

    print(
        f"Parcial 2:    {parcial2:.2f} / 17"
    )

    print(
        f"Parcial 3:    {parcial3:.2f} / 17"
    )

    print(
        f"Examen Final: {examen_final:.2f} / 25"
    )

    print(
        f"Nota exacta:  {nota_exacta:.2f}"
    )

    print(
        f"Nota final:   {nota_final}"
    )

    print(
        f"Estado:       {estado}"
    )

    print(
        "=============================================="
    )

    # ========================================================
    # GUARDAR EN ARCHIVO
    # ========================================================

    guardar_archivo(
        carnet,
        nombre,
        tareas,
        parcial1,
        parcial2,
        parcial3,
        examen_final,
        nota_exacta,
        nota_final,
        estado
    )

    # ========================================================
    # GUARDAR EN POSTGRESQL
    # ========================================================

    guardar_bd(
        conn,
        carnet,
        nombre,
        tareas,
        parcial1,
        parcial2,
        parcial3,
        examen_final,
        nota_exacta,
        nota_final,
        estado
    )


# ============================================================
# LEER REGISTROS DESDE NOTAS.TXT
# ============================================================

def leer_registros():

    if not os.path.exists(ARCHIVO):

        return []

    try:

        with open(
            ARCHIVO,
            "r",
            encoding="utf-8"
        ) as archivo:

            contenido = archivo.read()

    except Exception:

        return []

    if not contenido.strip():

        return []

    bloques = contenido.split(
        "========================================"
    )

    registros = []

    for bloque in bloques:

        if "Carnet:" not in bloque:

            continue

        registro = {}

        for linea in bloque.strip().splitlines():

            if ":" not in linea:

                continue

            clave, valor = linea.split(
                ":",
                1
            )

            registro[
                clave.strip()
            ] = valor.strip()

        if "Carnet" in registro:

            registros.append(
                registro
            )

    return registros


# ============================================================
# HISTORIAL TABULADO
# ============================================================

def mostrar_historial():

    registros = leer_registros()

    if not registros:

        print(
            "\nNo existen registros."
        )

        return

    print(
        "\n================ HISTORIAL ================="
    )

    print(
        "=" * 125
    )

    print(
        f"{'Carnet':<15}"
        f"{'Nombre':<25}"
        f"{'Tareas':<10}"
        f"{'P1':<8}"
        f"{'P2':<8}"
        f"{'P3':<8}"
        f"{'Examen':<10}"
        f"{'Final':<8}"
        f"{'Estado':<12}"
    )

    print(
        "=" * 125
    )

    for registro in registros:

        print(
            f"{registro.get('Carnet', ''):<15}"
            f"{registro.get('Nombre', ''):<25}"
            f"{registro.get('Tareas', ''):<10}"
            f"{registro.get('Parcial 1', ''):<8}"
            f"{registro.get('Parcial 2', ''):<8}"
            f"{registro.get('Parcial 3', ''):<8}"
            f"{registro.get('Examen Final', ''):<10}"
            f"{registro.get('Nota final', ''):<8}"
            f"{registro.get('Estado', ''):<12}"
        )

    print(
        "=" * 125
    )


# ============================================================
# DASHBOARD
# ============================================================

def generar_dashboard():

    registros = leer_registros()

    if not registros:

        print(
            "\nNo existen registros para generar las graficas."
        )

        return

    nombres = []
    notas = []
    tareas = []
    parcial1 = []
    parcial2 = []
    parcial3 = []
    examenes = []

    aprobados = 0
    reprobados = 0

    for registro in registros:

        nombres.append(
            registro.get(
                "Nombre",
                ""
            )
        )

        notas.append(
            float(
                registro.get(
                    "Nota final",
                    0
                )
            )
        )

        tareas.append(
            float(
                registro.get(
                    "Tareas",
                    0
                )
            )
        )

        parcial1.append(
            float(
                registro.get(
                    "Parcial 1",
                    0
                )
            )
        )

        parcial2.append(
            float(
                registro.get(
                    "Parcial 2",
                    0
                )
            )
        )

        parcial3.append(
            float(
                registro.get(
                    "Parcial 3",
                    0
                )
            )
        )

        examenes.append(
            float(
                registro.get(
                    "Examen Final",
                    0
                )
            )
        )

        if registro.get(
            "Estado"
        ) == "Aprobado":

            aprobados += 1

        elif registro.get(
            "Estado"
        ) == "Reprobado":

            reprobados += 1

    print(
        "\nGenerando Dashboard de Analitica Academica..."
    )

    # ========================================================
    # GRAFICA 1: RENDIMIENTO INDIVIDUAL
    # ========================================================

    plt.figure()

    plt.bar(
        nombres,
        notas
    )

    plt.title(
        "Rendimiento Individual"
    )

    plt.xlabel(
        "Estudiante"
    )

    plt.ylabel(
        "Nota Final"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.grid(
        axis="y"
    )

    plt.tight_layout()

    # ========================================================
    # GRAFICA 2: INDICE DE APROBACION
    # ========================================================

    plt.figure()

    valores = [
        aprobados,
        reprobados
    ]

    etiquetas = [
        "Aprobado",
        "Reprobado"
    ]

    if sum(valores) > 0:

        plt.pie(
            valores,
            labels=etiquetas,
            autopct="%1.1f%%"
        )

        plt.title(
            "Indice de Aprobacion"
        )

    # ========================================================
    # GRAFICA 3: DESEMPEÑO POR RUBRO
    # ========================================================

    promedios = [

        sum(tareas) / len(tareas),

        sum(parcial1) / len(parcial1),

        sum(parcial2) / len(parcial2),

        sum(parcial3) / len(parcial3),

        sum(examenes) / len(examenes)

    ]

    evaluaciones = [

        "Tareas",
        "Parcial 1",
        "Parcial 2",
        "Parcial 3",
        "Examen Final"

    ]

    plt.figure()

    plt.bar(
        evaluaciones,
        promedios
    )

    plt.title(
        "Desempeño Promedio por Rubro"
    )

    plt.xlabel(
        "Evaluacion"
    )

    plt.ylabel(
        "Promedio"
    )

    plt.xticks(
        rotation=20
    )

    plt.grid(
        axis="y"
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def main():

    conn = conectar_bd()

    crear_tabla(
        conn
    )

    opcion = 0

    while opcion != 4:

        print("\n")

        print(
            "=============================================="
        )

        print(
            "       SISTEMA DE ANALITICA ACADEMICA"
        )

        print(
            "=============================================="
        )

        print(
            "1. Ingresar datos del estudiante"
        )

        print(
            "2. Historial de datos"
        )

        print(
            "3. Dashboard de graficas"
        )

        print(
            "4. Salir"
        )

        print(
            "=============================================="
        )

        entrada = input(
            "Seleccione una opcion: "
        ).strip()

        try:

            opcion = int(
                entrada
            )

        except ValueError:

            print(
                "ERROR: Seleccione una opcion entre 1 y 4."
            )

            opcion = 0

            continue

        if opcion < 1 or opcion > 4:

            print(
                "ERROR: Seleccione una opcion entre 1 y 4."
            )

            opcion = 0

            continue

        if opcion == 1:

            ingresar_datos(
                conn
            )

        elif opcion == 2:

            mostrar_historial()

        elif opcion == 3:

            generar_dashboard()

        elif opcion == 4:

            print("\n")

            print(
                "=============================================="
            )

            print(
                "Programa finalizado."
            )

            print(
                "Gracias por utilizar el Sistema de Analitica Academica."
            )

            print(
                "=============================================="
            )

    if conn is not None:

        conn.close()


# ============================================================
# EJECUTAR PROGRAMA
# ============================================================

if __name__ == "__main__":

    main()