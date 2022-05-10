from django.db import models
from ast import literal_eval
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

DATA_ERROR_MESSAGE = "{} должен быть списком списков."
CODE_ERROR_MESSAGE = (
    "code должна содержать функцию get_result(), "
    "которая возвращает результат работы кода после каждого его запуска в виде списка. "
    "Результат будет сравниваться со списком ожиданий в поле expected."
)
ADVICE_ERROR_MESSAGE = "advices должен быть двухуровневым словарём или оставаться пустым"


class Task(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()
    task = models.TextField()
    code = models.TextField()
    call = models.CharField(max_length=300)
    data = models.CharField(max_length=300)
    default = models.TextField(blank=True, null=True)
    expected = models.CharField(max_length=300)
    advices = models.TextField(blank=True, null=True)
    is_pub = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]


class Solution(models.Model):
    folder = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="responses")
    resolve = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["id"]
