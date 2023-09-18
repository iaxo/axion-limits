import matplotlib.pyplot as plt
import matplotlib as mpl
from XPlotter import BasePlot, ExPltItem


# ==============================================================================#
# class to encapsulate the needed tools to plot sensitivities in the
# ALP g_ag versus m_a parameter space
class WimpPlot:
    # ==============================================================================#
    # build and plot...
    #

    ListOfPlotTypes = {'large_panorama', 'panorama', 'lowmass'}

    def __init__(self, plottype="lowmass", projections=False, showplot=True, saveplot=True):
        # print(projections, showplot, saveplot)
        self.ListOfPlotTypes = {'large_panorama', 'panorama', 'lowmass'}

        if plottype not in self.ListOfPlotTypes:
            print('ERROR: ' + plottype + ' not a known plot type')
            exit()

        # if (plottype == "lowmass"):
        figx = 6
        figy = 6
        ymin = 1e-45
        ymax = 1e-37
        xmin = 0.2
        xmax = 20
        ticksopt_x = 'normal'
        ticksopt_y = 'normal'
        labelx = r'WIMP mass $m_\chi$ (GeV)'
        labely = r'SI WIMP-nucleon cross section $\sigma^{\rm SI}_N$ (cm$^2$)'

        self.wimpplot = BasePlot(xlab=labelx, ylab=labely, \
                                 figsizex=figx, figsizey=figy,
                                 y_min=ymin, y_max=ymax,
                                 x_min=xmin, x_max=xmax,
                                 ticksopt_x=ticksopt_x, ticksopt_y=ticksopt_y)

        self.wimpDB = BuildDB()
        self.PlotData(plottype, projections)
        self.PlotLabels(plottype, projections)
        if showplot:
            self.wimpplot.ShowPlot()
        if saveplot:
            print('saving...')
            self.wimpplot.SavePlot('WIMP_' + plottype)
        print('done')

        # ==============================================================================#

    # which lines & regions to plot here...
    #
    def PlotData(self, plottype, projections=False):

        # ===========================================================================#
        if plottype == "lowmass":
            for item in ['COGENT', 'CRESST_1', 'CRESST_2', 'CDMS_Si', 'DAMA']:
                self.wimpDB[item].DrawItem(self.wimpplot)
            # if (projections):
            #     for item in ['ALPSII_l','JURA_l','BabyIAXO_l','IAXO_l','IAXOplus_l']:
            #         self.wimpDB[item].DrawItem(self.wimpplot)
            for item in ['NEWSG2018', 'CRESST2015', 'CDMSlite2015', 'LUX2015', 'EDELWEISS2016', 'SuperCDMS',
                         'DarkSide2018', 'DAMIC2016']:
                self.wimpDB[item].DrawItem(self.wimpplot)

    # ==============================================================================#
    # which labels to include in plot...
    #
    def PlotLabels(self, plottype, projections=False):
        # ===========================================================================#
        if plottype == "lowmass":
            pass
            # plt.text(1e-6,2e-10,r'{\bf Helioscopes}',color="black",size=10)
            # plt.text(1e-7,2e-7,r'{\bf Laboratory}',color="white",size=10)
            # plt.text(1e-9,2e-12,r"$\gamma \textrm{-rays}$",color="black",size=10)
            # plt.text(1e-8,1e-13,'Haloscopes',color="black",size=8)
            # plt.text(5e7,4e-8,'SN1987A',color="black",size=6, rotation=-90,ha='center',va='center')
            # plt.text(1e-4,7e-14,'KSVZ',color="green",size=6,rotation=47)
            # plt.text(5,1e-13,'Telescopes',color="black",size=6,rotation=90)
            # plt.text(2e2,1.5e-10,r'{\bf HB}',color="darkgreen",size=10)
            # plt.text(1e2,2e-9,r'{\bf Sun}',color="white",size=10)
            # plt.text(1.5e7,5e-6,r'{\bf Beam dump}',color="white",size=8,rotation=-45,ha='center',va='center')
            # plt.text(1e4,3e-17,'X rays',color="white",size=10,rotation=-57,ha='center',va='center')
            # plt.text(1e5,1e-14,r'{\bf EBL}',color="black",size=10,rotation=-57,ha='center',va='center')
            # plt.text(2e8,1e-14,r'{\bf CMB}',color="white",size=10,rotation=-57,ha='center',va='center')
            # plt.text(1e8,1e-10,r'{\bf BBN}',color="black",size=10,rotation=-57,ha='center',va='center')
            # plt.text(1e2,1e-11,r'$x_{\rm ion}$',color="black",size=10,ha='center')

            # if (projections):
            #     plt.text(5e-4,5e-12,r'{\bf IAXO}',color="black",size=10,ha='center',va='center')
            #     plt.text(1e-6,5e-11,r'{\bf ALPS-II}',color="black",size=8,ha='center',va='center')
            #     plt.text(1e-6,5e-12,r'{\bf JURA}',color="black",size=8,ha='center',va='center')


