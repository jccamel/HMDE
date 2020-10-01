![alt tag](pics/logo.jpg)
# HMDE Hand-Me-Down Exploit

### Inception

Explotar de forma simultánea los mercados de segunda mano que existen en internet.

### Motivos
Por comodidad, muchos de los objetos que ya no queremos y los que pensamos que aún pueden tener una utilización por parte de otras personas, los ponemos a la venta en el mercado online. Este mercado online se traduce en infinidad de páginas web y aplicaciones móviles que nos permiten de forma sencilla venderlos, cambiar o regalar.

Es sabido también que este mercado es el lugar ideal para los vendedores que buscan el anonimato y quieren vender sus objetos que han adquirido de forma ilícita, ya sean productos electrónicos de consumo, bicicletas, maquinaria o ropa.

No sólo se esconden vendedores de objetos sustraídos, sino usuarios que mediante técnicas fraudulentas (phishing, pagos pocos seguros ...) también intentan estafar a los compradores.

En definitiva, es el caldo de cultivo para todos aquellos que quieren hacer dinero de forma ilícita.

Es por estos motivos y otros de carácter personal que nace la idea de crear una herramienta que permita explotar toda la información abierta que estas páginas facilitan para vender objetos en ellas expuestos.

### SOBRE LOS DATOS EXPLOTADOS

La información que trabajará esta herramienta será obtenida de forma legal, y provendrá de las propias páginas web publicadas en Internet. Estos datos serán obtenidos mediante técnicas OSINT. En ningún momento se realiza ningún acceso no autorizado a ninguna de las páginas explotadas, ni a los servidores que alojan los datos con los que construyen las webs.


### Autor

* **Juan Carlos** - *Initial work* - [jccamel](https://github.com/jccamel)

### Licencia: GNU General Public License v3.0 

Esta aplicación está bajo licencia GNU General Public License, es un tipo de licencia para software que permite la copia, distribución (comercial o no) y modificación del código, siempre que cualquier modificación se continúe distribuyendo con la misma licencia GPL. La licencia GPL no permite la distribución de programas ejecutables sin el código fuente correspondiente o una oferta de cómo obtenerlo gratuitamente.

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://choosealicense.com/licenses/gpl-3.0/)

## Programa 
### Librerias

Librerias utilizadas
````text
appdirs
beautifulsoup4
certifi
chardet
colorama
fs
getpass3
helium
idna
lxml
pymongo
pytz
requests
selenium
six
soupsieve
tabulate
urllib3
````
Instalación:
````python
pip install -r requirements.txt
````