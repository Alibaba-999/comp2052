from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Carga un usuario desde su ID, necesario para el sistema de sesiones de Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de libro personal asociado a un usuario (propietario)
class Libro(db.Model):
    __tablename__ = 'libro'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    anio_publicacion = db.Column(db.Integer, nullable=True)
    genero = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    notas = db.Column(db.Text, nullable=True)
    etiquetas = db.Column(db.String(255), nullable=True)
    propietario_id = db.Column(db.Integer, db.ForeinKey('user.id'), nullable=False)


# Modelo de usuarios del sistema
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Asegura suficiente espacio para el hash
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relación con cursos (si es profesor)
    libros = db.relationship('Libros', backref='propietario', lazy=True)

    def set_password(self, password: str):
        """
        Genera y guarda el hash de la contraseña.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña ingresada es válida comparando con el hash.
        """
        return check_password_hash(self.password_hash, password)
