from __future__ import annotations

import DataBaseClass as db

FILE_DATABASE = "databases/Axions.db"

print("File database: " + FILE_DATABASE)
print("If it already exists, the table will be appended. Note this can cause to have duplicated rows.")
if input("Are you sure you want to continue? (y/n)\n") not in ["y", "yes", "Y", "YES"]:
    print("Aborting")
    exit()

# ==================== DATABASES ====================
path = "data/axion/"
AxionsGag = [
    ['qcdband', 'band', path + 'QCD_band.dat', "facecolor='yellow'", 1, 1, 1, 1, 1, 1, 0],
    ['ksvz', 'region', path + 'ksvz.dat', "facecolor='white', edgecolor='orange', linewidth=1", 1, 1, 1, 1, 1, 1, 0],
    ['dfsz', 'region', path + 'dfsz.dat', "facecolor='white', edgecolor='orange', linewidth=1", 0, 0, 1, 0, 0, 0, 0],
    ['old_haloscopes', 'band', path + 'MicrowaveCavities.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['admx', 'band', path + 'admx.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['admx_hf_2016', 'band', path + 'admx_hf_2016.dat', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, 0, 0, 0, 0, 0, 0],
    ['ADMX2018', 'band', path + 'ADMX2018.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, 0, 0, 0, 0, 0, 0],
    ['ADMX2019', 'band', path + 'ADMX2019.dat', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['ADMX2019_1', 'band', path + 'ADMX2019_1.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['ADMX2019_2', 'band', path + 'ADMX2019_2.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['ADMX_sidecar', 'band', path + 'ADMX_sidecar.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 0, 0, 0],
    ['ADMX2021', 'band', path + 'ADMX2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['CAPP-8TB', 'band', path + 'CAPP-8TB.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, 0, 0, 0, 1, 0, 0],
    ['CAPP_multicell', 'band', path + 'CAPP_multicell_2020.dat', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, 0, 1, 0, 1, 0, 0],
    ['CAPP2021', 'band', path + 'CAPP2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['HAYSTAC', 'band', path + 'HAYSTAC.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['HAYSTAC2020', 'band', path + 'haystac2020.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['ORGAN', 'band', path + 'ORGAN.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['QUAX', 'band', path + 'QUAX.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['QUAX2021', 'band', path + 'QUAX2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 1, 1, 1, 1, 1, 0, 0],
    ['RADES2021', 'band', path + 'RADES2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, 0, 0, 1, 0, 1, 1],
    ['ABRA10cm', 'band', path + 'ABRA10cm.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=0.5", 0, 0, 0, 0, 0, 1, 1],
    ['ABRA_2021', 'band', path + 'ABRA_2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=0.5", 0, 0, 0, 0, 0, 0, 0],
    ['BASE_2021', 'band', path + 'BASE2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=0.5", 0, 0, 0, 1, 0, 0, 0],
    ['ADMX_SLIC', 'band', path + 'ADMX_SLIC.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=1", 1, 1, 1, 1, 1, 0, 0],
    ['SHAFT', 'band', path + 'SHAFT.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=0.5", 1, 1, 1, 1, 0, 1, 0],
    ['hess', 'band', path + 'hess.dat', "facecolor='lightseagreen', edgecolor='darkgreen', linewidth=0.5", 1, 1, 1, 1, 0, 1, 0],
    ['mrk421', 'band', path + 'Mrk421.txt', "facecolor='mediumturquoise', edgecolor='darkgreen', linewidth=0.5, alpha=0.6", 1, 1, 1, 1, 0, 1, 0],
    ['sn1987a_photon', 'band', path + 'sn1987a_photon.dat', "facecolor='turquoise', edgecolor='darkgreen', linewidth=0.5", 1, 1, 1, 1, 0, 1, 0],
    ['FERMI_NG1275', 'region', path + 'FERMI_NG1275_region.dat', "facecolor='mediumturquoise', edgecolor='darkgreen', linewidth=0.5, alpha=0.6", 1, 1, 0, 0, 0, 0, 0],
    ['SN1987energyloss', 'band', path + 'cosmoalp/SN1987energyloss.txt', "facecolor='lightgreen', edgecolor='green', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['Xray', 'band', path + 'cosmoalp/Xray.txt', "facecolor='green', edgecolor='darkgreen', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['Deut2016', 'region', path + 'cosmoalp/Deut2016.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['OpticalDepthTerm', 'band', path + 'cosmoalp/OpticalDepthTerm.txt', "facecolor='yellowgreen', edgecolor='green', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['gEBL1', 'band', path + 'cosmoalp/gEBL1.txt', "facecolor='lightgreen', edgecolor='green', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['EBL2', 'region', path + 'cosmoalp/EBL2.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['cmb_mu', 'region', path + 'cosmoalp/CMB_mu.txt', "facecolor='green', edgecolor='darkgreen', linewidth=0.5", 0, 0, 0, 0, 0, 0, 0],
    ['CMB_DEsuE', 'band', path + 'cosmoalp/CMB_DEsuE.txt', "facecolor='forestgreen', edgecolor='darkgreen', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['Overduin', 'region', path + 'cosmoalp/Overduin.txt', "facecolor='lightgreen', edgecolor='green', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['Ressell', 'band', path + 'cosmoalp/Ressell.txt', "facecolor='lightgreen', edgecolor='green', linewidth=0.5", 1, 1, 1, 1, 0, 0, 0],
    ['endlist2_gamma_projimprov', 'band', path + 'endlist2_gamma_projimprov.txt', "facecolor='gray', edgecolor='black', linewidth=0.5", 1, 1, 0, 0, 0, 0, 0],
    ['telescopes', 'band', path + 'telescopes.dat', "facecolor='green', edgecolor='darkgreen', linewidth=0.5", 0, 0, 1, 1, 0, 0, 0],
    ['telescopes_new', 'band', path + 'telescopes_new.dat', "facecolor='green', edgecolor='darkgreen', linewidth=0.5", 1, 1, 1, 1, 0, 0, 0],
    ['HBalpbound', 'band', path + 'HBalpbound.txt', "facecolor='skyblue', edgecolor='blue', alpha=1, linewidth=0.5", 1, 1, 1, 1, 0, 0, 0],
    ['HBalpbound_l', 'line', path + 'HBalpbound.txt', "color='blue', linewidth=0.5", 1, 1, 1, 1, 0, 0, 0],
    ['solar_nu', 'band', path + 'ALPSun_nu.txt', "facecolor='steelblue', edgecolor='blue', linewidth=0.5", 1, 1, 1, 0, 1, 0, 1],
    ['CAST', 'band', path + 'cast_env_2016.dat', "facecolor='deepskyblue', edgecolor='blue', linewidth=0.5", 1, 1, 1, 0, 1, 0, 1],
    ['CROWS', 'band', path + 'CROWS.txt', "facecolor='gray', edgecolor='white', linewidth=0.5", 1, 1, 1, 0, 1, 0, 1],
    ['ALPSI', 'band', path + 'ALPSI.dat', "facecolor='gray', edgecolor='white', linewidth=0.5", 1, 1, 1, 0, 1, 0, 1],
    ['OSCAR2015', 'band', path + 'osqar2015.dat', "facecolor='gray', edgecolor='black', linewidth=0.5", 0, 0, 1, 0, 0, 0, 1],
    ['PVLAS2015', 'band', path + 'pvlas2015.dat', "facecolor='gray', edgecolor='black', linewidth=0.5", 0, 0, 1, 0, 0, 0, 1],
    ['BeamDump', 'region', path + 'llSLAC137.txt', "facecolor='gray', edgecolor='black', linewidth=0.5", 1, 1, 0, 0, 1, 0, 1],
    ['BabyIAXO', 'band', path + 'miniIAXO.dat', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, 1, 1, 0, 1, 0, 1],
    ['IAXO', 'band', path + 'IAXO_nominal.txt', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, 1, 1, 0, 1, 0, 1],
    ['IAXOplus', 'band', path + 'IAXO_plus.txt', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 0, 0, 1, 0, 0, 0, 1],
    ['ALPSII', 'band', path + 'ALPSII.dat', "facecolor='gray', linewidth=0.5, alpha=0.2, linestyle=':'", 1, 1, 1, 0, 1, 0, 1],
    ['ORGANprosp', 'line', path + 'ORGAN2.dat', "color='darkgreen', linewidth=0.1, linestyle='-'", 1, 1, 0, 0, 0, 0, 1],
    ['castcapp2', 'band', path + 'CASTCAPP2.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 0, 0, 0, 0, 1, 0, 1],
    ['CAPP4', 'line', path + 'CAPP4.dat', "color='darkgreen', linewidth=0.1, linestyle='-'", 0, 0, 0, 0, 1, 0, 1],
    ['MADMAX', 'band', path + 'MADMAX.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 1, 1, 0, 0, 0, 0, 1],
    ['ADMXprosp_2GHz', 'band', path + 'ADMX_prospects_2GHz.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 0, 0, 0, 0, 0, 0, 1],
    ['ADMXprosp_10GHz', 'band', path + 'ADMX_prospects_10GHz.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 0, 0, 1, 0, 1, 0, 1],
    ['ABRA1', 'band', path + 'ABRAres_1.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 1, 1, 1, 1, 1, 0, 0],
    ['ABRA1_l', 'line', path + 'ABRAres_1.dat', "color='green', linewidth=0.1, linestyle='-'", 0, 0, 1, 0, 0, 0, 1],
    ['ABRA2', 'line', path + 'ABRAres_2.dat', "color='green', linewidth=0.1, linestyle='-'", 0, 0, 1, 0, 0, 0, 1],
    ['ABRA3', 'line', path + 'ABRAres_3.dat', "color='green', linewidth=0.1, linestyle='-'", 1, 1, 1, 1, 1, 1, 0],
    ['KLASH', 'line', path + 'KLASH.dat', "color='green', linewidth=0.1, linestyle='-'", 0, 0, 1, 1, 0, 0, 0],
    ['TOORAD', 'line', path + 'TOORAD2.txt', "color='green', linewidth=0.1, linestyle='-'", 0, 0, 1, 1, 0, 0, 0],
    ['BRASS', 'line', path + 'BRASS.txt', "color='green', linewidth=0.1, linestyle='-'", 1, 1, 1, 1, 1, 0, 1],
    ['IAXODM', 'band', path + 'IAXODM.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 0, 0, 1, 1, 1, 0, 1],
    ['STAX1', 'line', path + 'STAX1.dat', "color='black', linewidth=0.2, linestyle='-.'", 1, 1, 1, 1, 1, 0, 1],
    ['STAX2', 'line', path + 'STAX2.dat', "color='black', linewidth=0.2, linestyle='-.'", 1, 1, 0, 1, 0, 1, 1],
    ['BabyIAXO_l', 'line', path + 'miniIAXO.dat', "color='black', linewidth=0.6, alpha=1, linestyle='--'", 0, 0, 0, 0, 1, 0, 1],
    ['IAXO_l', 'line', path + 'IAXO_nominal.txt', "color='black', linewidth=0.6, alpha=1, linestyle='--'", 0, 0, 0, 0, 1, 0, 1],
    ['IAXOplus_l', 'line', path + 'IAXO_plus.txt', "color='black', linewidth=0.6, alpha=1, linestyle='--'", 0, 0, 0, 0, 0, 1, 1],
    ['ALPSII_l', 'line', path + 'ALPSII.dat', "color='black', linewidth=0.5, alpha=1, linestyle=':'", 0, 0, 0, 0, 0, 1, 1],
    ['CAPP4_l', 'line', path + 'CAPP4.dat', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 1, 1, 1, 1, 1, 0, 1],
    ['MADMAX_l', 'line', path + 'MADMAX.dat', "color='darkgreen', linewidth=0.3, alpha=1, linestyle='--'", 0, 0, 1, 1, 1, 0, 1],
    ['ADMXprosp_2GHz_l', 'line', path + 'ADMX_prospects_2GHz.dat', "color='darkgreen', linewidth=0.3, alpha=1, linestyle='--'", 1, 1, 1, 1, 1, 0, 1],
    ['ADMXprosp_10GHz_l', 'line', path + 'ADMX_prospects_10GHz.dat', "color='darkgreen', linewidth=0.3, alpha=1, linestyle='--'", 1, 1, 1, 1, 0, 0, 1],
    ['ABRA1_l', 'line', path + 'ABRAres_1.dat', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 0, 0, 0, 0, 0, 0, 1],
    ['ABRA_2021_l', 'line', path + 'ABRA_2021.txt', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 0, 0, 0, 1, 0, 0, 1],
    ['KLASH_l', 'line', path + 'KLASH.dat', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 0, 0, 0, 0, 0, 1, 1],
    ['IAXODM_l', 'line', path + 'IAXODM.dat', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 1, 1, 1, 1, 0, 1, 0],
    ['AMELIE', 'line', path + 'amelie_1m3_arXiv_1508.03006.txt', "color='gray', linewidth=0.6, alpha=1, linestyle='--'", 1, 1, 1, 1, 0, 1, 0],
    ['THintMayer', 'region', path + 'Mayer_2013.dat', "facecolor='yellow', edgecolor='orange', linewidth=0.5", 0, 0, 1, 1, 0, 1, 0],
    ['THintCIBER', 'region', path + 'CIBER_contour_data.dat', "facecolor='yellow', edgecolor='orange', linewidth=0.5", 1, 1, 0, 0, 0, 1, 0],
    ['HBhint', 'region', path + 'hints/HB_hint.dat', "facecolor='none', edgecolor='orangered', linewidth=0.3, linestyle='-', hatch='////'", 1, 1, 0, 0, 0, 0, 0],
]


path1 = 'data/axion/hints/'
path2 = 'data/axion/gaegag/'
AxionsGae= [
    ["DFSZ1_starhint", "region", path1 + "DFSZ1_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='springgreen', edgecolor='darkgreen', alpha=0.2", 1, 0],
    ["DFSZ2_starhint", "region", path1 + "DFSZ2_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='lime', edgecolor='darkgreen', alpha=0.2", 1, 0],
    ["AJ23_starhint", "region", path1 + "AJ23_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='orange', edgecolor='red', alpha=0.2", 1, 0],
    ["AJ53_starhint", "region", path1 + "AJ53_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='yellow', edgecolor='orange', alpha=0.2", 1, 0],
    ["AJ83_starhint", "region", path1 + "AJ83_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='red', edgecolor='red', alpha=0.2", 1, 0],
    ["QCDband", "band", path2 + "DFSZband_gaegag.dat", "facecolor='lemonchiffon', edgecolor='none', linewidth=1", 1, 0],
    ["CAST_gae", "band", path2 + "CAST_gae_gagg.dat", "facecolor='steelblue', edgecolor='darkblue', linewidth=0.5", 1, 0],

    ["IAXO_gae", "band", path2 + "sqrtgaagae_sc2.dat", "facecolor='skyblue', edgecolor='black', linewidth=0.5, alpha=0.3", 0, 1],
    ["IAXOplus_gae", "band", path2 + "sqrtgaagae_sc3.dat", "facecolor='skyblue', edgecolor='black', linewidth=0.5, alpha=0.3", 0, 1],
    ["IAXO_gae_l", "line", path2 + "sqrtgaagae_sc2.dat", "color='black', linewidth=0.5, linestyle='--'", 0, 1],
    ["IAXOplus_gae_l", "line", path2 + "sqrtgaagae_sc3.dat", "color='black', linewidth=0.5, linestyle='--'", 0, 1],
]

large_panorama = [
    [r'{\bf Helioscopes (CAST)}', 1e-5, 2e-10, " color='black', size=11", 1, 0],
    [r'{\bf Laboratory}', 1e-7, 2e-7, " color='white', size=11", 1, 0],
    [r'HE $\gamma \textrm{-rays}$', 2e-9, 6e-12, " color='black', size=10", 1, 0],
    [r'{\bf Haloscopes}', 5e-6, 1e-13, " color='black', size=11, ha='center'", 1, 0],
    ['KSVZ', 3e-4, 21e-14, " color='black', size=6, rotation=47", 1, 0],
    ['Telescopes', 5, 1e-13, " color='black', size=6, rotation=90", 1, 0],
    ['Horizontal \n Branch Stars', 2e2, 1.6e-10, " color='black', size=7, va='center', ha='center'", 1, 0],
    [r'{\bf Sun}', 1e2, 2e-9, " color='white', size=10", 1, 0],
    [r'{\bf Beam dump}', 1.5e7, 5e-6, " color='white', size=8, rotation=-45, ha='center', va='center'", 1, 0],
    ['X rays', 1e4, 3e-17, " color='white', size=10, rotation=-57, ha='center', va='center'", 1, 0],
    # [ 1e-14, r'{\bf EBL}',  1e5, " "color='black',size=10,rotation=-57,ha='center',va='center'"", 1, 0],
    ['Extra-galactic \n Background Light', 1e5, 1e-14, " color='black', size=9, rotation=-57, ha='center', va='center'", 1, 0],
    [r'{\bf CMB}', 2e8, 1e-14, " color='white', size=9, rotation=-57, ha='center', va='center'", 1, 0],
    ['Big-Bang \n Nucleosynthesis', 3e7, 1e-10, " color='black', size=10, rotation=-57, ha='center', va='center'", 1, 0],
    ['H$_2$ ionization \n fraction', 1e2, 1e-13, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],

    # added for Gaia's plot
    ['ADMX', 2.9e-6, 3e-13, " color='black', size=6, ha='center', va='center', rotation=90", 1, 0],
    ['BNL\n+UF', 8.3e-6, 3.5e-12, " color='black', size=5, ha='center', va='center', rotation=90", 1, 0],
    ['HAYSTAC', 1.3e-5, 2.5e-14, " color='black', size=4, ha='center', va='center', rotation=90", 1, 0],
    # [ 2.5e-14, 'KLASH',  1.1e-5, " "color='black',size=5,ha='center',va='center',rotation=90"", 1, 0],


    [r'{ BabyIAXO}', 1e-3, 3e-11, " color='black', size=8, ha='center', va='center'", 1, 1],
    [r'{ IAXO}', 1e-3, 5e-12, " color='black', size=8, ha='center', va='center'", 1, 1],
    [r'{ ALPS-II}', 1e-6, 3e-11, " color='black', size=8, ha='center', va='center'", 1, 1],
    # [r'{\bf JURA}', 1e-6, 5e-12, "color='black',size=8,ha='center',va='center'", 1, 0],

    # added for Gaia's plot
    ['ADMX+CAPP', 8e-6, 2e-16, " color='black', size=5, ha='center', va='center', rotation=47", 1, 1],
    ['MADMAX', 2e-4, 8e-15, " color='black', size=5, ha='center', va='center', rotation=47", 1, 1],
    ['ORGAN', 1.2e-4, 6e-13, " color='black', size=5, ha='center', va='center', rotation=90", 1, 1],
    ['DM-\n Radios', 7e-9, 4e-15, " color='black', size=6, ha='center', va='center'", 1, 1],

    # ===========================================================================#
]
panorama = [
    [r'{\bf Helioscopes (CAST)}', 1e-5, 2e-10, "color='black', size=11", 1, 0],
    [r'{\bf Laboratory}', 1e-7, 2e-7, " color='white', size=11", 1, 0],
    [r'HE $\gamma \textrm{-rays}$', 2e-9, 6e-12, " color='black', size=10", 1, 0],
    [r'{\bf Haloscopes}', 5e-6, 1e-13, " color='black', size=11, ha='center'", 1, 0],
    ['KSVZ', 3e-4, 2e-13, " color='green', size=9, rotation=40", 1, 0],
    # ['Axion models', 0.5e-3, 4e-14, "color='black',size=9,rotation=40", 1, 0],
    ['DSFZ', 0.5e-3, 1e-13, " color='green', size=9, rotation=40", 1, 0],
    ['Telescopes', 5, 3e-13, " color='black', size=8, rotation=90", 1, 0],
    ['HB', 1, 0.9e-10, " color='black', size=9", 1, 0],
    ['Sun', 3, 1.3e-9, " color='black', size=9, ha='center'", 1, 0],
    # [r'{\bf Sun}', 1e2, 2e-9, "color='white',size=10", 1, 0],


    [r'BabyIAXO', 2e-3, 2.5e-11, " color='black', size=10, ha='center', va='center'", 1, 1],
    [r'{\bf IAXO}', 2e-3, 7e-12, " color='black', size=11, ha='center', va='center'", 1, 1],
    # [r'{\bf IAXO+}', 1e-5, 1e-12, "color='black',size=9,ha='center',va='center'", 1, 1],
    [r'{\bf ALPS-II}', 5e-7, 3e-11, " color='black', size=10, ha='center', va='center'", 1, 1],
    # [r'{\bf JURA}', 5e-7, 1.5e-12, "color='black',size=9,ha='center',va='center'", 1, 1],
]

helioscopes = [
    [r'{\bf CAST}', 3e-6, 8.5e-11, " color='blue', size=13", 1, 0],
    # [r'{\bf Laboratory}', 1e-7, 2e-7, "color='white',size=12", 1, 0],
    [r'T-hints', 1e-8, 6e-12, " color='red', size=11", 1, 0],
    # [r'HE $\gamma \textrm{-rays}$', 2e-9, 6e-12, "color='black',size=10", 1, 0],
    [r'{\bf Haloscopes}', 1e-6, 1e-12, " color='black', size=13", 1, 0],
    ['KSVZ', 1.15e-3, 0.75e-12, " color='black', size=10, rotation=57", 1, 0],
    ['Axion models', 4.7e-3, 5e-13, " color='black', size=10, rotation=57", 1, 0],
    # ['Telescopes', 5, 3e-13, "color='black',size=8,rotation=90", 1, 0],
    ['HB', 8e-2, 7e-11, " color='black', size=10", 1, 0],
    ['HB hint', 1e-1, 1.3e-11, " color='red', size=10", 1, 0],
    ['WD \ncooling\n hint ', 3.5e-3, 6.e-12, " color='red', size=10, ha='center'", 1, 0],
    # ['Sun', 3, 1.3e-9, "color='black',size=9,ha='center'", 1, 0],
    # [r'{\bf Sun}', 1e2, 2e-9, "color='white',size=10", 1, 0],
    ['ABRA\n-10cm', 7e-10, 2e-9, " color='black', size=10", 1, 0],
    ['SHAFT', 2e-11, 4e-10, " color='black', size=10", 1, 0],
    ['HESS', 3e-8, 2e-11, " color='black', size=9, ha='center'", 1, 0],
    ['Mrk421', 1e-8, 4e-11, " color='black', size=9, ha='center'", 1, 0],
    ['SN1987A', 1.5e-11, 7e-12, " color='black', size=9", 1, 0],
    ['Fermi\nNG1275', 6e-10, 7e-12, " color='black', size=9", 1, 0],


    [r'{\bf AMELIE}', 1e-3, 8.5e-11, " color='gray', size=11", 1, 1],
    [r'BabyIAXO', 3e-4, 2e-11, " color='black', size=12", 1, 1],
    [r'{\bf IAXO}', 1.75e-4, 5e-12, " color='black', size=13", 1, 1],
    [r'{\bf IAXO+}', 1.4e-4, 3.2e-12, "color='black',size=9,ha='center',va='center'", 1, 1],
    [r'{ ALPS-II}', 5e-7, 2.7e-11, " color='black', size=12", 1, 1],
    # [r'{\bf JURA}', 5e-7, 1.5e-12, "color='black',size=9,ha='center',va='center'", 1, 1],
]

haloscopes = [
    [r'{\bf CAST}', 2.5e-3, 110, " color='black', size=12, ha='center', rotation=-57", 1, 0],
    ['ABRA/DM-Radio', 1e-8, 3, " color='black', size=12, ha='center', rotation=-57", 1, 0],
    ['KLASH', 3.3e-7, 70, " color='black', size=11, ha='center', va='center', rotation=90", 1, 0],
    ['KSVZ', 1e-3, 2.5, " color='green', size=9, va='center', ha='center'", 1, 0],
    ['Axion models', 1e-3, 0.32, " color='green', size=9, ha='center'", 1, 0],
    [r'{\bf ADMX}', 2.9e-6, 70, " color='black', size=12, ha='center', va='center', rotation=90", 1, 0],
    ['ACTION/IAXO-DM', 9.5e-7, 70, " color='black', size=10, ha='center', va='center', rotation=90", 1, 0],
    ['BNL\n+UF', 8.3e-6, 650, " color='black', size=8, ha='center', va='center'", 1, 0],
    ['ADMX', 7e-6, 0.86, " color='black', size=10, ha='center', va='center'", 1, 0],
    ['CAPP', 1.9e-5, 2.24, " color='black', size=10, ha='center', va='center'", 1, 0],
    ['HAYSTAC', 1.46e-5, 25, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
    ['MADMAX', 1.2e-4, 1.15, " color='black', size=8, ha='center', va='center'", 1, 0],
    ['ORGAN', 1.2e-4, 30, " color='black', size=8, ha='center', va='center'", 1, 0],
    ['RADES', 3e-5, 25, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],


    [r'BabyIAXO', 1.8e-3, 83, " color='black', size=10, ha='center', va='center', rotation=-57", 1, 1],
    [r'{\bf IAXO}', 1e-3, 36, " color='black', size=11, ha='center', va='center', rotation=-57", 1, 1],
    ['TOORAD', 0.01, 12, " color='black', size=8, ha='center', va='center', rotation=90", 1, 1],
    # [r'{\bf IAXO+}', 1e-5, 1e-12, "color='black',size=9,ha='center',va='center'", 1, 0],
    # [r'{\bf ALPS-II}', 5e-7, 3e-11, "color='black',size=10,ha='center',va='center'", 1, 0],
    # [r'{\bf JURA}', 5e-7, 1.5e-12, "color='black',size=9,ha='center',va='center'", 1, 0],
]

LSWexps = [
    [r'CAST', 1e-3, 1e-10, " color='black', size=10", 1, 0],
    [r'{ ALPS-I}', 1e-4, 1.4e-7, " color='white', size=10, ha='center', va='center'", 1, 0],
    [r'{ CROWS}', 1e-7, 1.5e-7, " color='white', size=10, ha='center', va='center'", 1, 0],
    [r'{ PVLAS}', 3e-3, 1e-7, " color='black', size=10, ha='center', va='center', rotation=45", 1, 0],
    [r'{ OSQAR}', 1e-4, 2e-8, " color='black', size=10, ha='center', va='center'", 1, 0],
    [r'T-hints', 2e-9, 6e-12, " color='black', size=10", 1, 0],


    ['STAX1', 3e-6, 1e-10, " color='black', size=10, ha='center', va='center'", 1, 1],
    ['STAX2', 2e-6, 5e-12, " color='black', size=10, ha='center', va='center'", 1, 1],
    # [r'{\bf IAXO+}', 1e-5, 1e-12, "color='black',size=9,ha='center',va='center'", 1, 1],
    [r'{\bf ALPS-II}', 1e-6, 3e-11, " color='black', size=10, ha='center', va='center'", 1, 1],
    [r'{\bf JURA}', 2e-5, 1.3e-12, " color='black', size=9, ha='center', va='center'", 1, 1],
]

haloscopes_zoom = [
    [r'CAST', 4e-3, 144, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 0],
    ['KSVZ', 1e-3, 2.8, " color='green', size=9, va='center', ha='center'", 1, 0],
    ['Axion models', 2e-3, 0.36, " color='green', size=9, ha='center'", 1, 0],
    [r'{ ADMX}', 2.9e-6, 70, " color='black', size=12, ha='center', va='center', rotation=90", 1, 0],
    ['BNL\n+UF', 8.3e-6, 400, " color='black', size=8, ha='center', va='center'", 1, 0],
    ['RADES', 34.6e-6, 25, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],

    ['CAPP', 8.1e-6, 0.93, " color='black', size=8, ha='center', va='top', rotation=90", 1, 0],
    ['HAYSTAC', 1.96e-5, 1.00, " color='black', size=8, ha='center', va='top', rotation=90", 1, 0],
    ['QUAX', 4.3e-5, 3.6, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
    ['ORGAN', 1.2e-4, 45, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],

    ['ADMX/CAPP', 8e-6, 1.14, " color='black', size=10, ha='center', va='center'", 1, 1],
    ['MADMAX', 1.2e-4, 1.15, " color='black', size=8, ha='center', va='center'", 1, 1],
    ['ORGAN', 1.2e-4, 30, " color='black', size=8, ha='center', va='center'", 1, 1],
    [r'BabyIAXO', 2e-3, 63, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 1],
    [r'IAXO', 1.5e-3, 24, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 1],
    ['BRASS', 2.6e-4, 16, " color='black', size=8, ha='center', va='center', rotation=15", 1, 1],
    ['TOORAD', 0.01, 12, " color='black', size=8, ha='center', va='center', rotation=90", 1, 1],

]


haloscopes_radeszoom = [
    [r'CAST', 4e-3, 144, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 0],
    ['KSVZ', 1e-3, 2.8, " color='green', size=9, va='center', ha='center'", 1, 0],
    ['Axion models', 2e-3, 0.36, " color='green', size=9, ha='center'", 1, 0],
    [r'{ ADMX}', 2.9e-6, 70, " color='black', size=12, ha='center', va='center', rotation=90", 1, 0],
    ['BNL\n+UF', 8.3e-6, 400, " color='black', size=8, ha='center', va='center'", 1, 0],
    ['RADES', 34.6e-6, 25, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],

    ['CAPP', 8.1e-6, 0.93, " color='black', size=8, ha='center', va='top', rotation=90", 1, 0],
    ['HAYSTAC', 1.96e-5, 1.00, " color='black', size=8, ha='center', va='top', rotation=90", 1, 0],
    ['QUAX', 4.3e-5, 3.6, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
    ['ORGAN', 1.2e-4, 45, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],

    ['ADMX/CAPP', 8e-6, 1.14, " color='black', size=10, ha='center', va='center'", 1, 1],
    ['MADMAX', 1.2e-4, 1.15, " color='black', size=8, ha='center', va='center'", 1, 1],
    ['ORGAN', 1.2e-4, 30, " color='black', size=8, ha='center', va='center'", 1, 1],
    [r'BabyIAXO', 2e-3, 63, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 1],
    [r'IAXO', 1.5e-3, 24, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 1],
    ['BRASS', 2.6e-4, 16, " color='black', size=8, ha='center', va='center', rotation=15", 1, 1],
    ['TOORAD', 0.01, 12, " color='black', size=8, ha='center', va='center', rotation=90", 1, 1],

]



gae_labels = [
    [r'{\bf CAST}', 2e-4, 1.2e-11, " color='white', size=12", 1, 0],
    [r'{\bf IAXO}',2e-4, 6e-13, " color='black', size=12", 1, 1],
    ['IAXO+', 2e-4, 3.2e-13, " color='black', size=11", 1 , 1],
]

# ===========================================================================#
expGag = db.DataBaseGag(FILE_DATABASE, "AxionsGag", True)
expGag.insert_rows(AxionsGag)

expGae = db.DataBaseGae(FILE_DATABASE, "AxionsGae", True)
expGae.insert_rows(AxionsGae)

lp = db.DataBaseLabels(FILE_DATABASE, "large_panorama", True)
lp.insert_rows(large_panorama)

pa = db.DataBaseLabels(FILE_DATABASE, "panorama", True)
pa.insert_rows(panorama)

he = db.DataBaseLabels(FILE_DATABASE, "helioscopes", True)
he.insert_rows(helioscopes)

h = db.DataBaseLabels(FILE_DATABASE, "haloscopes", True)
h.insert_rows(haloscopes)

l = db.DataBaseLabels(FILE_DATABASE, "LSWexps", True)
l.insert_rows(LSWexps)

hz = db.DataBaseLabels(FILE_DATABASE, "haloscopes_zoom", True)
hz.insert_rows(haloscopes_zoom)

hrz = db.DataBaseLabels(FILE_DATABASE, "haloscopes_radeszoom", True)
hrz.insert_rows(haloscopes_radeszoom)

gae = db.DataBaseLabels(FILE_DATABASE, "Gae_labels", True)
gae.insert_rows(gae_labels)

path = "data/wimp/"
Wimps = [
    ['PICO_CF3I_2015', 'line', path+'limit_data/PICO_CF3I_2015.dat', "color='#e6beff'", 0, '1510.07754', '2015', "PICO CF3I", 3.5, 9.4e-37, "color='#e6beff'"],
    ['CDEX10_2018', 'line', path+'limit_data/CDEX10_2018.dat', "color='#004444'", 0, '1802.09016', '2018', "CDEX10", 2.6, 1.2e-39, "color='#004444'"],
    ['eDM_SuperCDMS_FDM1_2018', 'line', path+'limit_data/eDM_SuperCDMS_FDM1_2018.dat', "color='#e6194b'", 0, '1804.10697', '2018', "SuperCDMS", 0.5, 8e-27, "color='#e6194b'"],
    ['CRESSTsurface_2017', 'line', path+'limit_data/CRESSTsurface_2017.dat', "color='#000075'", 0, '1707.06749', '2017', "CRESST-surface", 10, 2.8e-34, "color='#000075'"],
    ['eDM_PandaX_FDMq2_2021', 'line', path+'limit_data/eDM_PandaX_FDMq2_2021.dat', "color='#f58231'", 0, '2101.07479', '2021', "PandaX-II", 5.5, 1.9e-32, "color='#f58231'"],
    ['XENON1T_lowmass', 'line', path+'limit_data/XENON1T_lowmass.dat', "color='#3cb44b'", 0, '1907.11485', '2019', "XENON1T S2", 2.5, 7.3e-44, "color='#3cb44b'"],
    ['SI_NeutrinoFloor_Ruppin_Fig4Xe', 'fog', path+'limit_data/SI_NeutrinoFloor_Ruppin_Fig4Xe.txt', "color='gray', linewidth=2.5, linestyle='--', alpha=0.5", 0, '1907.11485', '2019', "XENON1T S2", 2.5, 7.3e-44, "color='#3cb44b'"],
    ['neutrino_floor_billard', 'fog', path+'limit_data/neutrino_floor_billard.txt', "color='gray', linewidth=2.5, linestyle='--', alpha=0.5", 0, '1907.11485', '2019', "XENON1T S2", 2.5, 7.3e-44, "color='#3cb44b'"],
    ['DAMA_Na', 'region', path+'limit_data/DAMA_Na.dat', "color='#ffd8b1'", 0, '---', '---', "DAMA/Na", 31, 7.2e-41, "color='#ffd8b1'"],
    ['DarkSide50_S2only_2018', 'line', path+'limit_data/DarkSide50_S2only_2018.dat', "color='#f032e6'", 0, '1802.06994', '2018', "DarkSide50", 1.7, 1.3e-42, "color='#f032e6'"],
    ['PandaX_light1MeV_2018', 'line', path+'limit_data/PandaX_light1MeV_2018.dat', "color='#800000'", 0, '1802.06912', '2018', "PandaX-II", 1e+04, 6.5e-38, "color='#800000'"],
    ['CDMSLite_2016', 'line', path+'limit_data/CDMSLite_2016.dat', "color='#e6194b'", 0, '1707.01632', '2017', "CDMSLite", 1.4, 9.1e-37, "color='#e6194b'"],
    ['XENON100S2_2016', 'line', path+'limit_data/XENON100S2_2016.dat', "color='#3cb44b'", 0, '1605.06262', '2016', "XENON100", 20, 2.2e-42, "color='#3cb44b'"],
    ['XENONnT_projection_2020', 'line', path+'limit_data/XENONnT_projection_2020.dat', "color='#3cb44b'", 0, '2007.08796', '2020', "XENONnT", 2e+02, 1.3e-48, "color='#3cb44b'"],
    ['DarkSide50_2022', 'line', path+'limit_data/DarkSide50_2022.dat', "color='#f032e6'", 0, '2207.11966', '2022', "DarkSide50", 1, 8e-40, "color='#f032e6'"],
    ['XENON1TMIGDAL', 'line', path+'limit_data/XENON1TMIGDAL.txt', "color='#3cb44b'", 0, '2104.07634', '2020', "XENON1T Migdal", 0.33, 3e-39, "color='#3cb44b'"],
    ['LUX_completeExposure_2016', 'line', path+'limit_data/LUX_completeExposure_2016.dat', "color='#000000'", 0, '1608.07648', '2016', "LUX", 3.8e+02, 1.6e-45, "color='#000000'"],
    ['DAMIC_2020', 'line', path+'limit_data/DAMIC_2020.dat', "color='#7E0505'", 0, '2007.15622', '2020', "DAMIC", 2, 2.5e-39, "color='#7E0505'"],
    ['DAMIC_SNOLAB_2016', 'line', path+'limit_data/DAMIC_SNOLAB_2016.dat', "color='#7E0505'", 0, '1607.07410', '2018', "DAMIC", 1, 2.2e-36, "color='#7E0505'"],
    ['XMASS_2018', 'line', path+'limit_data/XMASS_2018.dat', "color='#fabebe'", 0, '1804.02180', '2018', "XMASS", 0.38, 1.4e-31, "color='#fabebe'"],
    ['SuperCDMS_SNOLAB_projection_2017', 'line', path+'limit_data/SuperCDMS_SNOLAB_projection_2017.dat', "color='#e6194b'", 0, '1610.00006', '2017', "SuperCDMS", 1.4, 1.2e-44, "color='#e6194b'"],
    ['PandaX-4T_2022', 'line', path+'limit_data/PandaX-4T_2022.dat', "color='#f58231'", 0, '2107.13438', '2022', "PandaX-4T", 6, 9e-44, "color='#f58231'"],
    ['eDM_DAMIC_FDM1_2019', 'line', path+'limit_data/eDM_DAMIC_FDM1_2019.dat', "color='#7E0505'", 0, '1907.12628', '2019', "DAMIC", 0.55, 9.1e-30, "color='#7E0505'"],
    ['PICO_C3F8_2017', 'line', path+'limit_data/PICO_C3F8_2017.dat', "color='#911eb4'", 0, '1702.07666', '2017', "PICO C3F8", 2.6, 1.1e-37, "color='#911eb4'"],
    ['CRESSTIII_2019', 'line', path+'limit_data/CRESTIII_2019.txt', "color='#4363d8'", 0, '1904.00498', '2017', "CRESST-III", 0.23, 4e-36, "color='#4363d8'"],
    ['DAMIC_M_2020', 'line', path+'limit_data/DAMIC_M_2020.dat', "color='#7E0505'", 0, '2003.09497', '2020', "DAMIC-M", 1.5, 1e-43, "color='#7E0505'"],
    ['DAMA_I', 'region', path+'limit_data/DAMA_I.dat', "color='#ffd8b1'", 0, '---', '---', "DAMA/I", 5.9, 4.5e-40, "color='#ffd8b1'"],
    ['SI_NeutrinoFloor_Ruppin_LZ_Fig3_1000ty', 'fog', path+'limit_data/SI_NeutrinoFloor_Ruppin_LZ_Fig3_1000ty.dat', "color='gray', linewidth=2.5, linestyle='--', alpha=0.5", 0, '1408.3581', '2014', "Neutrino Fog", 1.5, 7e-47, "color='#ffd8b1'"],
    ['X1T_MIGDAL_2020', 'line', path+'limit_data/X1T_MIGDAL_2020.dat', "color='#3cb44b'", 0, '1907.12771', '2020', "XENON1T Migdal", 0.33, 3e-39, "color='#3cb44b'"],
    ['eDM_XENON1T_FDM1_2019', 'line', path+'limit_data/eDM_XENON1T_FDM1_2019.dat', "color='#3cb44b'", 0, '1907.11485', '2019', "XENON1T", 20, 1.6e-36, "color='#3cb44b'"],
    ['CRESSTII_2015', 'line', path+'limit_data/CRESSTII_2015.dat', "color='#42d4f4'", 0, '1509.01515', '2015', "CRESST-II", 0.6, 8.2e-37, "color='#42d4f4'"],
    ['eDM_DAMIC_FDMq2_2019', 'line', path+'limit_data/eDM_DAMIC_FDMq2_2019.dat', "color='#7E0505'", 0, '1907.12628', '2019', "DAMIC", 0.55, 4.4e-31, "color='#7E0505'"],
    ['eDM_PandaX_FDM1_2021', 'line', path+'limit_data/eDM_PandaX_FDM1_2021.dat', "color='#f58231'", 0, '2101.07479', '2021', "PandaX-II", 5.2, 7.6e-34, "color='#f58231'"],
    ['XENON1T_2018', 'line', path+'limit_data/XENON1T_2018.dat', "color='#3cb44b'", 0, '1805.12562', '2018', "XENON1T", 4, 2e-45, "color='#3cb44b'"],
    ['CRESSTIII_2017', 'line', path+'limit_data/CRESSTIII_2017.dat', "color='#4363d8'", 0, '1711.07692', '2017', "CRESST-III", 0.4, 4e-36, "color='#4363d8'"],
    ['eDM_SuperCDMS_FDMq2_2018', 'line', path+'limit_data/eDM_SuperCDMS_FDMq2_2018.dat', "color='#e6194b'", 0, '1804.10697', '2018', "SuperCDMS", 0.54, 3.9e-29, "color='#e6194b'"],
    ['XENON1T_2021', 'line', path+'limit_data/XENON1T_2021.dat', "color='#3cb44b'", 0, '10.1103/PhysRevLett.126.091301', '2021', "XENON1T $^8$B", 4, 2e-45, "color='#3cb44b'"],
    ['NuFloorXe', 'fog', path+'limit_data/NuFloorXe.dat', "color='gray', linewidth=2.5, linestyle='--', alpha=0.5", 0, 'https://github.com/cajohare/AtmNuFloor/blob/master/data/WIMPLimits/SI/nufloor-Xe.txt', '2020', "Neutrino Floor Xe", 1.5, 7e-46, "color='#3cb44b'"],
    ['NEWS_G_2018', 'line', path+'limit_data/NEWS_G_2018.dat', "color='#469990'", 0, '1809.02485', '2018', "NEWS-G", 0.7, 1.4e-37, "color='#469990'"],
    ['DEAP3600_2019', 'line', path+'limit_data/DEAP3600_2019.dat', "color='#800080'", 0, '1902.04048', '2019', "DEAP-3600", 25, 4.2e-43, "color='#800080'"],
    ['LZ_projection_2018', 'line', path+'limit_data/LZ_projection_2018.dat', "color='#000000'", 1, '1802.06039', '2018', "LZ", 3e+02, 1.1e-47, "color='#000000'"],
    ['PandaX_2017', 'line', path+'limit_data/PandaX_2017.dat', "color='#f58231'", 0, '1708.06917', '2017', "PandaX-II", 6, 9e-44, "color='#f58231'"],
]

w = db.DataBaseWimps(FILE_DATABASE.replace("Axions","Wimps"), "Wimps_SI", True)
w.insert_rows(Wimps)
