from bs4 import BeautifulSoup
import requests
from typing import Optional
import logging

from .base import RedisConnection

class Parse():
    def parse():
        raise NotImplementedError()

class ParseCBRF(Parse):
    identifier = ''
    valueField = 'Value'
    attribute = "ID"
    linkToCBRF = "http://www.cbr.ru/scripts/XML_daily.asp"

    def parse(self) -> Optional[str]:
        try:
            result = requests.get(self.linkToCBRF)
            soup = BeautifulSoup(result.content, features="xml", from_encoding="")
            for tag in soup.findAll("Valute"):
                if tag.attrs[self.attribute] == self.identifier:
                    value = tag.find(self.valueField).get_text()
                    return value
        except Exception as e:
            logging.error("Parsing was not successful", exc_info=e)
        return None
        

class ParseDollar(ParseCBRF):
    identifier = "R01235"

class ParseYan(ParseCBRF):
    identifier = "R01375"   

class ParseMetalTorg(Parse):
    link = ""
    rowNumberInTable = 0

    def parse(self) -> Optional[str]:
        try:
            r = requests.get(self.link)
            soup = BeautifulSoup(r.text, 'lxml')
            a = soup.findAll('table')[17]
            return a.find_all('tr')[1:][self.rowNumberInTable].find_all('td')[1].text
        except Exception as e:
            logging.error("Parsing Metal torg was not successful", exc_info=e)
        return None
    
class ParseCast(ParseMetalTorg):
    link = "https://www.metaltorg.ru/metal_catalog/metallurgicheskoye_syrye_i_polufabrikaty/chugun/chugun_peredelnyi/"
    rowNumberInTable = 5

class ParseSteel(ParseMetalTorg):
    link = "https://www.metaltorg.ru/metal_catalog/listovoi_prokat/list_rulon_bez_pokrytiya/goryachekatanaya_rulonnaya_stal/"
    rowNumberInTable = 1

def sourceFabrica(sourceType):
    if sourceType == "CBRF":
        return CBRFcurrencyFabrica
    elif sourceType == "METALTORG":
        return metalTorgFabrica

def metalTorgFabrica(strType):
    if strType == "CASTIRON":
        return ParseCast
    elif strType == "STEEL":
        return ParseSteel

def CBRFcurrencyFabrica(strType):
    if strType == "USDRUB":
        return ParseDollar
    elif strType == "YANRUB":
        return ParseYan

class Parser():
    def __init__(self) -> None:
        try:
            self.base = RedisConnection()
        except Exception as e:
            logging.critical("Can not connect to redis database", exc_info=e)
    def _convertToOne(self, source, value):
        return source + value
    def parseOutside(self, source : str, value : str) -> Optional[str]:
        baseKey = self._convertToOne(source, value)
        valueFromBase = self.base.get(baseKey)
        if valueFromBase == None:
            parseModule = sourceFabrica(source)(value)
            price = parseModule().parse()
            if price is not None:
                self.base.set(baseKey, price, 86400)
        else:
            price = valueFromBase.decode("utf-8")
        return price

source = "CBRF"
value = "USDRUB"

# if __name__ == "__main__":
#     outer = Parser()
#     print(outer.parseOutside("METALTORG", "CASTIRON"))
#     print("we are here, program works fine")
    #      outer.parseOutside("CBRF", "USDRUB"),
    #)
#r.set(source, 'home', 86400)
#r.get(source).decode("utf-8")
#parseModule = sourceFabrica(source)(value)
#parseModule = sourceFabrica("METALTORG")("CASTIRON")
#print(parseModule().parse())
#print(1)

