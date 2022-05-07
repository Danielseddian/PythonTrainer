from django.db import models
from ast import literal_eval
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()
    task = models.TextField()
    code = models.TextField()
    call = models.CharField(max_length=300)
    data = models.CharField(max_length=300)
    default = models.TextField(blank=True, null=True)
    expected = models.CharField(max_length=300)
    is_pub = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]

    def clean(self):
        for name, value in (("Data", literal_eval(self.data)), ("Expected", (expected := literal_eval(self.expected)))):
            if not isinstance(value, list):
                raise ValidationError(name + " должен быть списком")
        for value in expected:
            if not isinstance(value, list):
                raise ValidationError("Expected должен быть списком список")
        super().clean()


class Solution(models.Model):
    folder = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="responses")
    resolve = models.TextField(blank=True, null=True)
