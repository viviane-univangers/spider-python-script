# Generate_id_spider.py

Ce script Python génère un **identifiant unique** pour chaque patient, **quel que soit le laboratoire** qui a réalisé l’analyse.  
Il permet d'assurer que le même patient obtient **toujours le même identifiant SPIDER**, même si ses données proviennent de centres différents.

---

## 🎯 Objectif

Les fichiers exportés depuis SPIDER peuvent contenir plusieurs lignes pour un même patient, provenant de centres différents, avec plusieurs échantillons.

Ce script :

- analyse chaque fichier dans l’ordre chronologique t0 → t1 → t2 → …  
- attribue un identifiant unique de type `MI000000001` (il est recommandé de changer la configuration de votre identifiant unique directement dans le script --> fonction def _new_id(self)) 
- garantit que tous les échantillons d’un même patient partagent le même identifiant  
- reconstruit l’historique pour retrouver le même identifiant dans les fichiers suivants  
- ajoute une colonne `id_spider` dans chaque fichier

---

## 📁 Entrée / Sortie

### Entrée  
- Convertissez les sorties csv de votre SPIDER en fichier Excel
- Les fichiers Excel doivent contenir au minimum les colonnes :
- `medical_record_number`
- `sharing_center_name`
- `sample_id_in_lab*` (une ou plusieurs colonnes commençant par ce nom)

### Sortie  
Dans le dossier `output/` :

- `t0_with_spider.xlsx`
- `t1_with_spider.xlsx`
- `t2_with_spider.xlsx`
- etc.

Chaque fichier contient une nouvelle colonne :
- `id_spider`


## 🚀 Utilisation

1. Exportez depuis SPIDER le fichier csv et convertissez en fichier Excel : exemple `t0.xlsx`, `t1.xlsx`, `t2.xlsx`, etc.
2. Place-le dans un dossier et indiquer le chemin dans le script.
3. Modifie dans `Generate_id_spider.py` la liste des fichiers à traiter :

```python
input_files = [
    "/chemin/du/fichier/input/t0.xlsx",
    "/chemin/du/fichier/input/t1.xlsx",
    "/chemin/du/fichier/input/t2.xlsx",
]
```

4. Indiquer le dossier dans lequel le fichier de sortie sera enrégistré

```python
output_folder = "/chemin/du/fichier/output"
```

5. Dans un terminal et dans le repertoire ou se trouve le script lancez:

python3 Generate_id_spider.py

6. Vérification des fichiers de sortie :
- `/chemin/du/fichier/output/t0_with_spider.xlsx`
- `/chemin/du/fichier/output/t1_with_spider.xlsx`
- `/chemin/du/fichier/output/t2_with_spider.xlsx`


## 🧠 Fonctionnement interne

1. SpiderAssigner

- Maintient un historique : (centre, échantillon) → id_spider

- Attribue un identifiant unique selon le format MI000000001 (qui est recommandé de modifier en fonction de votre projet)

2. Processus d’attribution

Pour chaque patient (groupé par medical_record_number) :

Recherche si un de ses échantillons apparaît dans l’historique

Si oui → récupère son identifiant existant

Sinon → génère un nouvel identifiant

Met à jour l’historique

Écrit la colonne id_spider dans la sortie









