# GENREIZZ
## Video Demo:
## Description:
Genreizz is a web application using Python Flask, Jinja, and SQLite that recommends books to users based on their reading history, utilizing the Google Books API for data and featuring a frontend built with HTML, CSS, JavaScript, and jQuery.
## Usage:
First, you should **Fork/Clone** this repository.

Then, you should install all required libraries for this application to run by executing the following command in the terminal:

    pip install -r requirements.txt

To start the web application server, in the project directory, type the following command in your terminal:

    flask run

Click the link shown in the terminal to access the application.

If you are a new user, you will need to register first. To do so, simply click on the `Register` option in the navbar menu. After successfully registering, you should see the `Best Sellers` page where you can find the best-selling books.

In the navbar, you can find the `search` field where you can search books by its name and can add books to your bookshelf and readlist accordingly.

There is a offcanvas navbar using which you can navigate throughout the application. You can find the options `Best Sellers`, `Get Recommendations` _where you can get recommendations based on your reading history_, `Bookshelf` _where you can see your reading histroy_, `Readlist` _where you will find the books that you want to read in the future._

You are most welcome to play around in the application.

Finally in the offcanvas navbar, you can find the `Log Out` button clicking which you can log out from the application. The next time you want to use the application, you need to first log in using your credentials. However, if you simply close the tab or shut down the server without logging out, you will not need to log in again the next time you use it.

If you want to close the server simply press `Ctrl+C` in the terminal.

## Files and Folders:

### ***1. helpers.py***
This is the main project file that does most of the heavy lifting in the application including reading API responses, formatting API response, generating recommendations, checking if user is logged in.

You can run this file by typing the following command in your project directory:

    python3 helpers.py

### ***2. app.py***
app.py contains the Flask framework including routes, session configurations and database management. On running the command

    flask run

the app.py file is automatically run as the server using Flask framework.

### ***3. tables.sql***
This is the file that contains the schema of the database.

### ***4. genreizz.db***
This is the database of the application that stores hashed user credentials and book information.

### ***5. templates***
The templates folder contains the html templates that are rendered using Flask in app.py

### ***6. static***
The static folder contains all the static files like the `CSS` file, `Font` files, `JavaScript` files, `favicon` file and more.

##
> <span style="color:blue">**ℹ️ Note:**</span>  
> All the book data shown in this application is provided by the Google Books API and I do not own any of this data.
