from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=200)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True,
                             blank=True)

    class Meta:
        unique_together = ['title', 'test']

    def __str__(self):
        return self.title
    
    def correct_choice(self):
        return self.choice_set.filter(correct=True)


class Choice(models.Model):
    title = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Attempt(models.Model):
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    correct = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)
    questions = models.ManyToManyField(Question)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + str(self.started_at)

    def calculate_correct(self):
        self.correct = self.aswer_set.filter(choice__correct=True).count()
        self.save()
        return self.correct

    def null(self):
        return self.aswer_set.filter(choice__isnull=True).count()

    def wrong(self):
        return self.aswer_set.filter(choice__correct=False).count()

    def score(self):
        return round(self.correct / self.questions.count(), 2) * 10 if self.questions.count() != 0 else 0

    def duration(self):
        import arrow
        return arrow.get(self.ended_at) - arrow.get(self.started_at)


class Aswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True,
                                 blank=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True,
                               blank=True)
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, null=True,
                                blank=True)
