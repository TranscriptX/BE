# TranscriptX - BE

TranscriptX is an application to assist people with document summarizer and audio/video transcription. The backend for the application is store in this repository. The backend service is created using FastAPI and MySQL.

This project is authored by:
- Alexander Brian Susanto
- Evan Santosa
- Henry Wunarsa
- Kelson

Steps to run this project locally:
- Clone this repository.
- Create an empty local MySQL database.
- Create ```.env``` file and copy all of the attributes in the ```.env.example``` file. You can do this by running ```cp .env.example .env``` in the terminal. Make sure to configure these properties properly on ```.env``` based on your local database server:
    - ```DB_USER```
    - ```DB_PASSWORD```
    - ```DB_HOST```
    - ```DB_PORT```
    - ```DB_NAME``` 
- Create a virtual environment and switch to that environment. To create a virtual environment, follow these steps:
    - ```python -m venv venv```
    - ```venv\Scripts\activate```
    - ```pip install fastapi uvicorn sqlmodel dotenv pymysql torch transformers```
- Run the app locally using ```uvicorn main:app --reload``` in the terminal. If you run the project for the first time, it will automatically create migrations. 
- If you run the project for the first time, after running the application, create a new terminal and fill the database with initial value with ```python -m databases.seed_database```.