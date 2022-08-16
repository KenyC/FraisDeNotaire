# %%
import json
import enum


with open("baremes_imposition.json", "r") as f:
	baremes = json.load(f)

class Localisation(enum.Enum):
	METROPOLE_CORSE  = 1
	REUNION          = 2
	MAYOTTE          = 3
	GUADELOUPE       = 4
	MARTINIQUE       = 5
	GUYANNE          = 6


						
# localization = Localisation.METROPOLE_CORSE # Metropolitan France
# departement = "75" # Val-de-Marne
# is_new = False
# price = 200000

def compute_notary_fee(localization : Localisation, departement : str, is_new : bool, price : float) -> dict:
	if isinstance(departement, int): 
		departement = str(departement)
	tranches = baremes["Tranche"]

	# Emoluments du notaire (ce que le notaire perçoit)
	emoluments_notaires_ht = 0
	for tranche_info in baremes["Tranche"]:
		no_upper_limit = tranche_info["max_tranche"] is None
		if price < tranche_info["min_tranche"]:
			amount_in_tranche = 0
		elif no_upper_limit or price < tranche_info["max_tranche"]:
			amount_in_tranche = price - tranche_info["min_tranche"]
		else:
			amount_in_tranche = tranche_info["max_tranche"] - tranche_info["min_tranche"]
		emoluments_notaires_ht += (tranche_info["taux"] / 100) * amount_in_tranche

	emoluments_notaires_hors_majoration = emoluments_notaires_ht
	if localization in [Localisation.MAYOTTE, Localisation.REUNION]:
		emoluments_notaires_hors_majoration *= 1 + baremes["Majoration"]["mayotte_reunion"] / 100
	elif localization in [Localisation.GUADELOUPE, Localisation.MARTINIQUE, Localisation.GUYANNE]:
		emoluments_notaires_hors_majoration *= 1 + baremes["Majoration"]["martinique_guadeloupe_guyane"] / 100

	emoluments_notaires_ttc = emoluments_notaires_hors_majoration
	if localization == Localisation.METROPOLE_CORSE:  
		tva_emoluments = baremes["TVA"]["metropolitane_et_corse"]
	else: # outre-mer
		tva_emoluments = baremes["TVA"]["outre_mer"]
	emoluments_notaires_ttc *= 1 + tva_emoluments / 100

	# %%
	"""
	##  Droits Taxes

	DMTO + sécurité
	"""

	dmto = price * baremes["DMTO"][departement]["neuf" if is_new else "ancien"] / 100
	securite = max(price * (baremes["securite"] / 100), baremes["securite_min"])
	total_tax = dmto + securite

	# %%
	"""
	## Emoluments de débours et formalités

	Ceci est une estimation
	"""

	if localization in [Localisation.METROPOLE_CORSE]:
		emoluments_debours = baremes["Emoluments"]["metropolitane"]
	elif localization in [Localisation.MAYOTTE, Localisation.REUNION]:
		emoluments_debours = baremes["Emoluments"]["mayotte_reunion"]
	elif localization in [Localisation.GUADELOUPE, Localisation.GUYANNE, Localisation.MARTINIQUE]:
		emoluments_debours = baremes["Emoluments"]["martinique_guadeloupe_guyane"]

	total = emoluments_notaires_ttc + total_tax + emoluments_debours

	return {
		"emoluments_notaires_ht": emoluments_notaires_ht,
		"emoluments_notaires_hors_majoration": emoluments_notaires_hors_majoration,
		"emoluments_notaires_ttc": emoluments_notaires_ttc,
		"dmto": dmto,
		"securite": securite,
		"total_tax": total_tax,
		"emoluments_debours": emoluments_debours,
		"total": total
	}

# %%


