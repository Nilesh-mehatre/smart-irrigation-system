

import os

import json

from flask import Flask,render_template,session,redirect,send_file, request,flash,jsonify,Response,url_for,make_response

from datetime import datetime


import uuid



# from flask_jwt_extended import (
#     JWTManager, create_access_token,jwt_required,  get_jwt_identity, verify_jwt_in_request, get_jwt_identity)
from flask_bcrypt import Bcrypt
from __init__ import app, db
from models import *
from datetime import datetime
from functools import wraps
import jwt
from helper import *


with open("config.json","r") as c:
    params=json.load(c)['params']
    

app.config['JWT_SECRET_KEY'] = 'your-secret-key' # change this to a secret key of your choice

bcrypt = Bcrypt(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # token = request.headers.get("Authorization")
        token = session.get("token")
        if not token:
            # Save the current URL as the 'next' parameter in the login redirect URL
            login_url = url_for('login', redirect_url=request.url)
            return redirect(login_url)

        try:
            # Verify and decode the JWT
            payload = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            email = payload["email"]

            # Find the user by email
            user = Users.query.filter_by(email=email).first()
            if not user:
                return jsonify({"error": "Invalid user email"}), 401

            # Attach the user object to the request context
            request.user = user

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = Users.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Invalid user email"}), 401

        if bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({"email": email}, app.secret_key, algorithm="HS256")
            session["token"] = token
            return jsonify({"message": "Logged in successfully", "token": token}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    
    redirect_url = request.args.get('redirect_url') or "/"
    print(redirect_url)
    return render_template("login2.html", auth_type="login",redirect_url=redirect_url)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=="POST":
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")
        email = data.get("email")
        mobile = data.get("mobile")

        # Check if email already exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return jsonify({"error": "Email already exists"}), 409

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create new user
        
        new_user = Users(
            userId=uuid.uuid4(),
            name=name,
            email=email,
            mobile=mobile,
            password=hashed_password
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201
    
    elif request.method == 'GET':
        return render_template("login2.html", auth_type="signup")

    return jsonify({"message": "Method not allowed"}), 405


        
    # return render_template("login2.html",auth_type="signup")


@app.route('/logout')
@login_required
def logout():
    session.pop('token', None)
    session.clear()
    return redirect(url_for('login'))  # Redirect to the login page or any other desired location



# @app.route("/",methods=["GET","POST"])
# @login_required
# def home():
#     return render_template("index.html")


# @app.route("/prompt",methods=["GET","POST"])
# @login_required
# def home():
#     return render_template("prompt.html")





@app.route("/",methods=["GET","POST"])
@login_required
def index():
    # return render_template("Client/remote.html")
    return render_template("index.html")
 
motor_status = "OFF"
moisture=0
@app.route("/moisture", methods=["GET","POST"])
def receive_moisture_data():
    if request.method=="POST":
        data = request.get_json()
        global moisture
        moisture = data.get("moisture")
        print(moisture)
        
        
        return jsonify({"message": "Moisture data received"})

@app.route("/motor", methods=["GET"])
def control_motor():
    global motor_status
    if int(moisture) > 60:
            motor_status = "OFF"
    # print(motor_status)
    if motor_status == "ON":
        return jsonify({"status": "ON"}),200
    else:
        return jsonify({"status": "OFF"}),200
    

@app.route("/remote", methods=["GET","POST"])
def control_remote():
    global moisture
    global motor_status
    if request.method=="POST":
        data = request.get_json()
        # global motor_status
        if int(moisture) > 60:
            motor_status = "OFF"
            return jsonify({"message": "Sent data received","moisture":moisture,"motor_status":motor_status,"message_display": "Motor can't be turned ON as moisture is very high."})
            
        motor_status = data.get("motor_status")
        # print(motor_status)
        # return jsonify({"message": "Turned %s Motor." %(motor_status)})   
   
    return jsonify({"message": "Sent data received","moisture":moisture,"motor_status":motor_status,"message_display": "Turned %s Motor." %(motor_status)})
    
@app.context_processor
def inject_user():
    try:
        user = checkUser()
        user = Users.query.get(user.userId)
        # Uncomment the following line if you want to attach the user object to the request context
        # request.user = cust
        return {"user": user,"params":params}  # Inject the user object into the template context
    except (AuthenticationRequired, InvalidUserEmail, TokenExpired, InvalidToken) as e:
        print(f"Authentication error: {e}")
        return {"params":params}

                                      
 
