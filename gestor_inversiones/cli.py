import argparse
from .crud import registrar_compra, consultar_registros, borrar_transaccion

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

    # Subcomando: consulta
    parser_consulta = subparsers.add_parser('consulta', help='Consultar registros.')

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

    elif args.comando == 'consulta':
        df = consultar_registros()
        if len(df) > 0:
            print("\nRegistros encontrados:")
            print(df.to_string(index=False))
        else:
            print("No hay registros en la base de datos.")

    elif args.comando == 'borrar':
        if borrar_transaccion(args.id):
            print(f"✅ Transacción {args.id} eliminada exitosamente")
        else:
            print(f"❌ No se encontró la transacción {args.id}")

if __name__ == "__main__":
    main()
