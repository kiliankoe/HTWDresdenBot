from datetime import datetime

from .network import Network


class Week:
    ALL = 0
    ODD = 1
    EVEN = 2

    @staticmethod
    def current() -> int:
        if datetime.now().isocalendar()[1] % 2 == 0:
            return Week.EVEN
        else:
            return Week.ODD


class Day:
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @staticmethod
    def current() -> int:
        return datetime.now().isocalendar()[2] - 1


class Building:
    S = 'S'
    Z = 'Z'

    @staticmethod
    def all() -> [str]:
        return [Building.S, Building.Z]


class FreeRooms:
    @staticmethod
    def fetch(week: Week or int, day: Day or int, start_time: str, end_time: str, building: Building or str) -> [str]:
        rooms = Network.get('https://www2.htw-dresden.de/~app/API/GetFreeRooms.php',
                            params={
                                'week': week,
                                'day': day,
                                'startTime': start_time,
                                'endTime': end_time,
                                'building': building
                            })
        return rooms
