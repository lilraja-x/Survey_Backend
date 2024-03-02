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

1. **User Registration** : Register a user using the `/api/signup/` endpoint.
2. **Authentication** : Obtain an authentication token using the `/api/api-token-auth/` endpoint with the registered user's credentials.
3. **Survey Operations** :

* Create a survey using the `/api/surveys/` endpoint.
* Retrieve, update, or delete surveys using the `/api/surveys/<survey_id>/` endpoint.

4. **Question Operations** :

* Create questions using the `/api/questions/` endpoint.
* Retrieve, update, or delete questions using the `/api/questions/<question_id>/` endpoint.

5. **Question Choice Operations** :

* Add questions to surveys using the `/api/question-choices/` endpoint.
* Retrieve, update, or delete question choices using the `/api/question-choices/<question_choice_id>/` endpoint.
* Retrieve questions with their choices using the `/api/question-with-choices/<question_id>/` endpoint.

6. **Survey Question Operations** :

* Add questions to surveys using the `/api/survey-questions/` endpoint.
* Retrieve, update, or delete survey questions using the `/api/survey-questions/<survey_question_id>/` endpoint.

7. **Survey Question Answer Operations** :

* Record answers to survey questions using the `/api/survey-question-answers/` endpoint.
* Retrieve, update, or delete survey question answers using the `/api/survey-question-answers/<survey_question_answer_id>/` endpoint.
* Retrieve answers for a specific question against question id using the `/api/survey-question-answers/get-question/<int:question_id>/` endpoint.


## NOTE
* For further clarification visit postman collection:
  
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/27253326-a1ce3ab2-27c0-4928-8e9a-33b30ef46dd6?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D27253326-a1ce3ab2-27c0-4928-8e9a-33b30ef46dd6%26entityType%3Dcollection%26workspaceId%3Dc172560e-d4a8-456e-b702-879831cbc947)
