from flask import request
from ..modelos import db, Evento, Usuario, UsuarioSchema, EventoSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

evento_schema = EventoSchema()
usuario_schema = UsuarioSchema()


class VistaLogIn(Resource):
    def post(self):
            u_nombre = request.json["nombre"]
            u_contrasena = request.json["contrasena"]
            usuario = Usuario.query.filter_by(nombre=u_nombre, contrasena = u_contrasena).all()
            if usuario:
                return {'mensaje':'Inicio de sesión exitoso'}, 200
            else:
                return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401


class VistaSignIn(Resource):
    
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return 'Usuario creado exitosamente', 201

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

class VistaSignInDel(Resource):

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return 'Usuario eliminado',204
    
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)    

class VistaEventosUsuario(Resource):

    def post(self, id_usuario):
        nuevo_evento = Evento(Nomevento=request.json["Nomevento"],\
                                Lugar=request.json["Lugar"],\
                                Direccion=request.json["Direccion"],\
                                TipoModalidad=request.json["TipoModalidad"],\
                                TipoCategoria=request.json["TipoCategoria"]
                                )
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.UsrEventos.append(nuevo_evento)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un evento con dicho nombre',409

        return evento_schema.dump(nuevo_evento)

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [evento_schema.dump(al) for al in usuario.UsrEventos]
    
    
class VistaEventos(Resource):

    def get(self, id_evento):
        return evento_schema.dump(Evento.query.get_or_404(id_evento))

    def put(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        evento.Nomevento = request.json.get("Nomevento",evento.evento)
        evento.Lugar = request.json.get("anio", evento.Lugar)
        evento.Direccion = request.json.get("Direccion", evento.Direccion)
        evento.TipoModalidad = request.json.get("TipoModalidad", evento.TipoModalidad)
        evento.TipoCategoria = request.json.get("TipoCategoria", evento.TipoCategoria)
        db.session.commit()
        return evento_schema.dump(evento)

    def delete(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        db.session.delete(evento)
        db.session.commit()
        return '',204

