#########################################################################################imports
#                                           Imports                                            #
################################################################################################
from flask import Flask, render_template, request, Markup, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from waitress import serve
import pickle
import os
import pandas as pd
import datetime
import os
import pandas
import secrets
import hashlib
################################################################################################
#                                           Imports                                            #
################################################################################################








































######################################################################################app config
#                                          app config                                          #
################################################################################################
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='templates', static_folder='templates/assets')

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'databases/data.db') 
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///' + os.path.join(basedir, 'databases/users.db')}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config["DEBUG"] = False

db = SQLAlchemy(app)
################################################################################################
#                                          app config                                          #
######################################################################################app config








































#######################################################################################Functions
#                                          Functions                                           #
#############################################################################all pages functions
def menu(level : int) -> str : 

    if level == 0:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
        <li><a href="{url_for('login')}">Log In</a></li>
        <li><a href="{url_for('sign_up')}">Sign Up</a></li>
        """
        
    if level == 1:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
        <li><a href="{url_for('logout')}">Log out</a></li>      
        """
    
    if level == 2:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
		<li><a href="{url_for('admin')}">admin panel</a></li>
        <li><a href="{url_for('logout')}">Log out</a></li>      
        """
    
    if level == 3:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
		<li><a href="{url_for('admin')}">admin panel</a></li>
        <li><a href="{url_for('logout')}">Log out</a></li>      
        """

    return "Error attribution level"
################################################################################################

############################################################################home pages functions
def buttons(level : int, username : str) -> str:
    if level == 0:

        return f"""

        <section>
        <h3 class="major">Where do you want to go?</h3>

        <ul class="actions fit">
			<li><a href="{url_for('login')}" class="button fit icon solid fa-user">Login</a></li>
			<li><a href="{url_for('sign_up')}" class="button fit icon solid fa-user-plus">Sign up</a></li>
		</ul>        
        </section>

        """

    if level == 1:

        return f"""

        <section>
        <h3 class="major">Where do you want to go {username}?</h3>


		<ul class="actions fit">
			<li><a href="{url_for('logout')}" class="button fit icon solid fa-user-slash">Logout</a></li>
		</ul>       
        </section>

        """

    if level == 2:

        return f"""

        <section>
        <h3 class="major">Where do you want to go {username}?</h3>


        <ul class="actions fit">
			<li><a href="{url_for('admin')}" class="button fit icon solid fa-chess-queen">Admin panel</a></li>
            <li><a href="{url_for('logout')}" class="button fit icon solid fa-user-slash">Logout</a></li>
		</ul>    
        </section>

        """
    
    if level == 3:

        return f"""

        <section>
        <h3 class="major">Where do you want to go {username}?</h3>

        <ul class="actions fit">
			<li><a href="{url_for('admin')}" class="button fit icon solid fa-chess-queen">Admin panel</a></li>
            <li><a href="{url_for('logout')}" class="button fit icon solid fa-user-slash">Logout</a></li>
		</ul>       
        </section>

        """

    return "Error attribution level"
################################################################################################

##################################################################admin & signup pages functions
def add_user(username : str, password : str, level : int) -> None:
    """Add a user to the database"""
    #encrypt the password wit hashlib
    password = hashlib.sha256(password.encode()).hexdigest() 
    #use engine_USR to add the user to the database
    engine_USR = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/users.db'), echo=False)
    conn_USR = engine_USR.connect()
    conn_USR.execute('INSERT INTO users (username, password, attr_level) VALUES (?, ?, ?)', (username, password, level), check_same_thread=False)
    conn_USR.close()

    return None
################################################################################################

#################################################################admin & signup pages functions
def check_user(username : str) -> bool:
    """Check if the user exists in the database"""   
    #use engine_USR to check if the user exists in the database
    engine_USR = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/users.db'), echo=False)
    conn_USR = engine_USR.connect()
    result = conn_USR.execute('SELECT * FROM users WHERE username = ?', (username)).fetchall()
    conn_USR.close()

    if len(result) == 0:
        return False

    return True
################################################################################################

############################################################################login page functions
def loginf(username : str, password : str) -> bool:
    """check if username and password are correct"""
    password = hashlib.sha256(password.encode()).hexdigest() 
    #use engine_USR to check if the user exists in the database and get the password
    engine_USR = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/users.db'), echo=False)
    conn_USR = engine_USR.connect()
    #get result from the database where username = username and password = password
    result = conn_USR.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password), check_same_thread=False).fetchall()
    conn_USR.close()

    if len(result) == 0:
        return False
    
    return result[0][2]
