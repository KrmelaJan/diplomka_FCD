# -*- coding: utf-8 -*-
"""
Skript obsahující více funkcí na předzpracování a analýzu dat. Funkce budou popsány jednotlivě.
"""
from img_load import load_nifti_data
import numpy as np
import matplotlib.pyplot as plt
from dipy.denoise.nlmeans import nlmeans
from dipy.denoise.noise_estimate import estimate_sigma
from dipy.io.image import save_nifti
import SimpleITK as sitk
import ants
from antspynet.utilities import brain_extraction
from nilearn import masking
from nilearn.image import load_img, get_data
from scipy import ndimage
import nibabel as nib

def nacteni_dat(cesta_k_souboru):
    """Volání funkce load_nifti_data ze souboru img_load.py pro načtení dat a affiní matice"""
    data, affine = load_nifti_data(cesta_k_souboru)
    return data, affine


def denoising(data, affine, output_path):
    """Funkce k provedení potlačení šumu v obraze metodou non-local means. Na vstup jdou proměnné data a affine,
    ktere jsou vytvorene ve funkci nacteni_dat. take je treba zadat output_path, coz je cesta na ulozeni vystupniho obrazu-"""
    # Odhad smerodatne odchylky sumu z obrazu
    sigma = estimate_sigma(data)
    
    # Samotne provedeni metody NLN - patch_radius a block_radius jsou parametry ovlivnujici vystupni obraz,
    # neni jednotne pravidlo pro jejich hodnoty, pro kazda data mohou byt vhodnejsi jine hodnoty, je potreba
    # optimalizacne najit nejlepsi kombinaci
    data_denoised = nlmeans(data, sigma, patch_radius=1, block_radius=2)
    
    # Uložení denoised dat
    save_nifti(output_path, data_denoised, affine)
    

def korekce_nehomogenit(vstupni_soubor, cesta_na_ulozeni):
    """Tato funkce provadi korekci nehomogenit v obraze metodou N4. Promenna vstupni_soubor oznacuje cestu k
    obrazu s potlacenym sumem. cesta_na_ulozeni je cesta, kam bude ulozen obraz s korigovanymi nehomogenitami"""
    # Načtení dat ze souboru
    data_denoised_new = sitk.ReadImage(vstupni_soubor, sitk.sitkFloat32)
    data_denoised_arr = sitk.GetArrayFromImage(data_denoised_new)
    
    # Transformace obrazu - intenzita v hodnotach 0 až 255
    transformed = sitk.RescaleIntensity(data_denoised_new, 0, 255)
    transformed = sitk.LiThreshold(transformed, 0, 1)
    head_mask = transformed
    
    # Shrink - zmenseni obrazu pro snizeni vypocetni narocnosti
    shrinkFactor = 4
    inputImage = data_denoised_new
    inputImage = sitk.Shrink(data_denoised_new, [shrinkFactor] * inputImage.GetDimension())
    maskImage = sitk.Shrink(head_mask, [shrinkFactor] * inputImage.GetDimension())
    
    # N4 Bias Field Correction - samotne provedeni N4 algoritmu tak jak je popsano v praci
    bias_corrector = sitk.N4BiasFieldCorrectionImageFilter()
    corrected = bias_corrector.Execute(inputImage, maskImage)
    log_bias_field = bias_corrector.GetLogBiasFieldAsImage(data_denoised_new)
    data_denoised_corrected = data_denoised_new / sitk.Exp(log_bias_field)
    data_denoised_corrected_arr = sitk.GetArrayFromImage(data_denoised_corrected)
    
    # Uložení korigovaných dat
    sitk.WriteImage(data_denoised_corrected, cesta_na_ulozeni)
    
def skull_stripping(vstupni_soubor, cesta_na_ulozeni):
    """Tato funkce provadi odstraneni nemozkovych struktur. vstupni_soubor je cesta k datum s korekci nehomogenit
    , cesta_na_ulozeni cesta, kam ulozit vystupni data"""
    # Načtení obrázku
    ants_im = ants.image_read(vstupni_soubor, reorient='IAL')
    
    # Extrakce mozku metodou predtrenovanych NN z knihovny ANTs, tak jak je popsano v praci. parametr low_thresh je
    # mozno menit, ale hodnoty 0.5 se osvedcila jako dobre fungujici.
    prob_brain_mask = brain_extraction(ants_im, modality="t1")
    brain_mask = ants.get_mask(prob_brain_mask, low_thresh=0.5)
    
    # Maskování obrázku - aplikace masky na puvodni data
    masked = ants.mask_image(ants_im, brain_mask)
    
    # Uložení výsledku
    masked.to_file(cesta_na_ulozeni)
    
