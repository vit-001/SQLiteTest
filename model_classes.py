from openpyxl import Workbook
from openpyxl.styles import Alignment

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

    def proceed_to_xls(self, fname):
        wb = Workbook()
        ws = wb.active

        c_row=0

        for workout in self.base.days:
            c_row=c_row+1
            ws.cell(c_row, 1).value = workout.date
            ws.cell(c_row, 2).value = workout.name

            for ex in workout.excercises:
                c_row = c_row + 1
                use_third_line = False

                ws.cell(c_row, 3).value = ex.name

                i = 4
                for set in ex.sets:
                    ws.cell(c_row, i).value = set.weight
                    ws.cell(c_row+1, i).value = set.repeats

                    t=''
                    if set.anydata:
                        t=t+set.anydata
                        use_third_line = True
                    if set.comment:
                        t = t + set.comment
                        use_third_line = True

                    ws.cell(c_row + 2, i).value = t

                    i = i + 1

                if ex.sets:

                    ws.merge_cells(f'C{c_row}:C{c_row+1}')

                    ws.cell(c_row, 21).value = 'V'
                    ws.cell(c_row+1, 21).value = f'=SUMPRODUCT(D{c_row}:T{c_row},D{c_row+1}:T{c_row+1})'

                    ws.cell(c_row, 22).value = 'КПШ'
                    ws.cell(c_row+1, 22).value = f'=SUM(D{c_row+1}:T{c_row+1})'

                    ws.cell(c_row, 23).value = 'Ио'
                    ws.cell(c_row+1, 23).value = f'=X{c_row+1}/Y{c_row+1}'
                    ws.cell(c_row + 1, 23).number_format = '0.0%'

                    ws.cell(c_row, 24).value = 'ср вес'
                    ws.cell(c_row+1, 24).value = f'=U{c_row+1}/V{c_row+1}'
                    ws.cell(c_row + 1, 24).number_format = '0.0'

                    ws.cell(c_row, 25).value = '1ПМ'
                    ws.cell(c_row+1, 25).value = Statistic.exercises.get_1PM(ex.name)
                    ws.cell(c_row+1, 25).number_format = '0.0'

                    ws.cell(c_row, 26).value = 'КО'
                    ws.cell(c_row+1, 26).value = f'=W{c_row+1}*V{c_row+1}'
                    ws.cell(c_row+1, 26).number_format = '0.0'

                    c_row = c_row + 1

                    if use_third_line:
                        c_row = c_row + 1

        self.format_exersises_sheet(ws,c_row)
        wb.save(fname)

    def format_exersises_sheet(self, ws, last_row):

        align_center = Alignment(horizontal='center',
                                 vertical='top',
                                 text_rotation=0,
                                 wrap_text=False,
                                 shrink_to_fit=False,
                                 indent=0)

        align_left_wrap = Alignment(horizontal='left',
                                 vertical='top',
                                 text_rotation=0,
                                 wrap_text=True,
                                 shrink_to_fit=False,
                                 indent=0)


        for col in ws.iter_cols(min_col=21, max_col=26, max_row=last_row):
            for cell in col:
                cell.alignment=align_center

        for cell in ws['C']:
            cell.alignment = align_left_wrap

        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 1
        ws.column_dimensions['C'].width = 30

if __name__ == "__main__":


    wb1 = Workbook()

    # grab the active worksheet
    ws1 = wb1.active

    # Data can be assigned directly to cells
    # ws['A1'] = 42

    # Rows can also be appended
    ws1.append([1, 2, 3])

    ws1['D1']='=SUM(A1:C1)'

    # Python types will automatically be converted
    # import datetime
    #
    # ws['A2'] = datetime.datetime.now()

    # Save the file
    wb1.save("sample.xlsx")