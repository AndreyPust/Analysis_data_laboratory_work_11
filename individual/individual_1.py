#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from multiprocessing import Process, Manager
import sympy as sp

"""
Необходимо с использованием многопоточности для заданного значения x найти сумму ряда S 
с точностью члена ряда по абсолютному значению и произвести сравнение полученной суммы с 
контрольным значением функции y(x) для двух бесконечных рядов.
Необходимо доработать программу лабораторной работы 2.23, организовав вычисления значений 
двух функций в отдельных процессах.
Вариант 26, задачи 1 и 2.
"""

E = 1e-7  # Точность


def series_1(x, eps, results):
    """
    Функция вычисления суммы ряда задачи №1 (x = 1).
    """
    s = 0
    n = 0
    while True:
        term = x**n * sp.log(3)**n / math.factorial(n)
        if abs(term) < eps:
            break
        s += term
        n += 1
    results["series_1"] = s


def series_2(x, eps, results):
    """
    Функция вычисления суммы ряда задачи №2 (x = 0,7).
    """
    s = 0
    n = 0
    while True:
        term = x**n
        if abs(term) < eps:
            break
        s += term
        n += 1
    results["series_2"] = s


def main():
    """
    Главная функция программы.
    """
    with Manager() as manager:
        results = manager.dict({"series1": 0, "series2": 0})

        x1 = 1
        control_1 = 3**x1

        x2 = 0.7
        control_2 = 1/(1-x2)

        # Создание процессов.
        process_1 = Process(target=series_1, args=(x1, E, results))
        process_2 = Process(target=series_2, args=(x2, E, results))

        process_1.start()
        process_2.start()

        process_1.join()
        process_2.join()

        sum_1 = results["series_1"]
        sum_2 = results["series_2"]

        print(f"x1 = {x1}")
        print(f"Сумма ряда 1: {sum_1:.7f}")
        print(f"Контрольное значение 1: {control_1:.7f}")
        print(f"Совпадение 1: {round(sum_1, 7) == round(control_1, 7)}")

        print(f"x2 = {x2}")
        print(f"Сумма ряда 2: {sum_2:.7f}")
        print(f"Контрольное значение 2: {control_2:.7f}")
        print(f"Совпадение 2: {round(sum_2, 7) == round(control_2, 7)}")


if __name__ == "__main__":
    main()
