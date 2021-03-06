import string
import secrets
import os
import importlib
import shutil

from ast import literal_eval
from django.core.paginator import Paginator
from django.db.models import ObjectDoesNotExist

from Trainer.settings import MEDIA_ROOT
from .models import Solution


def make_folder_name(prefix="temp_", symbols=string.ascii_letters + string.digits, length=10):
    return prefix + "".join(secrets.choice(symbols) for _ in range(length))


def check_directory(folder_name=None, base_directory=MEDIA_ROOT):
    if not folder_name:
        folder_name = make_folder_name()
    directory = "\\".join((base_directory, folder_name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def write_to_the_file(data, directory=None, file_name="py_file"):
    if not directory:
        directory = check_directory()
    path = "\\".join((directory, file_name + ".py"))
    with open(path, "w", encoding="UTF-8") as file:
        file.write(data)
    return path


def get_import(module_name, directory):
    spec = importlib.util.spec_from_file_location(module_name, directory)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_page(queryset, page, count=1):
    paginator = Paginator(queryset, count)
    return paginator.get_page(page)


def get_resolve(task, user):
    try:
        return Solution.objects.get(user=user, task=task)
    except ObjectDoesNotExist:
        return Solution.objects.create(folder=make_folder_name(), user=user, task=task)


class Result:
    def __init__(self, status=False, title="Не решено", message=[]):
        self.status = status
        self.title = title
        self.message = message


def get_matrix_length(matrix):
    return tuple(len(n) for n in matrix if isinstance(n, list))


def make_message(result, expected, advices):
    message = []
    if advices:
        for n, value in enumerate(result):
            if value != expected[n]:
                msg = []
                for m in range(len(value)):
                    if value[m] != expected[n][m]:
                        msg.append(advices[m][value[m]])
                message.append(f"Проверка №{n + 1}: " + "; ".join(msg))
    return message


def check_resolve(task, resolve):
    file_name, result, message = "resolve", [], Result()
    file_path = write_to_the_file("\n\n".join((resolve.resolve, task.code)), check_directory(resolve.folder), file_name)
    try:
        for data in literal_eval(task.data):
            resolving = get_import(file_name, file_path)
            getattr(resolving, task.call)(*data)
            result.append(getattr(resolving, "get_result")())
    except Exception as exc:
        if "block after function" in str(exc):
            message.title = "Напиши свой код ниже."
        else:
            message.title = "Функция не работает:"
            message.message = [exc.__repr__()[:57] + "..."]
    else:
        if result == (expected := literal_eval(task.expected)):
            message.status, message.title = True, (advices["Решено"] if (advices := literal_eval(task.advices)) and "Решено" in advices else "Решено")
        elif not get_matrix_length(result) == get_matrix_length(expected):
            message.title = "Неожиданный результат, возможно, стоит обратиться в поддержку"
        else:
            message.title, message.message = "Не решено:", make_message(result, expected, literal_eval(task.advices))
    finally:
        shutil.rmtree(os.path.join(MEDIA_ROOT, resolve.folder))
    return message
