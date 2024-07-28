from django.db import models


# Create your models here.
class Question(models.Model):
    question_number = models.IntegerField(default=0)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class CareerOption(models.Model):
    career_option_text = models.CharField(max_length=200)

    def __str__(self):
        return self.career_option_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # career = models.ForeignKey(CareerOption, on_delete=models.CASCADE)
    career = models.JSONField(None)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return (
            Question.objects.get(id=self.question_id).__str__()
            + ": "
            + self.choice_text
        )
