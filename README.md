# Maquette de structure — ecommerce B2B matériel médical et hospitalier

Construite sur le modèle de structure demandé par le client (WebstaurantStore),
et **pas** sur le thème Arolax : un thème d'agence s'effondre sur un catalogue
de plusieurs milliers de références.

## Ce qui est réel dans cette maquette

L'**arborescence** : 14 rayons, 59 familles, 227 sous-familles, écrites à la
main d'après la nomenclature du secteur. C'est la pièce qui structure les URL,
le fil d'Ariane, les facettes disponibles et le référencement.

La **mécanique B2B** :
- distinction caisse / unité sur chaque fiche, avec les deux prix
- paliers de quantité (1+, 6+, 24+, 96+)
- facettes cumulables, recomptées sur le résultat courant
- commande rapide par référence
- demande de devis plutôt que paiement carte

## Ce qui ne l'est pas

Les **articles et les prix sont des données de démonstration**, et un bandeau
le dit en haut de chaque page. Les fourchettes de prix sont calées par rayon
pour rester crédibles, mais ce ne sont pas de vrais tarifs. Le catalogue réel
viendra du fournisseur du client ou d'un import.

Le nom **8MED** est un placeholder.

## Régénérer

    python3 build.py index.html

Le catalogue est déterministe (dérivé d'un hachage) : deux constructions
donnent le même fichier.
