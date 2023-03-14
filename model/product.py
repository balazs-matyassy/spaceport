class Product:
    def __init__(self, product_id, name, unit_price, discount=0):
        self.product_id = product_id
        self.name = name
        self.unit_price = unit_price
        self.discount = discount

    @property
    def discounted_price(self):
        return round((self.unit_price * (100 - self.discount)) / 100)
