import sqlite3


class GymBoomReader:
    def __init__(self,filename):
        conn = sqlite3.connect(filename)
        self.cursor=conn.cursor()
        self._init_tables()
        conn.close()

    def _init_tables(self):
        self.exercises = self.parse_table('exercises')
        # print(self.exercises)
        self.exercises_measures = self.parse_table('exercises_measures')

        self.groups=self.parse_table('groups')
        self.measures=self.parse_table('measures')

        self.sets=self.parse_table('sets')
        self.sets_measures=self.parse_table('sets_measures')
        self.workouts=self.parse_table('workouts')

        self.workouts_exercises = self.parse_table('workouts_exercises')

    def parse_table(self, tablename, test=False):
        # print()
        # print('Parsing table "' + tablename + '"')

        coloumn_names=[]
        for item in self.cursor.execute('PRAGMA table_info(' + tablename + ')'):
            coloumn_names.append(item[1])
        # print(coloumn_names)

        result = dict()
        for item in self.cursor.execute("SELECT * FROM " + tablename):
            if test: print(item)
            temp = dict()
            for id, field in zip(coloumn_names[1:], item[1:]):
                temp[id] = field

            result[item[0]] = temp

        # print(len(result), 'items')
        return result