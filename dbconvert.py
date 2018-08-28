from datetime import datetime

from gymboomreader import GymBoomReader
from base import Set, Exercise, Workout, Base


class DBConvert:
    def __init__(self, gb: GymBoomReader, base: Base):
        self.gb=gb
        self.base=base
        self.proceed()

    def proceed(self):
        self.convert_sets_measures()
        for id_wo, wo in self.gb.workouts.items():
            self.proceed_day(id_wo, wo)

    def convert_sets_measures(self):
        self.sets_measures=dict()
        for id, item in self.gb.sets_measures.items():
            # print(id,item)
            id_se=item['id_se']
            value=item['value']
            name=self.gb.measures[item['id_me']]['name']
            # print(id_se,name,value)

            measure={'name':name, 'value':value}

            temp=self.sets_measures.get(id_se,[])
            temp.append(measure)
            self.sets_measures[id_se]=temp

        # for id, item in self.sets_measures.items():
        #     print(id, item)


    def proceed_day(self, id_workout, workout):
        date = datetime.fromtimestamp(float(workout['date']) / 1000).date()
        name = workout['name']
        # print('----------------------')
        # print(date, name)
        wo=self.base.new_workout(date,name)

        day_exercises=dict()
        for id_wo_ex, wo_ex in self.gb.workouts_exercises.items():
            if wo_ex['id_wo'] == id_workout:
                number=wo_ex['number']
                exercize=self.gb.exercises[wo_ex['id_ex']]
                exercize_data={'ex':exercize, 'id':id_wo_ex}
                day_exercises[number]=exercize_data
        for number in sorted(day_exercises):
            # print(day_exercises[number])
            exercize=day_exercises[number]['ex']
            id_wo_ex = day_exercises[number]['id']

            self.proceed_exercise(wo, id_wo_ex, exercize)

    def proceed_exercise(self, wo:Workout, id_wo_exercise, exercise):
        # print(exercise, id_wo_exercise)

        ex=wo.new_exercise(exercise['name'])

        attempts=dict()
        for attempt_number, attempt in self.gb.sets.items():
            if attempt['id_wo_ex']==id_wo_exercise:
                # print(attempt_number,attempt, self.sets_measures[attempt_number])
                number=attempt['number']
                comment=attempt['comment']
                measures=self.sets_measures[attempt_number]
                attempt_data={'measures':measures, 'comment':comment}
                attempts[number]=attempt_data

        for number in sorted(attempts):
            # print(attempts[number])
            attempt=attempts[number]
            s=ex.new_set()
            s.comment=attempt['comment']
            for item in attempt['measures']:
                # print(item)
                if item['name']=='Вес':
                    s.weight=float(item['value'])
                    continue
                if item['name'].startswith('Повторения'):
                    s.repeats=int(item['value'])
                    continue

                s.anydata = s.anydata + ' ' + item['name'] + ' ' + item['value']