# -*- coding: utf-8 -*-
"""
tato funkce pocita prumernou kortikalni tloustku pro dane laloky. pred spustenim je treba v promenne pacients
uvest ID pacientu z datasetu, pro ktere se ma tloustka pocitat. dale je treba jiz mit vytvorene segmenaci jednotlivych
laloku, tento soubor se nacita do promenne lobes, je potreba zde zadat cestu k segmentacnimu nifti souboru. take je potreba
mit vytvoreny i soubor s vypocitanou kortikalni tloustkou pro daneho pacienta, zde je opet potreba zadat celou cestu k tomuto
souboru v promenne thickness
"""

import SimpleITK as sitk
import numpy as np
import csv
import os
import pandas as pd

# Název CSV souboru
csv_file = "public_thickness_results.csv"
file_exists = os.path.isfile(csv_file)
pacients = []

# Otevření CSV souboru pro zápis
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    if not file_exists:
        # Zápis záhlaví CSV souboru
        writer.writerow(["Pacient", "R_front", "L_front", "R_temp", "L_temp"])
    
    for pacient in pacients:
        # nacteni nasegmentovanych laloku a kortikalni tloustky
        pacient_id = pacient
        
        lobes = sitk.ReadImage(r"cesta")
        thickness = sitk.ReadImage(r"cesta")
        
        # Nastavení vlastností obrazu thickness tak, aby odpovídaly obrazu lobes
        thickness.SetOrigin(lobes.GetOrigin())
        thickness.SetSpacing(lobes.GetSpacing())
        thickness.SetDirection(lobes.GetDirection())
        
        row_data = [pacient_id]
        
        for label in range(1, 5):
            # pocitani prumerne kortikalni tloustky pro kazdy lalok, ktery je oznacen labelem 1 az 4, jejich poradi
            # odpovida poradi nazvu laloku v csv souboru
            region_mask = sitk.BinaryThreshold(lobes, lowerThreshold=label, upperThreshold=label)
            region_thickness = sitk.Mask(thickness, region_mask)
            region_array = sitk.GetArrayFromImage(region_thickness)
            non_zero_thickness = region_array[region_array != 0]
            average_thickness = np.mean(non_zero_thickness)
            
            row_data.append(average_thickness)
        
        # Zápis výsledků do CSV souboru po sloupcích
        writer.writerow(row_data)

print("Výsledky byly uloženy do CSV souboru:", csv_file)

# Název Excel souboru
excel_file = "public_thickness_results.xlsx"

# Načtení dat z CSV do pandas DataFrame
data = pd.read_csv(csv_file)

# Vytvoření Excel souboru
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    data.to_excel(writer, index=False)

print("Výsledky byly uloženy do Excel souboru:", excel_file)
