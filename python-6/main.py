from abc import ABC, abstractmethod

class Department:
    def __init__(self, name, code):
        self.name = name
        self.code = code


class Employee(ABC):

    _hours = 8

    def __init__(self):
        raise TypeError()

    @property
    def code(self):
        return self._code
    @code.setter
    def code(self, value):
        self._code = value
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    @property
    def salary(self):
        return self._salary
    @salary.setter
    def salary(self, value):
        self._salary = value

    @abstractmethod
    def calc_bonus(self):
        pass

    @abstractmethod
    def get_hours(self):
        pass

class Manager(Employee):
    def __init__(self, code, name, salary):
        self.code = code
        self.name = name
        self.salary = salary
        self._departament = Department('managers', 1)

    def get_departament(self):
        return self._departament.name

    def set_departament(self, value):
        self._departament.name = value

    def calc_bonus(self):
        return self.salary * 0.15

    def get_hours(self):
        return self._hours


class Seller(Manager, Employee):
    def __init__(self, code, name, salary):
        self.code = code
        self.name = name
        self.salary = salary
        self._departament = Department('sellers', 2)
        self._sales = 0

    def get_sales(self):
        return self._sales

    def put_sales(self, value):
        self._sales += value

    def calc_bonus(self):
        return self._sales * 0.15
