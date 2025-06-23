
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models.db import db
from models.usuario import Usuario
from models.paciente import Paciente
from models.especialidad import Especialidad
from models.medico import Medico
from models.cita import Cita
from models.historial import Historial
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def login_required(roles=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if "usuario" not in session:
                flash("Inicia sesión para continuar.")
                return redirect(url_for("index"))
            if roles and session.get("rol") not in roles:
                flash("No tienes permiso para acceder a esta sección.")
                return redirect(url_for("index"))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/home")
def home():
    if "rol" not in session:
        return redirect(url_for("index"))

    rol = session["rol"]
    if rol == "admin":
        return redirect(url_for("dashboard_admin"))
    elif rol == "medico":
        return redirect(url_for("dashboard_medico"))
    elif rol == "recepcionista":
        return redirect(url_for("dashboard_recepcionista"))
    else:
        return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login(): 
    usuario = request.form["usuario"]
    password = request.form["password"]
    user = Usuario.query.filter_by(nombre_usuario=usuario, password=password).first()
    if user:
        session["usuario"] = user.nombre_usuario
        session["rol"] = user.rol
        session["medico_id"] = user.id_usuario if user.rol == "medico" else None
        if user.rol == "admin":
            return redirect(url_for("dashboard_admin"))
        if user.rol == "medico":
            medico = Medico.query.filter_by(nombre=user.nombre_usuario).first()
            session["medico_id"] = medico.id_medico if medico else None
            return redirect(url_for("dashboard_medico"))
        elif user.rol == "recepcionista":
            return redirect(url_for("dashboard_recepcionista"))
    flash("Credenciales incorrectas.")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ADMIN
@app.route("/admin/dashboard")
@login_required(["admin"])
def dashboard_admin():
    return render_template("admin/dashboard.html")

@app.route("/admin/usuarios")
@login_required(["admin"])
def admin_usuarios():
    usuarios = Usuario.query.all()
    return render_template("admin/admin_usuarios.html", usuarios=usuarios)

@app.route("/admin/nuevo_usuario", methods=["GET", "POST"])
@login_required(["admin"])
def nuevo_usuario():
    if request.method == "POST":
        nuevo = Usuario(
            nombre_usuario=request.form["usuario"],
            password=request.form["password"],
            rol=request.form["rol"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("admin_usuarios"))
    return render_template("admin/nuevo_usuario.html")

@app.route("/admin/editar_usuario/<int:id>", methods=["GET", "POST"])
@login_required(["admin"])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        usuario.nombre_usuario = request.form["usuario"]
        usuario.password = request.form["password"]
        usuario.rol = request.form["rol"]
        db.session.commit()
        return redirect(url_for("admin_usuarios"))
    return render_template("admin/editar_usuario.html", usuario=usuario)

@app.route("/admin/medicos")
@login_required(["admin"])
def admin_medicos():
    medicos = Medico.query.all()
    return render_template("admin/admin_medicos.html", medicos=medicos)

@app.route("/admin/nuevo_medico", methods=["GET", "POST"])
@login_required(["admin"])
def nuevo_medico():
    especialidades = Especialidad.query.all()
    if request.method == "POST":
        nuevo = Medico(
            nombre=request.form["nombre"],
            especialidad_id=request.form["especialidad"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("admin_medicos"))
    return render_template("admin/nuevo_medico.html", especialidades=especialidades)

@app.route("/admin/editar_medico/<int:id>", methods=["GET", "POST"])
@login_required(["admin"])
def editar_medico(id):
    medico = Medico.query.get_or_404(id)
    especialidades = Especialidad.query.all()
    if request.method == "POST":
        medico.nombre = request.form["nombre"]
        medico.especialidad_id = request.form["especialidad"]
        db.session.commit()
        return redirect(url_for("admin_medicos"))
    return render_template("admin/editar_medico.html", medico=medico, especialidades=especialidades)

@app.route("/admin/especialidades")
@login_required(["admin"])
def admin_especialidades():
    especialidades = Especialidad.query.all()
    return render_template("admin/admin_especialidades.html", especialidades=especialidades)

@app.route("/admin/nueva_especialidad", methods=["GET", "POST"])
@login_required(["admin"])
def nueva_especialidad():
    if request.method == "POST":
        nueva = Especialidad(nombre=request.form["nombre"])
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for("admin_especialidades"))
    return render_template("admin/nueva_especialidad.html")

@app.route("/admin/editar_especialidad/<int:id>", methods=["GET", "POST"])
@login_required(["admin"])
def editar_especialidad(id):
    especialidad = Especialidad.query.get_or_404(id)
    if request.method == "POST":
        especialidad.nombre = request.form["nombre"]
        db.session.commit()
        return redirect(url_for("admin_especialidades"))
    return render_template("admin/editar_especialidad.html", especialidad=especialidad)

@app.route("/admin/eliminar_especialidad/<int:id>")
@login_required(["admin"])
def eliminar_especialidad(id):
    especialidad = Especialidad.query.get_or_404(id)
    db.session.delete(especialidad)
    db.session.commit()
    return redirect(url_for("admin_especialidades"))

# MEDICO
@app.route("/medico/dashboard")
@login_required(["medico"])
def dashboard_medico():
    return render_template("medico/dashboard.html")

@app.route("/medico/pacientes")
@login_required(["medico"])
def ver_pacientes():
    pacientes = Paciente.query.all()
    return render_template("medico/ver_pacientes.html", pacientes=pacientes)

@app.route("/medico/nuevo_paciente", methods=["GET", "POST"])
@login_required(["medico"])
def nuevo_paciente():
    if request.method == "POST":
        nuevo = Paciente(
            nombre=request.form["nombre"],
            fecha_nacimiento=request.form["fecha_nacimiento"],
            genero=request.form["genero"],
            telefono=request.form["telefono"],
            direccion=request.form["direccion"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("ver_pacientes"))
    return render_template("medico/nuevo_paciente.html")

@app.route("/medico/historiales")
@login_required(["medico"])
def ver_historiales():
    historiales = Historial.query.all()
    return render_template("medico/ver_historiales.html", historiales=historiales)

@app.route("/medico/nuevo_historial", methods=["GET", "POST"])
@login_required(["medico"])
def nuevo_historial():
    pacientes = Paciente.query.all()
    if request.method == "POST":
        nuevo = Historial(
            paciente_id=request.form["paciente"],
            medico_id=session["medico_id"],
            fecha=datetime.strptime(request.form["fecha"], "%Y-%m-%d"),
            descripcion=request.form["descripcion"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("ver_historiales"))
    return render_template("medico/nuevo_historial.html", pacientes=pacientes)

# RECEPCIONISTA
@app.route("/recepcionista/dashboard")
@login_required(["recepcionista"])
def dashboard_recepcionista():
    return render_template("recepcionista/dashboard.html")

@app.route("/recepcionista/pacientes")
@login_required(["recepcionista"])
def recepcionista_pacientes():
    pacientes = Paciente.query.all()
    return render_template("recepcionista/pacientes.html", pacientes=pacientes)

@app.route("/recepcionista/nuevo_paciente", methods=["GET", "POST"])
@login_required(["recepcionista"])
def recepcionista_nuevo_paciente():
    if request.method == "POST":
        nuevo = Paciente(
            nombre=request.form["nombre"],
            fecha_nacimiento=request.form["fecha_nacimiento"],
            genero=request.form["genero"],
            telefono=request.form["telefono"],
            direccion=request.form["direccion"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("recepcionista_pacientes"))
    return render_template("recepcionista/nuevo_paciente.html")

@app.route("/recepcionista/citas")
@login_required(["recepcionista"])
def recepcionista_citas():
    citas = Cita.query.all()
    return render_template("recepcionista/citas.html", citas=citas)


@app.route("/medico/citas")
@login_required(["medico"])
def medico_citas():
    citas = Cita.query.all()
    return render_template("medico/citas.html", citas=citas)


@app.route("/recepcionista/nueva_cita", methods=["GET", "POST"])
@login_required(["recepcionista"])
def nueva_cita():
    pacientes = Paciente.query.all()
    medicos = Medico.query.all()
    if request.method == "POST":
        nueva = Cita(
            paciente_id=request.form["paciente_id"],
            medico_id=request.form["medico_id"],
            fecha_hora=datetime.strptime(request.form["fecha_hora"], "%Y-%m-%dT%H:%M"),
            estado=request.form["estado"]
        )
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for("recepcionista_citas"))
    return render_template("recepcionista/nueva_cita.html", pacientes=pacientes, medicos=medicos)

 


if __name__ == "__main__":
    app.secret_key = "supersecreto"
    app.run(debug=True)
