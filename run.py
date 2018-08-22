# -*- coding: utf-8 -*-
__author__ = 'Vit'
import sqlite3
from datetime import datetime

class GymBoom:
    def __init__(self,cursor):
        self.cursor=cursor
        self._init_tables()

    def _init_tables(self):
        self.exercises = self.parse_table('exercises')
        self.exercises_measures = self.parse_table('exercises_measures')

        self.groups=self.parse_table('groups')
        self.measures=self.parse_table('measures')

        self.sets=self.parse_table('sets')
        self.sets_measures=self.parse_table('sets_measures')
        self.workouts=self.parse_table('workouts')

        self.workouts_exercises = self.parse_table('workouts_exercises')

    def parse_table(self, tablename, test=False):
        print()
        print('Parsing table "' + tablename + '"')

        coloumn_names=[]
        for item in self.cursor.execute('PRAGMA table_info(' + tablename + ')'):
            coloumn_names.append(item[1])
        print(coloumn_names)

        result = dict()
        for item in self.cursor.execute("SELECT * FROM " + tablename):
            if test: print(item)
            temp = dict()
            for id, field in zip(coloumn_names[1:], item[1:]):
                temp[id] = field

            result[item[0]] = temp

        print(len(result), 'items')
        return result

class Workouts:
    def __init__(self, gb:GymBoom):
        self.gb=gb
        self.table=dict()

        self._parse_gb()


    def _parse_gb(self):
        print()

        measures=dict()
        for k,item in  self.gb.measures.items():
            # print(k,item)
            measures[k]=item['unit']

        exercises=dict()
        for k,item in  self.gb.exercises.items():
            # print(k,item)
            exercises[k]=item['name']


        print(measures)
        print(exercises)

        sets_temp=dict()
        for item in self.gb.sets_measures.values():
            set=item['id_se']
            value=item['value']
            me= measures[item['id_me']]
            # print(set,value,me)

            t=sets_temp.get(set, dict())
            t[me]=value
            sets_temp[set]=t
            # print(sets_temp.get(set, dict()))
            # [me]=value

        # print(sets_temp)
        # print(len(sets_temp))

        exercises_temp=dict()
        # sets=dict()
        for k,item in self.gb.sets.items():
            # print(k,item)
            attempt=item['number']
            id_wo_ex=item['id_wo_ex']
            detail=sets_temp[k]
            detail['attempt']=attempt

            # print(id_wo_ex, detail)

            t=exercises_temp.get(id_wo_ex,list())
            t.append(detail)

            exercises_temp[id_wo_ex]=t

        # print(exercises_temp)

        workout_temp=dict()
        for k,item in self.gb.workouts_exercises.items():
            attempts=exercises_temp.get(k,list())
            ex=exercises[item['id_ex']]
            number= item['number']
            workout=item['id_wo']

            # print(k, workout, number, ex, attempts)

            excercise=dict(exercise=ex, number=number, attempts=attempts)

            t=workout_temp.get(workout,list())
            t.append(excercise)
            workout_temp[workout]=t

        # for k,item in workout_temp.items():
        #     print(k,item)

        #parsing workouts
        for k, item in self.gb.workouts.items():
            # print(k,item)
            date = datetime.fromtimestamp(float(item['date']) / 1000).date()
            name = item['name']
            workout=workout_temp[k]
            # print(date, name, workout)
            self.table[str(date)] = dict(name=name, workout=workout)

class Report:
    def __init__(self, gb:GymBoom):
        self.gb=gb

    def proceed(self):

        for id_wo, wo in gb.workouts.items():
            print(id_wo, wo)
            date = datetime.fromtimestamp(float(wo['date']) / 1000).date()
            name = wo['name']
            print(date, name)
            for id_wo_ex, wo_ex in gb.workouts_exercises.items():
                if wo_ex['id_wo']==id_wo:
                    print(id_wo_ex, wo_ex)





if __name__ == "__main__":

    conn = sqlite3.connect('base/1.gb')
    cursor = conn.cursor()

    gb=GymBoom(cursor)

    conn.close()

    r=Report(gb)

    r.proceed()



    # wo=Workouts(gb)
    #
    # for date, item in wo.table.items():
    #     print(date, item)
    #     pass


