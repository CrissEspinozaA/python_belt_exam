from flask_app import app 
from flask_app.models.users import User
from flask_app.models.pies import Pie
from flask_bcrypt import Bcrypt

from flask import render_template, request, redirect, url_for, session, flash 
bcrypt = Bcrypt(app)

@app.route('/') # crea una ruta
def users(): # crea una función
    return render_template('users.html') # devulve el template users.html

@app.route('/dashboard') 
def dashboard():
    if 'user.id' in session:
        pies = Pie.get_all_pies()
        print(pies)
        return render_template('dashboard.html', pies = pies)
    else:
        return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    User.save_user(data)
    logged_user = User.get_user_by_email(request.form)
    session ['user.id'] = logged_user.id
    session ['user.first_name'] = logged_user.first_name
    session ['user.last_name'] = logged_user.last_name
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    if not User.validate_login(request.form):
        print("login failed")
        return redirect('/')
    logged_user = User.get_user_by_email(request.form)
    if logged_user == None:
        flash ("Email/Contraseña no válidos", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(logged_user.password, request.form['password']):
        flash ("Email/Contraseña no válidos", "login")
        return redirect('/')
    session ['user.id'] = logged_user.id
    session ['user.first_name'] = logged_user.first_name
    session ['user.last_name'] = logged_user.last_name
    return redirect('/dashboard')
    
    # comienzo de pies
@app.route('/pies/new', methods = ['GET', 'POST'])
def pies(): 
    if not 'user.id' in session:
        print("no user logged in")
        return redirect('/')
    if request.method == 'GET':
        return render_template('pies.html')
    elif request.method == 'POST':
        print(request.form)    
        if not Pie.validate_pie(request.form):
            print("pie failed")
            return redirect('/dashboard')
        data = {
            "name": request.form['name'],
            "filling": request.form['filling'],
            "crust": request.form['crust'],
            "user_id": session['user.id']
            }
        Pie.save_pie(data)
        return redirect('/dashboard')

@app.route('/pies/edit/<int:id>')
def get_pie_by_id(id):
    data = {
        'id': id
    }
    pie = Pie.get_pie_by_id(data)
    return render_template ('edit.html', pie = pie)

@app.route('/pies/update', methods=['POST'])
def update_pie():
    Pie.update_pie(request.form)
    return redirect('/dashboard')

@app.route('/pie/<int:id>')
def show_pie(id):
    data = {
        "id" : id
    }
    pie = Pie.get_pie_by_id(data)
    return render_template('show_pie.html', pie = pie)

@app.route("/pies/delete/<int:id>")
def delete(id):
    data ={
        'id': id
    }
    Pie.delete_pie(data)
    return redirect("/dashboard")

@app.route('/pies') 
def all_pies():
    if 'user.id' in session:
        pies = Pie.get_all_pies()
        print(pies)
        return render_template('pies.html', pies = pies)
    else:
        return redirect('/')


@app.errorhandler(404) 
def url_error(e):
    return "Página no encontrada", 404