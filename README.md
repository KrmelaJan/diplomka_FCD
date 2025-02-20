# diplomka_FCD

Hlavičkový soubor k funkcím použitým v diplomové práci
Návrh a realizace softwarové aplikace pro analýzu neurologických
abnormalit z obrazů magnetické rezonance
Jan Krmela


avg_thick.py
Tato funkce počítá průměrnou kortikální tloušťku pro dané laloky. Před spuštěním je třeba v proměnné "pacients" uvést ID pacientu z datasetu, pro kterého se má tloušťka počítat. Dále je třeba již mít vytvořenou segmentaci jednotlivých laloků. Tento soubor se načítá do proměnné "lobes". Je potřeba zde zadat cestu k segmentačnímu NIFTI souboru. Také je potřeba mít vytvořený soubor s vypočítanou kortikální tloušťkou pro daného pacienta. Zde je opět potřeba zadat celou cestu k tomuto souboru v proměnné "thickness".

blandaltman.py
Tato funkce slouží k vytvoření Bland-Altmanova grafu z párových dat, které si v úvodu funkce uživatel definuje. Zde například proměnné "L_front_L" a "L_front_R". Dále si také musí nastavit cestu, kam uložit vytvořený graf (nebo argument "savePath" smazat, pokud graf nechce uložit).

cort_thick.py
Tato funkce počítá kortikální tloušťku pro celý obraz daného pacienta. V proměnné "pacients" je třeba definovat ID všech pacientů, pro které se má výpočet kortikální tloušťky provést. Dále je třeba do proměnné "img" zadat cestu k T1 obrazu pacienta, který je nepředzpracovaný, původní. Také je nutné při ukládání zadat cestu, kam se má uložit soubor se získanými daty. Součástí skriptu je i segmentace, která se také ukládá na uživatelem definovanou cestu.

dice_jac.py
Tato funkce počítá Dice a Jaccard koeficienty jako metriky pro srovnání segmentace mozku automatickou metodou vytvoření segmentačních masek a manuální segmentaci odborníkem. Uživatel nastaví na začátku ID pacienta a také cesty pro vytvořenou segmentační masku a manuálně anotovaný obraz. Koeficienty jsou jak vypsány, tak uloženy do txt souboru.

img_load.py
Tato funkce slouží k načítání dat z uživatelem zvolené cesty - file_path. Funkce dává na výstupu data ve formátu NumPy a afinní matici v téže formě.

pacient_reorient.py
Tato funkce slouží k reorientaci obrazu na formát "IAL". Nejprve se zvolí pacienti, u kterých je třeba reorientaci provést, a následně je načten podle cesty obraz k reorientaci. Poté je možno načíst další obraz, například segmentační masku atd., a je porovnáno, zda mají obrazy stejné rozměry. Na závěr je to vypsáno do terminálu.

preprocess.py


Skript obsahující více funkcí na předzpracování a analýzu dat. Funkce budou popsány jednotlivě:

nacteni_dat
Volání funkce load_nifti_data ze souboru img_load.py pro načtení dat a affiní matice.

denoising
Funkce k provedení potlačení šumu v obraze metodou non-local means. Na vstup jdou proměnné data a affine, které jsou vytvořeny ve funkci nacteni_dat. Také je třeba zadat output_path, což je cesta na uložení výstupního obrazu.

korekce_nehomogenit
Tato funkce provádí korekci nehomogenit v obraze metodou N4. Proměnná vstupni_soubor označuje cestu k obraze s potlačeným šumem. Cesta_na_ulozeni je cesta, kam bude uložen obraz s korigovanými nehomogenitami.

skull_stripping
Tato funkce provádí odstranění nemozkových struktur. Vstupni_soubor je cesta k datům s korekcí nehomogenit, cesta_na_ulozeni je cesta, kam uložit výstupní data.

MNI_registrace
Tato funkce provádí registraci dat na uživatelem zvolenou masku, která může, ale nemusí být v MNI prostoru, i když se tak funkce jmenuje. Vstupni_soubor je cesta k obrazu po odstranění nemozkových struktur, maska je cesta k masce - obrazu, na který bude provedena registrace, a cesta_na_ulozeni je cesta, kam bude uložen registrovaný obraz.

vytvoreni_konvoluce_image
Tato funkce nejprve získá segmentační masky pro jednotlivé kůry z celkové segmentační masky - ta je načítána z cesty v proměnné segmentovany_obraz. Následně jsou tyto masky aplikovány na 'nemaskový' obraz mozku - ten je načítán na cestě v proměnné nesegmentovany_obraz, a jsou tak získány samotná šedá a bílá kůra. Ty jsou uloženy do samostatných souborů na zvolené cesty v proměnných ulozeni_seda a ulozeni_bila. Následně je proveden postup vytvoření binárního obrazu a jeho konvoluce tak, jak je popsáno v práci. Binární obraz je uložen do souboru na zvolené cestě ulozeni_binar a konvoluce obraz je uložen do souboru na zvolené cestě v proměnné ulozeni_konvoluce.

junction_image
Tato funkce načítá konvoluční obrazy analyzovaného pacienta (cesta v proměnné konvoluce_pacient) a konvoluční obraz z normální databáze (cesta v proměnné konvoluce_normal). Následně je provedeno odčtení těchto obrazů od sebe, což vytváří tzv. obraz spojení (junction image). Ten je následně uložen do souboru podle cesty v proměnné ulozeni_junction.
