# NeoFi-Notes-api


This is a simple Notes api built using Python,Flask.

## Features

- User Authentication: Users can register, log in.
- Notes Posts: Users can create, edit, share, view, version-history their blog posts.
- Database: Data is stored in a SQLite database using Flask-SQLAlchemy.

## clone the repositroy to your device
- Clone the repo :
      ```
    git clone https://github.com/abhishekkassetty/NeoFi-Notes-Api.git
    ```

## Steps to Install
- Install the required dependencies : 
    ```
    pip install -r requirements.txt
    ```
### Endpoints we have created.

- POST /login: Create a simple login view
- POST /signup: Create a single user sign up view
- POST /notes/create: Create a new note.
- GET /notes/{id}: Retrieve a specific note by its ID.
- POST /notes/share: Share the note with other users. 
- PUT /notes/{id}: Update an existing note.
- GET /notes/version-history/{id}: GET all the changes associated with the note. 

### Test Script(unittest cases)
- Run the python script to test the api's.
  ```
    python3 -m unittest app.tests.test_endpoints 
  ```

### steps to run the flask app
    ```
    flask run.py or flask run
      ```
```
## To test the create_note,get_note,share_note,update_note,notes_version_history make sure you pass the access_token generated when user login.
  ```


### ___All set! Now run the Flask Application!___

