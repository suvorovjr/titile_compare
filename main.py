import re
from fuzzywuzzy import fuzz


class ProductsCompare:
    measure_units = dict(кг='Вес', г='Вес', л='Объем', шт='Количество', мл='Объем', уп='Упаковок', пак='Количество')
    measure_units['%'] = 'Процент алкоголя/жирности'

    def __init__(self, magnit_product: str, markets_product: str) -> None:
        """
        Инициализатор класса для сравнения двух товаров
        :param magnit_product: Название продукта в магните
        :param markets_product: Название товара на маркетплейсе
        """

        self.magnit_product = magnit_product
        self.markets_product = markets_product
        self.compare_status = True

    def get_attrs(self, product_name: str) -> dict:
        """
        Метод для парсинга атрибутов товара из названия
        :param product_name: Название товара
        :return: Словарь с атрибутами товара
        """

        product_charachteristicts = {}
        for unit, value in self.measure_units.items():
            pattern = rf'(\d+(?:[\.,]\d+)?)\s*{unit}'
            match = re.search(pattern, product_name)
            if match:
                product_unit = float(match.group(1).replace(',', '.'))
                until_value = product_unit if unit not in ['кг', 'л'] else product_unit * 1000
                product_charachteristicts[value] = until_value
        return product_charachteristicts

    def product_compare(self) -> bool:
        """
        Метод с логикой сравнения товаров. Основной метод, который отвечает за сравнение товаров
        :return: Булево значение, в зависимости от того, похожи ли товары друг на друга
        """

        magnit_attrs = self.get_attrs(self.magnit_product)
        market_attrs = self.get_attrs(self.markets_product)
        if len(magnit_attrs) > 0:
            self.compare_attrs(magnit_attrs, market_attrs)
        title_compare = fuzz.ratio(self.magnit_product, self.markets_product)
        if self.compare_status and title_compare >= 50:
            return True
        return False

    def compare_attrs(self, attrs_1: dict, attrs_2: dict) -> None:
        """
        Метод для сравнения товаров по атрибутам
        :param attrs_1: Атрибуты первого товара
        :param attrs_2: Атрибуты второго товара
        :return: None
        """

        for item, value in attrs_1.items():
            if attrs_2.get(item) and attrs_2[item] != value:
                self.compare_status = False
        if attrs_2.get('Количество') and not attrs_1.get('Количество'):
            self.compare_status = False
        if attrs_2.get('Упаковок') and not attrs_1.get('Упаковок'):
            self.compare_status = False

    def __call__(self) -> bool:
        """
        Магический метод для вызова класса как функции
        :return: Результат сравнения товаров из метода product_compare
        """

        return self.product_compare()
