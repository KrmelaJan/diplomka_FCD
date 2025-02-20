# -*- coding: utf-8 -*-
"""
Tato funkce pocita kortikalni tloustku pro cely obraz daneho pacienta. v promenne pacients je treba definovat ID
vsech pacientu, pro ktere se ma vypocet kortikalni tloustky provest. dale je treba do promenne img zadat cestu k
T1 obrazu pacienta, ktery je nepredzpracovan, puvodni. take je nutne pri ukladani zadat cestu, kam se ma ulozit soubor
se ziskanymi daty. soucasti skriptu je i segmentace, ktera se take uklada na uzivatelem definovanou cestu
"""

import ants
from antspynet.utilities import  cortical_thickness
pacients = []
for pacient in pacients:
    # pacient = "0{}".format(pacient)
    # nacteni puvodnich dat a ziskani promenne kk, ktera je typu slovnik. z neho jsou do promenne thickness ulozena kortikalni
    # tloustka a do promenne segm segmentacni maska, tyto dve promenne jsou nasledne ulozeny do souboru na uzivatelem definovanou cestu
    img = ants.image_read(r"cesta")
    
    kk = cortical_thickness(img)
    
    thickness = kk['thickness_image']
    segm = kk['segmentation_image']
    thickness.to_file(r"cesta")
    segm.to_file(r"cesta")