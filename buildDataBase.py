import DataBaseClass as db

FILE_DATABASE = "databases/Axions.db"

print("File database: " + FILE_DATABASE)
print("If it already exists, the table will be appended. Note this can cause to have duplicated rows.")
ans = input("Are you sure you want to continue? (y/n)\n")
if ans not in ["y", "yes", "Y", "YES"]:
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
    [r'{\bf Helioscopes (CAST)}', 1e-8, 1e-8, " color='black', size=10", 1, 0],
    [r'{\bf Laboratory}', 1e-9, 1e-9, " color='white', size=10", 1, 0],
    [r'$\gamma \textrm{-rays}$', 1e-9, 1e-9, " color='black', size=10, ha='center'", 1, 0],
    # plt.text(1e-8,1e-13,'Haloscopes',color='black',size=9)
    ["SN1987A", 5e7, 5e7, " color='black', size=6, rotation=-90, ha='center', va='center'", 1, 0],
    ["KSVZ", 3e-4, 3e-4, " color='black', size=6, rotation=47", 1, 0],
    ["Telescopes", 5, 5, " color='black', size=6, rotation=90", 1, 0],
    ["Horizontal \n Branch Stars", 2e2, 2e2, " color='black', size=7, va='center', ha='center'", 1, 0],
    [r'{\bf Sun}', 1e2, 1e2, " color='white', size=10", 1, 0],
    [r'{\bf Beam dump}', 1.5e7, 1.5e7, " color='white', size=8, rotation=-45, ha='center', va='center'", 1, 0],
    ["X rays", 1e4, 1e4, " color='white', size=10, rotation=-57, ha='center', va='center'", 1, 0],
    # plt.text(1e5,1e-14,r'{\bf EBL}',color='black',size=10,rotation=-57,ha='center',va='center')
    ["Extra-galactic \n Background Light", 1e5, 1e5, " color='black', size=9, rotation=-57, ha='center', va='center'", 1, 0],
    [r'{\bf CMB}', 2e8, 2e8, " color='white', size=9, rotation=-57, ha='center', va='center'", 1, 0],
    ["Big-Bang \n Nucleosynthesis", 3e7, 3e7, " color='black', size=10, rotation=-57, ha='center', va='center'", 1, 0],
    ["H$_2$ ionization \n fraction", 1e2, 1e2, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],

    # added for Gaia's plot
    ["ADMX", 2.9e-6, 2.9e-6, " color='black', size=6, ha='center', va='center', rotation=90", 1, 0],
    ["BNL\n+UF", 8.3e-6, 8.3e-6, " color='black', size=5, ha='center', va='center', rotation=90", 1, 0],
    ["HAYSTAC", 1.3e-5, 1.3e-5, " color='black', size=4, ha='center', va='center', rotation=90", 1, 0],
    # plt.text(1.1e-5,2.5e-14,'KLASH',color='black',size=5,ha='center',va='center',rotation=90)

        [r'{ BabyIAXO}', 1e-3, 1e-3, " color='black', size=8, ha='center', va='center'", 1, 1],
        [r'{ IAXO}', 1e-3, 1e-3, " color='black', size=8, ha='center', va='center'", 1, 1],
        [r'{ ALPS-II}', 1e-6, 1e-6, " color='black', size=8, ha='center', va='center'", 1, 1],
        # plt.text(1e-6,5e-12,r'{\bf JURA}',color='black',size=8,ha='center',va='center')

        # added for Gaia's plot
        ["ADMX+CAPP", 8e-6, 8e-6, " color='black', size=5, ha='center', va='center', rotation=47", 1, 1],
        ["MADMAX", 2e-4, 2e-4, " color='black', size=5, ha='center', va='center', rotation=47", 1, 1],
        ["ORGAN", 1.2e-4, 1.2e-4, " color='black', size=5, ha='center', va='center', rotation=90", 1, 1],
        ["DM-\n Radios", 7e-9, 7e-9, " color='black', size=6, ha='center', va='center'", 1, 1],
]