################################################################################################
#                                          Functions                                           #
#######################################################################################Functions







































########################################################################################app page
#                                           app page                                           #
#######################################################################################Home page							
@app.route('/')
def home():

    try:

        connected = session['connected'] 
        username = session['username']

    except: 

        session['connected'] : int = 3
        session['username'] : str = "Not connected"
        connected = session['connected'] 
        username = session['username']

    message = "Welcome! You are not connected."
    
    if connected == 1:
        message = f"Welcome {username}!"
    
    if connected == 2:
        message = f"Welcome {username}! You have employee privileges."
    
    if connected == 3:
        message = f"Welcome {username}! You have admin privileges."

    
    return render_template('index.html', 
                           Connected = username, 
                           menu = Markup(menu(connected)),
                           buttons = Markup(buttons(connected, username)),
                           message = message)
################################################################################################

######################################################################################Admin page
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    #if you are not connected & at least an admin
    if connected < 3:
         return home()
    
    if request.method == 'POST':

        if request.form['password'] != request.form['password2']:
            return render_template('admin.html', 
                                   wrong = "Passwords don't match", 
                                   Connected = username, 
                                   menu = Markup(menu(connected)))
        
        
        if check_user(request.form['username']):
            return render_template('admin.html', 
                                   wrong = "User already exists", 
                                   Connected = username, 
                                   menu = Markup(menu(connected)))
        


        attr_level = 1
        if request.form['attr_level'] == "Employee":
            attr_level = 2
        if request.form['attr_level'] == "Admin":
            attr_level = 3


        add_user(request.form['username'], request.form['password'], attr_level)

        return render_template('admin.html', 
                               wrong = "User added", 
                               Connected = username, 
                               menu = Markup(menu(connected)))



    return render_template('admin.html',
                            wrong = "",
                            Connected = username, 
                            menu = Markup(menu(connected)))
################################################################################################

########################################################################@#############Login page
@app.route('/login' , methods = ['GET', 'POST'])
def login():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()
    
    if connected > 0:
        return home()

    if request.method == 'POST':
        user = request.form['id']
        password = request.form['password']

        attr = loginf(user, password)

        if attr:
            session['connected'] = attr
            session['username'] = user
            return home()
        
        return render_template('login.html',
                                Connected = username, 
                                menu = Markup(menu(connected)),
                                wrong = "Wrong id or password")
    
    return render_template('login.html',
                            Connected = username, 
                            menu = Markup(menu(connected)),
                            wrong = "")
################################################################################################

####################################################################################Sign up page
@app.route('/signup', methods = ['GET', 'POST'])
def sign_up():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()
    
    if connected > 0:
        return home()
    
    if request.method == 'POST':
        
        if request.form['password'] != request.form['password2']:
            return render_template('signup.html', 
                                   wrong = "Passwords don't match", 
                                   Connected = username, 
                                   menu = Markup(menu(connected)))
        
        
        if check_user(request.form['username']):
            return render_template('signup.html', 
                                   wrong = "User already exists", 
                                   Connected = username, 
                                   menu = Markup(menu(connected)))
        


        attr_level = 1
        if request.form['attr_level'] == "Employee":
            attr_level = 2
        if request.form['attr_level'] == "Admin":
            attr_level = 3
        
                

        session['connected'] = attr_level
        session['username']= request.form['username']


        add_user(request.form['username'], request.form['password'], attr_level)
        return home()


    if session['connected'] == 0:
        return render_template('signup.html', 
                               Connected = username, 
                               menu = Markup(menu(connected)))
    
    return home()
################################################################################################

#####################################################################################Logout page
@app.route('/logout')
def logout():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    if session['connected'] == 0:
        return home()
    
    session['connected'] = 0
    session['username']= "Not connected"

    return render_template('logout.html')
################################################################################################
#                                           app page                                           #
########################################################################################app page







































#################################################################################@@@@@###app run
#                                            app run                                           #
################################################################################################
serve(app, host="0.0.0.0", port=8080)
app.run(debug=False)
################################################################################################
#                                            app run                                           #
#########################################################################################app run