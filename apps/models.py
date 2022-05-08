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
        check_list = (
            ("data", literal_eval(self.data)),
            ("expected", (expected := literal_eval(self.expected))),
            *(("expected_value", value) for value in expected),
        )
        for name, value in check_list:
            if not isinstance(value, list):
                raise ValidationError(name + " должен быть списком")
        for value in expected:
            if not isinstance(value, list):
                raise ValidationError("expected должен быть списком списков")
        if "def get_result():" not in self.code:
            raise ValidationError(
                "code должна содержать функцию get_result(), ",
                "которая будет возвращать результат проверки кода после каждого запуска. ",
                "Результат будет сравниваться со списком ожиданий в expected."
            )
        super().clean()


class Solution(models.Model):
    folder = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="responses")
    resolve = models.TextField(blank=True, null=True)
