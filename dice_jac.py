# -*- coding: utf-8 -*-
"""
Tato funkce pocita dice a jaccard koeficienty jakozto metriky pro srovnani segmentace mozku automatickou metodou vytvoreni segmentacnich masek a manualni segmentaci
odbornikem. Uzivatel nastavi na zacatku ID pacienta a take cesty pro vytvorenou segmentacni masku a manualne anotovany obraz. Koeficienty jsou jednak vypsany a jednak ulozeny
do txt souboru.
"""

from sklearn.metrics import jaccard_score, f1_score
import numpy as np
import nibabel as nib
pacient = []

# Načtení segmentací ze souborů .nii.gz
segm_aut_data = nib.load(r"cesta")
segm_manual_data = nib.load(r"cesta")

# Labely segmentací (3 pro bílou kůru, 2 pro šedou kůru)
segm_aut_white = np.where(segm_aut_data == 3, 1, 0)
segm_manual_white = np.where(segm_manual_data == 3, 1, 0)

segm_aut_grey = np.where(segm_aut_data == 2, 1, 0)
segm_manual_grey = np.where(segm_manual_data == 2, 1, 0)

# Celá segmentace spojeně
segm_aut_combined = segm_aut_white + segm_aut_grey
segm_manual_combined = segm_manual_white + segm_manual_grey

# Výpočet Dice koeficientu pro bílou kůru
dice_white = f1_score(segm_aut_white.flatten(), segm_manual_white.flatten())

# Výpočet Jaccard indexu pro bílou kůru
jaccard_white = jaccard_score(segm_aut_white.flatten(), segm_manual_white.flatten())

# Výpočet Dice koeficientu pro šedou kůru
dice_grey = f1_score(segm_aut_grey.flatten(), segm_manual_grey.flatten())

# Výpočet Jaccard indexu pro šedou kůru
jaccard_grey = jaccard_score(segm_aut_grey.flatten(), segm_manual_grey.flatten())

# Výpočet Dice koeficientu pro celou segmentaci
dice_combined = f1_score(segm_aut_combined.flatten(), segm_manual_combined.flatten())

# Výpočet Jaccard indexu pro celou segmentaci
jaccard_combined = jaccard_score(segm_aut_combined.flatten(), segm_manual_combined.flatten())


print("Dice coefficient pro bílou kůru:", dice_white)
print("Jaccard index pro bílou kůru:", jaccard_white)

print("Dice coefficient pro šedou kůru:", dice_grey)
print("Jaccard index pro šedou kůru:", jaccard_grey)

print("Dice coefficient pro celou segmentaci:", dice_combined)
print("Jaccard index pro celou segmentaci:", jaccard_combined)

with open("{}_segmentation_comparison_results.txt".format(pacient), "w") as file:
    file.write("Dice coefficient pro bílou kůru: {}\n".format(dice_white))
    file.write("Jaccard index pro bílou kůru: {}\n".format(jaccard_white))
    file.write("\n")
    file.write("Dice coefficient pro šedou kůru: {}\n".format(dice_grey))
    file.write("Jaccard index pro šedou kůru: {}\n".format(jaccard_grey))
    file.write("\n")
    file.write("Dice coefficient pro celou segmentaci: {}\n".format(dice_combined))
    file.write("Jaccard index pro celou segmentaci: {}\n".format(jaccard_combined))