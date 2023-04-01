#########################################################################################imports
#                                           Imports                                            #
################################################################################################
from flask import Flask, render_template, request, Markup, url_for, session, Response, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.local import LocalProxy
from waitress import serve
import pickle
import os
import pandas as pd
import datetime
import os
import secrets
import hashlib
import time
import cv2
from itertools import cycle
import psycopg2
from psycopg2.extras import DictCursor, DictRow
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import ssl
import base64
################################################################################################
#                                           Imports                                            #
################################################################################################





































#########################################################################################classes
#                                          Classes                                            #
################################################################################################
class TableManipulation():
    def __init__(self, host : str, port : str, database : str, user : str, password : str ) -> None:
        try:
            self.con = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
            self.cursor = self.con.cursor(cursor_factory=DictCursor)
        except Exception as e:
            print(e)
            
    def close(self) -> None:
        try:
            if self.con:
                self.cursor.close()
                self.con.close()
        except Exception as e:
            print(e)
################################################################################################    
class Capsule(TableManipulation):        
    def get_all(self) -> list[DictRow] or None:
        try:
            self.cursor.execute('''SELECT * FROM capsule;''')
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(e)
            return None
        
    def get_one(self, id : int) -> DictRow or None:
        try:
            self.cursor.execute(f'''SELECT * FROM capsule WHERE Id = {id}''')
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            print(e)
            return None
    
    def add_entry(self, id : int, image_hash : str, match_id : int, owner_id : int, opened : bool = False) -> None:
        try:
            self.cursor.execute('''INSERT INTO capsule (id, image_hash, match_id, owner_id, opened) VALUES (%s,%s,%s,%s,%s)''', [id, image_hash, match_id, owner_id, opened])
            self.con.commit()
        except Exception as e:
            print(e)
################################################################################################            
class Owner(TableManipulation):        
    def get_all(self) -> list[DictRow] or None:
        try:
            self.cursor.execute('''SELECT * FROM owners;''')
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(e)
            return None
        
    def get_one(self, id : int) -> DictRow or None:
        try:
            self.cursor.execute(f'''SELECT * FROM owners WHERE Id = {id}''')
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            print(e)
            return None
        
    def get_owner_mail(self, id : int) -> DictRow or None:
        try:
            self.cursor.execute(f"""SELECT mail FROM owners WHERE id = {id}""")
            mail = self.cursor.fetchone()
            return mail
        except Exception as e:
            print(e)
            return None
        
    def get_owner_name(self, id : int) -> DictRow or None:
        try:
            self.cursor.execute(f"""SELECT name FROM owners WHERE id = {id}""")
            name = self.cursor.fetchone()
            return name
        except Exception as e:
            print(e)
            return None
    
    def add_entry(self, id : int, name : str, mail : str) -> None:
        try:
            self.cursor.execute('''INSERT INTO owners (id, name, mail) VALUES (%s,%s,%s)''', [id, name, mail])
            self.con.commit()
        except Exception as e:
            print(e)
################################################################################################
class Match(TableManipulation):        
    def get_all(self) -> list[DictRow] or None:
        try:
            self.cursor.execute('''SELECT * FROM match;''')
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(e)
            return None
        
    def get_one(self, id : int) -> DictRow or None:
        try:
            self.cursor.execute(f'''SELECT * FROM match WHERE Id = {id}''')
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            print(e)
            return None
    
    def add_entry(self, id : int, local_team : str, visitor_team : str, stadium : str, date : datetime = datetime.datetime.today()) -> None:
        try:
            self.cursor.execute('''INSERT INTO match (id, date, local_team, visitor_team, stadium) VALUES (%s,%s,%s,%s,%s)''', [id, date, local_team,visitor_team, stadium])
            self.con.commit()
        except Exception as e:
            print(e)
#########################################################################################classes
#                                          Classes                                            #
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
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp', }

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
        <li><a href="{url_for('photomatic')}">photomatic</a></li>
        <li><a href="{url_for('logout')}">Log out</a></li>      
        """
    
    if level == 2:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
		<li><a href="{url_for('admin')}">admin panel</a></li>
        <li><a href="{url_for('photomatic')}">photomatic</a></li>
        <li><a href="{url_for('logout')}">Log out</a></li>      
        """
    
    if level == 3:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
		<li><a href="{url_for('admin')}">admin panel</a></li>
        <li><a href="{url_for('photomatic')}">photomatic</a></li>
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
            <li><a href="{url_for('photomatic')}" class="button fit icon solid fa-camera">photomatic</a></li>
			<li><a href="{url_for('logout')}" class="button fit icon solid fa-user-slash">Logout</a></li>
		</ul>       
        </section>

        """

    if level == 2:

        return f"""

        <section>
        <h3 class="major">Where do you want to go {username}?</h3>

        <ul class="actions fit">
            <li><a href="{url_for('photomatic')}" class="button fit icon solid fa-camera">photomatic</a></li>
		</ul>  

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
            <li><a href="{url_for('photomatic')}" class="button fit icon solid fa-camera">photomatic</a></li>
		</ul>  
        
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

########################################################################Camera detector function
def cameras_detector() -> list[int] :

    """Detects the number of cameras connected to the computer and their ids"""
    # This is a generator that yields the number of cameras connected to the 
    # computer and returns their ids

    devices = os.listdir("/dev")
    cameras_indices = [int(device[-1]) for device in devices 
                      if (device.startswith("video") 
                          and not(int(device[-1]) % 2))]

    cameras_indices.sort()

    return cameras_indices
