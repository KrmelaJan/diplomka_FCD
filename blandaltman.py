# -*- coding: utf-8 -*-
"""
Tato funkce slouzi k vytvoreni Bland-Altmanova grafu z parovych dat, ktere si v uvodu funkce uzivatel definuje. zde napriklad promenne
L_front_L a L_front_R. dale si take musi nastavit cestu, kam ulozit vytvoreny graf (nebo argument savePath smazat, pokud graf nechce ulozit).
"""

from pyCompare import blandAltman
import multiprocessing

L_front_L = []
L_front_R = []

if __name__ == '__main__':
    multiprocessing.freeze_support()
    blandAltman(L_front_L, L_front_R, confidenceIntervalMethod='exact paired', savePath=r"cesta",pointColour='#000000')