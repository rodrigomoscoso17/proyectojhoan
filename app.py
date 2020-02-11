from flask import Flask, render_template, flash, redirect, \
    url_for, session, request, logging
# Libreria que se conecta con MYSQL
from flask_mysqldb import MySQL
# Controles para el uso de formularios en Flask
from wtforms import Form, StringField, TextAreaField, \
    PasswordField, validators
# Libreria que me permite encriptar password
from passlib.hash import sha256_crypt
# salto de lineas en los formularios
from functools import wraps
from formularios import *

app = Flask(__name__)
app.debug = True
# Cadena de Conexion a Mi Bd
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'perritos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Inicializando MYSQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/paseadores')
def paseadores():
    return render_template('paseadores.html')


@app.route('/clientes')
def clientes():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM cliente")
    clientes = cur.fetchall()
    if result > 0:
        return render_template("clientes.html", clie=clientes)
    else:
        msg = "no hay clientes en la base de datos"
        return render_template("clientes.html", msg=msg)
    cur.close()


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrarUsuario(request.form)  # Herencia POO
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        apellido = form.apellido.data
        usuario = form.usuario.data
        correo = form.correo.data
        telefono = form.telefono.data
        contrasena = sha256_crypt.encrypt(str(form.contrasena.data))
        comentarios = form.comentarios.data
        # Grabarlo en la BD
        # crear un cursor
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usuario_cliente(nombre, apellido, usuario , correo, contrasena, telefono, descripcion)values(%s,%s,%s,%s,%s,%s,%s)",
            (nombre, apellido, usuario, correo, contrasena, telefono, comentarios))
        mysql.connection.commit()
        cur.close()
        flash("Registro Grabado con exito")
        redirect(url_for("login"))
    return render_template("registrar.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        pass_cand = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM usuario_cliente WHERE usuario = %s", [usuario])
        if result > 0:
            data = cur.fetchone()
            contrasena = data['contrasena']
            # comparar los passwords
            if sha256_crypt.verify(pass_cand, contrasena):
                session['logged_in'] = True
                session['username'] = usuario
                flash("Usuario Correcto", "success")
                return redirect(url_for('dashboard'))
            else:
                error = "Clave Errada"
                return render_template("login.html", error=error)
            cur.close()
        else:
            error = "Usuario No existe"
            return render_template("login.html", error=error)
    return render_template("login.html")


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Sin Autroizacion")
            return redirect(url_for('login'))

    return wrap


@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Session cerrada")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'secret123'

app.run(debug=True, port=5000)
