#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 02/2025
# viviane

# ce script creer un identifiant spider unique au patient peut importe dans quel labo a été fait l'analyse
# pour cela on a beosin des données intégré dans spider
# Tu mets tes fichiers Excel télécharger sur spider (t0.xlsx, t1.xlsx, etc.) dans ton dossier.
# Tu lances le script. python3 Generate_id_spider.py
# Dans le dossier output/, tu récupères les fichiers t0_with_spider.xlsx, t1_with_spider.xlsx, etc., 
# chacun avec la colonne id_spider ajoutée.


import pandas as pd
from pathlib import Path

class SpiderAssigner:
    def __init__(self):
        # historique : (centre, sample) -> id_spider
        self.history = {}
        self.next_id = 1

    def _new_id(self):     # à modifier exemple spider_id = f"XU{self.next_id:09d}" pour avoir des id_spider XU000000001
        spider_id = f"MI{self.next_id:09d}"
        self.next_id += 1
        return spider_id

    def assign_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["id_spider"] = None

        # Grouper par MRN pour que toutes les lignes d’un patient aient le même id dans ce fichier
        for mrn, group in df.groupby("medical_record_number"):
            assigned_id = None

            # Vérifier si déjà présent dans l’historique
            for idx, row in group.iterrows():
                centre = row["sharing_center_name"]
                samples = [row[col] for col in df.columns if col.startswith("sample_id_in_lab")]

                for sample in samples:
                    if pd.notna(sample) and (centre, sample) in self.history:
                        assigned_id = self.history[(centre, sample)]
                        break
                if assigned_id:
                    break

            # Si aucun match -> nouveau id_spider
            if not assigned_id:
                assigned_id = self._new_id()

            # Assigner à toutes les lignes du MRN
            df.loc[group.index, "id_spider"] = assigned_id

            # Mise à jour de l’historique
            for idx, row in group.iterrows():
                centre = row["sharing_center_name"]
                samples = [row[col] for col in df.columns if col.startswith("sample_id_in_lab")]
                for sample in samples:
                    if pd.notna(sample):
                        self.history[(centre, sample)] = assigned_id

        return df


def process_files(input_files, output_folder):
    assigner = SpiderAssigner()
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    for file in input_files:
        df = pd.read_excel(file)
        df_with_ids = assigner.assign_ids(df)

        output_file = Path(output_folder) / f"{Path(file).stem}_with_spider.xlsx"
        df_with_ids.to_excel(output_file, index=False)
        print(f"✅ Fichier traité : {output_file}")


if __name__ == "__main__":
    # Liste des fichiers Excel à traiter dans l’ordre chronologique
    input_files = [
        "/chemin/du/fichier/input/central.xlsx"         # mettre le bon chemin
        #"/chemin/du/fichier/input/patients_All_An_Ni_t0.xlsx",
        #"/chemin/du/fichier/input/patients_All_An_Ni_t1.xlsx",
        #"/chemin/du/fichier/input/patients_All_An_Ni_t2.xlsx",
        #"/chemin/du/fichier/input/patients_All_An_Ni_t3.xlsx",
        #"/chemin/du/fichier/input/patients_All_An_Ni_t4.xlsx",
    ]

    output_folder = "/chemin/du/fichier/output"        # mettre le bon chemin
    process_files(input_files, output_folder)



