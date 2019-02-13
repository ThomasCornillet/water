#!/usr/bin/python3
# -*-coding:Utf-8 -*

import requests
import re

requested_data = [ ["PH *", "pH"], ["NITRATES", "Nitrates (NO3)"], ["CALCIUM", "Calcium (Ca)"] , ["MAGNÉSIUM", "Magnésium (Mg)"], ["SODIUM", "Sodium (Na)"], ["CHLORURES", "Chlorures (Cl-)"], ["SULFATES", "Sulfates (SO4)"], ["POTASSIUM", "Potassium (K)"], ["TITRE ALCALIMÉTRIQUE COMPLET", "Alkalinity as HCO3"], ["TITRE HYDROTIMÉTRIQUE", "Alkalinity as CaCO3"] ]

post_data = {
	"methode": "rechercher",
	"idRegion": "73",
	"usd": "AEP",
	"posPLV": "0",
	"departement": "031",
	"communeDepartement": "31555",
	"reseau": "031000006_031"
}

i = 0
resultat = []
while i < len(requested_data):


	http_session = requests.session()

	first_url = "https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&idRegion={region}&dpt={dpt}&usd={usd}&comDpt={comdpt}".format( region=post_data["idRegion"], dpt=post_data["departement"], usd=post_data["usd"], comdpt=post_data["communeDepartement"] )

	print ( "Loading website" )
	#print( "Loading:", first_url )
	result = http_session.get( first_url )

	if result.status_code == 200:
		failure = False
		pos_plv = 0
		source_url = "https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do"

		pattern = re.compile( r"{0}".format( requested_data[i][0] ) )

		while pattern.search( result.text ) is None:

			print( "Try #{}, searching \"{}\"".format( pos_plv, requested_data[i][1] ) )
			print( "Loading:", source_url )
			result = http_session.post( source_url, post_data )

			if result.status_code != 200:
		  		print( "Unable to get page:", result.status_code, result.reason )
		  		failure = True
		  		break

			pos_plv += 1
			post_data["posPLV"] = str(pos_plv)

		if not failure:
			print( "Data found." )

			soup = BeautifulSoup( result.text, features="html.parser" )

			# All page tables have the same "id"...
			for table in soup.find_all( id="tableau" ):
				tds = table.find_all( "td", { "class": "gras" } )
				found = False

				for td in tds:
					if len(td.contents):
						# Some td have div tag inside...
						title = td.contents[0].find( "Valeur" )

						if title is not None and title >= 0:
							# Good table !
							found = True
							break

				if found:
					for tr in table.find_all( "tr" ):
						td = tr.find( "td" )
						needed_data = False
						
						if len(td.contents) and td.contents[0].find(requested_data[i][0] ) >= 0:
							needed_data=True
						
						if needed_data:
							print( " ".join( tr.stripped_strings ) )
							resultat.append( " ".join( tr.stripped_strings) )

		else:
			print( "Unable to find criteria" )

	else:
		print( "Can not get main page:", result.status_code, result.reason )

	i += 1

i = 0
while i < len(resultat):
	unit = resultat[i].split(" ")
	if unit[0] == "IODOSULFURON-METHYL-SODIUM":
		del resultat[i]
		break

	i += 1

print("Voici le résumé des résultats :\n")
for elt in resultat:
	unit = elt.split(" ")
	for elt2 in requested_data:
		if unit[0] == "PH":
			nom = "pH"
		elif unit[0] == "TITRE":
			if unit[1] == "ALCALIMÉTRIQUE":
				nom = "Alkalinity as HCO3"
			else:
				nom = "Alkalinity as CaCO3"
		else:
			if unit[0] == elt2[0]:
				nom = elt2[1]
	if unit[0] == "PH":
		print("{} = {}".format(nom, unit[2]))
	elif unit[0] == "TITRE":
		if unit[1] == "ALCALIMÉTRIQUE":
			deg_f_str1 = unit[3]
			deg_f_list = deg_f_str1.split(",")
			deg_f_str2 = ".".join(deg_f_list)
			deg_f = float(deg_f_str2)
			alca_hco3 = deg_f * 12.2
			print("{} = {} mgl/L".format(nom, alca_hco3))
			print("    Titre alcalimétrique complet (TAC) = {} °f".format(deg_f_str1))
		else:
			deg_f_str1 = unit[2]
			deg_f_list = deg_f_str1.split(",")
			deg_f_str2 = ".".join(deg_f_list)
			deg_f = float(deg_f_str2)
			alca_caco3 = deg_f * 10
			print("Alkalinity as CaCO3 = {} mg/L".format(alca_caco3))
			print("    Titre hydrotimétrique (TH) = {} °f".format(deg_f_str1))
	else:
		print("{} = {} {}".format(nom, unit[1], unit[2]))

for elt in resultat:
	unit = elt.split(" ")
	if unit[0] == "CALCIUM":
		resu_ca_str1 = unit[1]
		test = []
		for elt1 in resu_ca_str1:
			if elt1 == ",":
				test.append("virgule")
		if len(test) != 0:
			resu_ca_list = resu_ca_str1.split(",")
			resu_ca_str2 = ".".join(resu_ca_list)
			resu_ca = float(resu_ca_str2)
		else:
			resu_ca = float(resu_ca_str1)
	elif unit[0] == "MAGNÉSIUM":
		resu_mg_str1 = unit[1]
		test = []
		for elt1 in resu_mg_str1:
			if elt1 == ",":
				test.append("virgule")
		if len(test) != 0:
			resu_mg_list = resu_mg_str1.split(",")
			resu_mg_str2 = ".".join(resu_mg_list)
			resu_mg = float(resu_mg_str2)
		else:
			resu_mg = float(resu_mg_str1)
res_alka = alca_caco3 - ((resu_ca / 14) + (resu_mg / 1.7))
print("\nResidual Alkalinity as CaCO3 = {} mg/L".format(res_alka))
