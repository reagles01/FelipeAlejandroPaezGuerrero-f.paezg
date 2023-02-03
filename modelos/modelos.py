from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum


db = SQLAlchemy()



class Modalidad1(enum.Enum):
   VIR = 1
   PRES = 2
   
class Categoria1(enum.Enum):
   CONF = 1
   SEM = 2
   CONG = 3
   CON = 4

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Nomevento = db.Column(db.String(128))
    Lugar = db.Column(db.String(128))
    Direccion = db.Column(db.String(128))
    TipoModalidad = db.Column(db.Enum(Modalidad1))
    TipoCategoria = db.Column(db.Enum(Categoria1))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    UsrEventos = db.relationship('Evento', cascade='all, delete, delete-orphan')

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class EventoSchema(SQLAlchemyAutoSchema):
    TipoModalidad = EnumADiccionario(attribute=("TipoModalidad"))
    TipoCategoria = EnumADiccionario(attribute=("TipoCategoria"))
    class Meta:
         model = Evento
         include_relationships = True
         load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True
