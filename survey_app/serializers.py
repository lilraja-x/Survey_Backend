from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import QuestionType, Question, QuestionChoice, Survey, SurveyQuestion, SurveyQuestionAnswer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'

class QuestionChoiceSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)

    class Meta:
        model = QuestionChoice
        fields = ['id', 'question', 'question_text', 'choice_text']

    def validate(self, data):
        question = data.get('question')
        question_type = question.question_type
        question_type_name = question_type.name
        if question_type_name != 'dropdown':
            raise serializers.ValidationError("Choices can only be added to questions with dropdown type.")

        return data
            
            
class QuestionWithChoicesSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    question_text = serializers.CharField()
    choices = QuestionChoiceSerializer(many=True)

class QuestionSerializer(serializers.ModelSerializer):
    question_type_name = serializers.CharField(source='question_type.name', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'question_type_name']

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

class SurveyQuestionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=True)

    class Meta:
        model = SurveyQuestion
        fields = ['id', 'survey', 'question']

    def get_question(self, obj):
        question = obj.question
        question_data = {
            'id': question.id,
            'text': question.text,
            'question_type_name': question.question_type.name
        }
        if question.question_type.name == 'dropdown':
            choices = QuestionChoice.objects.filter(question=question)
            question_data['choices'] = QuestionChoiceSerializer(choices, many=True).data
        return question_data
        
class SurveyQuestionAnswerSerializer(serializers.ModelSerializer):
    survey_question_text = serializers.CharField(source='survey_question.question.text', read_only=True)
    survey_question_type_name = serializers.CharField(source='survey_question.question.question_type.name', read_only=True)
    choices = serializers.SerializerMethodField()
    class Meta:
        model = SurveyQuestionAnswer
        fields = ['survey_question', 'survey_question_text', 'survey_question_type_name', 'answer_text', 'choices']
        
    def create(self, data):
        survey_question = data.get('survey_question')

        if isinstance(survey_question, SurveyQuestion):
            survey_question_id = survey_question.pk
        else:
            survey_question_id = survey_question

        survey_question_instance = get_object_or_404(SurveyQuestion, pk=survey_question_id)
        data['survey_question'] = survey_question_instance

        return SurveyQuestionAnswer.objects.create(**data)

    def get_choices(self, obj):
        choices = []
        if obj.survey_question.question.question_type.name == 'dropdown':
            question_choices = obj.survey_question.question.questionchoice_set.all()
            for choice in question_choices:
                choices.append({
                    'id': choice.id,
                    'choice_text': choice.choice_text
                })
        return choices
