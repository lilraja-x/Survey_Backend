from django.urls import path
from .views import *
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('signup/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
    
    # URLs for QuestionType
    path('question-types/', QuestionTypeListCreateAPIView.as_view(), name='questiontype-list'),
    path('question-types/<int:pk>/', QuestionTypeRetrieveUpdateDestroyAPIView.as_view(), name='questiontype-detail'),

    # URLs for Question
    path('questions/', QuestionListCreateAPIView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDestroyAPIView.as_view(), name='question-detail'),

    # URLs for QuestionChoice
    path('question-choices/', QuestionChoiceListCreateAPIView.as_view(), name='questionchoice-list'),
    path('question-choices/<int:pk>/', QuestionChoiceRetrieveUpdateDestroyAPIView.as_view(), name='questionchoice-detail'),

    # URLs for Survey
    path('surveys/', SurveyListCreateAPIView.as_view(), name='survey-list'),
    path('surveys/<int:pk>/', SurveyRetrieveUpdateDestroyAPIView.as_view(), name='survey-detail'),

    # URLs for SurveyQuestion
    path('survey-questions/', SurveyQuestionListCreateAPIView.as_view(), name='surveyquestion-list'),
    path('survey-questions/<int:pk>/', SurveyQuestionRetrieveUpdateDestroyAPIView.as_view(), name='surveyquestion-detail'),

    # URLs for SurveyQuestionAnswer
    path('survey-question-answers/', SurveyQuestionAnswerListCreateAPIView.as_view(), name='surveyquestionanswer-list'),
    path('survey-question-answers/<int:pk>/', SurveyQuestionAnswerRetrieveUpdateDestroyAPIView.as_view(), name='surveyquestionanswer-detail'),
]
