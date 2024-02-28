# Survey API

## Introduction

This is a Django REST framework-based API for managing surveys, questions, and their answers. It provides endpoints to create, retrieve, update, and delete surveys, questions, and their associated data.

**Note:** This API is intended for educational and testing purposes only. It is not suitable for use in live projects. All rights reserved. No one else is allowed to use it for live projects.

## Installation

1. Clone the repository:
   ```console
   git clone https://github.com/your_username/survey-api.git
   cd survey-api
   ```
3. (Optional) Create and activate a virtual environment:
   ```console
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```console
   pip install -r requirements.txt
   ```
   
## Running the API

To run the API server locally, follow these steps:

1. Migrate the database:
   ```console
   python manage.py migrate
   ```
3. Start the development server:
   ```console
   python manage.py runserver
   ```
   
The API will be accessible at `http://127.0.0.1:8000/`.


## Testing the API

Once the server is running, you can test the API endpoints using tools like Postman or cURL. Here is the sequence to follow for testing:

1. **User Registration** : Register a user using the `/signup/` endpoint.
2. **Authentication** : Obtain an authentication token using the `/api-token-auth/` endpoint with the registered user's credentials.
3. **Survey Operations** :

* Create a survey using the `/surveys/` endpoint.
* Retrieve, update, or delete surveys using the `/surveys/<survey_id>/` endpoint.

1. **Question Operations** :

* Create questions using the `/questions/` endpoint.
* Retrieve, update, or delete questions using the `/questions/<question_id>/` endpoint.

1. **Survey Question Operations** :

* Add questions to surveys using the `/survey-questions/` endpoint.
* Retrieve, update, or delete survey questions using the `/survey-questions/<survey_question_id>/` endpoint.

1. **Survey Question Answer Operations** :

* Record answers to survey questions using the `/survey-question-answers/` endpoint.
* Retrieve, update, or delete survey question answers using the `/survey-question-answers/<survey_question_answer_id>/` endpoint.
