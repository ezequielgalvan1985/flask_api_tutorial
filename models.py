from sqlalchemy import Column, Integer, String, Float

from db import db, BaseModelMixin,Mapped, mapped_column


#Modelos
class User(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password = db.Column(db.String(80))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'User({self.username} {self.email})'

    def __str__(self):
        return f'{self.username} {self.email}'

class Categoria(db.Model, BaseModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    descripcion: Mapped[str]

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f'Categoria ({self.nombre} {self.descripcion})'

    def __str__(self):
        return f'{self.nombre} {self.nombre}'


class Producto(db.Model, BaseModelMixin):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship("Categoria", backref=db.backref("productos", uselist=False))
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    precio = Column(Float)

    def __init__(self, nombre, descripcion,precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio


    def __repr__(self):
        return f'Producto({self.nombre}, {self.precio})'

    def __str__(self):
        return self.nombre