# ==============================================================================#
# build a data base (dictionary) with all axion data (sensitivity/exclusion
# lines, etc.) for plots
#
def BuildDB():
    db = {}
    path = "data/wimp/"

    # hints
    db['COGENT'] = ExPltItem("COGENT", "region", path + "cogent.dat", facecolor="orange", edgecolor='red')
    db['CDMS_Si'] = ExPltItem("CDMS_Si", "region", path + "cdms_Si.dat", facecolor="skyblue", edgecolor='blue')
    db['CRESST_1'] = ExPltItem("CRESST_1", "region", path + "cresst_1.dat", facecolor="pink", edgecolor='red')
    db['CRESST_2'] = ExPltItem("CRESST_2", "region", path + "cresst_2.dat", facecolor="pink", edgecolor='red')
    db['DAMA'] = ExPltItem("DAMA_no_channelling", "region", path + "dama.dat", facecolor="orange", edgecolor='red')

    db['NEWSG2018'] = ExPltItem("NEWSG2018", "line", path + "newsg.dat", color="red")
    db['CRESST2015'] = ExPltItem("CRESST2015", "line", path + "cresst_2015.dat", color="blue")
    db['CDMSlite2015'] = ExPltItem("CDMSlite2015", "line", path + "cdmsLite_2015.dat", color="red")
    db['LUX2015'] = ExPltItem("LUX2015", "line", path + "LUX_2015.dat", color="red")
    db['EDELWEISS2016'] = ExPltItem("EDELWEISS2016", "line", path + "edelweiss2016.dat", color="red")
    db['SuperCDMS'] = ExPltItem("SuperCDMS", "line", path + "superCDMS.dat", color="orange")
    db['DarkSide2018'] = ExPltItem("DarkSide2018", "line", path + "darkside2018_noQ.dat", color="red")
    db['DAMIC2016'] = ExPltItem("DAMIC2016", "line", path + "damic2016.dat", color="red")

    # db['ksvz'] = ExPltItem("ksvz","region",path+"ksvz.dat",facecolor="white",edgecolor="orange",linewidth=1)

    # db['old_haloscopes'] = ExPltItem("old_haloscopes","band", path+"MicrowaveCavities.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['admx'] = ExPltItem("admx","band", path+"admx.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['admx_hf_2016'] = ExPltItem("haystack","band", path+"admx_hf_2016.dat",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['ADMX2018'] = ExPltItem("ADMX2018","band", path+"ADMX2018.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['ADMX2019_1'] = ExPltItem("ADMX2019_1","band", path+"ADMX2019_1.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['ADMX2019_2'] = ExPltItem("ADMX2019_2","band", path+"ADMX2019_2.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['ADMX_sidecar'] = ExPltItem("ADMX_sidecar","band", path+"ADMX_sidecar.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['CAPP-8TB'] = ExPltItem("CAPP-8TB","band", path+"CAPP-8TB.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['HAYSTAC'] = ExPltItem("HAYSTAC","band", path+"HAYSTAC.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['ORGAN'] = ExPltItem("ORGAN","band", path+"ORGAN.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    # db['QUAX'] = ExPltItem("QUAX","band", path+"QUAX.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)

    # db['ABRA10cm'] = ExPltItem("ABRA10cm","band", path+"ABRA10cm.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.5,alpha=0.5)
    # db['SHAFT'] = ExPltItem("SHAFT","band", path+"SHAFT.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.5,alpha=0.5)

    # db['hess'] = ExPltItem('HESS','band',path+'hess.dat',facecolor="lightseagreen",edgecolor="darkgreen", linewidth=0.5)
    # db['sn1987a_photon'] = ExPltItem('sn1987a_photon','band',path+'sn1987a_photon.dat',facecolor="turquoise",edgecolor="darkgreen", linewidth=0.5)
    # db['FERMI_NG1275'] = ExPltItem("FERMI_NG1275_region",'region',path+"FERMI_NG1275_region.dat",facecolor="mediumturquoise",edgecolor="darkgreen", linewidth=0.5, alpha=0.6)

    # db['SN1987energyloss'] = ExPltItem('SN1987energyloss','band',path+'cosmoalp/SN1987energyloss.txt',facecolor="lightgreen",edgecolor="green", linewidth=0.5)
    # db['Xray'] = ExPltItem('Xray','band',path+'cosmoalp/Xray.txt',facecolor="green",edgecolor="darkgreen", linewidth=0.5)
    # db['Deut2016'] = ExPltItem('Deut2016','region',path+'cosmoalp/Deut2016.txt',facecolor="limegreen",edgecolor="darkgreen", linewidth=0.5)
    # db['OpticalDepthTerm'] = ExPltItem('OpticalDepthTerm','band',path+'cosmoalp/OpticalDepthTerm.txt',facecolor="yellowgreen",edgecolor="green", linewidth=0.5)
    # db['gEBL1'] = ExPltItem('gEBL1','band',path+'cosmoalp/gEBL1.txt',facecolor="lightgreen",edgecolor="green", linewidth=0.5)
    # db['EBL2'] = ExPltItem('EBL2','region',path+'cosmoalp/EBL2.txt',facecolor="limegreen",edgecolor="darkgreen", linewidth=0.5)
    # db['cmb_mu'] = ExPltItem('cmb_mu','region',path+'cosmoalp/cmb_mu.txt',facecolor="green",edgecolor="darkgreen", linewidth=0.5)
    # db['CMB_DEsuE'] = ExPltItem('CMB_DEsuE','band',path+'cosmoalp/CMB_DEsuE.txt',facecolor="forestgreen",edgecolor="darkgreen", linewidth=0.5)
    # db['Overduin'] = ExPltItem('Overduin','region',path+'cosmoalp/Overduin.txt',facecolor="lightgreen",edgecolor="green", linewidth=0.5)
    # db['Ressell'] = ExPltItem('Ressell','band',path+'cosmoalp/Ressell.txt',facecolor="lightgreen",edgecolor="green", linewidth=0.5)
    # db['endlist2_gamma_projimprov'] = ExPltItem("endlist2_gamma_projimprov","band",path+"endlist2_gamma_projimprov.txt",facecolor="gray",edgecolor="black",linewidth=0.5)

    # db['telescopes'] = ExPltItem("telescopes","band", path+"telescopes.dat",facecolor="green",edgecolor="darkgreen",linewidth=0.5)
    # db['telescopes_new'] = ExPltItem("telescopes_new","band", path+"telescopes_new.dat",facecolor="green",edgecolor="darkgreen",linewidth=0.5)

    # db['HBalpbound'] = ExPltItem('HBalpbound','band',path+'HBalpbound.txt',facecolor="skyblue",edgecolor="blue", linewidth=0.5)
    # db['HBalpbound_l'] = ExPltItem('HBalpbound_l','line',path+'HBalpbound.txt',color="blue", linewidth=0.5)
    # db['solar_nu'] = ExPltItem('solar_nu','band',path+'ALPSun_nu.txt',facecolor="steelblue",edgecolor="blue", linewidth=0.5)

    # db['CAST'] = ExPltItem('CAST','band',path+'cast_env_2016.dat',facecolor="deepskyblue",edgecolor="blue", linewidth=0.5)

    # db['CROWS'] = ExPltItem("CROWS","band", path+"CROWS.txt",facecolor="gray",edgecolor="white",linewidth=0.5)
    # db['ALPSI'] = ExPltItem("ALPSI","band", path+"ALPSI.dat",facecolor="gray",edgecolor="white",linewidth=0.5)
    # db['OSCAR2015'] = ExPltItem('OSCAR2015','band',path+'osqar2015.dat',facecolor="gray",edgecolor="black", linewidth=0.5)
    # db['PVLAS2015'] = ExPltItem('PVLAS2015','band',path+'pvlas2015.dat',facecolor="gray",edgecolor="black", linewidth=0.5)
    # db['BeamDump'] = ExPltItem('BeamDump','region',path+'llSLAC137.txt',facecolor="gray",edgecolor="black", linewidth=0.5)

    # #projecions
    # db['BabyIAXO'] = ExPltItem('BAbyIAXO','band',path+'miniIAXO.dat',facecolor="deepskyblue", linewidth=0.5, alpha=0.2, linestyle="-")
    # db['IAXO'] = ExPltItem('IAXO','band',path+'IAXO_nominal.txt', facecolor="deepskyblue",linewidth=0.5, alpha=0.2, linestyle="-")
    # db['IAXOplus'] = ExPltItem('IAXOplus','band',path+'IAXO_plus.txt',facecolor="deepskyblue", linewidth=0.5, alpha=0.3, linestyle="-")
    # db['ALPSII'] = ExPltItem('ALPSII','band',path+'ALPSII.dat',facecolor="gray", linewidth=0.5, alpha=0.2, linestyle=":")
    # db['ORGANprosp'] = ExPltItem('ORGANprosp','line',path+'ORGAN2.dat',color="darkgreen", linewidth=0.1, linestyle="-")
    # db['castcapp2'] = ExPltItem('castcapp2','band',path+'CASTCAPP2.dat',facecolor="limegreen", edgecolor="black",linewidth=0.1, alpha=0.1, linestyle="-")
    # db['CAPP4'] = ExPltItem('CAPP4','line',path+'CAPP4.dat',color="darkgreen", linewidth=0.1, linestyle="-")
    # db['MADMAX'] = ExPltItem('MADMAX','band',path+'MADMAX.dat',facecolor="limegreen", edgecolor="black",linewidth=0.1, alpha=0.1, linestyle="-")
    # db['ADMXprosp_2GHz'] = ExPltItem('ADMXprosp_2GHz','band',path+'admx_prospects_2ghz.dat',facecolor="limegreen", edgecolor="black",linewidth=0.1, alpha=0.1, linestyle="-")
    # db['ADMXprosp_10GHz'] = ExPltItem('ADMXprosp_10GHz','band',path+'ADMX_prospects_10GHz.dat',facecolor="limegreen", edgecolor="black",linewidth=0.1, alpha=0.1, linestyle="-")
    # db['ABRA1'] = ExPltItem('ABRA1','band',path+'ABRAres_1.dat',facecolor="limegreen", edgecolor="black",linewidth=0.1, alpha=0.1, linestyle="-")
    # db['ABRA1_l'] = ExPltItem('ABRA1','line',path+'ABRAres_1.dat',color="green", linewidth=0.1, linestyle="-")
    # db['ABRA2'] = ExPltItem('ABRA2','line',path+'ABRAres_2.dat',color="green", linewidth=0.1,  linestyle="-")
    # db['ABRA3'] = ExPltItem('ABRA3','line',path+'ABRAres_3.dat',color="green", linewidth=0.1,  linestyle="-")
    # db['KLASH'] = ExPltItem('KLASH','line',path+'KLASH.dat',color="green", linewidth=0.1, linestyle="-")
    # db['IAXODM'] = ExPltItem('IAXODM.dat','band',path+'IAXODM.dat',facecolor="limegreen", edgecolor="black",linewidth=0.1, alpha=0.1, linestyle="-")
    # db['STAX1'] = ExPltItem('STAX1','line',path+'STAX1.dat',color="black", linewidth=0.2, linestyle="-.")
    # db['STAX2'] = ExPltItem('STAX2','line',path+'STAX2.dat',color="black", linewidth=0.2, linestyle="-.")

    # #"only_line" versions
    # db['BabyIAXO_l'] = ExPltItem('BAbyIAXO','line',path+'miniIAXO.dat',color="black", linewidth=0.3, alpha=1, linestyle="--")
    # db['IAXO_l'] = ExPltItem('IAXO','line',path+'IAXO_nominal.txt', color="black",linewidth=0.5, alpha=1, linestyle="--")
    # db['IAXOplus_l'] = ExPltItem('IAXOplus','line',path+'IAXO_plus.txt',color="black", linewidth=0.5, alpha=1, linestyle="--")
    # db['ALPSII_l'] = ExPltItem('ALPSII','line',path+'ALPSII.dat',color="black", linewidth=0.5, alpha=1, linestyle=":") 
    # db['CAPP4_l'] = ExPltItem('ORGANprosp','line',path+'CAPP4.dat',color="darkgreen",linewidth=0.1, alpha=1, linestyle="--")
    # db['MADMAX_l'] = ExPltItem('MADMAX','line',path+'MADMAX.dat',color="darkgreen",linewidth=0.1, alpha=1, linestyle="--")
    # db['ADMXprosp_2GHz_l'] = ExPltItem('ADMXprosp_2GHz','line',path+'admx_prospects_2ghz.dat',color="darkgreen",linewidth=0.1, alpha=1, linestyle="--")
    # db['ADMXprosp_10GHz_l'] = ExPltItem('ADMXprosp_10GHz','line',path+'ADMX_prospects_10GHz.dat',color="darkgreen",linewidth=0.1, alpha=1, linestyle="--")
    # db['ABRA1_l'] = ExPltItem('ABRA1','line',path+'ABRAres_1.dat',color="darkgreen",linewidth=0.1, alpha=1, linestyle="--")
    # db['KLASH_l'] = ExPltItem('KLASH','line',path+'KLASH.dat',color="darkgreen",linewidth=0.1, alpha=1, linestyle="--")
    # db['IAXODM_l'] = ExPltItem('IAXODM.dat','line',path+'ORGAN2.dat',color="darkgreen",linewidth=0.1, alpha=1, linestyle="--")

    # db['JURA'] = ExPltItem('JURA','line',path+'ALPSIII.dat',color="black", linewidth=0.5, alpha=1, linestyle=":")

    # #hints
    # db['THintMayer'] = ExPltItem('THintMayer','region',path+'Mayer_2013.dat',facecolor='yellow',edgecolor="orange", linewidth=0.5)
    # db['THintCIBER'] = ExPltItem('THintCIBER','region',path+'CIBER_contour_data.dat',facecolor='yellow',edgecolor="orange", linewidth=0.5)
    # mpl.rcParams['hatch.linewidth'] = 0.1
    # db['HBhint'] = ExPltItem('HBhint','region',path+'hints/HB_hint.dat',facecolor='none',edgecolor='red', linewidth=0, hatch='////')

    return db


# ==============================================================================#
# renormalize data, to plot C_ag instead of g_ag
#
def RenormItem(item):
    for i in range(len(item.data)):
        item.data[i, 1] = item.data[i, 1] / item.data[i, 0] * 5.172e9
        # print(item.data[i,0],item.data[i,1])
        # C_ag = g_ag / m_a * 5.172e9
