# 💼 Gestor de Inversiones Doméstico

Una herramienta en Python para registrar, consultar y gestionar inversiones personales (CRYPTO y ETFs) usando SQLite. Diseñada para uso local en Linux, permitiéndote mantener un registro detallado de tus inversiones con su costo en dólares y moneda local.

## 🎯 Propósito

Este proyecto nace de la necesidad de mantener un registro claro y organizado de inversiones personales, especialmente útil para:

- 📊 Seguimiento de inversiones en múltiples activos (CRYPTO/ETFs)
- 💵 Control de costos y tipo de cambio al momento de la compra
- 📈 Análisis histórico de transacciones
- 🧮 Base para cálculos impositivos y rendimientos

## 🚀 Características

- ✨ Registro de compras con:
  - Tipo de activo (CRYPTO/ETF)
  - Cantidad y precio unitario
  - Costo total (incluyendo comisiones)
  - Tipo de cambio del dólar al momento de la compra
- 📋 Consulta de transacciones con formato tabular
- 🗑️ Gestión de registros (borrado de transacciones)
- 🔒 Almacenamiento local en SQLite
- 💻 Interfaz de línea de comandos intuitiva

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/gestor_inversiones.git
cd gestor_inversiones
```

2. Crea y activa un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
.\\venv\\Scripts\\activate  # En Windows
```

3. Instala el paquete en modo desarrollo:
```bash
pip install -e .
```

## 🎮 Uso

### Registrar una nueva compra:
```bash
python -m gestor_inversiones registro \
    --activo BTC \
    --tipo CRYPTO \
    --cantidad 0.1 \
    --precio 35000 \
    --costo 3500 \
  --dolar 1000

# Si quieres registrar la transacción con una fecha diferente (por ejemplo, para movimientos atrasados
# al aplicar DCA), usa la opción `--fecha` con formato ISO (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS):
python -m gestor_inversiones registro \
  --activo BTC --tipo CRYPTO --cantidad 0.05 --precio 30000 --costo 1500 --dolar 1000 \
  --fecha 2025-11-01
```

### Consultar todas las transacciones:
```bash
python -m gestor_inversiones consulta
```

### Borrar una transacción:
```bash
python -m gestor_inversiones borrar --id 1
```

## 🧱 Estructura del Proyecto

```
gestor_inversiones/
├── gestor_inversiones/
│   ├── __init__.py
│   ├── __main__.py       # Punto de entrada como módulo
│   ├── db.py            # Gestión de base de datos SQLite
│   ├── crud.py          # Operaciones CRUD
│   ├── utils.py         # Utilidades y validaciones
│   └── cli.py           # Interface de línea de comandos
├── data/                # Almacenamiento de la base de datos
│   └── .gitkeep
├── tests/              # Pruebas unitarias
│   ├── __init__.py
│   └── test_crud.py
├── setup.py           # Configuración del paquete
└── requirements.txt   # Dependencias del proyecto
```

## 📝 Próximas Características

- [ ] Exportación a CSV para análisis en Excel
- [ ] Cálculo de rendimientos y ganancias/pérdidas
- [ ] Filtros por fecha y tipo de activo
- [ ] Gráficos de distribución de portfolio
- [ ] Respaldo automático de la base de datos

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## � Control de Versiones y GitHub

### Preparación Inicial del Repositorio

1. Crear un nuevo repositorio en GitHub (sin inicializar con README)

2. Configurar el `.gitignore` (ya incluido en el proyecto):
```
# Base de datos y archivos generados
data/*.db
__pycache__/
*.pyc

# Entorno virtual
venv/
env/

# Archivos de sistema
.DS_Store
Thumbs.db
```

3. Inicializar el repositorio local y vincularlo con GitHub:
```bash
# Inicializar repositorio Git local
git init

# Agregar todos los archivos excepto los ignorados
git add .

# Primer commit
git commit -m "Inicialización del proyecto gestor_inversiones"

# Agregar el repositorio remoto (reemplaza USERNAME y REPO)
git remote add origin https://github.com/USERNAME/REPO.git

# Subir el código al repositorio remoto
git branch -M main
git push -u origin main
```

### Flujo de Trabajo Diario

1. Antes de comenzar a trabajar:
```bash
# Obtener cambios del repositorio remoto
git pull origin main
```

2. Al hacer cambios:
```bash
# Ver estado de cambios
git status

# Agregar cambios (excluyendo la base de datos automáticamente)
git add .

# Crear commit con los cambios
git commit -m "Descripción de los cambios realizados"

# Subir cambios a GitHub
git push origin main
```

### ⚠️ Consideraciones Importantes

- La carpeta `data/` está en el repositorio pero su contenido está ignorado
- La base de datos (`*.db`) no se sube a GitHub por seguridad
- Cada desarrollador tendrá su propia base de datos local
- Los archivos `__pycache__` y `.pyc` se ignoran automáticamente
- El entorno virtual (`venv/`) debe crearse localmente y no subirse

### 🔄 Respaldo de la Base de Datos

Para mantener un respaldo de tus datos:

1. Exportar datos (próxima característica):
```bash
# Próximamente
python -m gestor_inversiones exportar --formato csv
```

2. Guardar el archivo CSV en una ubicación segura

3. Para restaurar en una nueva instalación:
```bash
# Próximamente
python -m gestor_inversiones importar --archivo respaldo.csv
```

## �📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
