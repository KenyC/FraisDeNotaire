Frais d'acquisition (aka frais de notaires)
=========================

Dernière date de mise à jour: 2022/08/16

Ce scrypt python calcule les fraise de notaires d'un achat immobilier en France. Je me suis contenté de transcrire le script utilisé par [le simulateur de l'ANIL](https://www.anil.org/outils/outils-de-calcul/frais-dacquisition-dits-frais-de-notaire/) (qui est celui recommandé par le site du gouvernement).

## Usage

```python
compute_notary_fee(localization.METROPOLE_CORSE, "75", is_new = False, 200000)
```

```
{'emoluments_notaires_ht': 2033.4099999999999,
 'emoluments_notaires_hors_majoration': 2033.4099999999999,
 'emoluments_notaires_ttc': 2440.0919999999996,
 'dmto': 11613.3,
 'securite': 200.0,
 'total_tax': 11813.3,
 'emoluments_debours': 1360,
 'total': 15613.392}
```
## Frais d'acquisition vs frais de notaires

Dans le langage courant, on utilise l'expression "frais de notaire" pour désigner l'argent collecté par le notaire sur toute acquisition. C'est un chouïa impropre ; cela donne l'impression que c'est le notaire qui pratique et empoche ces frais. En réalité, le notaire collecte l'argent pour le compte de l'état et n'en perçoit qu'une partie. L'ANIL utilise le terme *frais d'acquisition*, qui est plus logique.

## Qui paie ?

Ces frais sont normalement à la charge de celui qui achète. Si acheteur et vendeur tombent d'accord, le vendeur peut éventuellement payer.

## Que contiennent les frais d'acquisition ?

   * Emoluments du notaires: ce que le notaire perçoit 
      - Base (calculée sur le principe d'un l'impôt par tranches décroissant !)
      - + Majoration (uniquement pour l'Outre-Mer)
      - + TVA (pour tout le monde)
   * Droits et taxes: ce que l'Etat perçoit 
   	  - Droits de Mutation à Titre Onéreux (DMTO): nom étrange s'il en est, cette taxe est considérablement réduite sur un bien neuf.
   	  - Contribution de sécurité immobilière
   * Emoluments de débours: ce que j'imagine correspondre à des frais de dossier.


## Ordres de grandeur et facteurs

Pourcentages estimés sur la base de l'achat d'un bien ancien de 200 000€ à Paris:

Total 15 613 € (soit 8% du prix d'achat) dont:

  - émoluments du notaire (~ 15 % des frais)
  - droits et taxes (~ 75 % des frais)
  - émoluments de débours (~ 10% des frais)

Pour un bien neuf, les frais sont seulement de 5430 € (soit un tiers de leur valeur originale), dûs à une réduction du DMTO mentionnée plus haut. En général, une réduction par 2.

