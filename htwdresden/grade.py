import requests
import json

from .login import RZLogin
from .exceptions import HTWAuthenticationException


class Grade:
    def __init__(self,
                 exam_nr,
                 state,
                 ects_credits,
                 title,
                 semester,
                 try_count,
                 exam_date,
                 grade,
                 publication_date,
                 exam_form,
                 annotation,
                 ects_grade,
                 note,
                 id):
        self.exam_nr = exam_nr
        self.state = state
        self.ects_credits = ects_credits
        self.title = title
        self.semester = semester
        self.try_count = try_count
        self.exam_date = exam_date
        self.grade = grade
        self.publication_date = publication_date
        self.exam_form = exam_form
        self.annotation = annotation
        self.ects_grade = ects_grade
        self.note = note
        self.id = id

    @staticmethod
    def from_json(j: dict):
        return Grade(j.get('nr'),
                     j.get('state'),
                     j.get('credits'),
                     j.get('text'),
                     j.get('semester'),
                     j.get('tries'),
                     j.get('examDate'),
                     j.get('grade'),
                     j.get('publicDate'),
                     j.get('form'),
                     j.get('annotation'),
                     j.get('ectsGrade'),
                     j.get('note'),
                     j.get('id'))

    @staticmethod
    def fetch(login: RZLogin, degree_nr: str, course_nr: str, reg_version: int):
        req = requests.get(f'https://wwwqis.htw-dresden.de/appservice/v2/getgrades?AbschlNr={degree_nr}&StgNr={course_nr}&POVersion={reg_version}',
                           auth=requests.auth.HTTPBasicAuth(login.s_number, login.password))
        if req.status_code is 401:
            raise HTWAuthenticationException()
        if req.status_code is not 200:
            print(req.status_code)
            print(req.text)
            return None
        grades = json.loads(req.text)
        return [Grade.from_json(grade) for grade in grades]

    def __repr__(self):
        grade = int(self.grade) / 100 if self.grade is not None else 'n/a'
        if self.state == 'BE':
            # passed
            state = '✔︎'
        elif self.state == 'NB':
            # not passed
            state = '✘'
        elif self.state == 'AN':
            # 'angemeldet', usually only the case if explicitly opted out of the exam, e.g. 'geschoben'
            state = '↻'
        else:
            state = ' '
        return '{} {}: {}'.format(state, self.title, grade)
