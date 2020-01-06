from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse


class Test(models.Model):
    title = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='sources/', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tests:test_detail', kwargs={'pk': self.pk})


@receiver(post_save, sender=Test)
def import_questions_set(sender, instance, created, **kwargs):
    """Imports all questions from file uploaded"""
    if created:
        from .helpers import import_docxs
        try:
            import_docxs("media/" + instance.file.url)
        except Exception as e:
            print(e)
            pass


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
        score = self.correct / self.questions.count() * 10 if self.questions.count() != 0 else 0
        return round(score, 2)

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
