# -*- coding: utf-8 -*-
"""
Tato funkce slouzi k reorientaci obrazu na formát "IAL". nejprve se zvoli pacienti, u kterych je treba reorientaci provest
a nasledne je nacten podle cesty obraz k reorientaci. pote je mozno nacist dalsi obraz, napr segmentaci masku atd. a je porovnano
zda maji obrazy stejne rozmery. na zaver je to vypsano do terminalu
"""

from img_load import load_nifti_data
import ants


pacients = []

for pacient in pacients:
    # provedeni reorientace
    
    pacient_reorient = ants.image_read(r"cesta", reorient='IAL')
    ants.image_write(pacient_reorient, r"cesta")

    # Načtení obou obrázků
    obraz1 = ants.image_read(r"cesta")
    obraz2 = ants.image_read(r"cesta")

    # Kontrola, zda mají shodné rozměry
    if obraz1.shape == obraz2.shape:
        print(f"Obrázky {pacient} mají shodné rozměry: {obraz1.shape}")
    else:
        print(f"Obrázky {pacient} mají různé rozměry: {obraz1.shape} a {obraz2.shape}")