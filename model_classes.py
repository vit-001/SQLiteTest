class Exportable:
    def export(self):
        print('Not implemented')

    def export_csv(self, fd):
        print('Not implemented')

class Set(Exportable):
    def __init__(self):
        self.weight=0.0
        self.repeats=0
        self.comment=''
        self.anydata=''

    def export(self):
        print('    ',self.weight,'X', self.repeats, self.anydata, self.comment)

class Exercise(Exportable):
    def __init__(self, name):
        self.name=name
        self.sets=[]
        self.current_set=None

    def new_set(self)->Set:
        self.current_set=Set()
        self.sets.append(self.current_set)
        return self.current_set

    def export(self):
        print('  ',self.name)
        for set in self.sets:
            # set.export()
            print('%10.1f' % set.weight, end=' ')
        print()
        for set in self.sets:
            # set.export()
            print('%10d' % set.repeats, end=' ')
        print()

        t=''
        for set in self.sets:
            if set.comment:
                t=t+set.comment
        if t:
            print(t)

        t=''
        for set in self.sets:
            if set.anydata:
                t=t+set.anydata
        if t:
            print(t)

    def export_csv(self, fd):
        print('  ',self.name, file=fd)
        for set in self.sets:
            # set.export()
            print(('%10.1f;' % set.weight).replace('.',','), end=' ', file=fd)
        print(file=fd)
        for set in self.sets:
            # set.export()
            print('%10d;' % set.repeats, end=' ', file=fd)
        print(file=fd)

        t=''
        for set in self.sets:
            if set.comment:
                t=t+set.comment
        if t:
            print(t, file=fd)

        t=''
        for set in self.sets:
            if set.anydata:
                t=t+set.anydata
        if t:
            print(t, file=fd)

class Workout(Exportable):
    def __init__(self, date, name):
        self.date=date
        self.name=name
        self.excercises=[]
        self.current_exercise=None

    def new_exercise(self, name)->Exercise:
        self.current_exercise=Exercise(name)
        self.excercises.append(self.current_exercise)
        return self.current_exercise

    def export(self):
        print(self.date, self.name)
        for ex in self.excercises:
            ex.export()

    def export_csv(self, fd):
        print(self.date,';', self.name, file=fd)
        for ex in self.excercises:
            ex.export_csv(fd)

class Base(Exportable):
    def __init__(self):
        self.days=[]
        self.current_workout=None

    def new_workout(self, date, name)->Workout:
        self.current_workout=Workout(date, name)
        self.days.append(self.current_workout)
        return self.current_workout

    def export(self):
        for wo in self.days:
            wo.export()

    def export_csv(self, fd):
        for wo in self.days:
            wo.export_csv(fd)