# ===========================================================================#
panorama = [
    [r'{\bf Helioscopes (CAST)}', 1e-5, 1e-5, " color='black', size=11", 1, 0],
    [r'{\bf Laboratory}', 1e-7, 1e-7, " color='white', size=11", 1, 0],
    [r'HE $\gamma \textrm{-rays}$', 2e-9, 2e-9, " color='black', size=10", 1, 0],
    [r'{\bf Haloscopes}', 5e-6, 5e-6, " color='black', size=11, ha='center'", 1, 0],
    ["KSVZ", 3e-4, 3e-4, " color='green', size=9, rotation=40", 1, 0],
    # plt.text(0.5e-3,4e-14,'Axion models',color='black',size=9,rotation=40)
    ["DSFZ", 0.5e-3, 0.5e-3, " color='green', size=9, rotation=40", 1, 0],
    ["Telescopes", 5, 5, " color='black', size=8, rotation=90", 1, 0],
    ["HB", 1, 1, " color='black', size=9", 1, 0],
    ["Sun", 3, 3, " color='black', size=9, ha='center'", 1, 0],
    # plt.text(1e2,2e-9,r'{\bf Sun}',color='white',size=10)

        [r'BabyIAXO', 2e-3, 2e-3, " color='black', size=10, ha='center', va='center'", 1, 1],
        [r'{\bf IAXO}', 2e-3, 2e-3, " color='black', size=11, ha='center', va='center'", 1, 1],
        # plt.text(1e-5,1e-12,r'{\bf IAXO+}',color='black',size=9,ha='center',va='center')
        [r'{\bf ALPS-II}', 5e-7, 5e-7, " color='black', size=10, ha='center', va='center'", 1, 1],
        # plt.text(5e-7,1.5e-12,r'{\bf JURA}',color='black',size=9,ha='center',va='center')
]


# ===========================================================================#
helioscopes = [
    [r'{\bf CAST}', 3e-6, 3e-6, " color='blue', size=13", 1, 0],
    # plt.text(1e-7,2e-7,r'{\bf Laboratory}',color='white',size=12)
    [r'T-hints', 1e-8, 1e-8, " color='red', size=11", 1, 0],
    # plt.text(2e-9,6e-12,r'HE $\gamma \textrm{-rays}$',color='black',size=10)
    [r'{\bf Haloscopes}', 1e-6, 1e-6, " color='black', size=13", 1, 0],
    ["KSVZ", 1.15e-3, 1.15e-3, " color='black', size=10, rotation=57", 1, 0],
    ["Axion models", 4.7e-3, 4.7e-3, " color='black', size=10, rotation=57", 1, 0],
    # plt.text(5,3e-13,'Telescopes',color='black',size=8,rotation=90)
    ["HB", 8e-2, 8e-2, " color='black', size=10", 1, 0],
    ["HB hint", 1e-1, 1e-1, " color='red', size=10", 1, 0],
    ["WD \ncooling\n hint ", 3.5e-3, 3.5e-3, " color='red', size=10, ha='center'", 1, 0],
    # plt.text(3,1.3e-9,'Sun',color='black',size=9,ha='center')
    # plt.text(1e2,2e-9,r'{\bf Sun}',color='white',size=10)
    ["ABRA\n-10cm", 7e-10, 7e-10, " color='black', size=10", 1, 0],
    ["SHAFT", 2e-11, 2e-11, " color='black', size=10", 1, 0],
    ["HESS", 3e-8, 3e-8, " color='black', size=9, ha='center'", 1, 0],
    ["Mrk421", 1e-8, 1e-8, " color='black', size=9, ha='center'", 1, 0],
    ["SN1987A", 1.5e-11, 1.5e-11, " color='black', size=9", 1, 0],
    ["Fermi\nNG1275", 6e-10, 6e-10, " color='black', size=9", 1, 0],

   
        [r'{\bf AMELIE}', 1e-3, 1e-3, " color='gray', size=11", 1, 1],
        [r'BabyIAXO', 3e-4, 3e-4, " color='black', size=12", 1, 1],
        [r'{\bf IAXO}', 1.75e-4, 1.75e-4, " color='black', size=13", 1, 1],
        [r'{\bf IAXO+}', 1.4e-4, 3.2e-12, " color='black',size=9,ha='center',va='center'", 1, 1],
        [r'{ ALPS-II}', 5e-7, 5e-7, " color='black', size=12", 1, 1],
        # plt.text(5e-7,1.5e-12,r'{\bf JURA}',color='black',size=9,ha='center',va='center')
]



