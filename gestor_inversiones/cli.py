import argparse
from .crud import registrar_compra, consultar_registros, borrar_transaccion, actualizar_transaccion

def main():
    parser = argparse.ArgumentParser(
        description="Gestor de inversiones doméstico (CRYPTO/ETF) con SQLite.",
        epilog="Ejecuta 'python -m gestor_inversiones <comando> -h' para ayuda específica."
    )
    subparsers = parser.add_subparsers(dest='comando', required=True)

    # Subcomando: registro
    parser_registro = subparsers.add_parser('registro', help='Registrar una nueva compra.')
    parser_registro.add_argument('--activo', required=True)
    parser_registro.add_argument('--tipo', required=True, choices=['CRYPTO', 'ETF'])
    parser_registro.add_argument('--cantidad', required=True, type=float)
    parser_registro.add_argument('--precio', dest='precio_unitario', required=True, type=float)
    parser_registro.add_argument('--costo', dest='costo_total', required=True, type=float)
    parser_registro.add_argument('--dolar', dest='dolar_cambio', required=True, type=float)
    parser_registro.add_argument('--fecha', dest='fecha', required=False,
                                 help="Fecha de la transacción (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS). Si se omite, se usa la fecha actual.)")

    # Subcomando: actualizar
    parser_actualizar = subparsers.add_parser('actualizar', help='Actualizar una transacción existente.')
    parser_actualizar.add_argument('--id', required=True, type=int, help='ID de la transacción a actualizar.')
    parser_actualizar.add_argument('--activo', required=False, help='Nuevo nombre del activo.')
    parser_actualizar.add_argument('--tipo', required=False, choices=['CRYPTO', 'ETF'], help='Nuevo tipo de activo.')
    parser_actualizar.add_argument('--cantidad', required=False, type=float, help='Nueva cantidad.')
    parser_actualizar.add_argument('--precio', dest='precio_unitario', required=False, type=float, help='Nuevo precio unitario.')
    parser_actualizar.add_argument('--costo', dest='costo_total', required=False, type=float, help='Nuevo costo total.')
    parser_actualizar.add_argument('--dolar', dest='dolar_cambio', required=False, type=float, help='Nuevo tipo de cambio del dólar.')
    parser_actualizar.add_argument('--fecha', dest='fecha', required=False, help='Nueva fecha (formato ISO: YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS).')

    # Subcomando: consulta
    parser_consulta = subparsers.add_parser('consulta', help='Consultar registros con filtros opcionales.')
    parser_consulta.add_argument('--activo', required=False, help='Filtrar por nombre de activo (ej: BTC, ETH).')
    parser_consulta.add_argument('--tipo', required=False, choices=['CRYPTO', 'ETF'], help='Filtrar por tipo de activo.')
    parser_consulta.add_argument('--desde', dest='fecha_desde', required=False, help='Filtrar desde una fecha (formato: YYYY-MM-DD).')
    parser_consulta.add_argument('--hasta', dest='fecha_hasta', required=False, help='Filtrar hasta una fecha (formato: YYYY-MM-DD).')

    # Subcomando: borrar
    parser_borrar = subparsers.add_parser('borrar', help='Borrar una transacción.')
    parser_borrar.add_argument('--id', required=True, type=int)

    args = parser.parse_args()

    if args.comando == 'registro':
        # Pasar la fecha tal cual; `crud.registrar_compra` acepta string o datetime
        registrar_compra(
            args.activo,
            args.tipo,
            args.cantidad,
            args.precio_unitario,
            args.costo_total,
            args.dolar_cambio,
            fecha=args.fecha
        )
        print("✅ Compra registrada exitosamente")

    elif args.comando == 'actualizar':
        # Recopilar solo los argumentos que fueron proporcionados
        campos_a_actualizar = {}
        if args.activo is not None:
            campos_a_actualizar['activo'] = args.activo
        if args.tipo is not None:
            campos_a_actualizar['tipo'] = args.tipo
        if args.cantidad is not None:
            campos_a_actualizar['cantidad'] = args.cantidad
        if args.precio_unitario is not None:
            campos_a_actualizar['precio_unitario'] = args.precio_unitario
        if args.costo_total is not None:
            campos_a_actualizar['costo_total'] = args.costo_total
        if args.dolar_cambio is not None:
            campos_a_actualizar['dolar_cambio'] = args.dolar_cambio
        if args.fecha is not None:
            campos_a_actualizar['fecha'] = args.fecha

        if not campos_a_actualizar:
            print("❌ Debes especificar al menos un campo a actualizar.")
            return

        if actualizar_transaccion(args.id, **campos_a_actualizar):
            print(f"✅ Transacción {args.id} actualizada exitosamente")
        else:
            print(f"❌ No se encontró la transacción {args.id}")

    elif args.comando == 'consulta':
        # Pasar los filtros a la función de consulta
        df = consultar_registros(
            activo=args.activo,
            tipo=args.tipo,
            fecha_desde=args.fecha_desde,
            fecha_hasta=args.fecha_hasta
        )
        
        if len(df) > 0:
            print("\nRegistros encontrados:")
            print(df.to_string(index=False))
        else:
            print("No hay registros que coincidan con los filtros especificados.")

    elif args.comando == 'borrar':
        if borrar_transaccion(args.id):
            print(f"✅ Transacción {args.id} eliminada exitosamente")
        else:
            print(f"❌ No se encontró la transacción {args.id}")

if __name__ == "__main__":
    main()
