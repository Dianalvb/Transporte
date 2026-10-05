from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel

app = FastAPI()

def conectar_bd():
    return psycopg2.connect(
        host="localhost",
        database="transporte_db",
        user="postgres",
        password="postgres123"
    )

@app.get("/")
def inicio():
    return {"mensaje": "Servidor funcionando"}

@app.get("/unidades")
def obtener_unidades():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM unidades;")
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return datos

class Ubicacion(BaseModel):
    unidad_id: int
    latitud: float
    longitud: float
    velocidad: float

@app.post("/ubicaciones")
def guardar_ubicacion(ubicacion: Ubicacion):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO ubicaciones
        (unidad_id, latitud, longitud, velocidad)
        VALUES (%s, %s, %s, %s)
        """,
        (
            ubicacion.unidad_id,
            ubicacion.latitud,
            ubicacion.longitud,
            ubicacion.velocidad
        )
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return {"mensaje": "Ubicación guardada correctamente"}