# ===========================================================================#
haloscopes = [
    [r'{\bf CAST}', 2.5e-3, 2.5e-3, " color='black', size=12, ha='center', rotation=-57", 1, 0],
    ["ABRA/DM-Radio", 1e-8, 1e-8, " color='black', size=12, ha='center', rotation=-57", 1, 0],
    ["KLASH", 3.3e-7, 3.3e-7, " color='black', size=11, ha='center', va='center', rotation=90", 1, 0],
    ["KSVZ", 1e-3, 1e-3, " color='green', size=9, va='center', ha='center'", 1, 0],
    ["Axion models", 1e-3, 1e-3, " color='green', size=9, ha='center'", 1, 0],
    [r'{\bf ADMX}', 2.9e-6, 2.9e-6, " color='black', size=12, ha='center', va='center', rotation=90", 1, 0],
    ["ACTION/IAXO-DM", 9.5e-7, 9.5e-7, " color='black', size=10, ha='center', va='center', rotation=90", 1, 0],
    ["BNL\n+UF", 8.3e-6, 8.3e-6, " color='black', size=8, ha='center', va='center'", 1, 0],
    ["ADMX", 7e-6, 7e-6, " color='black', size=10, ha='center', va='center'", 1, 0],
    ["CAPP", 1.9e-5, 1.9e-5, " color='black', size=10, ha='center', va='center'", 1, 0],
    ["HAYSTAC", 1.46e-5, 1.46e-5, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
    ["MADMAX", 1.2e-4, 1.2e-4, " color='black', size=8, ha='center', va='center'", 1, 0],
    ["ORGAN", 1.2e-4, 1.2e-4, " color='black', size=8, ha='center', va='center'", 1, 0],
    ["RADES", 3e-5, 3e-5, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],

        [r'BabyIAXO', 1.8e-3, 1.8e-3, " color='black', size=10, ha='center', va='center', rotation=-57", 1, 1],
        [r'{\bf IAXO}', 1e-3, 1e-3, " color='black', size=11, ha='center', va='center', rotation=-57", 1, 1],
        ["TOORAD", 0.01, 0.01, " color='black', size=8, ha='center', va='center', rotation=90", 1, 1],
        # plt.text(1e-5,1e-12,r'{\bf IAXO+}',color='black',size=9,ha='center',va='center')
        # plt.text(5e-7,3e-11,r'{\bf ALPS-II}',color='black',size=10,ha='center',va='center')
        # plt.text(5e-7,1.5e-12,r'{\bf JURA}',color='black',size=9,ha='center',va='center')
]


# ===========================================================================#
LSWexps = [
    [r'CAST', 1e-3, 1e-3, " color='black', size=10", 1, 0],
    [r'{ ALPS-I}', 1e-4, 1e-4, " color='white', size=10, ha='center', va='center'", 1, 0],
    [r'{ CROWS}', 1e-7, 1e-7, " color='white', size=10, ha='center', va='center'", 1, 0],
    [r'{ PVLAS}', 3e-3, 3e-3, " color='black', size=10, ha='center', va='center', rotation=45", 1, 0],
    [r'{ OSQAR}', 1e-4, 1e-4, " color='black', size=10, ha='center', va='center'", 1, 0],
    [r'T-hints', 2e-9, 2e-9, " color='black', size=10", 1, 0],

    
        ["STAX1", 3e-6, 3e-6, " color='black', size=10, ha='center', va='center'", 1, 1],
        ["STAX2", 2e-6, 2e-6, " color='black', size=10, ha='center', va='center'", 1, 1],
        # plt.text(1e-5,1e-12,r'{\bf IAXO+}',color='black',size=9,ha='center',va='center')
        [r'{\bf ALPS-II}', 1e-6, 1e-6, " color='black', size=10, ha='center', va='center'", 1, 1],
        [r'{\bf JURA}', 2e-5, 2e-5, " color='black', size=9, ha='center', va='center'", 1, 1],
]


# ===========================================================================#
haloscopes_zoom = [
    [r'CAST', 4e-3, 4e-3, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 0],
    ["KSVZ", 1e-3, 1e-3, " color='green', size=9, va='center', ha='center'", 1, 0],
    ["Axion models", 2e-3, 2e-3, " color='green', size=9, ha='center'", 1, 0],
    [r'{ ADMX}', 2.9e-6, 2.9e-6, " color='black', size=12, ha='center', va='center', rotation=90", 1, 0],
    ["BNL\n+UF", 8.3e-6, 8.3e-6, " color='black', size=8, ha='center', va='center'", 1, 0],
    ["RADES", 34.6e-6, 34.6e-6, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
     ["CAPP", 8.1e-6, 8.1e-6, " color='black', size=8, ha='center', va='top', rotation=90", 1, 0],
        
        ["HAYSTAC", 1.96e-5, 1.96e-5, " color='black', size=8, ha='center', va='top', rotation=90", 1, 0],
        

        ["QUAX", 4.3e-5, 4.3e-5, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
        ["ORGAN", 1.2e-4, 1.2e-4, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
   
        ["ADMX/CAPP", 8e-6, 8e-6, " color='black', size=10, ha='center', va='center'", 1, 1],
        ["MADMAX", 1.2e-4, 1.2e-4, " color='black', size=8, ha='center', va='center'", 1, 1],
        ["ORGAN", 1.2e-4, 1.2e-4, " color='black', size=8, ha='center', va='center'", 1, 1],
        [r'BabyIAXO', 2e-3, 2e-3, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 1],
        [r'IAXO', 1.5e-3, 1.5e-3, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 1],
        ["BRASS", 2.6e-4, 2.6e-4, " color='black', size=8, ha='center', va='center', rotation=15", 1, 1],
        ["TOORAD", 0.01, 0.01, " color='black', size=8, ha='center', va='center', rotation=90", 1, 1],       
]


haloscopes_radeszoom = [
    [r'CAST', 4e-3, 4e-3, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 0],
    ["KSVZ", 1e-3, 1e-3, " color='green', size=9, va='center', ha='center'", 1, 0],
    ["Axion models", 2e-3, 2e-3, " color='green', size=9, ha='center'", 1, 0],
    [r'{ ADMX}', 2.9e-6, 2.9e-6, " color='black', size=12, ha='center', va='center', rotation=90", 1, 0],
    ["BNL\n+UF", 8.3e-6, 8.3e-6, " color='black', size=8, ha='center', va='center'", 1, 0],
    ["RADES", 34.6e-6, 34.6e-6, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
     ["CAPP", 8.1e-6, 8.1e-6, " color='black', size=8, ha='center', va='top', rotation=90", 1, 0],
        
        ["HAYSTAC", 1.96e-5, 1.96e-5, " color='black', size=8, ha='center', va='top', rotation=90", 1, 0],
        

        ["QUAX", 4.3e-5, 4.3e-5, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
        ["ORGAN", 1.2e-4, 1.2e-4, " color='black', size=8, ha='center', va='center', rotation=90", 1, 0],
   
        ["ADMX/CAPP", 8e-6, 8e-6, " color='black', size=10, ha='center', va='center'", 1, 1],
        ["MADMAX", 1.2e-4, 1.2e-4, " color='black', size=8, ha='center', va='center'", 1, 1],
        ["ORGAN", 1.2e-4, 1.2e-4, " color='black', size=8, ha='center', va='center'", 1, 1],
        [r'BabyIAXO', 2e-3, 2e-3, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 1],
        [r'IAXO', 1.5e-3, 1.5e-3, " color='black', size=10, ha='center', va='center', rotation=-40", 1, 1],
        ["BRASS", 2.6e-4, 2.6e-4, " color='black', size=8, ha='center', va='center', rotation=15", 1, 1],
        ["TOORAD", 0.01, 0.01, " color='black', size=8, ha='center', va='center', rotation=90", 1, 1],       
]



gae_labels = [
    [r'{\bf CAST}', 2e-4, 1.2e-11, " color='white', size=12", 1, 0],
    [r'{\bf IAXO}',2e-4, 6e-13, " color='black', size=12", 1, 1],
    ['IAXO+', 2e-4, 3.2e-13, " color='black', size=11", 1 , 1],
]

# ===========================================================================#
expGag = db.DataBaseGag(FILE_DATABASE, "AxionsGag")
expGag.insert_rows(AxionsGag)

expGae = db.DataBaseGae(FILE_DATABASE, "AxionsGae")
expGae.insert_rows(AxionsGae)

lp = db.DataBaseLabels(FILE_DATABASE, "large_panorama")
lp.insert_rows(large_panorama)

pa = db.DataBaseLabels(FILE_DATABASE, "panorama")
pa.insert_rows(panorama)

he = db.DataBaseLabels(FILE_DATABASE, "helioscopes")
he.insert_rows(helioscopes)

h = db.DataBaseLabels(FILE_DATABASE, "haloscopes")
h.insert_rows(haloscopes)

l = db.DataBaseLabels(FILE_DATABASE, "LSWexps")
l.insert_rows(LSWexps)

hz = db.DataBaseLabels(FILE_DATABASE, "haloscopes_zoom")
hz.insert_rows(haloscopes_zoom)

hrz = db.DataBaseLabels(FILE_DATABASE, "haloscopes_radeszoom")
hrz.insert_rows(haloscopes_radeszoom)

gae = db.DataBaseLabels(FILE_DATABASE, "Gae_labels")
gae.insert_rows(gae_labels)