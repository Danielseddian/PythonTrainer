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
    def __init__(self, status=False, title="Не решено", message=None):
        self.message = message
        self.title = title
        self.status = status


def get_matrix_length(matrix):
    return tuple(len(n) for n in matrix if isinstance(n, list))


def make_message(result, expected, dictionary):
    advices = {
        0: {
            0: "Похоже, не сработала ни одна из функций, abra_cadabra() или focus_pocus()",
            1: "Должно было сработать исключение для функции abra_cadabra()",
            2: "Сработало лишнее исключение для функции abra_cadabra()",
        },
        1: {
            0: "Рома не получил сообщения об ошибке, необходимо использовать print()",
            1: "Здесь всё должно работать правильно, сообщение об ошибке лишнее",
            2: "Текст сообщения об ошибке не соответствует",
        },
    }
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
    file_name = "resolve"
    file_path = write_to_the_file("\n\n".join((resolve.resolve, task.code)), check_directory(resolve.folder), file_name)
    result = []
    for data in literal_eval(task.data):
        try:
            resolving = get_import(file_name, file_path)
            getattr(resolving, task.call)(data)
            result.append(getattr(resolving, "get_result")())
        except Exception as exc:
            shutil.rmtree(os.path.join(MEDIA_ROOT, resolve.folder))
            return Result(False, "Функция не работает:", [str(exc)[:57] + "..."])
    shutil.rmtree(os.path.join(MEDIA_ROOT, resolve.folder))
    if not get_matrix_length(result) == get_matrix_length(expected := literal_eval(task.expected)):
        return Result(False, "Неожиданный результат, возможно, стоит обратиться в поддержку", [])
    elif result == expected:
        return Result(True, "Решено", [])
    else:
        message = make_message(result, expected, task)
        return Result(False, "Не решено:", message)
