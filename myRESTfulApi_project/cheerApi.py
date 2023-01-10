# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:23:55 2023

@author: user
"""

import db
from flask import Flask, request,jsonify
from flask_restful import Api, Resource

import secrets
import hashlib



app = Flask(__name__)
api = Api(app)

class AuthorToken(Resource):
    def post(self):
        qtype = request.form.get("check_type")
        email = request.form.get("email")
        password = request.form.get("password")
        data_sha = hashlib.sha3_256(password.encode("utf-8")).hexdigest()
        
        if qtype is None or qtype != "token":
            response = jsonify("BAD Message!")
            response.status_code = 400
            return response
        
        sql = "select * from member where email=%s and password=%s"
        
        cursor = db.conn.cursor()
        cursor.execute(sql,(email,data_sha))
        data = cursor.fetchone()
        
        if data is None:
            response = jsonify("Account Do Not Exist, Check Email Or Password Again")
            response.status_code = 400
            return response
        
        token = {}
        tokendata = secrets.token_hex(16)
        token['token'] = tokendata
        
        sql = "update member set token=%s where email=%s"

        
        cursor.execute(sql,(tokendata,email))
        db.conn.commit()
        
        return jsonify(token)






class Cheerleaders(Resource):
    def post(self):
        
        qtype = request.form.get('grant_type')
        email = request.form.get('email')
        token = request.form.get('token')
        
        if qtype is None:
            response = jsonify("BAD Message!")
            response.status_code = 400
            
            return response
        
        if qtype == "cheerleaders":
        
            cursor = db.conn.cursor()
            sql = "select * from member where email=%s and token=%s"
            cursor.execute(sql,(email,token))
            data = cursor.fetchone()
            
            if data is not None:
                sql = "select * from player"
                cursor.execute(sql)
            
                result = cursor.fetchall()
                player = list()
            
                for item in result:
                    json = {}
                    json["id"] = item[0]
                    json["name"] = item[1]
                    json["zodiac"] = item[2]
                    json["height"] = item[3]
                    json["weight"] = item[4]
                    
                    player.append(json)
                return {"cheerleaders":player},200
            else:
                response = jsonify("Check email and Token Please!")
                response.status_code = 400
                return response
        
        else:
            response = jsonify("BAD Message! ")
            response.status_code = 400
            return response
        
    
    
api.add_resource(Cheerleaders,"/cheerleaders")
api.add_resource(AuthorToken,"/getToken")

if __name__ == "__main__":
    app.run(debug=True)
        
        
        
        