###############################################################################################

##########################################################################Face detector function
def face_detection_in_frame(frame : any) -> any:

    """Detects faces in a frame"""
    # This function detects faces in a frame

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                         "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    return faces
################################################################################################

##########################################################################Face detector function
def generate_frames(flag : bool = False) -> any or None:
    cams = cameras_detector()
    camera = cv2.VideoCapture(cams[0])
    store = os.path.join(basedir, 'images')
    for _ in cycle([True]):
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            faces = face_detection_in_frame(frame)

            if len(faces) == 0:
                font = cv2.FONT_HERSHEY_DUPLEX
                color = (0, 0, 255) 
                fontsize = 2/3
                text = "No face detected"
                position = (25, 50)

                cv2.putText(frame, text, position, font, fontsize, color=color)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            color = (255, 255, 255) 
            fontsize = 2/3
            time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            text = f"whatfeur vs world - {time}"
            position = (25, 25)

            

            cv2.putText(frame, text, position, font, fontsize, color=color)            
                
            ret,buffer=cv2.imencode('.jpg',frame)


            if len(faces) != 0 and flag:
                #store the image as a jpeg
                image_to_string = base64.b64encode(buffer)

                #store the image in the database


                return None

            frame=buffer.tobytes()

            


        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
################################################################################################

###############################################################################################
def send_mail(owner_mail : str, subject : str, body : str, image_path : str) -> None:
    email_sender = 'Capshot.noreply@gmail.com'
    smtp_password = 'spztwywgatukgtse'
    message = MIMEMultipart()
    message["Subject"] = subject
    content = MIMEText(body)
    message.attach(content)
    
    with open(image_path, "rb") as attachment :
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='capsule.png')
        message.attach(part)
        
    text = message.as_string()
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, smtp_password)
            smtp.sendmail(email_sender, owner_mail, text)
    except Exception as e:
        print(e)
################################################################################################

###############################################################################################        
def send_mail_rematch(owner_mail : str, owner_name: str, stadium : str, local_team_name : str, visitor_team_name : str, image_path : str) -> None:
    subject = "HEY! IT'S MEMORY TIME!"
    body = f"""Hello, {owner_name}!
    Do you remember that time when you used this strange photomaton at the {stadium} for the match {local_team_name} vs {visitor_team_name} ?
    Maybe you don't remember but we do !
    The same teams are once again facing each others and we would be thrilled to see you there again !
    It's time to reunite the team,
    Capshoters, assemble !"""
    send_mail(owner_mail, subject, body, image_path)
################################################################################################

################################################################################################   
def send_mail_new_match(owner_mail : str, owner_name : str, stadium : str, image_path : str):
    subject = "HEY! TIME TO CREATE NEW MEMORIES!"
    body = f"""Hello, {owner_name}!
    Do you remember that time you used this strange photomaton at the {stadium} ?
    Maybe you don't remember but we do !
    It's been a while since you created new memories and a new match his happening soon!
    It's time to reunite the team,
    Capshoters, assemble !"""
    send_mail(owner_mail, subject, body, image_path)
################################################################################################

################################################################################################
def imagefile_to_textfile(image_file_path : str, text_file_path : str) -> None:
    with open(image_file_path, 'rb') as image_file:
        image_bytes = image_file.read()
        base64_bytes = base64.b64encode(image_bytes)
        base64_string = base64_bytes.decode('utf-8')
    with open(text_file_path, 'w') as text_file:
        text_file.write(base64_string)
################################################################################################

################################################################################################
def imagefile_to_string(image_file_path : str) -> str:
    with open(image_file_path, 'rb') as image_file:
        image_bytes = image_file.read()
        base64_bytes = base64.b64encode(image_bytes)
        base64_string = base64_bytes.decode('utf-8')
    return base64_string
################################################################################################

################################################################################################
def string_to_imagefile(data : str, image_file_path : str) -> None:
    data = data.encode('utf-8')
    data = base64.b64decode(data)
    with open(image_file_path, 'wb') as image_file:
        image_file.write(data)
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

######################################################################################photo page
@app.route('/photomatic', methods = ['GET', 'POST'])
def photomatic():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    #if you are not connected & at least an admin
    if connected < 1:
         return home()
    
    if request.method == 'POST':
        return render_template('redirect.html')
        
    return render_template('photomatic.html', 
                           Connected = username, 
                           menu = Markup(menu(connected)),
                           src = Markup("""<img src="{{ url_for('video_feed') }}" width="100%"/>"""))
################################################################################################

###################################################################################redirect page
@app.route('/picture')
def picture():
    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    #if you are not connected & at least an admin
    if connected < 1:
         return home()
    
    generate_frames(True)
    return render_template('redirect2.html')
################################################################################################

###################################################################################redirect page
@app.route('/redirect')
def redirect():
    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    #if you are not connected & at least an admin
    if connected < 1:
         return home()
    
    return render_template('redirect3.html')
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



































#########################################################################################app run
#                                       app response                                           #
################################################################################################
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
################################################################################################
@app.route('/video_feed2')
def video_feed2():
    return Response(generate_frames(flag = True),mimetype='multipart/x-mixed-replace; boundary=frame')
################################################################################################
#                                        app response                                          #
########################################################################################app page



































#########################################################################################app run
#                                            app run                                           #
################################################################################################
serve(app, host="0.0.0.0", port=8080)
app.run(debug=False)
################################################################################################
#                                            app run                                           #
#########################################################################################app run