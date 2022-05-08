# Сломанная клавиатура и небольшая ошибка.
Галина Гренкина учится в школе программирования и является лучшей ученицей курса, у неё по всем предметам оценки только: «Отлично». Недавно ей дали сложное домашнее задание: вместе с друзьями написать программу, которая состоит из нескольких частей.

Друзья договорились, что каждый будет писать свою часть, но Галина знает, что у Ромы Слизнева треснула клавиатура, поэтому иногда он допускает ошибки, пропуская некоторые буквы. А поменять клавиатуру Рома не решается, потому что для этого необходимо пойти к школьному завхозу, Филипу Августовичу, который отличается скверным характером.

Галина предложила Слизневу посмотреть его функцию, abra_cadabra(), и исправить ошибки, если они есть, но он отказался, потому что считает, что Гренкина снова будет читать ему нотации. Тогда подруга решила схитрить и написать свою версию Роминой функции, которая будет называться focus_pocus(), а чтобы проучить друга, ей нужно сначала вызвать его функцию и, если она выдаст ошибку, напечатать об этом сообщение: "Рома, у тебя в программе ошибка!".

Так как у Ромы не печатаются некоторые буквы, то точно возникнет ошибка «KeyError», когда он попытается извлечь значения из словаря magic_dictionary. Галина слишком занята, поэтому попросила вас написать небольшой код, чтобы проверить функцию abra_cadabra() и напечатать предупреждение, если возникнет ошибка, а затем вызвать её функцию, focus_pocus().

## задача

Написать функцию make_magic_replace(), которая принимает переменную magic_dictionary, вызывает функцию abra_cadabra() и передаёт в неё эту переменную. Если работа функции вызывает ошибку KeyError необходимо перехватить её, напечатать сообщение «Рома, у тебя в программе ошибка!», а затем вызывать функцию focus_pocus() и передать переменную в неё.

## сode
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

## call
make_magic_replace

## data
[1, 0, 2]

## default
def make_magic_replace(magic_dictionary):
    # Напиши свой код ниже

## expected
[[1, 0], [2, 1], [1, 0]]

## advices
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