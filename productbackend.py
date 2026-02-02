from abc import ABC, abstractmethod
from typing import Protocol
from crm_usermanagement import Produkt

class ProductList():
    def __init__(self):
        self.arrrayOfProducts: list[Produkt] = []
    
    def veroeffentlicheProdukt(self, hersteller, product : Produkt):
        self.arrrayOfProducts.append([product, hersteller])
    def get_all_products(self):
        return self.arrrayOfProducts   
    
