from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import QuestionType, Question, QuestionChoice, Survey, SurveyQuestion, SurveyQuestionAnswer
from .serializers import QuestionTypeSerializer, QuestionSerializer, QuestionChoiceSerializer, QuestionWithChoicesSerializer, SurveySerializer, SurveyQuestionSerializer, SurveyQuestionAnswerSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Question type created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class QuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Question added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class QuestionChoiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class QuestionChoiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class QuestionChoiceListAPIView(generics.ListAPIView):
    serializer_class = QuestionChoiceSerializer

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return QuestionChoice.objects.filter(question_id=question_id)

class QuestionWithChoicesAPIView(generics.RetrieveAPIView):
    serializer_class = QuestionWithChoicesSerializer
    
    def retrieve(self, request, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        queryset = QuestionChoice.objects.filter(question_id=question_id)
        question_text = queryset.first().question.text
        choices = queryset.values('id', 'choice_text')
        response_data = {
            'question': question_id,
            'question_text': question_text,
            'choices': choices
        }
        return Response(response_data)

class SurveyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Survey created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SurveyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SurveyQuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer

    def create(self, request, *args, **kwargs):
        try:
            survey_id = request.data.get('survey')
            question_id = request.data.get('question')
            if not Survey.objects.filter(pk=survey_id).exists():
                return Response({"error": "Survey does not exist."}, status=status.HTTP_404_NOT_FOUND)
            if not Question.objects.filter(pk=question_id).exists():
                return Response({"error": "Question does not exist."}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Survey question added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'error': str(e)})


class SurveyQuestionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SurveyQuestionAnswerListCreateAPIView(generics.ListCreateAPIView):
    queryset = SurveyQuestionAnswer.objects.all()
    serializer_class = SurveyQuestionAnswerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        survey_question_id = request.data.get('survey_question')
        answer_text = request.data.get('answer_text')

        if not survey_question_id or not answer_text:
            return Response({"error": "Both survey_question and answer_text are required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'survey_question': survey_question_id, 'answer_text': answer_text})

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Answer added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurveyQuestionAnswerRetrieveAPIView(generics.RetrieveAPIView):
    queryset = SurveyQuestionAnswer.objects.all()
    serializer_class = SurveyQuestionAnswerSerializer
    lookup_url_kwarg = 'question_id'

    def retrieve(self, request, *args, **kwargs):
        question_id = self.kwargs.get(self.lookup_url_kwarg)

        survey_answer = get_object_or_404(self.queryset, survey_question=question_id)

        serializer = self.get_serializer(survey_answer)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SurveyQuestionAnswerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurveyQuestionAnswer.objects.all()
    serializer_class = SurveyQuestionAnswerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
