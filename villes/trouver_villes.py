#!/usr/bin/python3
# -*-coding:Utf-8 -*

import requests
import re
import os
from bs4 import BeautifulSoup

http_session = requests.session()

resultat = []

a = 1
while a < 100:
	if a < 10:
		b = str(a)
		c = "0" + b
	else:
		c = str(a)
	url = "https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&idRegion=" + c
	result = http_session.get(url)
	soup = BeautifulSoup(result.text)
	select = soup.find("select", {"name":"departement"})
	for option in select.find_all("option"):
		id_region = c
		id_dpt = option.get("value")
		nom_dpt = option.get_text()
		ensemble = [id_region, id_dpt, nom_dpt]
		resultat.append(ensemble)
	a += 1

print(resultat)

resultat2 = []

i = 0
while i < len(resultat):
	id_region = resultat[i][0]
	id_dpt = resultat[i][1]
	nom_dpt = resultat[i][2]
	url = "https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&idRegion={rg}&dpt={dt}".format(rg=id_region, dt=id_dpt)
	result = http_session.get(url)
	soup = BeautifulSoup(result.text)
	select = soup.find("select", {"name":"communeDepartement"})
	for option in select.find_all("option"):
		id_ville = option.get("value")
		nom_ville = option.get_text()		
		ensemble = [id_region, id_dpt, nom_dpt, id_ville, nom_ville]
		resultat2.append(ensemble)
	i += 1

print(resultat2)

resultat3 = []
	
i = 0
while i < len(resultat2):
	id_region = resultat2[i][0]
	id_dpt = resultat2[i][1]
	nom_dpt = resultat2[i][2]
	id_ville = resultat2[i][3]
	nom_ville = resultat2[i][4]
	url = "https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&idRegion={rg}&dpt={dt}&comDpt={vil}".format(rg=id_region, dt=id_dpt, vil=id_ville)
	result = http_session.get(url)
	soup = BeautifulSoup(result.text)
	select = soup.find("select", {"name":"reseau"})
	for option in select.find_all("option"):
		id_reseau = option.get("value")
		nom_reseau = option.get_text()
		ensemble = [id_region, id_dpt, nom_dpt, id_ville, nom_ville, id_reseau, nom_reseau]
		resultat3.append(ensemble)
	i += 1

print(resultat3)

resultat3.sort()
tt_dpt = {}

i = 0
while i < len(resultat3):
	id_dpt = resultat3[i][1]
	nom_dpt = resultat3[i][2]
	if i == 0:
		tt_dpt[nom_dpt] = [resultat3[i]]
	elif id_dpt == resultat3[i - 1][1]:
		tt_dpt[nom_dpt].append(resultat3[i])
	else:
		tt_dpt[nom_dpt] = [resultat3[i]]
	i += 1

path = os.getcwd() + "/villes/dpt/ini"
os.chdir(path)
liste_dpt = list(tt_dpt.keys())

i = 0
while i < len(liste_dpt):
	nom_dpt = liste_dpt[i].capitalize()
	info_dpt = tt_dpt[liste_dpt[i]]
	id_dpt = info_dpt[0][1]
	id_region = info_dpt[0][0]
	url_dpt = "https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&idRegion={rg}&dpt={dt}".format(rg=id_region, dt=id_dpt)
	fichier_ini = configparser.ConfigParser()
	# création des informations de bases sur le département
	fichier_ini['infos'] = {}
	fichier_ini['infos']['nom_dpt'] = nom_dpt
	fichier_ini['infos']['code_dpt'] = id_dpt
	fichier_ini['infos']['nom_region'] = ""
	fichier_ini['infos']['code_region'] = id_region
	fichier_ini['infos']['nb_ville'] = ""
	fichier_ini['infos']['nb_reseaux'] = ""
	fichier_ini['infos']['url_dpt'] = url_dpt
	# création des villes
	j = 0
	while j < len(info_dpt):
		if j < 9:
			no_ville = "00" + str(j+1)
		elif j >= 9  and j < 99:
			no_ville = "0" + str(j+1)
		else:
			no_ville = str(j+1)
		code_ini = "ville_" + no_ville
		info_ville = info_dpt[j]
		nom_ville = info_ville[4]
		id_ville = info_ville[3]
		url_ville = "https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&idRegion={rg}&dpt={dt}&comDpt={vil}".format(rg=id_region, dt=id_dpt, vil=id_ville)
		nom_reseau = info_ville[6]
		id_reseau = info_ville[5]
		fichier_ini[code_ini] = {}
		fichier_ini[code_ini]['nom_ville'] = nom_ville
		fichier_ini[code_ini]['code_ville'] = id_ville
		fichier_ini[code_ini]['url_ville'] = url_ville
		fichier_ini[code_ini]['nom_reseau'] = nom_reseau
		fichier_ini[code_ini]['code_reseau'] = id_reseau
		j += 1
	nb_villes = len(fichier_ini) - 2
	fichier_ini['infos']['nb_villes'] = str(nb_villes)
	nom_fichier = nom_dpt + ".ini"
	with open(nom_fichier, 'w') as departement:
		fichier_ini.write(departement)
	i += 1
