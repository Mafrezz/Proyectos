import psycopg2

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mafer123",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# INSERT
cursor.execute("""
INSERT INTO redes (nombre, carnet)
VALUES ('Carlos López', 202045678);
""")
conn.commit()

print("=== Después del INSERT ===")
cursor.execute("SELECT * FROM redes;")
for fila in cursor.fetchall():
    print(fila)

# UPDATE
cursor.execute("""
UPDATE redes
SET nombre = 'Carlos Alberto López'
WHERE carnet = 202045678;
""")
conn.commit()

print("\n=== Después del UPDATE ===")
cursor.execute("SELECT * FROM redes;")
for fila in cursor.fetchall():
    print(fila)

# DELETE
cursor.execute("""
DELETE FROM redes
WHERE carnet = 20201537;
""")
conn.commit()

print("\n=== Después del DELETE ===")
cursor.execute("SELECT * FROM redes;")
for fila in cursor.fetchall():
    print(fila)

# Cerrar conexión
cursor.close()
conn.close()