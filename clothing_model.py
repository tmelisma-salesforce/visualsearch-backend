class ClothingItem:
    def __init__(self, brand, name, color, type, gender, product_number):
        self.brand = brand
        self.name = name
        self.color = color
        self.type = type
        self.gender = gender
        self.product_number = product_number

    def to_dict(self):
        return {
            "brand": self.brand,
            "name": self.name,
            "color": self.color,
            "type": self.type,
            "gender": self.gender,
            "product_number": self.product_number
        }