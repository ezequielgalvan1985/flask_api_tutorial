from sqlalchemy import Column, Integer, String, Float

from db import db, BaseModelMixin,Mapped, mapped_column


#Modelos
class User(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password = db.Column(db.String(80))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'User({self.username} {self.email})'

    def __str__(self):
        return f'{self.username} {self.email}'

class Rol(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    descripcion: Mapped[str]

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f'Rol ({self.nombre} {self.descripcion})'

    def __str__(self):
        return f'{self.nombre} {self.nombre}'


class Permiso(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    descripcion: Mapped[str]
    recurso: Mapped[str]
    acceso: Mapped[str]

    def __repr__(self):
        return f'Rol ({self.nombre} {self.descripcion})'

    def __str__(self):
        return f'{self.nombre} {self.nombre}'

class RolPermiso(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
    permiso_id = db.Column(db.Integer, db.ForeignKey('permiso.id'))

    def __init__(self, rol_id, permiso_id):
        self.rol_id = rol_id
        self.permiso_id = permiso_id

    def __repr__(self):
        return f'Rol ({self.rol_id}) - Permiso ({self.permiso_id})'



class Categoria(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    descripcion: Mapped[str]
    rubro_id = db.Column(db.Integer, db.ForeignKey('rubro.id'))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion


    def __repr__(self):
        return f'Categoria ({self.nombre} {self.descripcion})'

    def __str__(self):
        return f'{self.nombre} {self.nombre}'


class Marca(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    descripcion: Mapped[str]
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f'Marca ({self.nombre} {self.descripcion})'

    def __str__(self):
        return f'{self.nombre} {self.nombre}'


class Rubro(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    descripcion: Mapped[str]

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f'Rubro ({self.nombre} {self.descripcion})'

    def __str__(self):
        return f'{self.nombre} {self.nombre}'


class Producto(db.Model, BaseModelMixin):
    id = Column(Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship("Categoria")
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))
    marca = db.relationship("Marca")
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    precio = Column(Float)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    empresa = db.relationship("Empresa")
    precio_oferta = Column(Float)

    def __init__(self, nombre, descripcion,precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio


    def __repr__(self):
        return f'Producto({self.nombre}, {self.precio})'

    def __str__(self):
        return self.nombre



class Empresa(db.Model, BaseModelMixin):
    id = Column(Integer, primary_key=True)
    rubro_id = db.Column(db.Integer, db.ForeignKey('rubro.id'))
    rubro = db.relationship("Rubro")
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    frase = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    usuario = db.relationship("User")
    def __init__(self, nombre, usuario_id, rubro_id ):
        self.nombre = nombre
        self.user_id = usuario_id
        self.rubro_id = rubro_id


    def __repr__(self):
        return f'Empresa({self.nombre})'

    def __str__(self):
        return self.nombre

class Publicidad(db.Model, BaseModelMixin):
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    cantidad = Column(Float, nullable=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    empresa = db.relationship("Empresa")
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship("Producto")
    precio = Column(Float, nullable=True)
    porcentaje = Column(Float, nullable=True)
    def __init__(self, titulo,descripcion, empresa_id, producto_id ):
        self.titulo = titulo
        self.descripcion = descripcion
        self.empresa_id = empresa_id
        self.producto_id = producto_id
    def __repr__(self):
        return f'Empresa({self.titulo})'

    def __str__(self):
        return self.titulo