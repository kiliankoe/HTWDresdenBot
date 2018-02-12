from requests.auth import HTTPBasicAuth

from .login import RZLogin
from .network import Network


class Course:
    def __init__(self,
                 reg_version: int,
                 degree_txt: str,
                 degree_nr: str,
                 course_nr: str,
                 course_txt: str):
        self.reg_version = reg_version
        self.degree_txt = degree_txt
        self.degree_nr = degree_nr
        self.course_nr = course_nr
        self.course_txt = course_txt

    @staticmethod
    def from_json(j: dict):
        return Course(j.get('POVersion'),
                      j.get('AbschlTxt'),
                      j.get('AbschlNr'),
                      j.get('StgNr'),
                      j.get('StgTxt'))

    @staticmethod
    def fetch(login: RZLogin):
        courses = Network.get('https://wwwqis.htw-dresden.de/appservice/v2/getcourses',
                              auth=HTTPBasicAuth(login.s_number, login.password))
        return [Course.from_json(course) for course in courses]

    def __repr__(self):
        return '{} {} {}'.format(self.degree_txt, self.course_txt, self.reg_version)
