# -*- coding: utf-8 -*-
"""
Tato funkce slouzi k nacitani dat z uzivatelem zvolene cesty - file_path. funkce dava na vystup data ve formatu numpy a afinni matici v teze formatu.
"""
import nibabel as nib

def load_nifti_data(file_path):
    nifti_img = nib.load(file_path)
    affine = nifti_img.affine
    data = nifti_img.get_fdata()
    return data, affine