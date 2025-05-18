from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import LibroForm, ChangePasswordForm
from app.models import db, Libro, User

# Blueprint principal que maneja el dashboard, gestión de cursos y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')  # 🔁 Traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra los libros del usuario.
    """
    libros = Libro.query.filter_by(propietario_id=current_user.id).all()
    return render_template('dashboard.html', libros=libros)

@main.route('/libros/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_libro():
    """
    Permite crear un nuevo libro.
    """
    form = LibroForm()
    if form.validate_on_submit():
        libro = Libro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            año_publicacion=form.año_publicacion.data,
            genero=form.genero.data,
            propietario_id=current_user.id
        )
        db.session.add(libro)
        db.session.commit()
        flash("Libro agregado exitosamente.")  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))
    return render_template('libro_form.html', form=form)

@main.route('/libros/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    """
    Permite editar un libro existente si es del usuario.
    """
    libro = Libro.query.get_or_404(id)

    # Validación de permisos
    if libro.propietario_id != current_user.id:
        flash('No tienes permiso para editar este libro.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    form = LibroForm(obj=libro)

    if form.validate_on_submit():
        libro.titulo = form.titulo.data
        libro.autor = form.autor.data
        libro.año_publicacion = form.año_publicacion.data
        libro.genero = form.genero.data
        db.session.commit()
        flash("Libro actualizado exitosamente.")  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('libro_form.html', form=form, editar=True, libro=libro)

@main.route('/libros/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_libro(id):
    """
    Elimina un libro si es del usuario.
    """
    libro = Libro.query.get_or_404(id)

    if libro.propietario_id != current_user.id:
        flash('No tienes permiso para eliminar este libro.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    db.session.delete(libro)
    db.session.commit()
    flash("Libro eliminado exitosamente.")  # 🔁 Traducido
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)
