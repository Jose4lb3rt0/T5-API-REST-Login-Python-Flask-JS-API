from flask import Flask, render_template, request, jsonify
import mysql.connector
from db_config import configRemote, config

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(dictionary=True)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    if request.method == 'POST':
        data = request.json
        nombre = data['nombre']
        correo = data['correo']
        contraseña = data['contraseña']
        try:
            # Llamar al procedimiento almacenado para guardar o actualizar el usuario
            cursor.callproc('sp_Usuario_Guardar', (nombre, correo, contraseña))
            cnx.commit()
            return jsonify({'message': 'Usuario registrado correctamente'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)