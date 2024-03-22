from flask import Flask, render_template, request, jsonify,redirect,url_for
import mysql.connector
from db_config import configRemote, config

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(dictionary=True)
app = Flask(__name__)

#################### RUTAS ####################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/iniciar', methods=['POST'])
def iniciar():
    correo = request.form['correo-ingresar']
    contraseña = request.form['contraseña-ingresar']
    cursor.callproc('sp_Usuario_Login', (correo, contraseña))
    for data in cursor.stored_results():
        cuenta = data.fetchall()
    if cuenta:
        return cuenta
    else:
        return jsonify({'respuesta': 'Los datos que has ingresado no son validos'}), 401


@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        nombres = request.form['nombres-registrar']
        correo = request.form['correo-registrar']
        contraseña = request.form['contraseña-registrar']
        cursor.callproc('sp_Usuario_Guardar', (nombres, correo, contraseña))
        cnx.commit()
        #Una vez registrado, nos logeamos autoamticamente
        cursor.callproc('sp_Usuario_Login', (correo, contraseña))
        for data in cursor.stored_results():
            cuenta = data.fetchall()
        if cuenta:
            return cuenta
    except Exception as e:
        return jsonify({'respuesta': 'Algo ha fallado'}), 401


@app.route('/recuperar', methods=['POST'])
def recuperar():
    correo = request.form['correo-recuperarcontraseña']
    cursor.callproc('sp_Usuario_RecuperarPassword', (correo,))
    for result in cursor.stored_results():
        contraseña = result.fetchone()
        if contraseña:
            return jsonify({'respuesta': f'La contraseña del correo {correo} es: {contraseña}'})
        else:
            return jsonify({'respuesta': "No se encontró ninguna cuenta asociada a este correo electrónico"})


@app.route('/actualizar', methods=['POST'])
def actualizar():
    return


if __name__== '__main__':
    app.run(debug=True)