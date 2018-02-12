class RZLogin:
    def __init__(self, s_number: str, password: str):
        self.s_number = s_number
        self.password = password

    def __repr__(self):
        return f'RZLogin <{self.s_number}>'
