from flask import Flask ,jsonify, request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configura la aplicación Flask con la configuración apropiada
app.config.from_object(config['development'])
conexion = MySQL(app)

@app.route('/cursos',methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "select codigo, nombre, credito FROM cursos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        print(datos)
        cursos = []
        for fila in datos:
            curso = {'codigo':fila[0], 'nombre':fila[1],'credito':fila[2]}
            cursos.append(curso)
        return jsonify({'cursos':cursos,'mensaje':"cursos listados"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})  

@app.route('/cursos/<codigo>',methods=['GET'])
def leer_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "select codigo, nombre, credito FROM cursos WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        dato = cursor.fetchone()
        print(dato)
        if dato != None:
            curso = {'codigo':dato[0], 'nombre':dato[1],'credito':dato[2]}
            return jsonify({'cursos':curso,'mensaje':"cursos listados"})
        else:
            return jsonify({'mensaje':"curso no encontrado"})

    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@app.route('/cursos', methods=['POST'])
def crear_curso():
    try:
        data = request.json  # Obtén los datos JSON de la solicitud
        # print(data)  # Imprime los datos JSON recibidos
        cursor = conexion.connection.cursor()        
        sql = """INSERT INTO cursos (codigo, nombre, credito) VALUES ('{0}', '{1}', '{2}')""".format(data['codigo'], data['nombre'], data['credito'])
        cursor.execute(sql)
        conexion.connection.commit()
        print(cursor)
        return jsonify({'mensaje': "curso creado exitosamente"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        if not codigo.isdigit():
            return jsonify({'mensaje':"Codigo Invalido"}), 400
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM cursos WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            conexion.connection.commit()
            return jsonify({'mensaje': "Curso eliminado exitosamente"})
        else:        
            return jsonify({'mensaje': "Curso no existe"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        data = request.json
        cursor = conexion.connection.cursor()
        sql = """UPDATE cursos SET nombre = '{0}', credito= '{1}' WHERE codigo = '{2}'""".format(data['nombre'],
        data['credito'],codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "curso Actualizado exitosamente"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe</h1>",404

if __name__ == '__main__':
   app.register_error_handler(404,pagina_no_encontrada)
   app.run()  # Inicia el servidor Flask
