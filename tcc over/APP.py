
from flask import Flask, request, redirect, session
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = "clave_sistema_negocio"

# Crear la base de datos y sus tablas
def conectar():
    db = sqlite3.connect("negocio.db")
    db.row_factory = sqlite3.Row
    return db

with conectar() as db:
    db.execute("""CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        documento TEXT UNIQUE NOT NULL
    )""")

    db.execute("""CREATE TABLE IF NOT EXISTS prestamos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        monto REAL,
        total REAL,
        saldo REAL,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )""")

    db.execute("""CREATE TABLE IF NOT EXISTS pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prestamo_id INTEGER,
        monto REAL
    )""")

    db.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        correo TEXT PRIMARY KEY,
        clave TEXT NOT NULL
    )""")

    db.execute(
    """
    INSERT OR IGNORE INTO usuarios (correo, clave)
    VALUES (?, ?)
    """,
    ("admin@negocio.com", "1234")
)
    
    
    


# Proteger las páginas internas
def requiere_login(funcion):
    @wraps(funcion)
    def revisar(*args, **kwargs):
        if not session.get("usuario"):
            return redirect("/login")
        return funcion(*args, **kwargs)
    return revisar


# Página de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        clave = request.form["clave"]

        with conectar() as db:
            usuario = db.execute(
                "SELECT * FROM usuarios WHERE correo=? AND clave=?",
                (correo, clave)
            ).fetchone()

        if usuario:
            session["usuario"] = correo
            return redirect("/")

        return "Correo o contraseña incorrectos. <a href='/login'>Volver</a>"

    return """
    <h1>Iniciar sesión</h1>
    <form method="post">
        Correo: <input name="correo" type="email" required><br><br>
        Clave: <input name="clave" type="password" required><br><br>
        <button>Ingresar</button>
    </form>
    <p>Usuario: admin@negocio.com</p>
    <p>Clave: 1234</p>
    """


# Menú principal
@app.route("/")
@requiere_login
def inicio():
    return """
    <h1>Sistema de pequeños negocios</h1>
    <a href="/clientes">Registrar clientes</a><br><br>
    <a href="/prestamos">Registrar préstamos</a><br><br>
    <a href="/logout">Cerrar sesión</a>
    """


# Registrar y consultar clientes
@app.route("/clientes", methods=["GET", "POST"])
@requiere_login
def clientes():
    mensaje = ""

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        documento = request.form["documento"].strip()

        if not nombre or not documento:
            mensaje = "Completa todos los campos."
        else:
            try:
                with conectar() as db:
                    db.execute(
                        "INSERT INTO clientes (nombre, documento) VALUES (?, ?)",
                        (nombre, documento)
                    )
                mensaje = "Cliente registrado correctamente."
            except sqlite3.IntegrityError:
                mensaje = "Ese documento ya está registrado."

    with conectar() as db:
        lista = db.execute("SELECT * FROM clientes").fetchall()

    resultado = "".join(
        f"<li>{c['nombre']} - Documento: {c['documento']}</li>"
        for c in lista
    )

    return f"""
    <h1>Clientes</h1>
    <p>{mensaje}</p>
    <form method="post">
        Nombre: <input name="nombre" required><br><br>
        Documento: <input name="documento" required><br><br>
        <button>Guardar cliente</button>
    </form>
    <h2>Clientes registrados</h2>
    <ul>{resultado}</ul>
    <a href="/">Volver al menú</a>
    """


# Registrar préstamos y calcular el total
@app.route("/prestamos", methods=["GET", "POST"])
@requiere_login
def prestamos():
    mensaje = ""

    if request.method == "POST":
        try:
            cliente_id = int(request.form["cliente_id"])
            monto = float(request.form["monto"])
            tasa = float(request.form["tasa"])
            meses = int(request.form["meses"])

            if monto <= 0 or tasa < 0 or meses <= 0:
                raise ValueError

            if monto > 1_000_000_000 or tasa > 100 or meses > 600:
                raise ValueError

            with conectar() as db:
                cliente = db.execute(
                    "SELECT id FROM clientes WHERE id=?",
                    (cliente_id,)
                ).fetchone()

                if not cliente:
                    mensaje = "El cliente no existe."
                else:
                    interes = tasa / 100

                    if interes == 0:
                        cuota = monto / meses
                    else:
                        cuota = monto * interes / (
                            1 - (1 + interes) ** (-meses)
                        )

                    total = round(cuota, 2) * meses

                    db.execute(
                        """INSERT INTO prestamos
                        (cliente_id, monto, total, saldo)
                        VALUES (?, ?, ?, ?)""",
                        (cliente_id, monto, total, total)
                    )

                    mensaje = (
                        f"Préstamo registrado. Cuota aproximada: "
                        f"${cuota:,.2f}. Total: ${total:,.2f}"
                    )

        except (ValueError, TypeError):
            mensaje = "Revisa los datos ingresados."

    with conectar() as db:
        clientes_lista = db.execute(
            "SELECT * FROM clientes"
        ).fetchall()

        prestamos_lista = db.execute("""
            SELECT prestamos.*, clientes.nombre
            FROM prestamos
            JOIN clientes ON clientes.id = prestamos.cliente_id
        """).fetchall()

    opciones = "".join(
        f"<option value='{c['id']}'>{c['nombre']}</option>"
        for c in clientes_lista
    )

    filas = "".join(
        f"""<li>{p['nombre']} - Monto: ${p['monto']:,.2f}
        - Saldo: ${p['saldo']:,.2f}
        - <a href="/pago/{p['id']}">Registrar pago</a></li>"""
        for p in prestamos_lista
    )

    return f"""
    <h1>Préstamos</h1>
    <p>{mensaje}</p>
    <form method="post">
        Cliente:
        <select name="cliente_id" required>{opciones}</select><br><br>
        Monto: <input name="monto" type="number" min="1" step="0.01" required><br><br>
        Interés mensual (%): <input name="tasa" type="number" min="0" step="0.01" value="2" required><br><br>
        Plazo en meses: <input name="meses" type="number" min="1" required><br><br>
        <button>Calcular y guardar</button>
    </form>
    <h2>Préstamos registrados</h2>
    <ul>{filas}</ul>
    <a href="/">Volver al menú</a>
    """


# Registrar pagos y actualizar el saldo
@app.route("/pago/<int:id>", methods=["GET", "POST"])
@requiere_login
def pago(id):
    mensaje = ""

    with conectar() as db:
        prestamo = db.execute(
            "SELECT * FROM prestamos WHERE id=?", (id,)
        ).fetchone()

    if prestamo is None:
        return "Préstamo no encontrado. <a href='/prestamos'>Volver</a>"

    if request.method == "POST":
        try:
            monto = round(float(request.form["monto"]), 2)

            if monto <= 0 or monto > prestamo["saldo"] + 0.005:
                mensaje = "El pago no es válido o supera el saldo."
            else:
                saldo = max(round(prestamo["saldo"] - monto, 2), 0)

                with conectar() as db:
                    db.execute(
                        "INSERT INTO pagos (prestamo_id, monto) VALUES (?, ?)",
                        (id, monto)
                    )
                    db.execute(
                        "UPDATE prestamos SET saldo=? WHERE id=?",
                        (saldo, id)
                    )

                mensaje = f"Pago guardado. Saldo pendiente: ${saldo:,.2f}"

        except ValueError:
            mensaje = "Escribe un valor numérico válido."

    with conectar() as db:
        pagos = db.execute(
            "SELECT * FROM pagos WHERE prestamo_id=?", (id,)
        ).fetchall()

        prestamo = db.execute(
            "SELECT * FROM prestamos WHERE id=?", (id,)
        ).fetchone()

    historial = "".join(
        f"<li>Pago de ${p['monto']:,.2f}</li>" for p in pagos
    )

    return f"""
    <h1>Registrar pago</h1>
    <p>Saldo actual: ${prestamo['saldo']:,.2f}</p>
    <p>{mensaje}</p>
    <form method="post">
        Valor del pago:
        <input name="monto" type="number" min="0.01" step="0.01" required>
        <button>Guardar pago</button>
    </form>
    <h2>Historial de pagos</h2>
    <ul>{historial}</ul>
    <a href="/prestamos">Volver a préstamos</a>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
