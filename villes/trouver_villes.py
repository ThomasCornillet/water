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

path = os.getcwd() + "/villes/dpt/info"
os.chdir(path)
liste_dpt = list(tt_dpt.keys())

i = 0
while i < len(liste_dpt):
	nom_dpt = liste_dpt[i]
	nom_fichier = nom_dpt + ".info"
	contenu_fichier_l = tt_dpt[nom_dpt]
	contenu_fichier = "\n".join(" - ".join(v) for v in contenu_fichier_l)
	with open(nom_fichier, 'w') as mon_fichier:
		mon_fichier.write(contenu_fichier)
	i += 1