def MNI_registrace(vstupni_soubor, maska, cesta_na_ulozeni):
    """Tato funkce provadi registraci dat na uzivatelem zvolenou masku, ktera muze ale nemusi byt v MNI prostoru, i kdyz se tak funkce jmenuje.
    vstupni_soubor je cesta k obrazu po odstranění nemozkových struktur, maska je cesta k masce - obrazu na ktery bude provadena registrace a 
    cesta_na_ulozeni je cesta, kam bude ulozen registrovany obraz"""
    # Načtení obrázků
    unregistered = ants.image_read(vstupni_soubor, reorient='IAL')
    template = ants.image_read(maska, reorient='IAL')
    
    # Prvni krok registrace - afinní transformace
    initial_affine = ants.registration(fixed=template, moving=unregistered, type_of_transform='SyN')

    # Druhý krok registrace - nelineární normalizace
    registered = ants.apply_transforms(fixed=template, moving=unregistered, transformlist=initial_affine['fwdtransforms'])

    # Uložení výsledku
    ants.image_write(registered, cesta_na_ulozeni)
    
def vytvoreni_konvoluce_image(nesegmentovany_obraz, segmentovany_obraz, ulozeni_seda, ulozeni_bila, ulozeni_binar, ulozeni_konvoluce):
    """Tato funkce nejprve získá segmentační masky pro jednotlivé kůry z celkové segmentační masky - ta je načítána z cesty v proměnné segmentovany_obraz. Následně jsou tyto masky aplikovány na 'nemaskový' obraz mozku - 
    ten je načítán na cestě v proměnné nesegmentovany_obraz, a jsou tak získány samotná šedá a bílá kůra. Ty jsou uloženy do samostatných souborů na zvolené cesty v proměnných ulozeni_seda a ulozeni_bila. Nasledne je 
    proveden postup vytvoreni binarniho obrazu a jeho konvoluce tak, jak je popsano v praci. Binarni obraz je ulozen do souboru na zvolene ceste ulozeni_binar a konvoluci obraz je ulozen do souboru na zvolene ceste v promenne
    ulozeni_konvoluce."""
    # Načtení nesegmentovaneho obrazu
    to_be_segmented = load_img(nesegmentovany_obraz)
    segmented_aut, affine_norm = load_nifti_data(segmentovany_obraz)
    to_be_segmented_arr = get_data(to_be_segmented)

    # Ziskani sede a bile kury
    gray_matter_mask_aut = np.where(segmented_aut == 2, 1, 0)
    white_matter_mask_aut = np.where(segmented_aut == 3, 1, 0)
    gray_matter_aut = np.where(gray_matter_mask_aut == 1, to_be_segmented_arr, 0)
    white_matter_aut = np.where(white_matter_mask_aut == 1, to_be_segmented_arr, 0)

    # Uložení sedé a bílé kůry
    gray_matter_aut_save = nib.Nifti1Image(gray_matter_aut, affine_norm)
    nib.save(gray_matter_aut_save, ulozeni_seda)
    white_matter_aut_save = nib.Nifti1Image(white_matter_aut, affine_norm)
    nib.save(white_matter_aut_save, ulozeni_bila)

    # Ziskání statistických parametrů ze sedé a bílé kůry
    gray_mean_aut = np.mean(gray_matter_aut[gray_matter_aut > 0])
    white_mean_aut = np.mean(white_matter_aut[white_matter_aut > 0])
    gray_sd_aut = np.std(gray_matter_aut[gray_matter_aut > 0])
    white_sd_aut = np.std(white_matter_aut[white_matter_aut > 0])

    # Vytvoření binárního obrazu
    korovy_mozek = np.where((segmented_aut == 2) | (segmented_aut == 3), to_be_segmented_arr, 0)
    binary_image_aut = np.where((korovy_mozek >= (gray_mean_aut + (1 / 2 * gray_sd_aut))) & (korovy_mozek <= (white_mean_aut - (1 / 2 * white_sd_aut))), 1, 0)

    # Uložení binárního obrazu
    binary_image_aut_save = nib.Nifti1Image(binary_image_aut, affine_norm)
    nib.save(binary_image_aut_save, ulozeni_binar)

    # Vytvoreni konvolucniho obrazu
    kernel = np.ones((5, 5, 5))
    convolved_image_aut = ndimage.convolve(binary_image_aut, kernel, mode='constant', cval=0.0)

    # Uložení konvolucniho obrazu
    convolved_image_aut_save = nib.Nifti1Image(convolved_image_aut, affine_norm)
    nib.save(convolved_image_aut_save, ulozeni_konvoluce)
    
def junction_image(konvoluce_pacient, konvoluce_normal, ulozeni_junction):
    """Tato funkce nacita konvolucni obrazy analyzovaneho pacienta (cesta v promenne konvoluce_pacient) a konvolucni obraz z normalni databaze (cesta v promenne konvoluce_normal). Nasledne je provedeno odecteni techto obrazu od sebe, coz
    dava za vznik tzv. obrazu spojeni (junction image). Ten je nasledne ulozen do souboru podle cesty v promenne ulozeni_junction."""
    # Nacteni konvolucnich obrazu
    konv_pacient, affine_norm = load_nifti_data(konvoluce_pacient)
    konv_normal, affine_norm = load_nifti_data(konvoluce_normal)
    # Odecteni obrazu
    junction_img_data = konv_pacient - konv_normal
    
    # Ulozeni obrazu spojeni
    junction_img = nib.Nifti1Image(junction_img_data, affine_norm)
    nib.save(junction_img, ulozeni_junction)