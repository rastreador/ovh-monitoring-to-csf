#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests, os
from bs4 import BeautifulSoup as bs4

# requerimientos:
# pip3 install bs4

# Ruta del csf, por defecto es /etc/csf/csf.allow
ruta_csf='/etc/csf/csf.allow'

url='https://docs.ovh.com/gb/en/dedicated/monitoring-ip-ovh/'
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
try:
	response = requests.get(url, headers=headers)
	response.status_code
	pagina=response.content
	data = bs4(pagina, "html.parser")

	ips=[]
	for tr in data.find_all('table')[0].findAll('tr'):
		td=tr.findAll('td')
		if len(td)>0:
			if td[1].text.find('xxx')==-1:
				ips.append(td[1].text)
except:
	print("Ha fallado la descarga de las ips de monitorización de OVH")

# Miramos nuestra ip
try:
    url="https://api.ipify.org/"
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.status_code
    ip_externa=response.text
    i=str(ip_externa).split(".")
    i[3]='250 '
    ips.append('.'.join(i))
    i[3]='251 '
    ips.append('.'.join(i))
except:
    print("Ha fallado sacando nuestra ip")

# Comprobar si existe el csf
if os.path.isfile(ruta_csf):
	if len(ips)>0:
		f=open(ruta_csf,'a')
		for ip in ips:
		    f.write(ip+" # OVH Monitoring\n")
		f.close()
		print("Ips de monitorización de OVH añadidas correctamente")
	else:
		print("No hay ninguna ip que añadir al CSF")
else:
	print("No existe el fichero del CSF")
