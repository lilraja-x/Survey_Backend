from django.db import models

class QuestionType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=255) 
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text

class Survey(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.survey.name} - {self.question.text}"

class SurveyQuestionAnswer(models.Model):
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f"{self.survey_question.survey.name} - {self.survey_question.question.text} - {self.answer_text}"
