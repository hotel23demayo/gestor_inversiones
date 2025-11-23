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

def consultar_registros(activo=None, tipo=None, fecha_desde=None, fecha_hasta=None):
    """Consulta registros de transacciones con filtros opcionales.
    
    Parámetros:
    - activo: filtrar por nombre de activo (ej: "BTC", "ETH")
    - tipo: filtrar por tipo (ej: "CRYPTO", "ETF")
    - fecha_desde: filtrar transacciones desde una fecha (formato ISO: YYYY-MM-DD)
    - fecha_hasta: filtrar transacciones hasta una fecha (formato ISO: YYYY-MM-DD)
    
    Retorna:
    - DataFrame con los registros que coinciden con los filtros
    """
    conn = get_db_connection()
    
    query = "SELECT * FROM transacciones WHERE 1=1"
    params = []
    
    # Agregar filtros dinámicamente
    if activo:
        query += " AND LOWER(activo) = LOWER(?)"
        params.append(activo)
    
    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)
    
    if fecha_desde:
        query += " AND DATE(fecha) >= ?"
        params.append(fecha_desde)
    
    if fecha_hasta:
        query += " AND DATE(fecha) <= ?"
        params.append(fecha_hasta)
    
    query += " ORDER BY fecha DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def actualizar_transaccion(id_transaccion, **kwargs):
    """Actualiza uno o más campos de una transacción existente.
    
    Parámetros:
    - id_transaccion: ID del registro a actualizar
    - **kwargs: pares campo=valor a actualizar (activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio, fecha)
    
    Retorna:
    - True si se actualizó exitosamente
    - False si el registro no existe
    """
    if not kwargs:
        return False
    
    # Validar que los campos sean válidos
    campos_validos = {'activo', 'tipo', 'cantidad', 'precio_unitario', 'costo_total', 'dolar_cambio', 'fecha'}
    campos = set(kwargs.keys())
    
    campos_invalidos = campos - campos_validos
    if campos_invalidos:
        raise ValueError(f"Campos no válidos: {campos_invalidos}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Construir dinámicamente la sentencia UPDATE
    set_clause = ", ".join([f"{campo} = ?" for campo in kwargs.keys()])
    values = list(kwargs.values())
    values.append(id_transaccion)
    
    query = f"UPDATE transacciones SET {set_clause} WHERE id = ?"
    cursor.execute(query, values)
    actualizado = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    return actualizado

def borrar_transaccion(id_transaccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM transacciones WHERE id = ?", (id_transaccion,))
    eliminado = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    return eliminado
