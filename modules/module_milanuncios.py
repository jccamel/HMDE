#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import re
from random import randint
from time import sleep

# utilities
from modules.util import *

# Globals
url_base_milanuncios = 'https://www.milanuncios.com'
urls = ["https://www.milanuncios.com/telefonos-moviles-en-barcelona/?demanda=n&fromSearch=1&orden=date&pagina=",
        "https://www.milanuncios.com/telefonos-moviles-en-girona/?demanda=n&fromSearch=1&orden=date&part&pagina="]


class MilAnuncios(object):

    def __init__(self):

        self.url_producto = ""  # La URL del productoV
        self.ref = ""  # Numero de refencia del productoV
        self.producto = ""  # Titulo que ha pusto el usuario
        self.descripcion = ""  # Descripcion del productoV
        self.fecha = ""  # Fecha en la que se ofrece el productoV
        self.categoria = []  # Categoria dentro de Mil Anuncios
        self.precio = ""  # Precio del productoV
        self.localidad = ""  # Localidad donde está la oferta
        self.loc = []  # Geolocalización de la Oferta
        self.nombre = ""  # Nombre del usuario de contacto
        self.telefono = ""  # Numero de telefono de contacto
        self.fotos = []  # Fotografias del productoV en oferta

    def genera_diccionario(self):
        dicc = {'url_producto': self.url_producto, 'referencia': self.ref, 'productoV': self.producto,
                'descripcion': self.descripcion, 'fecha': self.fecha, 'categoria': self.categoria,
                'precio': self.precio, 'localidad': self.localidad, 'usuario': self.nombre,
                'telefono': self.telefono, 'fotos_producto': self.fotos}
        return dicc

    def __del__(self):
        pass

    def __tratar_fecha(self, fecha):

        import datetime
        from datetime import datetime as dt

        anyo = int(fecha.split('-')[2])
        mes = int(fecha.split('-')[1])
        dia = int(fecha.split('-')[0])

        fecha = datetime.date(anyo, mes, dia)
        fecha_iso = fecha.isoformat()
        nueva_fecha = dt.strptime(fecha_iso, "%Y-%m-%d")
        return nueva_fecha

    def recupera_producto(self, url, soup_packtpage):

        self.url_producto = url

        if get_canonical(soup_packtpage) == url:
            # Categorias productoV ----------------------------------------------
            try:
                class_categoria = (soup_packtpage.find("div", {"class": "beacrumb"}))
                categorias = class_categoria.findAll('a')
                for cat in categorias:
                    self.categoria.append(cat.text)
            except:
                pass

            # Referncia productoV ----------------------------------------------
            try:
                class_referencia = soup_packtpage.find("div", ["pillDiv", "pillRef"])
                referencia = class_referencia.find('strong')
                self.ref = referencia.text
            except:
                pass

            # Fecha productoV ----------------------------------------------
            try:
                class_fecha = (soup_packtpage.find("div", {"class": "pagAnuStatsCreated"}))
                self.fecha = self.__tratar_fecha(class_fecha.text)
            except:
                pass

            # Titulo productoV ----------------------------------------------
            try:
                class_titulo = (soup_packtpage.find("h1", {"class": "ad-detail-title"}))
                self.producto = class_titulo.text
            except:
                pass

            # Localidad productoV ----------------------------------------------
            try:
                class_anutitulo = (soup_packtpage.find("div", {"class": "pagAnuCatLoc"}))
                localidad = class_anutitulo.text
                self.localidad = localidad.split('(')[1].split(')')[0]
            except:
                pass

            # Descripcion productoV ----------------------------------------------
            try:
                class_descrip = (soup_packtpage.find("p", {"class": "pagAnuCuerpoAnu"}))
                self.descripcion = class_descrip.text
            except:
                pass

            # Precio productoV ----------------------------------------------
            try:
                class_pre = (soup_packtpage.find("div", {"class": "pagAnuPrecioTexto"}))
                precio = class_pre.text
                self.precio = precio.split()[0]
            except:
                pass

            # Fotos productoV ----------------------------------------------------
            try:
                class_fotos= (soup_packtpage.findAll("div", {"class": "pagAnuFoto"}))
                pat = re.compile ('<img [^>]*src="([^"]+)')
                for foto in class_fotos:
                    link = pat.findall(str(foto))[0]
                    self.fotos.append(link.split('?')[0])
            except:
                pass

            # Nombre usuario ----------------------------------------------------
            try:
                nombre = (soup_packtpage.find("div", {"class": "pagAnuContactNombre"}))
                self.nombre = nombre.text
            except:
                pass

            # Telefono usuario ----------------------------------------------------
            try:
                url_contacto = "http://www.milanuncios.com/datos-contacto/?id=" + str(self.ref)
                conten = request(url_contacto)
                soup_packtpage_telefono = str(get_soup_packtpage(conten))
                self.telefono = soup_packtpage_telefono.split('getTrackingPhone(')[1].split(')')[0]
            except:
                pass
        else:
            pass


"""     # GeoLocalizacion del productoV -----------------------------------------
        geo = Geocoder(api_key='')
        address = geo.geocode(str(self.localidad[0]) + ', ' + str(self.localidad[1]) + ", Cataluña, España")
        self.loc.append(float(address.latitude))
        self.loc.append(float(address.longitude))
"""


def paginas_con_items(soup_packtpage):
    paginas = 0
    try:
        paginas_txt = soup_packtpage.find("div", {"class": "adlist-paginator-summary"}).text
        paginas = int(paginas_txt.split()[-1])
    except:
        pass
    return paginas


def recupera_tabla_list_container_milanuncios(urls):
    for url in urls:
        sleep(randint(1, 3))
        conten = request(url + '1')
        soup_packtpage = get_soup_packtpage(conten)
        p = paginas_con_items(soup_packtpage)
        print('Pages items: ' + str(p), '\n\n')
        pagina = 1
        lista_urls_scan = []
        while pagina <= p:
            print("Page: " + url + str(pagina))
            print('--------------------------------------------------------------------------')
            try:
                tabla = soup_packtpage.find_all('a', {"class": "aditem-detail-title"})
            except:
                tabla = []
            for a in tabla:
                print(a['href'])
                lista_urls_scan.append(a['href'])
            pagina += 1
            sleep(randint(3, 5))
            conten = request(url + str(pagina))
            soup_packtpage = get_soup_packtpage(conten)
            print('\n\n')
    print('Total recuperado: ' + str(len(lista_urls_scan)))
    print('-----------------------------------------------------------------------------------')
    print('-----------------------------------------------------------------------------------')
    print('\n\n')
    return lista_urls_scan


if __name__ == '__main__':
    lista_urls = recupera_tabla_list_container_milanuncios(urls)
    milanuncios = MilAnuncios()

    for u in lista_urls:
        url = url_base_milanuncios + u
        conten = request(url)
        milanuncios.recupera_producto(url, get_soup_packtpage(conten))
        dicc = milanuncios.genera_diccionario()
        print(dicc)
