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
    # name, type, path, drawOptions, projection, source, year, hint, model, cosmology, haloscope, stellar, helisocope, laboratory, LSW

    # HINTS
    ['THintMayer', 'region', path + 'Mayer_2013.dat', "facecolor='yellow', edgecolor='orange', linewidth=0.5", 0, '', '', 1, 0, 0, 0, 0, 0, 0, 0],
    ['THintCIBER', 'region', path + 'CIBER_contour_data.dat', "facecolor='yellow', edgecolor='orange', linewidth=0.5", 0, '', '', 1, 0, 0, 0, 0, 0, 0, 0],
    ['HBhint', 'region', path + 'hints/HB_hint.dat', "facecolor='none', edgecolor='orangered', linewidth=0.3, linestyle='-', hatch='////'", 0, '', '', 1, 0, 0, 0, 0, 0, 0, 0],
    # HINTS - MODELS
    ['qcdband', 'band', path + 'QCD_band.dat', "facecolor='yellow'", 0, '', '', 1, 1, 0, 0, 0, 0, 0, 0],
    ['ksvz', 'region', path + 'ksvz.dat', "facecolor='white', edgecolor='orange', linewidth=1", 0, '', '', 1, 1, 0, 0, 0, 0, 0, 0],
    ['dfsz', 'region', path + 'dfsz.dat', "facecolor='white', edgecolor='orange', linewidth=1", 0, '', '', 1, 1, 0, 0, 0, 0, 0, 0],

    # COSMOLOGY
    ['endlist2_gamma_projimprov', 'band', path + 'endlist2_gamma_projimprov.txt', "facecolor='gray', edgecolor='black', linewidth=0.5", 0, '', '', 0, 0, 1, 0, 0, 0, 0, 0],
    ['telescopes', 'band', path + 'telescopes.dat', "facecolor='green', edgecolor='darkgreen', linewidth=0.5", 0, '', '', 0, 0, 1, 0, 0, 0, 0, 0],
    ['telescopes_new', 'band', path + 'telescopes_new.dat', "facecolor='green', edgecolor='darkgreen', linewidth=0.5", 0, '', '', 0, 0, 1, 0, 0, 0, 0, 0],
    ['hess', 'band', path + 'hess.dat', "facecolor='lightseagreen', edgecolor='darkgreen', linewidth=0.5", 0, '', '', 0, 0, 1, 0, 0, 0, 0, 0],
    ['mrk421', 'band', path + 'Mrk421.txt', "facecolor='mediumturquoise', edgecolor='darkgreen', linewidth=0.5, alpha=0.6", 0, '2008.09464', '2020', 0, 0, 1, 0, 0, 0, 0, 0],
    ['sn1987a_photon', 'band', path + 'sn1987a_photon.dat', "facecolor='turquoise', edgecolor='darkgreen', linewidth=0.5", 0, '', '', 0, 0, 1, 0, 0, 0, 0, 0],
    ['FERMI_NG1275', 'region', path + 'FERMI_NG1275_region.dat', "facecolor='mediumturquoise', edgecolor='darkgreen', linewidth=0.5, alpha=0.6", 0, '', '', 0, 0, 1, 0, 0, 0, 0, 0],
    ['SN1987energyloss', 'band', path + 'cosmoalp/SN1987energyloss.txt', "facecolor='lightgreen', edgecolor='green', linewidth=0.5", 0, '10.1103/PhysRevD.57.2005', '1998', 0, 0, 1, 0, 0, 0, 0, 0],
    ['Xray', 'band', path + 'cosmoalp/Xray.txt', "facecolor='green', edgecolor='darkgreen', linewidth=0.5", 0, '', '', 0, 0, 1, 0, 0, 0, 0, 0],
    ['Deut2016', 'region', path + 'cosmoalp/Deut2016.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5", 0, '', '', 0, 0, 1, 0, 0, 0, 0, 0],
    ['OpticalDepthTerm', 'band', path + 'cosmoalp/OpticalDepthTerm.txt', "facecolor='yellowgreen', edgecolor='green', linewidth=0.5", 0, '1110.2895', '2011', 0, 0, 1, 0, 0, 0, 0, 0],
    ['gEBL1', 'band', path + 'cosmoalp/gEBL1.txt', "facecolor='lightgreen', edgecolor='green', linewidth=0.5", 0, '1110.2895', '2011', 0, 0, 1, 0, 0, 0, 0, 0],
    ['cmb_mu', 'region', path + 'cosmoalp/CMB_mu.txt', "facecolor='green', edgecolor='darkgreen', linewidth=0.5", 0, '1110.2895', '2011', 0, 0, 1, 0, 0, 0, 0, 0],
    ['CMB_DEsuE', 'band', path + 'cosmoalp/CMB_DEsuE.txt', "facecolor='forestgreen', edgecolor='darkgreen', linewidth=0.5", 0, '1110.2895', '2011', 0, 0, 1, 0, 0, 0, 0, 0],
    ['Overduin', 'region', path + 'cosmoalp/Overduin.txt', "facecolor='lightgreen', edgecolor='green', linewidth=0.5", 0, '1110.2895', '2011', 0, 0, 1, 0, 0, 0, 0, 0],
    ['Ressell', 'band', path + 'cosmoalp/Ressell.txt', "facecolor='lightgreen', edgecolor='green', linewidth=0.5", 0, '1110.2895', '2011', 0, 0, 1, 0, 0, 0, 0, 0],
    ['EBL2', 'region', path + 'cosmoalp/EBL2.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5", 0, '1110.2895', '2011', 0, 0, 1, 0, 0, 0, 0, 0],
    # COSMOLOGY - HALOSCOPES
    ['old_haloscopes', 'band', path + 'MicrowaveCavities.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['admx', 'band', path + 'admx.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['admx_hf_2016', 'band', path + 'admx_hf_2016.dat', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMX2018', 'band', path + 'ADMX2018.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMX2019', 'band', path + 'ADMX2019.dat', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '10.1103/PhysRevLett.124.101303', '2019', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMX2019_1', 'band', path + 'ADMX2019_1.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '10.1103/PhysRevLett.124.101303', '2019', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMX2019_2', 'band', path + 'ADMX2019_2.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '10.1103/PhysRevLett.124.101303', '2019', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMX_sidecar', 'band', path + 'ADMX_sidecar.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '1901.00920', '2018', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMX2021', 'band', path + 'ADMX2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '2110.06096', '2021', 0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP-8TB', 'band', path + 'CAPP-8TB.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP_multicell', 'band', path + 'CAPP_multicell_2020.dat', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP2021', 'band', path + 'CAPP2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP2024', 'band', path + 'CAPP2024-12T.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '2402.12892', '2024', 0, 0, 1, 1, 0, 0, 0, 0],
    ['HAYSTAC', 'band', path + 'HAYSTAC.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['HAYSTAC2020', 'band', path + 'haystac2020.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '2008.01853', '2020', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ORGAN', 'band', path + 'ORGAN.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ORGAN-Q2024', 'band', path + 'ORGAN-Q2024.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '2407.18586', '2024', 0, 0, 1, 1, 0, 0, 0, 0],
    ['QUAX', 'band', path + 'QUAX.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['QUAX2021', 'band', path + 'QUAX2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '2012.09498', '2021', 0, 0, 1, 1, 0, 0, 0, 0],
    ['QUAX2024', 'band', path + 'QUAX2024.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '2402.19063', '2024', 0, 0, 1, 1, 0, 0, 0, 0],
    ['RADES2021', 'band', path + 'RADES2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.2", 0, '2104.13798', '2021', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ABRA10cm', 'band', path + 'ABRA10cm.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=0.5", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ABRA_2021', 'band', path + 'ABRA_2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=0.5", 0, '2102.06722', '2021', 0, 0, 1, 1, 0, 0, 0, 0],
    ['BASE_2021', 'band', path + 'BASE2021.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=0.5", 0, '10.1103/PhysRevLett.126.041301', '2021', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMX_SLIC', 'band', path + 'ADMX_SLIC.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=1", 0, '1911.05772', '2019', 0, 0, 1, 1, 0, 0, 0, 0],
    ['SHAFT', 'band', path + 'SHAFT.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5, alpha=0.5", 0, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['TransmonMW_PC', 'band', path + 'TransmonMWphotoncounter_2024.txt', "facecolor='limegreen', edgecolor='darkgreen', linewidth=0.5", 0, '2403.02321', '2024', 0, 0, 1, 1, 0, 0, 0, 0],
    
    ['TASEH_2022','band', path+'TASEH_2022.txt',"facecolor='limegreen',edgecolor='darkgreen',linewidth=0.2",0,'2205.05574','2022',0, 0, 1, 1, 0, 0, 0, 0],
    ['GraHal_2022','band', path+'GraHal_2022.txt',"facecolor='limegreen',edgecolor='darkgreen',linewidth=0.2",0,'2110.14406','2022',0, 0, 1, 1, 0, 0, 0, 0],
    ['NeutronStars','band', path+'NeutronStars.txt',"facecolor='limegreen',edgecolor='darkgreen',linewidth=0.2",0,'2202.08274','2022',0, 0, 1, 1, 0, 0, 0, 0],
    ['ORGAN1a_2022','band', path+'ORGAN1a_2022.txt',"facecolor='limegreen',edgecolor='darkgreen',linewidth=0.2",0,'2203.12152','2022',0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP12T_2022','band', path+'CAPP12T_2022.txt',"facecolor='limegreen',edgecolor='darkgreen',linewidth=0.2",0,'2210.10961','2022',0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP-PACE_2022','band', path+'CAPP-PACE_2022.txt',"facecolor='limegreen',edgecolor='darkgreen',linewidth=0.2",0,'2207.13597','2022',0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP18T_2022','band', path+'CAPP18T_2022.txt',"facecolor='limegreen',edgecolor='darkgreen',linewidth=0.2",0,'2206.08845','2022',0, 0, 1, 1, 0, 0, 0, 0],
    ['CAST-CAPP','band', path+'CAST-CAPP.txt',"facecolor='limegreen',edgecolor='darkgreen',linewidth=0.2",0,'https://doi.org/10.1038/s41467-022-33913-6','2022',0, 0, 1, 1, 0, 0, 0, 0],
    
    
    
    # COSMOLOGY - HALOSCOPES - PROJECTIONS
    ['ORGANprosp', 'line', path + 'ORGAN2.dat', "color='darkgreen', linewidth=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['castcapp2', 'band', path + 'CASTCAPP2.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP4', 'line', path + 'CAPP4.dat', "color='darkgreen', linewidth=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['CAPP4_l', 'line', path + 'CAPP4.dat', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['MADMAX', 'band', path + 'MADMAX.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['MADMAX_l', 'line', path + 'MADMAX.dat', "color='darkgreen', linewidth=0.3, alpha=1, linestyle='--'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMXprosp_2GHz', 'band', path + 'ADMX_prospects_2GHz.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMXprosp_10GHz', 'band', path + 'ADMX_prospects_10GHz.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMXprosp_2GHz_l', 'line', path + 'ADMX_prospects_2GHz.dat', "color='darkgreen', linewidth=0.3, alpha=1, linestyle='--'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ADMXprosp_10GHz_l', 'line', path + 'ADMX_prospects_10GHz.dat', "color='darkgreen', linewidth=0.3, alpha=1, linestyle='--'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ABRA1', 'band', path + 'ABRAres_1.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ABRA1_l', 'line', path + 'ABRAres_1.dat', "color='green', linewidth=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ABRA2', 'line', path + 'ABRAres_2.dat', "color='green', linewidth=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ABRA3', 'line', path + 'ABRAres_3.dat', "color='green', linewidth=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ABRA1_l', 'line', path + 'ABRAres_1.dat', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['ABRA_2021_l', 'line', path + 'ABRA_2021.txt', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 1, '2102.06722', '2021', 0, 0, 1, 1, 0, 0, 0, 0],
    ['KLASH', 'line', path + 'KLASH.dat', "color='green', linewidth=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['KLASH_l', 'line', path + 'KLASH.dat', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['TOORAD', 'line', path + 'TOORAD2.txt', "color='green', linewidth=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['BRASS', 'line', path + 'BRASS.txt', "color='green', linewidth=0.1, linestyle='-'", 1, 'http://www.iexp.uni-hamburg.de/groups/astroparticle/brass/brassweb.htm', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['IAXODM', 'band', path + 'IAXODM.dat', "facecolor='limegreen', edgecolor='black', linewidth=0.1, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],
    ['IAXODM_l', 'line', path + 'IAXODM.dat', "color='darkgreen', linewidth=0.1, alpha=1, linestyle='--'", 1, '', '', 0, 0, 1, 1, 0, 0, 0, 0],

    # STELLAR
    ['HBalpbound', 'band', path + 'HBalpbound.txt', "facecolor='skyblue', edgecolor='blue', alpha=1, linewidth=0.5", 0, 'Ayala et al.', '', 0, 0, 0, 0, 1, 0, 0, 0],
    ['HBalpbound_l', 'line', path + 'HBalpbound.txt', "color='blue', linewidth=0.5", 0, '', '', 0, 0, 0, 0, 1, 0, 0, 0],
    ['solar_nu', 'band', path + 'ALPSun_nu.txt', "facecolor='steelblue', edgecolor='blue', linewidth=0.5", 0, 'Raffelt & Gondolo', '2008', 0, 0, 0, 0, 1, 0, 0, 0],
    # STELLAR - HELIOSCOPES
    ['CAST', 'band', path + 'cast_env_2016.dat', "facecolor='deepskyblue', edgecolor='blue', linewidth=0.5", 0, '10.1038/nphys4109', '2017', 0, 0, 0, 0, 1, 1, 0, 0], #Up to Nature paper (2017)
    ['CAST2021', 'band', path + 'CAST_2019_2021_PRL.txt', "facecolor='deepskyblue', edgecolor='blue', linewidth=0.5", 0, '10.1103/PhysRevLett.133.221005', '2024', 0, 0, 0, 0, 1, 1, 0, 0], #Legacy results of all the data up to 2021.
    # STELLAR - HELIOSCOPES - PROJECTIONS
    ['BabyIAXO', 'band', path + 'miniIAXO.dat', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
    ['IAXO', 'band', path + 'IAXO_nominal.txt', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
    ['IAXOplus', 'band', path + 'IAXO_plus.txt', "facecolor='deepskyblue', linewidth=0.5, alpha=0.1, linestyle='-'", 1, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
    ['BabyIAXO_l', 'line', path + 'miniIAXO.dat', "color='black', linewidth=0.6, alpha=1, linestyle='--'", 1, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
    ['IAXO_l', 'line', path + 'IAXO_nominal.txt', "color='black', linewidth=0.6, alpha=1, linestyle='--'", 1, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
    ['IAXOplus_l', 'line', path + 'IAXO_plus.txt', "color='black', linewidth=0.6, alpha=1, linestyle='--'", 1, '', '', 0, 0, 0, 0, 1, 1, 0, 0],
    ['AMELIE', 'line', path + 'amelie_1m3_arXiv_1508.03006.txt', "color='gray', linewidth=0.6, alpha=1, linestyle='--'", 1, '1508.03006', '2015', 0, 0, 0, 0, 1, 1, 0, 0],

    # LABORATORY
    ['BeamDump', 'region', path + 'llSLAC137.txt', "facecolor='gray', edgecolor='black', linewidth=0.5", 0, 'Bjorken et al.', '', 0, 0, 0, 0, 0, 0, 1, 0],
    # LABORATORY - LSW
    ['CROWS', 'band', path + 'CROWS.txt', "facecolor='gray', edgecolor='white', linewidth=0.5", 0, '', '', 0, 0, 0, 0, 0, 0, 1, 1],
    ['ALPSI', 'band', path + 'ALPSI.dat', "facecolor='gray', edgecolor='white', linewidth=0.5", 0, '', '', 0, 0, 0, 0, 0, 0, 1, 1],
    ['OSCAR2015', 'band', path + 'osqar2015.dat', "facecolor='gray', edgecolor='black', linewidth=0.5", 0, '', '', 0, 0, 0, 0, 0, 0, 1, 1],
    ['PVLAS2015', 'band', path + 'pvlas2015.dat', "facecolor='gray', edgecolor='black', linewidth=0.5", 0, '', '', 0, 0, 0, 0, 0, 0, 1, 1],
    # LABORATORY - LSW - projection
    ['ALPSII', 'band', path + 'ALPSII.dat', "facecolor='gray', linewidth=0.5, alpha=0.2, linestyle=':'", 1, '', '', 0, 0, 0, 0, 0, 0, 1, 1],
    ['ALPSII_l', 'line', path + 'ALPSII.dat', "color='black', linewidth=0.5, alpha=1, linestyle=':'", 1, '', '', 0, 0, 0, 0, 0, 0, 1, 1],
    ['STAX1', 'line', path + 'STAX1.dat', "color='black', linewidth=0.2, linestyle='-.'", 1, '', '', 0, 0, 0, 0, 0, 0, 1, 1],
    ['STAX2', 'line', path + 'STAX2.dat', "color='black', linewidth=0.2, linestyle='-.'", 1, '', '', 0, 0, 0, 0, 0, 0, 1, 1],

]

path = "data/wimp/"
Wimps = [
    ['PICO_CF3I_2015', 'line', path+'limit_data/PICO_CF3I_2015.dat', "color='#e6beff'", 0, '1510.07754', '2015', "PICO CF3I", 3.5, 9.4e-37, "color='#e6beff', size=10"],
    ['CDEX10_2018', 'line', path+'limit_data/CDEX10_2018.dat', "color='#004444'", 0, '1802.09016', '2018', "CDEX10", 2.6, 1.2e-39, "color='#004444', size=10"],
    ['eDM_SuperCDMS_FDM1_2018', 'line', path+'limit_data/eDM_SuperCDMS_FDM1_2018.dat', "color='#e6194b'", 0, '1804.10697', '2018', "SuperCDMS", 0.5, 8e-27, "color='#e6194b', size=10"],
    ['CRESSTsurface_2017', 'line', path+'limit_data/CRESSTsurface_2017.dat', "color='#000075'", 0, '1707.06749', '2017', "CRESST-surface", 10, 2.8e-34, "color='#000075', size=10"],
    ['eDM_PandaX_FDMq2_2021', 'line', path+'limit_data/eDM_PandaX_FDMq2_2021.dat', "color='#f58231'", 0, '2101.07479', '2021', "PandaX-II", 5.5, 1.9e-32, "color='#f58231', size=10"],
    ['XENON1T_lowmass', 'line', path+'limit_data/XENON1T_lowmass.dat', "color='#3cb44b'", 0, '1907.11485', '2019', "XENON1T S2", 2.5, 7.3e-44, "color='#3cb44b', size=10"],
    ['SI_NeutrinoFloor_Ruppin_Fig4Xe', 'fog', path+'limit_data/SI_NeutrinoFloor_Ruppin_Fig4Xe.txt', "color='gray', linewidth=2.5, linestyle='--', alpha=0.5", 0, '1907.11485', '2019', "XENON1T S2", 2.5, 7.3e-44, "color='#3cb44b', size=10"],
    ['neutrino_floor_billard', 'fog', path+'limit_data/neutrino_floor_billard.txt', "color='gray', linewidth=2.5, linestyle='--', alpha=0.5", 0, '1907.11485', '2019', "XENON1T S2", 2.5, 7.3e-44, "color='#3cb44b', size=10"],
    ['DAMA_Na', 'region', path+'limit_data/DAMA_Na.dat', "color='#ffd8b1'", 0, '---', '---', "DAMA/Na", 31, 7.2e-41, "color='#ffd8b1', size=10"],
    ['DarkSide50_S2only_2018', 'line', path+'limit_data/DarkSide50_S2only_2018.dat', "color='#f032e6'", 0, '1802.06994', '2018', "DarkSide50", 1.7, 1.3e-42, "color='#f032e6', size=10"],
    ['PandaX_light1MeV_2018', 'line', path+'limit_data/PandaX_light1MeV_2018.dat', "color='#800000'", 0, '1802.06912', '2018', "PandaX-II", 1e+04, 6.5e-38, "color='#800000', size=10"],
    ['CDMSLite_2016', 'line', path+'limit_data/CDMSLite_2016.dat', "color='#e6194b'", 0, '1707.01632', '2017', "CDMSLite", 1.4, 9.1e-37, "color='#e6194b', size=10"],
    ['XENON100S2_2016', 'line', path+'limit_data/XENON100S2_2016.dat', "color='#3cb44b'", 0, '1605.06262', '2016', "XENON100", 20, 2.2e-42, "color='#3cb44b', size=10"],
    ['XENONnT_projection_2020', 'line', path+'limit_data/XENONnT_projection_2020.dat', "color='#3cb44b'", 0, '2007.08796', '2020', "XENONnT", 2e+02, 1.3e-48, "color='#3cb44b', size=10"],
    ['DarkSide50_2022', 'line', path+'limit_data/DarkSide50_2022.dat', "color='#f032e6'", 0, '2207.11966', '2022', "DarkSide50", 1, 8e-40, "color='#f032e6', size=10"],
    ['XENON1TMIGDAL', 'line', path+'limit_data/XENON1TMIGDAL.txt', "color='#3cb44b'", 0, '2104.07634', '2020', "XENON1T Migdal", 0.33, 3e-39, "color='#3cb44b', size=10"],
    ['LUX_completeExposure_2016', 'line', path+'limit_data/LUX_completeExposure_2016.dat', "color='#000000'", 0, '1608.07648', '2016', "LUX", 3.8e+02, 1.6e-45, "color='#000000', size=10"],
    ['DAMIC_2020', 'line', path+'limit_data/DAMIC_2020.dat', "color='#7E0505'", 0, '2007.15622', '2020', "DAMIC", 0.95, 1.25e-37, "color='#7E0505', size=10"],
    ['DAMIC_SNOLAB_2016', 'line', path+'limit_data/DAMIC_SNOLAB_2016.dat', "color='#7E0505'", 0, '1607.07410', '2018', "DAMIC", 1, 2.2e-36, "color='#7E0505', size=10"],
    ['XMASS_2018', 'line', path+'limit_data/XMASS_2018.dat', "color='#fabebe'", 0, '1804.02180', '2018', "XMASS", 0.38, 1.4e-31, "color='#fabebe', size=10"],
    ['SuperCDMS_SNOLAB_projection_2017', 'line', path+'limit_data/SuperCDMS_SNOLAB_projection_2017.dat', "color='#e6194b'", 0, '1610.00006', '2017', "SuperCDMS", 1.4, 1.2e-44, "color='#e6194b', size=10"],
    ['PandaX-4T_2022', 'line', path+'limit_data/PandaX-4T_2022.dat', "color='#f58231'", 0, '2107.13438', '2022', "PandaX-4T", 3.8, 2.3e-45, "color='#f58231', size=10, rotation=-45"],
    ['eDM_DAMIC_FDM1_2019', 'line', path+'limit_data/eDM_DAMIC_FDM1_2019.dat', "color='#7E0505'", 0, '1907.12628', '2019', "DAMIC", 0.55, 9.1e-30, "color='#7E0505', size=10"],
    ['PICO_C3F8_2017', 'line', path+'limit_data/PICO_C3F8_2017.dat', "color='#911eb4'", 0, '1702.07666', '2017', "PICO C3F8", 3.45, 4.35e-38, "color='#911eb4', size=10"],
    ['CRESSTIII_2019', 'line', path+'limit_data/CRESTIII_2019.txt', "color='#4363d8'", 0, '1904.00498', '2017', "CRESST-III", 0.23, 4e-36, "color='#4363d8', size=10"],
    ['DAMIC_M_2020', 'line', path+'limit_data/DAMIC_M_2020.dat', "color='#7E0505'", 0, '2003.09497', '2020', "DAMIC-M", 1.5, 1e-43, "color='#7E0505', size=10"],
    ['DAMA_I', 'region', path+'limit_data/DAMA_I.dat', "color='#ffd8b1'", 0, '---', '---', "DAMA/I", 5.9, 5.3e-40, "color='#ffd8b1', size=10"],
    ['SI_NeutrinoFloor_Ruppin_LZ_Fig3_1000ty', 'fog', path+'limit_data/SI_NeutrinoFloor_Ruppin_LZ_Fig3_1000ty.dat', "color='gray', linewidth=2.5, linestyle='--', alpha=0.5", 0, '1408.3581', '2014', "Neutrino Fog", 1.5, 7e-47, "color='#ffd8b1', size=10"],
    ['X1T_MIGDAL_2020', 'line', path+'limit_data/X1T_MIGDAL_2020.dat', "color='#3cb44b'", 0, '1907.12771', '2020', "XENON1T Migdal", 0.33, 3e-39, "color='#3cb44b', size=10"],
    ['eDM_XENON1T_FDM1_2019', 'line', path+'limit_data/eDM_XENON1T_FDM1_2019.dat', "color='#3cb44b'", 0, '1907.11485', '2019', "XENON1T", 20, 1.6e-36, "color='#3cb44b', size=10"],
    ['CRESSTII_2015', 'line', path+'limit_data/CRESSTII_2015.dat', "color='#42d4f4'", 0, '1509.01515', '2015', "CRESST-II", 0.51, 2.3e-36, "color='#42d4f4', size=10"],
    ['eDM_DAMIC_FDMq2_2019', 'line', path+'limit_data/eDM_DAMIC_FDMq2_2019.dat', "color='#7E0505'", 0, '1907.12628', '2019', "DAMIC", 0.55, 4.4e-31, "color='#7E0505', size=10"],
    ['eDM_PandaX_FDM1_2021', 'line', path+'limit_data/eDM_PandaX_FDM1_2021.dat', "color='#f58231'", 0, '2101.07479', '2021', "PandaX-II", 5.2, 7.6e-34, "color='#f58231', size=10"],
    ['XENON1T_2018', 'line', path+'limit_data/XENON1T_2018.dat', "color='#3cb44b'", 0, '1805.12562', '2018', "XENON1T", 6.3, 2.7e-44, "color='#3cb44b', size=10"],
    ['CRESSTIII_2017', 'line', path+'limit_data/CRESSTIII_2017.dat', "color='#4363d8'", 0, '1711.07692', '2017', "CRESST-III", 0.4, 4e-36, "color='#4363d8', size=10"],
    ['eDM_SuperCDMS_FDMq2_2018', 'line', path+'limit_data/eDM_SuperCDMS_FDMq2_2018.dat', "color='#e6194b'", 0, '1804.10697', '2018', "SuperCDMS", 0.54, 3.9e-29, "color='#e6194b', size=10"],
    ['XENON1T_2021', 'line', path+'limit_data/XENON1T_2021.dat', "color='#3cb44b'", 0, '10.1103/PhysRevLett.126.091301', '2021', "XENON1T $^8$B", 2.5, 3.2e-42, "color='#3cb44b', size=10"],
    ['NuFloorXe', 'fog', path+'limit_data/NuFloorXe.dat', "color='gray', linewidth=2.5, linestyle='--', alpha=0.5", 0, 'https://github.com/cajohare/AtmNuFloor/blob/master/data/WIMPLimits/SI/nufloor-Xe.txt', '2020', "Neutrino Floor Xe", 1.5, 7e-46, "color='gray', size=10"],
    ['NEWS_G_2018', 'line', path+'limit_data/NEWS_G_2018.dat', "color='#469990'", 0, '1809.02485', '2018', "NEWS-G", 10.6, 5.6e-39, "color='#469990', size=10"],
    ['DEAP3600_2019', 'line', path+'limit_data/DEAP3600_2019.dat', "color='#800080'", 0, '1902.04048', '2019', "DEAP-3600", 25, 4.2e-43, "color='#800080', size=10"],
    ['LZ_projection_2018', 'line', path+'limit_data/LZ_projection_2018.dat', "color='#000000'", 1, '1802.06039', '2018', "LZ", 3e+02, 1.1e-47, "color='#000000', size=10"],
    ['PandaX_2017', 'line', path+'limit_data/PandaX_2017.dat', "color='#f58231'", 0, '1708.06917', '2017', "PandaX-II", 6, 9e-44, "color='#f58231', size=10"],
]

path1 = 'data/axion/hints/'
path2 = 'data/axion/gaegag/'
AxionsGae= [
    ["DFSZ1_starhint", "region", path1 + "DFSZ1_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='springgreen', edgecolor='darkgreen', alpha=0.2", 0, '', ''],
    ["DFSZ2_starhint", "region", path1 + "DFSZ2_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='lime', edgecolor='darkgreen', alpha=0.2", 0, '', ''],
    ["AJ23_starhint", "region", path1 + "AJ23_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='orange', edgecolor='red', alpha=0.2", 0, '', ''],
    ["AJ53_starhint", "region", path1 + "AJ53_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='yellow', edgecolor='orange', alpha=0.2", 0, '', ''],
    ["AJ83_starhint", "region", path1 + "AJ83_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", "facecolor='red', edgecolor='red', alpha=0.2", 0, '', ''],
    ["QCDband", "band", path2 + "DFSZband_gaegag.dat", "facecolor='lemonchiffon', edgecolor='none', linewidth=1", 0, '', ''],
    ["CAST_gae", "band", path2 + "CAST_gae_gagg.dat", "facecolor='steelblue', edgecolor='darkblue', linewidth=0.5", 0, '', ''],

    ["IAXO_gae", "band", path2 + "sqrtgaagae_sc2.dat", "facecolor='skyblue', edgecolor='black', linewidth=0.5, alpha=0.3", 1, '', ''],
    ["IAXOplus_gae", "band", path2 + "sqrtgaagae_sc3.dat", "facecolor='skyblue', edgecolor='black', linewidth=0.5, alpha=0.3", 1, '', ''],
    ["IAXO_gae_l", "line", path2 + "sqrtgaagae_sc2.dat", "color='black', linewidth=0.5, linestyle='--'", 1, '', ''],
    ["IAXOplus_gae_l", "line", path2 + "sqrtgaagae_sc3.dat", "color='black', linewidth=0.5, linestyle='--'", 1, '', ''],
]

# ===========================================================================#
expGag = db.DataBaseGag(FILE_DATABASE, "AxionsGag", True)
expGag.insert_rows(AxionsGag)

expGae = db.DataBaseGae(FILE_DATABASE, "AxionsGae", True)
expGae.insert_rows(AxionsGae)

w = db.DataBaseWimps(FILE_DATABASE.replace("Axions","Wimps"), "Wimps_SI", True)
w.insert_rows(Wimps)
