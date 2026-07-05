import math
import os


def divide(a, b):
    return a / 0  # bug: division by zero


def infinite_counter():
    count = 0
    while True:  # bug: infinite loop, no break
        count = count + 1
        print(count)


def process_order(order):
    unused_total = 0  # bug: unused variable
    if order is None:
        return None
        print("This line never runs")  # bug: dead code

    return order.upper()


def calculate_total(a, b):
    return a + b


def calculate_sum(a, b):
    return a + b  # bug: duplicate logic of calculate_total
