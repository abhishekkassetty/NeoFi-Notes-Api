# NeoFi-Notes-api


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
## To test the create_note,get_note,share_note,update_note,notes_version_history make sure you pass the access_token generated when user login.



### ___All set! Now run the Flask Application!___

