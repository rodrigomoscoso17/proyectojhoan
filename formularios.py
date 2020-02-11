from wtforms import Form, StringField, TextAreaField, \
    PasswordField, validators


class RegistrarUsuario(Form):
    nombre = StringField('Nombre', [validators.length(min=1, max=50)])
    apellido = StringField('Apellido', [validators.length(min=1, max=50)])
    usuario = StringField('Usuario', [validators.length(min=4, max=25)])
    correo = StringField('Email', [validators.length(min=4, max=25)])
    contrasena = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message="Password Vacio")])
    confirm = PasswordField("Confirmar Password")
    telefono = StringField('Telefono', [validators.length(min=1, max=10)])
    comentarios = TextAreaField('Comentarios', [validators.length(min=1, max=500)])
