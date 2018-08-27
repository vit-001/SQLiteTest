from local_setting import LocalSetting, fft

class Exportable:
    def export(self):
        print('Not implemented')

    def export_csv(self, fd):
        print('Not implemented')

class Exercises:
    def __init__(self):
        self.base=dict()

    def add(self, name:str, value:float, repeat:int):
        old=self.base.get(name,{'max':0.0, 'repeat':1})
        if value<old['max']:
            return

        if value>old['max']:
            old['max']=value
            old['repeat']=repeat
        else:
            if repeat>old['repeat']:
                old['repeat']=repeat
            else:
                return
        self.base[name] = old


    def output(self):
        for name,data in self.base.items():
            m=data['max']
            k=data['repeat']
            print(name, m,'x',k, '%1.1f' % (m*(36/(37-k))))

    def get_1PM(self, name:str)->float:
        ex=self.base.get(name,{'max':0.0, 'repeat':1})
        m = ex['max']
        k = ex['repeat']
        return (m*(36/(37-k)))

class Statistic:
    max_repeat=17
    exercises=Exercises()
    def stat(self):
        print('Not implemented')

class Set(Exportable,Statistic):
    def __init__(self):
        self.weight=0.0
        self.repeats=0
        self.comment=''
        self.anydata=''

    def export(self):
        print('    ',self.weight,'X', self.repeats, self.anydata, self.comment)



class Exercise(Exportable,Statistic):
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
        table_width=Statistic.max_repeat+3
        first_line=['' for i in range(table_width)]
        second_line = ['' for i in range(table_width)]
        third_line = ['' for i in range(table_width)]
        use_third_line=False

        first_line[2]=self.name
        i=3

        for set in self.sets:
            first_line[i]=fft(set.weight)
            second_line[i]='%10d' % set.repeats

            if set.anydata:
                third_line[i]=set.anydata
                use_third_line=True
            if set.comment:
                third_line[i]=third_line[i]+set.comment
                use_third_line=True

            i=i+1

        for item in first_line:
            print(item, end=';', file=fd)

        print('V=;"=СУММПРОИЗВ(RC[-18]:RC[-2];R[1]C[-18]:R[1]C[-2])"', end=';', file=fd)
        print('Ио=;"=RC[2]/R[1]C[2]"', end=';', file=fd)
        print('ср вес=;"=RC[-4]/R[1]C[-4]"', end=';', file=fd)
        print('КО=;"=RC[-4]*R[1]C[-6]"', file=fd)


        # , fft(Statistic.exercises.get_1PM(self.name)), file=fd)

        for item in second_line:
            print(item, end=';', file=fd)

        print('КПШ=;"=СУММ(RC[-18]:RC[-2])";;', end=';', file=fd)
        print('1ПМ=;', fft(Statistic.exercises.get_1PM(self.name)), file=fd)

        if use_third_line:
            for item in third_line:
                print(item, end=';', file=fd)
            print(file=fd)


    def stat(self):
        for item in self.sets:
            Statistic.exercises.add(self.name,item.weight, item.repeats)

class Workout(Exportable, Statistic):
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

    def stat(self):
        # print(self.date, self.name)
        for ex in self.excercises:
            ex.stat()

class Base(Exportable, Statistic):
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

    def stat(self):
        for wo in self.days:
            wo.stat()
        Statistic.exercises.output()
