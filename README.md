[![Contributors][contributors-shield]][contributors-url]

<h2 align="center"> CAPSHOT </h2>
<p align="center"><a href="https://www.odoo.com/">
<img src="https://odoocdn.com/openerp_website/static/src/img/assets/png/odoo_logo.png" alt="Logo" width="300" height="100"></a></p>
<h3 align="center"> ODOO HACKATHON PROJECT THEMED ON TIME CAPSULE </h4>
<h4 align="center"> DURATION :  2 DAYS </h3>

##  Description

Capshot is a Python project that manages the collection of capsules related to a sports event. Each capsule is associated with a match and an owner, and can be opened or closed. The project uses a PostgreSQL database to store and retrieve data about the capsules, the owners, and the matches Capshot is a digital time capsule application created for sports lovers. It is an innovative photo booth project that captures memorable moments in sports stadiums and creates time capsules for fans to enjoy at future events and for their memories to be projected into the stadium and remembered in the future.

Our goal is to create a unique and immersive spectator experience for sports fans. We want to let fans experience unforgettable moments and keep them forever. Imagine going to a football or basketball game with your family or friends. You are at halftime, the match is intense and you want to take a break to relax and take a souvenir photo. That's what our photo booth is for! You can capture an unforgettable moment with your loved ones in seconds, and our advanced technology instantly turns your photo into a unique time capsule.

You will receive your time capsule a year later when the same date approaches, or when the poster of the match you are about to watch is presented again, you will be taken to this very moment of the match. You will be able to share your photo with your friends and family and remember how wonderful that moment was. You will also have the opportunity to buy tickets for the next match and thus reconnect with your previous memories while creating new ones.

Our photo booth is not just a keepsake, but a powerful marketing tool for sports teams and related brands.
We are sure that our innovative photo booth will be highly appreciated by sports fans and sports teams. We look forward to working with you to bring this unique spectator experience to sporting events around the world!

<p align="center"><a href="https://www.odoo.com/">
<img src="https://i.hizliresim.com/spwesl9.png" alt="Logo" width="250" height="250"></a></p>

## Requirements
<!DOCTYPE html>
<html>
  <body>
    <ul>
      <li>Flask==2.2.2</li>
      <li>flask_sqlalchemy==3.0.3</li>
      <li>pandas==1.5.2</li>
      <li>waitress==2.1.2</li>
      <li>Python 3.5 or later</li>
      <li>PostgreSQL 9.5 or later</li>
      <li>psycopg2 2.8 or later</li>
      <li>hashlib</li>
    </ul>
  </body>
</html>


## Installation

Clone the project

```bash
  git clone https://github.com/Flotchet/Odoo-Hackathon
```
 Install the required packages using

```bash
  pip install -r requirements.txt
```
 
Go to the project directory

```bash
  cd YourPath/Odoo-Hackathon
```
Create a PostgreSQL database for the project. 

```bash
 Create the required tables in the database by running the **`create_tables.sql`** script.
```
Last 
```bash
   Edit the **`config.ini`** file with the connection details for your PostgreSQL database.
   ```
   
## Some Interfaces of the application
<p align="center"><img src="https://imgyukle.com/f/2023/04/02/Q1AGaN.png"></p>


## App Config

This is a configuration code snippet for a Flask web application. It sets up various configurations for the app, such as the app's secret key, database URI, bind, and track modifications. It also configures the upload folder for file uploads and sets a maximum content length of 16MB. Finally, it initializes a SQLAlchemy instance using the app object created earlier.

This code can be used as a template for configuring a Flask app with similar requirements.

## Functions 

There is many functions in the documents. For the functions codes are Flask web application written in Python. The code defines several functions that handle different routes or actions in the web application.

The **`menu`** function takes an integer parameter **`level`** and returns a string containing an HTML unordered list with links to different pages in the web application depending on the value of **`level`**. The **`get_table_limited_matches`** function returns an HTML table containing information about matches. The **`buttons`** function takes two parameters, **`level`** and **`username`**, and returns an HTML section containing buttons to different pages in the web application depending on the value of **`level`**.

**Def login:**
```sh
    - Check if the user's login credentials are correct.
    - Hash the password entered by the user using the SHA-256 algorithm.
    - Make a connection using the SQLite database engine to check if the user is present in the database.
    - Retrieve a result matching the user's name and hashed password in the database.
    - Return False if there is no result. Otherwise, return the user's authorization level (result[0][2]).
```
 **Def add_user:**
 ```sh
    - Add a user to the database.
    - Hash the password entered by the user using the SHA-256 algorithm.
    - Make a connection using the SQLite database engine.
    - Add information such as the user's name, hashed password, and authorization level to the database.
    - Close the connection.
    - Return None.
```

**Def check_user:**
 ```sh
    - Check if a specified user exists in the database.
    - Make a connection using the SQLite database engine.
    - Search for information such as the user's name in the database.
    - Return False if there is no result. Otherwise, return True
```

**Def cameras_detector:**
 ```sh
    - Detect the number and IDs of cameras connected to a computer.
    - List the devices in the "/dev" directory.
    - Add the indices of devices starting with "video" and ending with an even number to the list.
    - Sort the indices of the cameras.
    - Return a list containing the indices of the cameras.
```

 **Def face_detection_in_frame:**
 ```sh
    - Detect faces in a frame.
    - Call a model trained for face detection using the CascadeClassifier class in the cv2 library.
    - Create a grayscale image of the frame.
    - Call the detectMultiScale() function to detect faces on this grayscale image.
    - Return a list containing the coordinates of the detected faces.
```

**Def generate_frames:**
```sh
   - Continuously read frames from the webcam and detect faces in each frame.
    - If no face is detected, display the message "No face detected".
    - If a face is detected, draw a rectangle around the face.
    - Add the string "whatfeur vs world - {time}" to each frame.
    - If the face is found and **`flag`** is True, convert the image to Base64 format and save it to a database.
    - Terminate the function.
    - Return a generator function that returns these frames one by one.
```

 **Def send_mail:**
 ```sh
    - Send an email to the specified email address.
    - The function parameters include the recipient email address, email subject, email body, and the path of an image file to be attached.
    - Set the MIME types of the email's headers, text, and attachments.
    - Send the email via an SSL connection using the **`smtplib`** module.
    - Print any errors that occur during the email sending process to the screen.
```

**Def send_mail_rematch:**
 ```sh
    - Take in several parameters including the email of the owner, the owner's name, the stadium name, local team name, visitor team name, and an image path.
    - Compose an email message with these parameters and attach the image located at the provided path.
    - Use SMTP to send the email to the owner's email address.
    - Connect to Gmail's SMTP server using SSL and log in with the sender email and SMTP password.
    - Send the email.
```


## Authors

> [Anil](https://github.com/anilembel)

> [Andy](https://github.com/andygilet)

> [Florent](https://github.com/Flotchet)

> [Cyril](https://github.com/chipsi44)


<!-- CONTACT -->

## Contact

Please, contact any of the authors via GitHub.

## **License**

The Capshot project is licensed under the MIT License. See the **`LICENSE`** file for more information.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/CorentinChanet/challenge-collecting-data.svg?style=for-the-badge

[contributors-url]: [https://github.com/Flotchet/Odoo-Hackathon/graphs/contributors]
