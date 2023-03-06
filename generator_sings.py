
class Generator_sings:
    def __init__(self):
        pass

    def generate_string(self):
        return "x" * self.n

    def russian_chars(self):
        return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    # Здесь мы взяли 20 популярных китайских иероглифов
    def chinese_chars(self):
        return '的一是不了人我在有他这为之大来以个中上们'

    def special_chars(self):
        return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

    def smile_chars(self,n):
        return "☻" * n
