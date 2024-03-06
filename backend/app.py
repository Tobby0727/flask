from flask import Flask 
from flask_cors import CORS
from flask import jsonify,request
import pymysql
app=Flask(__name__)
CORS(app)
def conectar(vhost,vuser,vpass,vbd):
    conn =pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vbd, charset='utf8mb4')
    return conn
@app.route("/")
def consulta_general():
    try:
        conn=conectar ('localhost','root','','gestor')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM baul """)
        datos=cur.fetchall()
        data=[]
        for row in datos:
            dato={'id_baul':row[0],'Plataforma':row[1] ,'usuario':row[2],'clave':row[3]}
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify({'baul':data,'mensaje':'baul de contraseñas'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'error'})
    
@app.route("/consulta_individual/<codigo>",methods=['GET'])
def consulta_individual(codigo):
    try:
        conn=conectar('localhost','root','','gestor')
        cur = conn.cursor()
        cur.excute("""Select * from baul where id_baul='{0}'""".format(codigo))
        datos=cur.fetchone()
        cur.close()
        conn.close()
        if datos!=None:
            dato={'id_baul':dato[0],'Plataforma':dato[1],'usuario':dato[2],'clave':dato[3]}
            return jsonify({'baul':dato,'mensaje':'registro encontrado'})
        else:
            return jsonify({'mensaje':'registro no encontrado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'error'})
    
@app.route("/registro", methods=['POST'])
def registro():
    try:
        conn=conectar('localhost','root','','gestor')
        cur = conn.cursor()
        x=cur.execute("""insert into baul (Plataforma,usuario,clave) values \
            ('{0}','{1}','{2}')""".format(request.json['Plataforma'],\
                request.json['usuario'],request.json['clave']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje':'registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'error'})
        
@app.route("/eliminar/<codigo>",methods=['DELETE'])
def eliminar(codigo):
    try:
        conn=conectar('localhost','root','','gestor')
        cur = conn.cursor()
        x=cur.execute(""" delete from baul where id_baul={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje':'eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'error'})
    
@app.route("/actualizar/<codigo>",methods=['PUT'])
def actualizar(codigo):
    try:
        conn=conectar('localhost','root','','gestor')
        cur = conn.cursor()
        x=cur.execute("""update baul set Plataforma='{0}',usuario='{1}',clave='{2}' where  id_baul='{3}'""".format(request.json['Plataforma'],request.json['usuario'],request.json['clave'],codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje':'registro actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'error'})


if __name__=='__main__':
    app.run(debug=True)