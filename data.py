# -*- coding: utf-8 -*-
"""L'arborescence produits et le catalogue de demonstration.

L'ARBRE EST LA VRAIE LIVRAISON. Le client a dit « un arbre effectivement, c'est
ce que je recherche » : c'est la piece qui structure tout le reste — les URL,
le fil d'Ariane, les facettes disponibles, le referencement, et la facon dont
un acheteur hospitalier navigue. Il est ecrit ici a la main, a partir de la
nomenclature reelle du secteur, et PAS copie d'un catalogue existant.

LES PRODUITS SONT DE LA DONNEE DE DEMONSTRATION, et le site le dit en haut de
chaque page. Ils servent a montrer la mise en page d'une fiche B2B : reference,
unite de vente, prix a l'unite ET prix a la caisse, paliers de quantite,
disponibilite. Les vrais produits viendront de son fournisseur ou de son
import — je n'invente pas un catalogue reel et je ne recopie pas celui d'un
concurrent.
"""

MARQUE = '8MED'          # PLACEHOLDER — le client n'a pas encore donne le nom
ACCENT   = '#c1121f'     # ROUGE, demande du client. 6,22 sur blanc, 5,90 sur
                         # le fond teinte, et le blanc dessus fait 6,22 aussi :
                         # il marche comme couleur de texte ET comme fond de
                         # bouton, ce qui n'est pas vrai de tous les rouges.
ACCENT_D = '#9b1220'     # survol. Il etait reste BLEU quand j'ai bascule
                         # l'accent : le bouton virait au bleu marine au survol.

