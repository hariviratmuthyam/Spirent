import os
from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

def create_app(test_config=None):
    app=Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
    SECRET_KEY="2629",
    DATABASE=os.path.join(app.instance_path,'spirentusers.sqlite'),
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from db import init_app
    init_app(app)
    @app.route("/login")
    def login():
        if request.method =='POST':
            username=request.form['username']
            password=request.form['password']
            db=get_db()
            error=None
            user=db.execute(
            "SELECT * FROM user WHERE username=?",(username,)
            ).fetchone()
            if user is None:
                error ="incorrect username"
            elif not check_password_hash(user["password"], password):
                error ="ïncorrect password"
            if error is None:
                session.clear()
                session["user_id"] = user["id"]
            return redirect(url_for("user_page"))
        return render_template("login.html")
    
    @app.route("/signup")
    def signup():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            db = get_db()
            error = None

            if not username:
                error = "Username is required."
            elif not password:
                error = "Password is required."
            elif (
                db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
            is not None):
                error = "User {0} is already registered.".format(username)

            if error is None:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                return redirect(url_for("login"))
            flash(error)
        return render_template("signup.html")
    @app.route("/logout")
    def logout():
        session.clear()
        return render_template("index.html")
        
    
        
    return app
    