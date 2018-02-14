from datetime import datetime

from .network import Network


class FreeDay:
    def __init__(self, name: datetime, begin: datetime, end):
        self.name = name
        self.begin = begin
        self.end = end

    @staticmethod
    def from_json(j):
        begin = datetime.strptime(j.get('beginDay'), '%Y-%m-%d')
        end = datetime.strptime(j.get('endDay'), '%Y-%m-%d')
        return FreeDay(j.get('name'), begin, end)

    def __repr__(self):
        begin = self.begin.strftime('%d.%m.%Y')
        end = self.end.strftime('%d.%m.%Y')
        if begin == end:
            return '{} {}'.format(self.name, begin)
        else:
            return '{} {} bis {}'.format(self.name, begin, end)


class Semester:
    def __init__(self,
                 year,
                 kind,
                 begin,
                 end,
                 lecture_begin,
                 lecture_end,
                 exam_begin,
                 exam_end,
                 reregistration_begin,
                 reregistration_end,
                 free_days):
        self.year = year
        self.type = kind

        self.begin = begin
        self.end = end

        self.lecture_begin = lecture_begin
        self.lecture_end = lecture_end

        self.exam_begin = exam_begin
        self.exam_end = exam_end

        self.reregistration_begin = reregistration_begin
        self.reregistration_end = reregistration_end

        self.free_days = free_days

    @staticmethod
    def from_json(j):
        return Semester(j.get('year'),
                        j.get('type'),
                        datetime.strptime(j.get('period').get('beginDay'), '%Y-%m-%d'),
                        datetime.strptime(j.get('period').get('endDay'), '%Y-%m-%d'),
                        datetime.strptime(j.get('lecturePeriod').get('beginDay'), '%Y-%m-%d'),
                        datetime.strptime(j.get('lecturePeriod').get('endDay'), '%Y-%m-%d'),
                        datetime.strptime(j.get('examsPeriod').get('beginDay'), '%Y-%m-%d'),
                        datetime.strptime(j.get('examsPeriod').get('endDay'), '%Y-%m-%d'),
                        datetime.strptime(j.get('reregistration').get('beginDay'), '%Y-%m-%d'),
                        datetime.strptime(j.get('reregistration').get('endDay'), '%Y-%m-%d'),
                        [FreeDay.from_json(f) for f in j.get('freeDays')])

    def __repr__(self):
        kind = 'Wintersemester' if self.type == 'W' else 'Sommersemester'
        free_days = '\n'.join([str(f) for f in self.free_days])

        begin = self.begin.strftime('%d.%m.%Y')
        end = self.end.strftime('%d.%m.%Y')

        lecture_begin = self.lecture_begin.strftime('%d.%m.%Y')
        lecture_end = self.lecture_end.strftime('%d.%m.%Y')

        exam_begin = self.exam_begin.strftime('%d.%m.%Y')
        exam_end = self.exam_end.strftime('%d.%m.%Y')

        reregistration_begin = self.reregistration_begin.strftime('%d.%m.%Y')
        reregistration_end = self.reregistration_end.strftime('%d.%m.%Y')

        return f'''{kind} {self.year}
{begin} bis {end}

Vorlesungszeit
{lecture_begin} bis {lecture_end}

Prüfungszeit
{exam_begin} bis {exam_end}

Rückmeldezeitraum
{reregistration_begin} bis {reregistration_end}

Feiertage
{free_days}
'''


class SemesterPlan:
    def __init__(self, semesters: [Semester]):
        self.semesters = semesters

    @staticmethod
    def fetch():
        semesters = Network.get('https://www2.htw-dresden.de/~app/API/semesterplan.json')
        return SemesterPlan([Semester.from_json(s) for s in semesters])
