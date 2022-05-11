### name
Женя Слизнева и небольшая просьба.

### text
Младшая сестра Ромы Слизнева, Женя, тоже поступила в школу программирования. По средам у них проходят занятия по математике, и она придумала несколько методов для решения задач. Проблема в том, что они не всегда работают, и возникают ошибки, поэтому каждый раз ей приходится вручную проверять, какой метод работает, а какой - нет.

Недавно Женя узнала, что вы можете написать программу, которая находит ошибки, и попросила вас о помощи.

### task
Функция calculate_equation() принимает переменную equation_number и должна передать её, а также номер метода по очереди от 1 до 5 в функцию cast_magic_methods(). Если работа функции вызывает математическую ошибку необходимо перехватить её и добавить номер метода в список false_methods, а если работа выполняется - в список true_methods. В конце нужно вывести сообщение: 

"Метод № {method_number} {result} для задачи № {equation_number}"

- <equation_number> и <method_number> - это переменные, которые получает функция calculate_equation(),
- <result> - "работает" или "не работает" в зависимости от результата

### сode
result = [0, 0]
magic_book = {"leviosa": 1, "avis": 2, "lumos": 3, "descendo": 4}

def print(string):
    if string == "Рома, у тебя в программе ошибка!":
        result[1] = 1
    else:
        result[1] = 2


def get_result():
    return result


def abra_cadabra(i):
    keys = ["lefiosa", "avis", "lumos", "desendo"]
    magic_book[keys[i]]
    result[0] = 1


def focus_pocus(i):
    keys = ["leviosa", "avis", "lumos", "descendo"]
    magic_book[keys[i]]
    result[0] = 2

### call
make_magic_replace

### data
[[1], [0], [2]]

### default
def make_magic_replace(magic_dictionary):
    # Измени функцию, чтобы она проверяла работу 

### expected
[[1, 0], [2, 1], [1, 0]]

### advices
{
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