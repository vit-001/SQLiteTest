# -*- coding: utf-8 -*-
__author__ = 'Vit'


if __name__ == "__main__":
    pass


class Set():
    def __init__(self):
        self.weight = 0.0
        self.repeats = 0
        self.comment = ''
        self.anydata = ''


class Exercise():
    def __init__(self, name):
        self.name = name
        self.sets = []
        self.current_set = None

    def new_set(self) -> Set:
        self.current_set = Set()
        self.sets.append(self.current_set)
        return self.current_set


class Workout():
    def __init__(self, date, name):
        self.date = date
        self.name = name
        self.excercises = []
        self.current_exercise = None

    def new_exercise(self, name) -> Exercise:
        self.current_exercise = Exercise(name)
        self.excercises.append(self.current_exercise)
        return self.current_exercise


class Base():
    def __init__(self):
        self.days = []
        self.current_workout = None

    def new_workout(self, date, name) -> Workout:
        self.current_workout = Workout(date, name)
        self.days.append(self.current_workout)
        return self.current_workout