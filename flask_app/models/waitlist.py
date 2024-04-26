import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, url_for
from flask_app import app
from flask_app.models.email import Email

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class Waitlist:


    dB = "lotus_website"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.confirmed = data['confirmed']
        



    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO waitlists (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM waitlists;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM waitlists WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def get_by_email(cls, email):
        query = """
            SELECT * FROM waitlists WHERE email = %(email)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"email": email})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None
    

    @staticmethod
    def validate_inputs(data):
        errors = []

        # Validate first name
        if len(data['first_name']) < 2 or any(char.isdigit() for char in data['first_name']):
            errors.append("First name should be greater than 1 character and contain no numbers")

        # Validate last name
        if len(data['last_name']) < 2 or any(char.isdigit() for char in data['last_name']):
            errors.append("Last name should be greater than 1 character and contain no numbers")

        # Validate email
        valid_domains = ['yahoo.com', 'gmail.com', 'hotmail.com', 'icloud.com', 'outlook.com']
        if '@' not in data['email'] or not any(domain in data['email'] for domain in valid_domains):
            errors.append("Invalid email format or domain")

        return errors
    
    @classmethod
    def email(cls, data):
        Email.send(data["first_name"], to_email=data["email"], data=data)
        return 