# ---------------------------------------------------------------------------
# L'arbre. Trois niveaux : rayon > famille > sous-famille.
# ---------------------------------------------------------------------------
ARBRE = [
 ('Protection individuelle', 'epi', [
    ('Gants', 'gants', ['Gants d’examen nitrile', 'Gants d’examen latex',
                        'Gants d’examen vinyle', 'Gants chirurgicaux stériles',
                        'Gants de manutention']),
    ('Masques et protection respiratoire', 'masques',
        ['Masques chirurgicaux type II', 'Masques chirurgicaux type IIR',
         'Appareils filtrants FFP2 / N95', 'Appareils filtrants FFP3',
         'Visières et écrans faciaux']),
    ('Blouses et tabliers', 'blouses',
        ['Blouses d’isolement', 'Blouses chirurgicales stériles',
         'Tabliers à usage unique', 'Combinaisons']),
    ('Coiffes et chaussants', 'coiffes',
        ['Charlottes', 'Calots', 'Couvre-chaussures', 'Surbottes']),
    ('Protection oculaire', 'oculaire', ['Lunettes de protection', 'Surlunettes']),
 ]),
 ('Consommables de soin', 'soin', [
    ('Pansements', 'pansements',
        ['Pansements adhésifs', 'Pansements hydrocolloïdes',
         'Pansements alginate', 'Pansements film transparent',
         'Pansements post-opératoires']),
    ('Compresses et gazes', 'compresses',
        ['Compresses stériles', 'Compresses non stériles',
         'Gaze hydrophile', 'Compresses imprégnées']),
    ('Bandages et contention', 'bandages',
        ['Bandes de crêpe', 'Bandes cohésives', 'Bandes de contention',
         'Filets tubulaires']),
    ('Fixation', 'fixation',
        ['Sparadraps', 'Rubans microporeux', 'Films de fixation']),
    ('Sutures et fermeture', 'sutures',
        ['Fils de suture résorbables', 'Fils de suture non résorbables',
         'Agrafeuses cutanées', 'Sutures adhésives']),
 ]),
 ('Injection et perfusion', 'injection', [
    ('Seringues', 'seringues',
        ['Seringues 1 ml', 'Seringues 2 à 5 ml', 'Seringues 10 à 20 ml',
         'Seringues à gavage', 'Seringues pré-remplies']),
    ('Aiguilles', 'aiguilles',
        ['Aiguilles hypodermiques', 'Aiguilles de sécurité',
         'Aiguilles à ailettes', 'Lancettes']),
    ('Abords vasculaires', 'abords',
        ['Cathéters IV périphériques', 'Prolongateurs', 'Robinets et rampes',
         'Valves bidirectionnelles']),
    ('Perfusion', 'perfusion',
        ['Perfuseurs par gravité', 'Tubulures pour pompe',
         'Poches et flacons', 'Régulateurs de débit']),
    ('Collecte des piquants', 'opct',
        ['Collecteurs 0,5 à 2 L', 'Collecteurs 3 à 6 L', 'Collecteurs 10 L et +']),
 ]),
 ('Diagnostic et monitorage', 'diagnostic', [
    ('Pression artérielle', 'tension',
        ['Tensiomètres manuels', 'Tensiomètres électroniques',
         'Brassards de rechange']),
    ('Auscultation', 'auscultation',
        ['Stéthoscopes simple pavillon', 'Stéthoscopes double pavillon',
         'Stéthoscopes pédiatriques']),
    ('Température', 'temperature',
        ['Thermomètres frontaux', 'Thermomètres auriculaires',
         'Thermomètres digitaux', 'Embouts de protection']),
    ('Oxymétrie et ECG', 'oxy',
        ['Oxymètres de pouls', 'Capteurs SpO2', 'Électrodes ECG',
         'Gel de contact']),
    ('Tests rapides', 'tests',
        ['Bandelettes urinaires', 'Tests glycémie', 'Tests antigéniques']),
 ]),
 ('Désinfection et hygiène', 'hygiene', [
    ('Antisepsie cutanée', 'antisepsie',
        ['Chlorhexidine', 'Povidone iodée', 'Alcool modifié',
         'Compresses imprégnées']),
    ('Désinfection des surfaces', 'surfaces',
        ['Sprays désinfectants', 'Lingettes désinfectantes',
         'Détergents-désinfectants sols', 'Désinfectants dispositifs médicaux']),
    ('Hygiène des mains', 'mains',
        ['Solutions hydro-alcooliques', 'Savons antiseptiques',
         'Distributeurs', 'Crèmes de soin']),
    ('Stérilisation', 'sterilisation',
        ['Sachets de stérilisation', 'Rubans indicateurs',
         'Intégrateurs chimiques', 'Tests de Bowie-Dick']),
 ]),
 ('Bloc opératoire', 'bloc', [
    ('Champs et draps', 'champs',
        ['Champs opératoires stériles', 'Champs fenêtrés', 'Draps de table',
         'Housses de protection']),
    ('Kits de procédure', 'kits',
        ['Sets de pansement', 'Sets de suture', 'Sets de sondage',
         'Sets de perfusion']),
    ('Instruments à usage unique', 'instruments',
        ['Pinces', 'Ciseaux', 'Bistouris et lames', 'Écarteurs']),
    ('Aspiration', 'aspiration',
        ['Sondes d’aspiration', 'Bocaux et poches', 'Tubulures d’aspiration']),
 ]),
 ('Respiratoire', 'respi', [
    ('Oxygénothérapie', 'oxygene',
        ['Lunettes à oxygène', 'Masques à oxygène', 'Masques haute concentration',
         'Humidificateurs']),
    ('Aérosolthérapie', 'aerosol',
        ['Nébuliseurs', 'Masques de nébulisation', 'Chambres d’inhalation']),
    ('Voies aériennes', 'voies',
        ['Canules de Guedel', 'Sondes d’intubation', 'Masques laryngés',
         'Ballons insufflateurs']),
 ]),
 ('Soins au patient', 'patient', [
    ('Incontinence', 'incontinence',
        ['Protections anatomiques', 'Changes complets', 'Alèses jetables',
         'Alèses lavables']),
    ('Sondage urinaire', 'sondage',
        ['Sondes vésicales', 'Poches à urine', 'Étuis péniens',
         'Sets de sondage']),
    ('Hygiène du patient', 'toilette',
        ['Gants de toilette', 'Shampooings sans rinçage',
         'Soins de bouche', 'Bassins et urinaux']),
    ('Prévention des escarres', 'escarres',
        ['Coussins de positionnement', 'Matelas à air', 'Talonnières']),
 ]),
 ('Mobilier et équipement', 'mobilier', [
    ('Mobilier de soin', 'meubles',
        ['Tables d’examen', 'Chariots de soins', 'Guéridons',
         'Paravents', 'Escabeaux']),
    ('Lits et accessoires', 'lits',
        ['Lits médicalisés', 'Barrières', 'Potences', 'Tables de lit']),
    ('Éclairage', 'eclairage',
        ['Lampes d’examen', 'Lampes frontales', 'Négatoscopes']),
    ('Pesée et mesure', 'pesee',
        ['Pèse-personnes', 'Pèse-bébés', 'Toises']),
 ]),
 ('Aide à la mobilité', 'mobilite', [
    ('Fauteuils roulants', 'fauteuils',
        ['Fauteuils manuels', 'Fauteuils de transfert', 'Coussins et accessoires']),
    ('Marche', 'marche',
        ['Déambulateurs', 'Rollators', 'Cannes', 'Béquilles']),
    ('Transfert', 'transfert',
        ['Lève-personnes', 'Sangles', 'Disques et planches de transfert']),
 ]),
 ('Gestion des déchets', 'dechets', [
    ('Déchets d’activités de soins', 'dasri',
        ['Sacs DASRI', 'Cartons et fûts', 'Supports de sacs']),
    ('Piquants, coupants, tranchants', 'pct',
        ['Collecteurs muraux', 'Collecteurs de paillasse', 'Fûts de regroupement']),
    ('Collecte et transport', 'collecte',
        ['Chariots de collecte', 'Bacs roulants', 'Étiquettes réglementaires']),
 ]),
 ('Psychiatrie et santé mentale', 'psy', [
    ('Sécurité et prévention du risque', 'securite',
        ['Mobilier anti-ligature', 'Poignées et robinetterie sécurisées',
         'Vitrage de sécurité', 'Miroirs incassables',
         'Textiles anti-déchirure']),
    ('Contention et apaisement', 'apaisement',
        ['Ceintures de maintien', 'Sangles de lit', 'Couvertures lestées',
         'Fauteuils d’apaisement', 'Salles de retour au calme']),
    ('Chambre d’isolement', 'isolement',
        ['Lits sécurisés', 'Matelas ignifugés', 'Éclairage encastré',
         'Interphonie et appel malade']),
    ('Évaluation et suivi', 'evaluation',
        ['Échelles d’évaluation', 'Classeurs de suivi',
         'Tablettes de saisie', 'Bracelets d’identification']),
    ('Activités thérapeutiques', 'therapie',
        ['Matériel d’ergothérapie', 'Matériel d’art-thérapie',
         'Stimulation sensorielle', 'Matériel de psychomotricité']),
 ]),
 ('Médicament et pharmacie', 'medicament', [
    ('Stockage et sécurité', 'stockage',
        ['Armoires à pharmacie', 'Coffres à stupéfiants',
         'Réfrigérateurs médicaux', 'Enregistreurs de température']),
    ('Préparation et distribution', 'preparation',
        ['Piluliers hebdomadaires', 'Sachets de préparation',
         'Broyeurs et coupe-comprimés', 'Gobelets doseurs',
         'Chariots de distribution']),
    ('Administration', 'administration',
        ['Seringues orales', 'Compte-gouttes', 'Cuillères doseuses',
         'Nébuliseurs de dose']),
    ('Traçabilité', 'tracabilite',
        ['Étiquettes de nominatif', 'Lecteurs de code-barres',
         'Registres de stupéfiants', 'Scellés de sécurité']),
    ('Consommables de pharmacie', 'conso_pharma',
        ['Flacons et piluliers vides', 'Sachets unidose',
         'Étiquettes vierges', 'Sacs de transport isothermes']),
 ]),
 ('Laboratoire et anatomopathologie', 'labo', [
    ('Prélèvement', 'prelevement',
        ['Tubes sous vide', 'Corps de pompe et adaptateurs',
         'Garrots', 'Portoirs']),
    ('Contenants d’échantillons', 'contenants',
        ['Flacons stériles', 'Pots à prélèvement', 'Cassettes d’inclusion',
         'Lames et lamelles']),
    ('Consommables de paillasse', 'paillasse',
        ['Pipettes', 'Embouts', 'Boîtes de Petri', 'Écouvillons']),
    ('Anatomopathologie et autopsie', 'anapath',
        ['Formol tamponné', 'Instruments d’autopsie',
         'Tabliers et manchettes', 'Sacs et housses']),
 ]),
]

# ---------------------------------------------------------------------------
# Les facettes. Elles se CUMULENT — c'est le point de la structure
# WebstaurantStore : un acheteur arrive par la categorie puis reduit.
# ---------------------------------------------------------------------------
FACETTES = [
    ('marque',      'Marque',              None),
    ('conditio',    'Conditionnement',     ['À l’unité', 'Boîte', 'Carton', 'Palette']),
    ('sterile',     'Stérilité',           ['Stérile', 'Non stérile']),
    ('usage',       'Usage',               ['Usage unique', 'Réutilisable']),
    ('latex',       'Latex',               ['Sans latex', 'Contient du latex']),
    ('dispo',       'Disponibilité',       ['En stock', 'Sur commande']),
]

MARQUES = ['Aurelis', 'Bervia', 'Cortemed', 'Dulane', 'Ferox Care', 'Helvia',
           'Kernos', 'Lumea Medical', 'Novaris', 'Praxa', 'Sorenta', 'Vantek']
