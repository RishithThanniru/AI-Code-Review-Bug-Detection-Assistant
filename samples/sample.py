import math
import os

class Student:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(self.name)


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


print(add(5, 7))