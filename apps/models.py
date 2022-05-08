from django.db import models
from ast import literal_eval
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

DATA_ERROR_MESSAGE = "{} должен быть списком."
EXPECTED_VALUE_ERROR_MESSAGE = "expected должен быть списком списков с ожидаемыми значениями."
CODE_ERROR_MESSAGE = (
    "code должна содержать функцию get_result(), "
    "которая будет возвращать список значений с результатами работы кода после каждого его запуска. "
    "Результат будет сравниваться со списком ожиданий в поле expected."
)
ADVICE_ERROR_MESSAGE = (
    "advice должен быть двухуровневым словарём: {ошибка: {вариация: сообщение}}, также поле можно оставить пустым"
)


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

    def clean(self):
        try:
            expected = literal_eval(self.expected)
        except ValueError:
            raise ValidationError(EXPECTED_VALUE_ERROR_MESSAGE)
        try:
            advices = literal_eval(self.advices)
        except SyntaxError:
            raise ValidationError(ADVICE_ERROR_MESSAGE)
        check_list = (
            ("data", literal_eval(self.data)),
            ("expected", expected),
        )
        for name, value in check_list:
            if not isinstance(value, list):
                raise ValidationError(DATA_ERROR_MESSAGE.format(name))
        for value in expected:
            if not isinstance(value, list):
                raise ValidationError(EXPECTED_VALUE_ERROR_MESSAGE)
        if "def get_result():" not in self.code:
            raise ValidationError(CODE_ERROR_MESSAGE)
        if self.advices and not isinstance(advices, dict):
            raise ValidationError(ADVICE_ERROR_MESSAGE)
        for value in advices.values():
            if not isinstance(value, dict):
                raise ValidationError(ADVICE_ERROR_MESSAGE)
        super().clean()


class Solution(models.Model):
    folder = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="responses")
    resolve = models.TextField(blank=True, null=True)
