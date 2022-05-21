from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL # import the connectToMySQL function from the application.config.mysqlconnection module
from flask import flash
import re

class Pie:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.filling = data["filling"]
        self.crust = data["crust"]
        self.vote = data["vote"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        
    @staticmethod
    def validate_pie(pie):
        is_valid = True
        if len(pie["name"]) < 3:
            flash("El nombre debe tener desde 3 caracteres", "error_pie")
            print("name failed")
            is_valid = False
        if len(pie["filling"]) < 3:
            flash("El relleno debe tener desde 3 caracteres", "error_pie")
            print("filling failed")
            is_valid = False
        if len(pie["crust"]) < 3:
            flash("La corteza debe tener desde 3 caracteres", "error_pie")
            print("crust failed")
            is_valid = False
        return is_valid
            
    @classmethod
    def save_pie(cls, data):
        query = "INSERT INTO t_pies (name, filling, crust, created_at, updated_at, user_id) VALUES (%(name)s, %(filling)s, %(crust)s, NOW(), NOW(), %(user_id)s)"
        mysql = connectToMySQL("db_pypie_derby")
        results = mysql.query_db(query, data)
        pie = {"user.id": results}
        return pie
    
    @classmethod
    def get_all_pies(cls):
        query = "SELECT * FROM t_pies"
        mysql = connectToMySQL("db_pypie_derby")
        results = mysql.query_db(query)
        pies = []
        for pie in results:
            pies.append(cls(pie))
        return pies
        
    @classmethod
    def update_pie(cls, data):
        query = "UPDATE t_pies SET name = %(name)s, filling = %(filling)s, crust = %(crust)s, updated_at = NOW() WHERE id = %(id)s"
        mysql = connectToMySQL("db_pypie_derby")
        results = mysql.query_db(query, data)
        return results
    
    @classmethod
    def get_pie_by_id(cls, data):
        query = "SELECT * FROM t_pies WHERE id = %(id)s"
        mysql = connectToMySQL("db_pypie_derby")
        results = mysql.query_db(query, data)
        return cls(results[0])

    @classmethod
    def update_vote(cls, data):
        query = "UPDATE t_pies SET vote = %(vote)s WHERE id = %(id)s"
        mysql = connectToMySQL("db_pypie_derby")
        results = mysql.query_db(query, data)
        pie = {"user.id": results}
        return pie
    
    @classmethod
    def delete_pie(cls, data):
        query = "DELETE FROM t_pies WHERE id = %(id)s"
        mysql = connectToMySQL("db_pypie_derby")
        results = mysql.query_db(query, data)
        return results