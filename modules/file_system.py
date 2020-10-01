#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from modules.util import proxy_rotator, request

"""
File system for recovery fotos from users and products
[recovery_data]
|-- Wallapop
|   |-- users
|   |     |-- 6454564dsfs
|   |         `-- 6454564dsfs-foto1.jpg
|   |         `-- 6454564dsfs-foto2.jpg
|   |-- products
|         |-- asd678asd
|            `-- asd678asd-foto1.jpg
|            `-- asd678asd-foto2.jpg
|-- Vibbo
|   |-- users
|   |     |-- ghdfghdfgh
|   |         `-- ghdfghdfgh-foto1.jpg
|   |         `-- ghdfghdfgh-foto2.jpg
|   |-- products
|         |-- asd678eeeasd
|            `-- asd678eeeasd-foto1.jpg
|            `-- asd678eeeasd-foto2.jpg
|-- Milanuncios
|   |-- users
|   |     |-- 645yyy4564dsfs
|   |         `-- 645yyy4564dsfs-foto1.jpg
|   |         `-- 645yyy4564dsfs-foto2.jpg
|   |-- products
|         |-- a1212sd678asd
|            `-- a1212sd678asd-foto1.jpg
|            `-- a1212sd678asd-foto2.jpg
"""


class HmdeFileSystem(object):
    def __init__(self):
        self.system = {
            'recovery_data':
                {
                    'wallapop': ['users', 'products'],
                    'vibbo': ['users', 'products'],
                    'vilanuncios': ['users', 'products']
                }
        }
        self.path = './'
        self.path_dir = ''
        self.id = ''
        self.url = ''

    def __del__(self):
        pass

    def create_dir_system(self):
        if not os.path.isdir('./recovery_data'):
            for directory, subdir in self.system.items():  # create recovery_data
                os.mkdir(directory)
                self.path_dir = self.path + directory + '/'
                for d, s in subdir.items():  # create Wallapop, Vibbo, Milanuncios
                    os.mkdir(self.path_dir + d)
                    new_path = self.path_dir + d + '/'
                    for ssub in s:  # create users and products into Wallapop, Vibbo, Milanuncios
                        os.mkdir(new_path + ssub)

    def __generate_dir(self, platform, selector, id_item):
        self.id = id_item
        self.path_dir = self.path + list(self.system.keys())[0] + '/' + platform + '/' + selector + '/' + self.id + '/'
        if not os.path.isdir(self.path_dir):
            os.mkdir(self.path_dir)

    def __get_FileStatusCode(self):
        status = ''
        response = 404
        try:
            response, status = request(self.url)
        except:
            pass
        return response, status

    def save_file(self, diccItemId):  # LISTA DE DICCIONARIOS
        """
        136788218 ----> CLAVE IDENTIFICADORA DEL PRODUCTO
        301795993 ----> CLAVE IDENTIFICADORA FOTO DEL PRODUCTO
        diccImagenes = {136788218: {301795993: 'URL1', 30179592548: 'URL2', ....}}
        """
        for itemID, diccItems in diccItemId.items():
            self.__generate_dir('wallapop', 'products', str(itemID))
            if len(diccItems) > 0:
                for imagenID, imagenURL in diccItems.items():
                    print('{} - {}'.format(imagenID, imagenURL))
                    self.url = imagenURL
                    cont, stat = self.__get_FileStatusCode()
                    if stat == 200:
                        print('File exist!!')
                        file = str(imagenID) + '-' + str(datetime.now()).split(':')[0] + str(datetime.now()).split(':')[1]
                        open(self.path_dir + self.id + '-' + file + '.jpg', 'wb').write(cont)
                        print('Saved!')
