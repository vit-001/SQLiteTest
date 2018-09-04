from gb_base import Base
from local_setting import fft


class Exercises:
    def __init__(self):
        self.base = dict()

    def add(self, name: str, value: float, repeat: int):
        old = self.base.get(name, {'max': 0.0, 'repeat': 1})
        if value < old['max']:
            return

        if value > old['max']:
            old['max'] = value
            old['repeat'] = repeat
        else:
            if repeat > old['repeat']:
                old['repeat'] = repeat
            else:
                return
        self.base[name] = old

    def output(self):
        for name, data in self.base.items():
            m = data['max']
            k = data['repeat']
            print(name, m, 'x', k, '%1.1f' % (m * (36 / (37 - k))))

    def get_1PM(self, name: str) -> float:
        ex = self.base.get(name, {'max': 0.0, 'repeat': 1})
        m = ex['max']
        k = ex['repeat']
        return (m * (36 / (37 - k)))


class Statistic:
    max_repeat = 17
    exercises = Exercises()

    def stat(self):
        print('Not implemented')

    @staticmethod
    def proceed(base: Base):
        for workout in base.days:
            for ex in workout.excercises:
                # ex.stat()
                for item in ex.sets:
                    Statistic.exercises.add(ex.name, item.weight, item.repeats)

        Statistic.exercises.output()


class CreateTable:
    @staticmethod
    def proceed(base: Base, fd):
        for workout in base.days:
            print(workout.date, ';', workout.name, file=fd)
            for ex in workout.excercises:
                table_width = Statistic.max_repeat + 3
                first_line = ['' for i in range(table_width)]
                second_line = ['' for i in range(table_width)]
                third_line = ['' for i in range(table_width)]
                use_third_line = False

                first_line[2] = ex.name
                i = 3

                for set in ex.sets:
                    first_line[i] = fft(set.weight)
                    second_line[i] = '%10d' % set.repeats

                    if set.anydata:
                        third_line[i] = set.anydata
                        use_third_line = True
                    if set.comment:
                        third_line[i] = third_line[i] + set.comment
                        use_third_line = True

                    i = i + 1

                for item in first_line:
                    print(item, end=';', file=fd)

                if ex.sets:
                    print('V;КПШ;Ио;ср вес; 1ПМ; КО', file=fd)

                    for item in second_line:
                        print(item, end=';', file=fd)

                    print('"=СУММПРОИЗВ(R[-1]C[-17]:R[-1]C[-1];RC[-17]:RC[-1])"', end=';', file=fd)
                    print('"=СУММ(RC[-18]:RC[-2])"', end=';', file=fd)
                    print('"=RC[1]/RC[2]"', end=';', file=fd)
                    print('"=RC[-3]/RC[-2]"', end=';', file=fd)
                    print(fft(Statistic.exercises.get_1PM(ex.name)), end=';', file=fd)
                    print('"=RC[-3]*RC[-4]"', file=fd)

                    if use_third_line:
                        for item in third_line:
                            print(item, end=';', file=fd)
                        print(file=fd)

                else:
                    print(file=fd)

class ExportXLS:
    def __init__(self, base:Base):
        self.base=base

    def proceed_to_xls(self, fd):
        pass

if __name__ == "__main__":
    from openpyxl import Workbook

    wb = Workbook()

    # grab the active worksheet
    ws = wb.active

    # Data can be assigned directly to cells
    ws['A1'] = 42

    # Rows can also be appended
    ws.append([1, 2, 3])

    # Python types will automatically be converted
    import datetime

    ws['A2'] = datetime.datetime.now()

    # Save the file
    wb.save("sample.xlsx")