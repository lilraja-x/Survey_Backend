from django.urls import path
from .views import *
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('signup/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
    
    path('question-types/', QuestionTypeListCreateAPIView.as_view(), name='questiontype-list'),
    path('question-types/<int:pk>/', QuestionTypeRetrieveUpdateDestroyAPIView.as_view(), name='questiontype-detail'),
    
    path('questions/', QuestionListCreateAPIView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDestroyAPIView.as_view(), name='question-detail'),
    
    path('question-choices/', QuestionChoiceListCreateAPIView.as_view(), name='questionchoice-list'),
    path('question-choices/<int:pk>/', QuestionChoiceRetrieveUpdateDestroyAPIView.as_view(), name='questionchoice-detail'),
    path('question-with-choices/<int:question_id>/', QuestionWithChoicesAPIView.as_view(), name='question-with-choices'),
    
    path('surveys/', SurveyListCreateAPIView.as_view(), name='survey-list'),
    path('surveys/<int:pk>/', SurveyRetrieveUpdateDestroyAPIView.as_view(), name='survey-detail'),
    
    path('survey-questions/', SurveyQuestionListCreateAPIView.as_view(), name='surveyquestion-list'),
    path('survey-questions/<int:pk>/', SurveyQuestionRetrieveUpdateDestroyAPIView.as_view(), name='surveyquestion-detail'),
    
    path('survey-question-answers/', SurveyQuestionAnswerListCreateAPIView.as_view(), name='surveyquestionanswer-list'),
    path('survey-question-answers/<int:pk>/', SurveyQuestionAnswerRetrieveUpdateDestroyAPIView.as_view(), name='surveyquestionanswer-detail'),
    path('survey-question-answers/get-question/<int:question_id>/', SurveyQuestionAnswerRetrieveAPIView.as_view(), name='survey_question_answer_retrieve'),
]
