#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard library
import argparse
import sys
from colorama import Style, Fore, init
from modules.module_wallapop import *
from modules.module_vibbo import *
from modules.file_system import *
from modules.module_mongodb import *

import logging

# Basic configuration for logging
logging.basicConfig(format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


lista = ['xzo89rr0g469', 'xzo89rr2o269', '36ew0x112q6d', 'wzynw55gx5j5', 'qzm4kyye2xzv', '0j2yx33q3vzy', '8z81d4g05163',
         '9jd7p25v4djk', 'p61owy7llgj5', '8z81d4gxr163', 'ejk4okk4o9zx', 'e65yog37ypjo', 'ejk4ok9nvyzx', '36ew0xn54k6d',
         '3zlg319w3pjx', '3zlg31g022jx', '0j2yx3yn7nzy', 'ejk4ok4n3qzx', 'p61owyoemxj5', '9jd7p25xyljk', 'e65yogyx9mjo',
         'w67d2yd2mw6x', 'vjrdgrdpdl6k', '3zlg31geo8jx', 'vjrdgrk03l6k', 'v6g4w24eq76e', '8j3y1eme5y69', 'qzm4ky9pqozv',
         'qzm4ky93ylzv', '0j2yx3we5nzy', '9jd7p2dr89jk', 'vjrdgry79x6k', 'mznld84xvgjn', 'pzp94r8v9m63', 'ejk4ok21xrzx',
         'ejk4ok2y1rzx', 'ejk4okxeerzx', 'wzvypn9oerzl', 'nz0mk09oe3jo', '8z81d4vpp863', '36ew0xdxly6d', 'e65yogvg0gjo',
         '9jd7p5g0odjk', 'qzm4kygpxgzv', '8z81dgyy3163', 'w67d2y82ky6x', 'x6qye9rrwojy', 'qjwy0dmm1ezo', 'xzo89vex2469',
         'qjwy0pl41kzo', 'mznld842ekjn', '9jd7p5g5g9jk', 'wzynw7dvpxj5', 'pzp941leg963', 'nz0mkv70l7jo', 'mznldv9gmyjn',
         ]


class Creditos:
    def __init__(self, **kwargs):
        try:
            self.program_name = "Hand-Me-Down Exploit"
            self.program_version = "v1.3"
            self.program_date = "01/01/2016"
            self.program_author_name = "GoalNefesh"
        except:
            pass

    def __del__(self):
        pass

    def credits(self):
        """Show program credits"""
        init()
        print('\n')
        print(Fore.GREEN, Style.BRIGHT + "  _    _ __  __ _____  ______ ")
        print(Fore.GREEN, Style.BRIGHT + " | |  | |  \/  |  __ \|  ____|")
        print(Fore.GREEN, Style.BRIGHT + " | |__| | \  / | |  | | |__   ")
        print(Fore.GREEN, Style.BRIGHT + " |  __  | |\/| | |  | |  __|  ")
        print(Fore.GREEN, Style.BRIGHT + " | |  | | |  | | |__| | |____ ")
        print(Fore.GREEN, Style.BRIGHT + " |_|  |_|_|  |_|_____/|______|")
        print(Fore.LIGHTYELLOW_EX, "  " + self.program_name + " " + self.program_version)
        print(Fore.LIGHTYELLOW_EX, "  by: " + self.program_author_name)
        print(Fore.LIGHTYELLOW_EX, "  " + self.program_date, Style.RESET_ALL, Fore.RESET)
        print('\n\n')


def main():
    """ Main function"""

    parser = argparse.ArgumentParser(description='OSINT tool -------------------------->', add_help=True)
    subparsers = parser.add_subparsers(help='commands')

    scrape_wallapop = subparsers.add_parser('wallapop', help='scrape Wallapop')
    scrape_wallapop.add_argument(
        '-px', '--proxy',
        help='Activate proxies',
        action='store_true',
        default=False)

    scrape_wallapop.add_argument(
        '-scrolls',
        help='Num of page scrolls to download (10 by default)',
        type=int,
        default=10,
        action="store",
        dest='items',
        nargs=1)

    scrape_wallapop.add_argument(
        '-wprv',
        help='List of providences',
        action='store_true',
        default=False)

    scrape_wallapop.add_argument(
        '-wcty',
        type=str,
        help='List of cities by providence: URL',
        nargs=1)

    scrape_wallapop.add_argument(
        '-wcpv',
        type=str,
        help='List categories by providence: URL',
        nargs=1)

    scrape_wallapop.add_argument(
        '-wdpro',
        type=str,
        help='Download products: URL',
        nargs=1)

    scrape_wallapop.add_argument(
        '-wdusr',
        help='Download users: -wdusr <UserID>',
        nargs=1)

    scrape_vibbo =  subparsers.add_parser('vibbo', help='scrape Vibbo')
    scrape_vibbo.add_argument(
        '-cat',
        help='List of categories to download',
        action='store_true',
        default=False)
    scrape_vibbo.add_argument(
        '-vdp',
        help='Vibbo download products - add URL',
        nargs=1)
    scrape_vibbo.add_argument(
        '-px', '--proxy',
        help='Activate proxies',
        action='store_true',
        default=False)

    scrape_milanuncios = subparsers.add_parser('milanuncios', help='scrape Milanuncios')
    scrape_milanuncios.add_argument(
        '-cat',
        help='List of categories to download',
        action='store_true',
        default=False)
    scrape_milanuncios.add_argument(
        '-mdobj',
        help='Download objects - add URL',
        nargs=1)
    scrape_milanuncios.add_argument(
        '-px', '--proxy',
        help='Activate proxies',
        action='store_true',
        default=False)

    creds = subparsers.add_parser('credits')

    args = parser.parse_args()

    try:
        vars(args)["action"] = sys.argv[1]
        if args.action == 'wallapop':
            cc_wallapop(args)
        elif args.action == 'vibbo':
            cc_vibbo(args)
        elif args.action == 'milanuncios':
            cc_milanuncios(args)
        elif args.action == 'credits':
            cr = Creditos()
            print(cr.credits())
            del cr

    except IndexError as e:
        logger.error("Please, add an option to execute")
        parser.print_help()
        sys.exit()


def cc_wallapop(arguments):
    fs = HmdeFileSystem()
    fs.create_dir_system()
    if arguments.wprv:
        dicc = recupera_provincias(arguments.proxy)
        print_dict(dicc, 'Provincia')
    elif arguments.wcpv:
        try:
            dicc = (recupera_categorias_poblaciones(arguments.wcpv[0], arguments.proxy, 0))
            print_dict(dicc, 'Categoria')
        except:
            pass
    elif arguments.wcty:
        try:
            dicc = (recupera_categorias_poblaciones(arguments.wcty[0], arguments.proxy, 1))
            print_dict(dicc, 'Poblaciones')
        except:
            pass
    elif arguments.wdpro:  # wallapop download products
        cmdb = ConexionMongoDB()
        cmdb.open_conexion()
        try:
            login = data_login()  # capture data to login process to platform wallapop
            app = WallapopApp(arguments.proxy)  # wallapop object
            app.log_in(login[0], login[1])  # login process
            app.charge_page(arguments.wdpro)  # take URL products
            list_ids_products = app.get_id_products_main_page(arguments.items[0])  # item list products
            app.closeApp()
            print(list_ids_products)  # temp line erase in future  **************************************************
            for ids in list_ids_products:  # take json file product process
                documento = app.get_item(ids)
                jp = TrataJsonItem(documento)  # download json file
                itemImages, typeCheck = jp.getImages()  # dictionary and json file check data
                if typeCheck == 'Ok':  # many json files don't contain product data
                    cmdb.insert_doc('wallapop', documento)  # save document
                    fs.save_file(itemImages)  # save photos
                del jp  # clean object
                print('-----------------------------------------------------------------------------------------------')
        except Exception as error:
            print('ERROR', error)
        cmdb.close_conexion()
        del cmdb
    elif arguments.wdusr:
        try:
            pass
        except:
            pass
    del fs


def cc_vibbo(arguments):
    import json
    if arguments.cat:
        with open('links.json') as links:
            data = json.load(links)
            links.close()
            print_dict(data['links'][0]['vibbo'], 'Categoria')
    elif arguments.vdp:
        login = data_login()
        #  tabla_objetos = recupera_tabla_list_container_vibbo(arguments.vdp[0], arguments.proxy)
        app = VibboApp(arguments.proxy)
        app.log_in(login[0], login[1])
        app.charge_page(arguments.vdp[0])
        app.get_products_main_page()
    else:
        print('Nothing')


def cc_milanuncios(arguments):
    import json
    if arguments.cat:
        with open('links.json') as links:
            data = json.load(links)
            links.close()
            print_dict(data['links'][0]['milanuncios'], 'Categoria')
    else:
        print('Nothing')


if __name__ == '__main__':
    main()
