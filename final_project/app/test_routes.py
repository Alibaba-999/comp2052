from flask import Blueprint, request, jsonify
from app.models import db, Libro

# Blueprint solo con endpoints de prueba para cursos
main = Blueprint('main', __name__)

@main.route('/') # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/libros', methods=['GET'])
def listar_libros():
    """
    Retorna una lista de libros (JSON).
    """
    libros = Libro.query.all()

    data = [
        {'id': libro.id,
        'titulo' : libro.titulo,
        'autor' : libro.autor,
        'anio_publicacion' : libro.anio_publicacion,
        'genero' : libro.genero,
        'url' : libro.url,
        'notas' : libro.notas,
        'etiquetas' : libro.etiquetas,
        'propietario_id' : libro.propietario_id
        }
        for libro in libros
    ]
    return jsonify(data), 200


@main.route('/libros/<int:id>', methods=['GET'])
def listar_un_libro(id):
    """
    Retorna un solo libros por su ID (JSON).
    """
    libros = Libro.query.get_or_404(id)

    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'autor': libro.autor,
        'genero': libro.genero,
        'anio_publicacion': libro.anio_publicacion,
        'url': libro.url,
        'notas': libro.notas,
        'etiquetas': libro.etiquetas,
        'propietario_id': libro.propietario_id
    }

    return jsonify(data), 200


@main.route('/libros', methods=['POST'])
def crear_libro():
    """
    Crea un libro sin validación.
    Espera JSON con los campos de libro.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    libro = Libro(
        titulo=data.get('titulo'),
        autor=data.get('autor'),
        genero=data.get('genero'),
        anio_publicacion=data.get('anio_publicacion'),
        url=data.get('url'),
        notas=data.get('notas'),
        etiquetas=data.get('etiquetas'),
        propietario_id=data.get('propietario_id')  # sin validación de usuario
    )

    db.session.add(libro)
    db.session.commit()

    return jsonify({'message': 'Libro creado', 'id': libro.id, 'propietario_id': libro.propietario_id}), 201

@main.route('/libros/<int:id>', methods=['PUT'])
def actualizar_libro(id):
    """
    Actualiza un libro sin validación de usuario o permisos.
    """
    libro = Libro.query.get_or_404(id)
    data = request.get_json()

    libro.titulo = data.get('titulo', libro.titulo)
    libro.autor = data.get('autor', libro.autor)
    libro.genero = data.get('genero', libro.genero)
    libro.anio_publicacion = data.get('anio_publicacion', libro.anio_publicacion)
    libro.url = data.get('url', libro.url)
    libro.notas = data.get('notas', libro.notas)
    libro.etiquetas = data.get('etiquetas', libro.etiquetas)
    libro.propietario_id = data.get('propietario_id', libro.propietario_id)

    db.session.commit()

    return jsonify({'message': 'Libro actualizado', 'id': libro.id}), 200

@main.route('/libros/<int:id>', methods=['DELETE'])
def eliminar_libro(id):
    """
    Elimina un libro sin validación de permisos.
    """
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()

    return jsonify({'message': 'Libro eliminado', 'id': libro.id}), 200
