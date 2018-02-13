from .network import Network


class Canteen:
    def __init__(self,
                 name: str,
                 address: str,
                 city: str,
                 coordinates: [float],
                 ident: int):
        self.name = name
        self.address = address
        self.city = city
        self.coordinates = coordinates
        self.id = ident

    @staticmethod
    def from_json(j: dict):
        coords = [j.get('coordinates').get('latitude'), j.get('coordinates').get('longitude')]

        return Canteen(j.get('name'),
                       j.get('address'),
                       j.get('city'),
                       coords,
                       j.get('id'))

    @staticmethod
    def fetch_all():
        canteens = Network.get('https://rubu2.rz.htw-dresden.de/API/emeal/canteens')
        return [Canteen.from_json(c) for c in canteens]

    @staticmethod
    def fetch_single(ident: int):
        canteen = Network.get('https://rubu2.rz.htw-dresden.de/API/emeal/canteens/{}'.format(ident))
        return Canteen.from_json(canteen)

    def __repr__(self):
        return self.name


class Meal:
    def __init__(self,
                 title: str,
                 canteen: str,
                 date: str,
                 is_sold_out: bool,
                 counter: str or None,
                 is_evening_offer: bool,
                 student_price: float or None,
                 employee_price: float or None,
                 image_url: str or None,
                 detail_url: str,
                 information: [str],
                 additives: [str],
                 allergens: [str]):
        self.title = title
        self.canteen = canteen
        self.date = date
        self.is_sold_out = is_sold_out
        self.counter = counter
        self.is_evening_offer = is_evening_offer
        self.student_price = student_price
        self.employee_price = employee_price
        self.image_url = image_url
        self.detail_url = detail_url
        self.information = information
        self.additives = additives
        self.allergens = allergens

    @staticmethod
    def from_json(j: dict):
        return Meal(j.get('title'),
                    j.get('canteen'),
                    j.get('date'),
                    j.get('isSoldOut'),
                    j.get('counter'),
                    j.get('isEveningOffer'),
                    j.get('studentPrice'),
                    j.get('employeePrice'),
                    j.get('image'),
                    j.get('detailURL'),
                    j.get('information'),
                    j.get('additives'),
                    j.get('allergens'))

    @staticmethod
    def fetch_today(canteen: int=None):
        if canteen is not None:
            meals = Network.get('https://rubu2.rz.htw-dresden.de/API/emeal/meals/{}'.format(canteen))
        else:
            meals = Network.get('https://rubu2.rz.htw-dresden.de/API/emeal/meals')

        return [Meal.from_json(m) for m in meals]# if len(meals) != 0 else []

    @staticmethod
    def fetch(canteen: int=None, date: str=None):
        meals = Network.get('https://rubu2.rz.htw-dresden.de/API/emeal/meals',
                            params={'canteen': canteen, 'date': date})
        return [Meal.from_json(m) for m in meals]# if len(meals) != 0 else []

    @staticmethod
    def search(query: str):
        meals = Network.get('https://rubu2.rz.htw-dresden.de/API/emeal/search',
                            params={'query': query})
        return [Meal.from_json(m) for m in meals]# if len(meals) != 0 else []

    def __repr__(self):
        return '{} @ {}'.format(self.title, self.canteen)
