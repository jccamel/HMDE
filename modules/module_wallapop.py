#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
from helium import *
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import *
from modules.util import request

# utilities
from modules.util import *

# globals
url_base_wallapop = 'https://es.wallapop.com'


# Wallapop Class
class WallapopApp(object):
    def __init__(self, proxy_select):
        self.path = 'ChromeDriver\chromedriver'
        capabilities = dict(DesiredCapabilities.CHROME)
        if proxy_select:
            proxyrotator = proxy_rotator()
            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxyrotator['proxy'],
                'ftpProxy': '',
                'sslProxy': '',
                'noProxy': ''
            })
            proxy.add_to_capabilities(capabilities)
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("user-agent=".join(proxyrotator['randomUserAgent']))
        self.driver = webdriver.Chrome(self.path, desired_capabilities=capabilities, options=chrome_options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, 800)
        self.driver.set_page_load_timeout(600)
        self.main_url = 'https://es.wallapop.com/'
        self.driver.get(self.main_url)
        self.error = False
        self.listado_ids = []
        print('Object created')

    def __del__(self):
        pass

    def closeApp(self):
        self.driver.close()

    def __accept_cookies(self):
        try:
            sleep(randint(3, 9))
            accept_button = self.driver.find_element_by_id("didomi-notice-agree-button")
            accept_button.click()
            print('Acepto clicked!')
            sleep(randint(1, 4))
        except NoSuchElementException:
            self.error = True
            print('Cookies: Unable to find Acepto button')

    def log_in(self, user, password):
        self.__accept_cookies()
        try:
            sleep(randint(2, 4))
            log_in_button = self.driver.find_element_by_id('btn-login')
            log_in_button.click()
            print('Registro/Inicio sesión clicked!')
            sleep(randint(3, 6))
            log_in_button = self.driver.find_element_by_class_name('Welcome__btn-go-login-form')
            log_in_button.click()
            print('Inicio sesión clicked!')
            sleep(randint(3, 5))
            try:
                # login process  --------------------------------------------------------------------------------------
                user_name_input = self.driver.find_element_by_xpath("//input[@name='email']")
                user_name_input.send_keys(user)
                print('User input')
                sleep(randint(2, 5))
                password_input = self.driver.find_element_by_xpath("//input[@name='password']")
                password_input.send_keys(password)
                sleep(randint(1, 3))
                user_name_input.submit()
                print('Password input')
                sleep(randint(2, 4))
                # end login process  ----------------------------------------------------------------------------------
                try:
                    self.__accept_cookies()
                except:
                    pass
            except Exception:
                print('Some exception occurred while trying to find username or password field')
                self.error = True
        except NoSuchElementException:
            print('Unable to find Login button')
            self.error = True

    def charge_page(self, url):
        self.driver.get(url)

    def get_item(self, id_item):
        sleep(randint(2, 5))
        url_api_get_item = 'http://pro2.wallapop.com/shnm-portlet/api/v1/item.json/' + id_item
        r = request.get(url_api_get_item)
        return r.json()

    def get_user(self, id_user):
        url_api_get_user = 'http://pro2.wallapop.com/shnm-portlet/api/v1/user.json/'
        url_user = url_api_get_user.join(id_user)
        r = request.get(url_api_get_user)
        return r.json()

    def get_sold_items(self, id_user, ini='0', end='200'):
        #  http://pro2.wallapop.com/shnm-portlet/api/v1/item.json/user2/42435754?init=0&end=200&statuses=SOLD_OUTSIDE
        url_api_get_sold = 'http://pro2.wallapop.com/shnm-portlet/api/v1/item.json/user2/'
        url_user_sold_objects = id_user + '?init=' + ini + '&end=' + end + '&statuses=SOLD_OUTSIDE'
        r = request.get(url_user_sold_objects)
        return r.json()

    def __addItem(self, ids):
        for id in ids:
            if id.get('itemid') not in self.listado_ids:
                # print('Number of Object added: ', id.get('pos'))
                self.listado_ids.append(id.get('itemid'))

    def get_id_products_main_page(self, scrolls):
        sleep(randint(2, 4))
        try:
            masprod = self.driver.find_element_by_id("js-more-products-list")
            masprod.click()
            print('Ver más productos de segunda mano: clicked!!')
        except Exception:
            print('No existe boton: Ver más productos de segunda mano')
            self.error = True

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(0, scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(randint(3, 6))

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height

        html_source = self.driver.page_source
        soup_packtpage = BeautifulSoup(html_source, 'lxml')  # substituir por requests()
        ids = soup_packtpage.find_all('div', {"class": "card js-masonry-item card-product product tracked"})
        self.__addItem(ids)
        print(len(self.listado_ids))
        return self.listado_ids


# Wallapop function get providences
def recupera_provincias(proxy):
    url = "https://es.wallapop.com/sitemap"
    try:
        conten, status = request(url, proxy)
        if status == 200:
            soup_packtpage = get_soup_packtpage(conten)
            provincias = soup_packtpage.find_all('div', class_='title-sitemap-main')
            provincias_dicc = {}
            for provincia in provincias:
                prov_url = url_base_wallapop + provincia.a['href']
                prov = provincia.a.text.split('Provincia de ')[1]
                provincias_dicc[prov] = prov_url
            return provincias_dicc
    except Exception as err:
        print('+++> Error occurred in function recupera_provincias: ' + str(err))
        pass


# Wallapop function get cities
def recupera_categorias_poblaciones(url, proxy, selector):
    dicc = {}
    lista = []
    try:
        conten, status = request(url, proxy)
        if status == 200:
            soup_packtpage = get_soup_packtpage(conten)
            sitemap_section_item_list = soup_packtpage.find_all('div', class_='sitemap-section-item-list')
            lista = sitemap_section_item_list[selector].findChildren('div', recursive=False)
            for elemento in lista:
                categoria_url = url_base_wallapop + elemento.a['href']
                elemento = elemento.a.text
                dicc[elemento] = categoria_url
            return dicc
    except Exception as err:
        print('+++> Error occurred in function recupera_categorias_poblaciones: ' + str(err))
        pass


def wp_timestamp_to_date(tsp):
    #  https://www.journaldev.com/23365/python-string-to-datetime-strptime
    d_str = tsp.split('T')[0] + ' ' + tsp.split('T')[1]
    datetime_object = datetime.strptime(d_str, '%Y-%m-%d %H:%M:%S')
    return datetime_object


# Visor de json files: http://jsonviewer.stack.hu/
class TrataJsonItem(object):

    def __init__(self, geison):
        self.coordinatesMDB = []
        self.geison = geison
        try:
            self.type = geison['type']  # control de carga geison si = error no exite
        except:
            self.type = 'Ok'
        try:
            self.itemId = geison['itemId']  # cadena
        except:
            pass
        try:
            self.title = geison['title']  # cadena
        except:
            pass
        try:
            self.description = geison['description']  # cadena
        except:
            pass
        try:
            self.categories = geison['categories']  # lista de diccionarios
        except:
            pass
        try:
            self.mainImage = geison['mainImage']  # diccionario
        except:
            pass
        try:
            self.images = geison['images']  # lista de diccionarios
        except:
            pass
        try:
            self.sellerUser = geison['sellerUser']  # diccionario
        except:
            pass
        try:
            self.salePrice = geison['salePrice']  # entero precio actual
        except:
            pass
        try:
            self.originalSalePrice = geison['originalSalePrice']  # entero precio original
        except:
            pass
        try:
            self.currency = geison['currency']  # diccionario moneda de comercio
        except:
            pass
        try:
            self.modifiedDate = geison['modifiedDate']  # linux timestamp
        except:
            pass
        try:
            self.publishDate = geison['publishDate']  # linux timestamp
        except:
            pass
        try:
            self.removed = geison['removed']  # boolean
        except:
            pass
        try:
            self.banned = geison['banned']  # boolean
        except:
            pass
        try:
            self.itemURL = geison['itemURL']  # URL
        except:
            pass
        try:
            self.itemActionsAllowed = geison['itemActionsAllowed']  # diccionario boolean
        except:
            pass
        try:
            self.itemFlags = geison['itemFlags']  # diccionario
        except:
            pass
        try:
            self.itemCounters = geison['itemCounters']  # diccionario
        except:
            pass
        try:
            self.shippingAllowed = geison['shippingAllowed']  # boolean
        except:
            pass
        try:
            self.itemUUID = geison['itemUUID']  # cadena
        except:
            pass
        try:
            self.vertical = geison['vertical']  # cadena
        except:
            pass

    def __del__(self):
        pass

    def __str__(self):
        return "Item ID: {} -- Articulo: {}".format(self.itemId, self.title)

    def __fechaitem(self):
        #  devuelve la fecha de publicaion y la de modificación listo para guradar en mongodb
        try:
            publishDate = datetime.fromtimestamp(int(self.publishDate)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
            self.publishDate = publishDate
        except:
            print('Error en conversion publishDate')
        try:
            modifiedDate = datetime.fromtimestamp(int(self.modifiedDate)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
            self.publishDate = modifiedDate
        except:
            print('Error en conversion modifiedDate')

    def getItemID(self):
        return self.itemId

    def getTitle(self):
        return self.title

    def getDescription(self):
        return self.description

    def getLocation(self):
        # Note: If specifying latitude and longitude coordinates in GEOSPHERE, list the longitude first and then latitude.
        self.coordinatesMDB.append(self.sellerUser['location']['approximatedLongitude'])
        self.coordinatesMDB.append(self.sellerUser['location']['approximatedLatitude'])
        self.geison.update(self.coordinatesMDB)
        return self.coordinatesMDB

    def getImages(self):  # devuelve diccionario con clave itemId y un valor diccionario con claves pictureId y sus URLs
        """
        Ejemplo:
        {136788218: {301795993: 'http://cdn.wallapop.com/images...', 30179592548: 'http://cdn.wallapop.com/images...'}}
        """
        images = {}
        dic_images = {}
        if self.type == 'Ok':
            if len(self.images) > 0:
                for image in self.images:
                    images[image['pictureId']] = image['xlargeURL']
                dic_images[self.itemId] = images
        return dic_images, self.type
