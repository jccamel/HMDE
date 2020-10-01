#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import colorama
from pymongo import MongoClient, errors


class ConexionMongoDB(object):
    def __init__(self):
        self.MONGODB_URI = 'mongodb://localhost:27017'
        self.db = ""
        self.client = ""
        self.coleccion = ""
        self.MONGODB_TIMEOUT = 1000

    def __del__(self):
        pass

    def open_conexion(self):
        try:
            self.client = MongoClient(self.MONGODB_URI, serverSelectionTimeoutMS=self.MONGODB_TIMEOUT)
            self.db = self.client.get_database('hmde')
        except errors.ServerSelectionTimeoutError as error:
            print(colorama.Fore.LIGHTRED_EX, 'Abriendo... Error TimeOut: %s\n\n' % str(error), colorama.Style.RESET_ALL,
                  colorama.Fore.RESET)
            exit(0)
        except errors.ConnectionFailure as error:
            print(colorama.Fore.LIGHTRED_EX, 'Abriendo... Error conexion con mongodb: %s\n\n' % str(error),
                  colorama.Style.RESET_ALL, colorama.Fore.RESET)
            exit(0)

    def close_conexion(self):
        try:
            self.client.close()
        except errors.ServerSelectionTimeoutError as error:
            print(colorama.Fore.LIGHTRED_EX, 'Cerrando... Error TimeOut: %s\n\n' % str(error), colorama.Style.RESET_ALL,
                  colorama.Fore.RESET)
            exit(0)
        except errors.ConnectionFailure as error:
            print(colorama.Fore.LIGHTRED_EX, 'Cerrando... Error conexion con mongodb: %s\n\n' % str(error),
                  colorama.Style.RESET_ALL, colorama.Fore.RESET)
            exit(0)

    def insert_doc(self, coleccion, doc):  # doc es un diccionario
        try:
            colecc = self.db[coleccion]
            colecc.insert_one(doc)
            print(" ************  Document Saved  ***************")
        except Exception as error:
            print(colorama.Fore.LIGHTRED_EX, 'Error saving data: %s\n\n' % str(error), colorama.Style.RESET_ALL,
                  colorama.Fore.RESET)
            exit(0)

    def existe_item_wallapop(self, item):
        self.coleccion = self.db['WProduct']
        if self.coleccion.find({"itemUUID": item}).count() > 0:
            print('Existe')
        else:
            print('No Existe')
