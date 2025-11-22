from .db import get_db_connection
import pandas as pd
from datetime import datetime

def registrar_compra(activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio, fecha=None):
    """Registra una compra en la base de datos.

    Parámetros:
    - activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio: campos habituales
    - fecha: opcional. Si se indica, puede ser:
        * un objeto `datetime`
        * un string en formato ISO (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS)
      Si no se indica, la base de datos usará la fecha/hora actual.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if fecha is None:
        cursor.execute("""
            INSERT INTO transacciones 
            (activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio))
    else:
        # Normalizar fecha a string
        if hasattr(fecha, 'isoformat'):
            fecha_str = fecha.isoformat(sep=' ')
        else:
            fecha_str = str(fecha)

        cursor.execute("""
            INSERT INTO transacciones 
            (fecha, activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (fecha_str, activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio))

    conn.commit()
    conn.close()
    return True

def consultar_registros():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM transacciones", conn)
    conn.close()
    return df

def borrar_transaccion(id_transaccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM transacciones WHERE id = ?", (id_transaccion,))
    eliminado = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    return eliminado
