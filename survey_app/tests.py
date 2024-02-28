from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from .models import QuestionType, Question, QuestionChoice, Survey, SurveyQuestion, SurveyQuestionAnswer

class SurveyAppTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.token, created = Token.objects.get_or_create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.question_type = QuestionType.objects.create(name="Text")
        self.question = Question.objects.create(text="What is your name?", question_type=self.question_type)
        self.question_choice = QuestionChoice.objects.create(question=self.question, choice_text="Option 1")
        self.survey = Survey.objects.create(name="Sample Survey", description="Test survey description")
        self.survey_question = SurveyQuestion.objects.create(survey=self.survey, question=self.question)
        self.survey_question_answer = SurveyQuestionAnswer.objects.create(survey_question=self.survey_question, answer_text="John Doe")

    def test_question_type_creation(self):
        self.assertEqual(QuestionType.objects.count(), 1)
        self.assertEqual(QuestionType.objects.first().name, "Text")

    def test_question_creation(self):
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.first().text, "What is your name?")

    def test_question_choice_creation(self):
        self.assertEqual(QuestionChoice.objects.count(), 1)
        self.assertEqual(QuestionChoice.objects.first().choice_text, "Option 1")

    def test_survey_creation(self):
        self.assertEqual(Survey.objects.count(), 1)
        self.assertEqual(Survey.objects.first().name, "Sample Survey")

    def test_survey_question_creation(self):
        self.assertEqual(SurveyQuestion.objects.count(), 1)
        self.assertEqual(SurveyQuestion.objects.first().survey.name, "Sample Survey")
        self.assertEqual(SurveyQuestion.objects.first().question.text, "What is your name?")

    def test_survey_question_answer_creation(self):
        self.assertEqual(SurveyQuestionAnswer.objects.count(), 1)
        self.assertEqual(SurveyQuestionAnswer.objects.first().survey_question.survey.name, "Sample Survey")
        self.assertEqual(SurveyQuestionAnswer.objects.first().survey_question.question.text, "What is your name?")
        self.assertEqual(SurveyQuestionAnswer.objects.first().answer_text, "John Doe")

    def test_question_type_api(self):
        response = self.client.get('/api/question-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Text")

    def test_question_api(self):
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], "What is your name?")

    def test_survey_api(self):
        response = self.client.get('/api/surveys/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Sample Survey")

    def test_create_question(self):
        data = {
            "text": "What is your age?",
            "question_type": self.question_type.id
        }
        response = self.client.post('/api/questions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_update_question(self):
        data = {
            "text": "What is your age?",
            "question_type": self.question_type.id
        }
        response = self.client.put(f'/api/questions/{self.question.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Question.objects.get(id=self.question.id).text, "What is your age?")

    def test_delete_question(self):
        response = self.client.delete(f'/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)

    def test_create_survey(self):
        data = {
            "name": "New Survey",
            "description": "This is a new survey"
        }
        response = self.client.post('/api/surveys/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 2)

    def test_update_survey(self):
        data = {
            "name": "Updated Survey",
            "description": "This is an updated survey"
        }
        response = self.client.put(f'/api/surveys/{self.survey.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Survey.objects.get(id=self.survey.id).name, "Updated Survey")

    def test_delete_survey(self):
        response = self.client.delete(f'/api/surveys/{self.survey.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Survey.objects.count(), 0)

    def test_survey_question_creation(self):
        response = self.client.post('/api/survey-questions/', data={'survey': self.survey.id, 'question': self.question.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SurveyQuestion.objects.count(), 2)

    def test_survey_question_answer_creation(self):
        response = self.client.post('/api/survey-question-answers/', data={'survey_question': self.survey_question.id, 'answer_text': 'Test answer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SurveyQuestionAnswer.objects.count(), 2)

    def test_invalid_token_access(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token InvalidToken')
        response = self.client.get('/api/surveys/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_invalid_survey_creation(self):
        response = self.client.post('/api/surveys/', data={'name': '', 'description': 'Test description'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_empty_response(self):
        response = self.client.post('/api/survey-question-answers/', data={'survey_question': self.survey_question.id, 'answer_text': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_survey_response_integration(self):
        survey_response = self.client.post('/api/surveys/', data={'name': 'Integration Survey', 'description': 'Integration Survey Description'}, format='json')
        survey_id = survey_response.data['id']
        questions = [self.question.id, self.question.id]
        for question_id in questions:
            self.client.post('/api/survey-questions/', data={'survey': survey_id, 'question': question_id}, format='json')

        answers = ['Answer 1', 'Answer 2']
        for index, question_id in enumerate(questions):
            self.client.post('/api/survey-question-answers/', data={'survey_question': question_id, 'answer_text': answers[index]}, format='json')

        response = self.client.get(f'/api/surveys/{survey_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for index, question_id in enumerate(questions):
            self.assertEqual(response.data['survey_questions'][index]['question'], question_id)
            self.assertEqual(response.data['survey_questions'][index]['answers'][0]['answer_text'], answers[index])

    def test_invalid_request(self):
        response = self.client.post('/api/invalid-endpoint/', data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)