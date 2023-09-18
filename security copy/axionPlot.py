import matplotlib.pyplot as plt
import matplotlib as mpl
from XPlotter import BasePlot, ExPltItem


# ==============================================================================#
# class to encapsulate the needed tools to plot sensitivities in the
# ALP g_ag versus m_a parameter space
class AxionGagPlot:
    # ==============================================================================#
    # build and plot...
    #
    ListOfPlotTypes = {'large_panorama', 'panorama', 'LSWexps', 'haloscopes', 'haloscopes_zoom',
                       'haloscopes_radeszoom', 'helioscopes'}

    def __init__(self, plottype="large_panorama", projections=False, showplot=True, saveplot=True):
        # print(projections, showplot, saveplot)

        if plottype not in self.ListOfPlotTypes:
            print('ERROR: ' + plottype + ' not a known plot type')
            exit()

        figx = 6.5
        figy = 5
        ymin = 1e-18
        ymax = 1e-4
        xmin = 1e-11
        xmax = 1e9
        ticksopt_x = 'dense'
        ticksopt_y = 'normal'
        labelx = '$m_a$ (eV)'
        labely = r'$|g_{a\gamma}|$ (GeV$^{-1}$)'

        if plottype == "panorama":
            figx = 6.5
            figy = 6
            ymin = 1e-17
            ymax = 1e-6
            xmin = 1e-9
            xmax = 10
            ticksopt_x = 'normal'
            ticksopt_y = 'normal'

        if plottype == "helioscopes":
            figx = 8
            figy = 6
            ymin = 1e-13
            ymax = 1e-8
            xmin = 1e-11
            xmax = 1
            ticksopt_x = 'normal'
            ticksopt_y = 'normal'

        if plottype == "LSWexps":
            figx = 6.5
            figy = 5
            ymin = 1e-13
            ymax = 1e-6
            xmin = 1e-10
            xmax = 1e-2
            ticksopt_x = 'normal'
            ticksopt_y = 'normal'

        if plottype in ["haloscopes", "haloscopes_zoom", "haloscopes_radeszoom"]:
            figx = 8
            figy = 5
            ymin = 1e-1
            ymax = 1e3
            xmin = 1e-9
            xmax = 1
            if plottype in ["haloscopes_zoom"]:
                xmin = 3e-7
                xmax = 3e-2
            if plottype in ["haloscopes_radeszoom"]:
                xmin = 3.4e-5
                xmax = 4.5e-5
            ticksopt_x = 'normal'
            ticksopt_y = 'normal'
            labely = r'$|C_{a\gamma}|\tilde{\rho}_a^{1/2}$'

        self.axplot = BasePlot(xlab=labelx, ylab=labely,
                               figsizex=figx, figsizey=figy,
                               y_min=ymin, y_max=ymax,
                               x_min=xmin, x_max=xmax,
                               ticksopt_x=ticksopt_x, ticksopt_y=ticksopt_y)

        self.axionDB = BuildDB()
        self.PlotData(plottype, projections)
        self.PlotLabels(plottype, projections)
        if showplot:
            self.axplot.ShowPlot()
        if saveplot:
            print('saving...')
            self.axplot.SavePlot('AxionPhoton_' + plottype, picklesave=True)
        print('done')

    # ==============================================================================#
    # which lines & regions to plot here...
    #
    def PlotData(self, plottype, projections=False):
        print("projections=", projections)

        # ===========================================================================#
        if plottype == "large_panorama":
            for item in ['qcdband', 'ksvz']:
                self.axionDB[item].DrawItem(self.axplot)
            if projections:
                for item in ['ABRA1', 'ABRA1_l',  # 'KLASH',
                             'ADMXprosp_2GHz', 'ADMXprosp_2GHz_l', 'ADMXprosp_10GHz', 'ADMXprosp_10GHz_l',
                             'CAPP4_l', 'MADMAX_l',  # 'BRASS'
                             'ORGANprosp']:
                    self.axionDB[item].DrawItem(self.axplot)
            for item in ['ADMX2018', 'ADMX2019', 'ADMX2021', 'ADMX_sidecar',
                         'CAPP-8TB', 'HAYSTAC', 'HAYSTAC2020', 'ORGAN', 'QUAX', 'QUAX2021', 'RADES2021', 'ADMX_SLIC',
                         'old_haloscopes', 'admx', 'admx_hf_2016',
                         'hess', 'mrk421', 'sn1987a_photon', 'FERMI_NG1275',
                         'SN1987energyloss', 'Xray', 'Deut2016', 'OpticalDepthTerm', 'gEBL1', 'EBL2',
                         'cmb_mu',  # 'CMB_DEsuE',
                         'Overduin', 'Ressell', 'endlist2_gamma_projimprov', 'telescopes', 'telescopes_new',
                         'HBalpbound', 'solar_nu', 'CAST']:
                self.axionDB[item].DrawItem(self.axplot)
            if projections:
                for item in ['ALPSII_l', 'BabyIAXO_l', 'IAXOplus_l']:
                    self.axionDB[item].DrawItem(self.axplot)
            for item in ['OSCAR2015', 'PVLAS2015', 'BeamDump']:
                self.axionDB[item].DrawItem(self.axplot)

        # ===========================================================================#

        if plottype == "helioscopes":
            for item in ['qcdband', 'ksvz',
                         'admx_hf_2016', 'ADMX2018', 'ADMX2019','ADMX2021', 'ADMX_sidecar',
                         'CAPP-8TB', 'HAYSTAC', 'HAYSTAC2020', 'ORGAN', 'QUAX', 'QUAX2021', 'RADES2021', 'ADMX_SLIC',
                         'old_haloscopes', 'admx',
                         'THintMayer', 'THintCIBER', 'HBhint', 'hess', 'mrk421', 'sn1987a_photon', 'FERMI_NG1275',
                         'endlist2_gamma_projimprov', 'telescopes', 'telescopes_new',
                         'HBalpbound_l', 'solar_nu', 'CAST']:
                self.axionDB[item].DrawItem(self.axplot)
            # if (projections):
            # for item in ['ABRA1','KLASH','IAXODM','ORGANprosp','castcapp2','CAPP4','ADMXprosp_2GHz','ADMXprosp_10GHz','MADMAX']:
            # for item in ['ADMXprosp_2GHz_l','ADMXprosp_10GHz_l','MADMAX_l','CAST']:
            #    self.axionDB[item].DrawItem(self.axplot)
            if (projections):
                for item in ['ALPSII_l', 'BabyIAXO', 'IAXO', 'IAXOplus', 'BabyIAXO_l', 'IAXO_l', 'IAXOplus_l', 'AMELIE']:
                    self.axionDB[item].DrawItem(self.axplot)
            for item in ['SHAFT', 'ABRA_2021', 'BASE_2021']:
                self.axionDB[item].DrawItem(self.axplot)
            for item in ['OSCAR2015', 'PVLAS2015', 'ALPSI']:
                self.axionDB[item].DrawItem(self.axplot)

        # ===========================================================================#
        if plottype == "panorama":
            for item in ['qcdband', 'ksvz', 'dfsz',
                         'admx_hf_2016', 'ADMX2018', 'ADMX2019','ADMX2021', 'ADMX_sidecar',
                         'CAPP-8TB', 'CAPP2021', 'HAYSTAC', 'HAYSTAC2020', 'ORGAN', 'QUAX', 'QUAX2021',
                         'old_haloscopes', 'admx', 'RADES2021', 'ADMX_SLIC',
                         'hess', 'mrk421', 'sn1987a_photon', 'FERMI_NG1275',
                         'endlist2_gamma_projimprov', 'telescopes', 'telescopes_new',
                         'HBalpbound_l', 'solar_nu', 'CAST']:
                self.axionDB[item].DrawItem(self.axplot)
            if projections:
                for item in ['ABRA1', 'KLASH', 'IAXODM', 'ORGANprosp', 'castcapp2', 'CAPP4', 'ADMXprosp_2GHz',
                             'ADMXprosp_10GHz', 'MADMAX',
                             'ADMXprosp_2GHz_l', 'ADMXprosp_10GHz_l', 'MADMAX_l', 'CAST']:
                    self.axionDB[item].DrawItem(self.axplot)
            if projections:
                for item in ['ALPSII_l', 'BabyIAXO', 'IAXO', 'IAXOplus', 'BabyIAXO_l', 'IAXO_l', 'IAXOplus_l']:
                    self.axionDB[item].DrawItem(self.axplot)
            for item in ['SHAFT', 'ABRA_2021']:
                self.axionDB[item].DrawItem(self.axplot)
            for item in ['OSCAR2015', 'PVLAS2015', 'ALPSI']:
                self.axionDB[item].DrawItem(self.axplot)

        # ===========================================================================#
        if plottype == "LSWexps":
            for item in ['qcdband', 'ksvz',
                         'THintMayer', 'THintCIBER', 'hess', 'mrk421', 'sn1987a_photon', 'FERMI_NG1275', 'CAST',
                         'HBhint']:
                self.axionDB[item].DrawItem(self.axplot)
            if projections:
                for item in ['ALPSII', 'STAX1', 'STAX2', 'ALPSII', 'JURA']:
                    self.axionDB[item].DrawItem(self.axplot)
                self.axionDB[item].DrawItem(self.axplot)
            for item in ['OSCAR2015', 'PVLAS2015', 'ALPSI', 'CROWS']:
                self.axionDB[item].DrawItem(self.axplot)

        # ===========================================================================#
        if plottype in ["haloscopes", "haloscopes_zoom", "haloscopes_radeszoom"]:
            self.axionDB['CAST'].drawopt['facecolor'] = 'steelblue'
            for item in ['qcdband', 'ksvz',
                         'ADMX2018', 'ADMX2019', 'ADMX2021', 'ADMX_sidecar',  # 'ADMX2019_2',
                         'CAPP-8TB', 'CAPP_multicell', 'CAPP2021', 'HAYSTAC', 'HAYSTAC2020', 'ORGAN', 'QUAX',
                         'QUAX2021', 'ADMX_SLIC',
                         'RADES2021', 'admx', 'CAST']:
                RenormItem(self.axionDB[item])
                self.axionDB[item].DrawItem(self.axplot)
            if projections:
                for item in ['ABRA1', 'ABRA2', 'ABRA3', 'ABRA1_l', 'KLASH', 'TOORAD',  # 'IAXODM','IAXODM_l',
                             'ADMXprosp_2GHz', 'ADMXprosp_2GHz_l', 'ADMXprosp_10GHz', 'ADMXprosp_10GHz_l',
                             'CAPP4_l', 'MADMAX_l', 'ORGANprosp', 'BRASS']:
                    RenormItem(self.axionDB[item])
                    self.axionDB[item].DrawItem(self.axplot)
            for item in ['old_haloscopes']:
                RenormItem(self.axionDB[item])
                self.axionDB[item].DrawItem(self.axplot)
            if projections:
                for item in ['BabyIAXO', 'BabyIAXO_l', 'IAXO', 'IAXO_l', 'IAXOplus', 'IAXOplus_l']:
                    RenormItem(self.axionDB[item])
                    self.axionDB[item].DrawItem(self.axplot)

    # ==============================================================================#
    # which labels to include in plot...
    #
    def PlotLabels(self, plottype, projections=False):
        # ===========================================================================#
        if plottype == "large_panorama":
            plt.text(1e-8, 2e-10, r'{\bf Helioscopes (CAST)}', color="black", size=10)
            plt.text(1e-7, 2e-7, r'{\bf Laboratory}', color="white", size=10)
            plt.text(1e-9, 5e-12, r"$\gamma \textrm{-rays}$", color="black", size=10, ha="center")
            # plt.text(1e-8,1e-13,'Haloscopes',color="black",size=9)
            plt.text(5e7, 4e-8, 'SN1987A', color="black", size=6, rotation=-90, ha='center', va='center')
            plt.text(3e-4, 21e-14, 'KSVZ', color="black", size=6, rotation=47)
            plt.text(5, 1e-13, 'Telescopes', color="black", size=6, rotation=90)
            plt.text(2e2, 1.6e-10, 'Horizontal \n Branch Stars', color="black", size=7, va='center', ha='center')
            plt.text(1e2, 2e-9, r'{\bf Sun}', color="white", size=10)
            plt.text(1.5e7, 5e-6, r'{\bf Beam dump}', color="white", size=8, rotation=-45, ha='center', va='center')
            plt.text(1e4, 3e-17, 'X rays', color="white", size=10, rotation=-57, ha='center', va='center')
            # plt.text(1e5,1e-14,r'{\bf EBL}',color="black",size=10,rotation=-57,ha='center',va='center')
            plt.text(1e5, 1e-14, 'Extra-galactic \n Background Light', color="black", size=9, rotation=-57, ha='center',
                     va='center')
            plt.text(2e8, 1e-14, r'{\bf CMB}', color="white", size=9, rotation=-57, ha='center', va='center')
            plt.text(3e7, 1e-10, 'Big-Bang \n Nucleosynthesis', color="black", size=10, rotation=-57, ha='center',
                     va='center')
            plt.text(1e2, 1e-13, 'H$_2$ ionization \n fraction', color="black", size=8, ha='center', va='center',
                     rotation=90)

            # added for Gaia's plot
            plt.text(2.9e-6, 3e-13, 'ADMX', color="black", size=6, ha='center', va='center', rotation=90)
            plt.text(8.3e-6, 3.5e-12, 'BNL\n+UF', color="black", size=5, ha='center', va='center', rotation=90)
            plt.text(1.3e-5, 2.5e-14, 'HAYSTAC', color="black", size=4, ha='center', va='center', rotation=90)
            # plt.text(1.1e-5,2.5e-14,'KLASH',color="black",size=5,ha='center',va='center',rotation=90)

            if projections:
                plt.text(1e-3, 3e-11, r'{ BabyIAXO}', color="black", size=8, ha='center', va='center')
                plt.text(1e-3, 5e-12, r'{ IAXO}', color="black", size=8, ha='center', va='center')
                plt.text(1e-6, 3e-11, r'{ ALPS-II}', color="black", size=8, ha='center', va='center')
                # plt.text(1e-6,5e-12,r'{\bf JURA}',color="black",size=8,ha='center',va='center')

                # added for Gaia's plot
                plt.text(8e-6, 2e-16, 'ADMX+CAPP', color="black", size=5, ha='center', va='center', rotation=47)
                plt.text(2e-4, 8e-15, 'MADMAX', color="black", size=5, ha='center', va='center', rotation=47)
                plt.text(1.2e-4, 6e-13, 'ORGAN', color="black", size=5, ha='center', va='center', rotation=90)
                plt.text(7e-9, 4e-15, '"DM-\n Radios"', color="black", size=6, ha='center', va='center')

        # ===========================================================================#
        if plottype == "panorama":
            plt.text(1e-5, 2e-10, r'{\bf Helioscopes (CAST)}', color="black", size=11)
            plt.text(1e-7, 2e-7, r'{\bf Laboratory}', color="white", size=11)
            plt.text(2e-9, 6e-12, r"HE $\gamma \textrm{-rays}$", color="black", size=10)
            plt.text(5e-6, 1e-13, r'{\bf Haloscopes}', color="black", size=11, ha='center')
            plt.text(3e-4, 2e-13, 'KSVZ', color="green", size=9, rotation=40)
            # plt.text(0.5e-3,4e-14,'Axion models',color="black",size=9,rotation=40)
            plt.text(0.5e-3, 1e-13, 'DSFZ', color="green", size=9, rotation=40)
            plt.text(5, 3e-13, 'Telescopes', color="black", size=8, rotation=90)
            plt.text(1, 0.9e-10, 'HB', color="black", size=9)
            plt.text(3, 1.3e-9, 'Sun', color="black", size=9, ha='center')
            # plt.text(1e2,2e-9,r'{\bf Sun}',color="white",size=10)

            if projections:
                plt.text(2e-3, 2.5e-11, r'BabyIAXO', color="black", size=10, ha='center', va='center')
                plt.text(2e-3, 7e-12, r'{\bf IAXO}', color="black", size=11, ha='center', va='center')
                # plt.text(1e-5,1e-12,r'{\bf IAXO+}',color="black",size=9,ha='center',va='center')
                plt.text(5e-7, 3e-11, r'{\bf ALPS-II}', color="black", size=10, ha='center', va='center')
                # plt.text(5e-7,1.5e-12,r'{\bf JURA}',color="black",size=9,ha='center',va='center')
        # ===========================================================================#
        if plottype == "helioscopes":
            plt.text(3e-6, 8.5e-11, r'{\bf CAST}', color="blue", size=13)
            # plt.text(1e-7,2e-7,r'{\bf Laboratory}',color="white",size=12)
            plt.text(1e-8, 6e-12, r"T-hints", color="red", size=11)
            # plt.text(2e-9,6e-12,r"HE $\gamma \textrm{-rays}$",color="black",size=10)
            plt.text(1e-6, 1e-12, r'{\bf Haloscopes}', color="black", size=13)
            plt.text(1.15e-3, 0.75e-12, 'KSVZ', color="black", size=10, rotation=57)
            plt.text(4.7e-3, 5e-13, 'Axion models', color="black", size=10, rotation=57)
            # plt.text(5,3e-13,'Telescopes',color="black",size=8,rotation=90)
            plt.text(8e-2, 7e-11, 'HB', color="black", size=10)
            plt.text(1e-1, 1.3e-11, 'HB hint', color="red", size=10)
            plt.text(3.5e-3, 6.e-12, 'WD \ncooling\n hint ', color="red", size=10, ha="center")
            # plt.text(3,1.3e-9,'Sun',color="black",size=9,ha='center')
            # plt.text(1e2,2e-9,r'{\bf Sun}',color="white",size=10)
            plt.text(7e-10, 2e-9, 'ABRA\n-10cm', color="black", size=10)
            plt.text(2e-11, 4e-10, 'SHAFT', color="black", size=10)
            plt.text(3e-8, 2e-11, 'HESS', color="black", size=9, ha='center')
            plt.text(1e-8, 4e-11, 'Mrk421', color="black", size=9, ha='center')
            plt.text(1.5e-11, 7e-12, 'SN1987A', color="black", size=9)
            plt.text(6e-10, 7e-12, 'Fermi\nNG1275', color="black", size=9)

            if projections:
                plt.text(1e-3, 8.5e-11, r'{\bf AMELIE}', color="gray", size=11)
                plt.text(3e-4, 2e-11, r'BabyIAXO', color="black", size=12)
                plt.text(1.75e-4, 5e-12, r'{\bf IAXO}', color="black", size=13)
                plt.text(1.4e-4,3.2e-12,r'{\bf IAXO+}',color="black",size=9,ha='center',va='center')
                plt.text(5e-7, 2.7e-11, r'{ ALPS-II}', color="black", size=12)
                # plt.text(5e-7,1.5e-12,r'{\bf JURA}',color="black",size=9,ha='center',va='center')

        # ===========================================================================#
        if plottype == "haloscopes":
            plt.text(2.5e-3, 110, r'{\bf CAST}', color="black", size=12, ha='center', rotation=-57)
            plt.text(1e-8, 3, 'ABRA/DM-Radio', color="black", size=12, ha='center', rotation=-57)
            plt.text(3.3e-7, 70, 'KLASH', color="black", size=11, ha='center', va='center', rotation=90)
            plt.text(1e-3, 2.5, 'KSVZ', color="green", size=9, va='center', ha='center')
            plt.text(1e-3, 0.32, 'Axion models', color="green", size=9, ha='center')
            plt.text(2.9e-6, 70, r'{\bf ADMX}', color="black", size=12, ha='center', va='center', rotation=90)
            plt.text(9.5e-7, 70, 'ACTION/IAXO-DM', color="black", size=10, ha='center', va='center', rotation=90)
            plt.text(8.3e-6, 650, 'BNL\n+UF', color="black", size=8, ha='center', va='center')
            plt.text(7e-6, 0.86, 'ADMX', color="black", size=10, ha='center', va='center')
            plt.text(1.9e-5, 2.24, 'CAPP', color="black", size=10, ha='center', va='center')
            plt.text(1.46e-5, 25, 'HAYSTAC', color="black", size=8, ha='center', va='center', rotation=90)
            plt.text(1.2e-4, 1.15, 'MADMAX', color="black", size=8, ha='center', va='center')
            plt.text(1.2e-4, 30, 'ORGAN', color="black", size=8, ha='center', va='center')
            plt.text(3e-5, 25, 'RADES', color="black", size=8, ha='center', va='center', rotation=90)

            if projections:
                plt.text(1.8e-3, 83, r'BabyIAXO', color="black", size=10, ha='center', va='center', rotation=-57)
                plt.text(1e-3, 36, r'{\bf IAXO}', color="black", size=11, ha='center', va='center', rotation=-57)
                plt.text(0.01, 12, 'TOORAD', color="black", size=8, ha='center', va='center', rotation=90)
                # plt.text(1e-5,1e-12,r'{\bf IAXO+}',color="black",size=9,ha='center',va='center')
                # plt.text(5e-7,3e-11,r'{\bf ALPS-II}',color="black",size=10,ha='center',va='center')
                # plt.text(5e-7,1.5e-12,r'{\bf JURA}',color="black",size=9,ha='center',va='center')

        # ===========================================================================#
        if plottype == "LSWexps":
            plt.text(1e-3, 1e-10, r'CAST', color="black", size=10)
            plt.text(1e-4, 1.4e-7, r'{ ALPS-I}', color="white", size=10, ha='center', va='center')
            plt.text(1e-7, 1.5e-7, r'{ CROWS}', color="white", size=10, ha='center', va='center')
            plt.text(3e-3, 1e-7, r'{ PVLAS}', color="black", size=10, ha='center', va='center', rotation=45)
            plt.text(1e-4, 2e-8, r'{ OSQAR}', color="black", size=10, ha='center', va='center')
            plt.text(2e-9, 6e-12, r"T-hints", color="black", size=10)

            if (projections):
                plt.text(3e-6, 1e-10, 'STAX1', color="black", size=10, ha='center', va='center')
                plt.text(2e-6, 5e-12, 'STAX2', color="black", size=10, ha='center', va='center')
                # plt.text(1e-5,1e-12,r'{\bf IAXO+}',color="black",size=9,ha='center',va='center')
                plt.text(1e-6, 3e-11, r'{\bf ALPS-II}', color="black", size=10, ha='center', va='center')
                plt.text(2e-5, 1.3e-12, r'{\bf JURA}', color="black", size=9, ha='center', va='center')

        # ===========================================================================#
        if plottype in ["haloscopes_zoom", "haloscopes_radeszoom"]:
            plt.text(4e-3, 144, r'CAST', color="black", size=10, ha='center', va='center', rotation=-40)
            plt.text(1e-3, 2.8, 'KSVZ', color="green", size=9, va='center', ha='center')
            plt.text(2e-3, 0.36, 'Axion models', color="green", size=9, ha='center')
            plt.text(2.9e-6, 70, r'{ ADMX}', color="black", size=12, ha='center', va='center', rotation=90)
            plt.text(8.3e-6, 400, 'BNL\n+UF', color="black", size=8, ha='center', va='center')
            plt.text(34.6e-6, 25, 'RADES', color="black", size=8, ha='center', va='center', rotation=90)

            if projections:
                plt.text(8e-6, 1.14, 'ADMX/CAPP', color="black", size=10, ha='center', va='center')
                plt.text(1.2e-4, 1.15, 'MADMAX', color="black", size=8, ha='center', va='center')
                plt.text(1.2e-4, 30, 'ORGAN', color="black", size=8, ha='center', va='center')
                plt.text(2e-3, 63, r'BabyIAXO', color="black", size=10, ha='center', va='center', rotation=-40)
                plt.text(1.5e-3, 24, r'IAXO', color="black", size=10, ha='center', va='center', rotation=-40)
                plt.text(2.6e-4, 16, 'BRASS', color="black", size=8, ha='center', va='center', rotation=15)
                plt.text(0.01, 12, 'TOORAD', color="black", size=8, ha='center', va='center', rotation=90)
            else:
                plt.text(8.1e-6, 0.93, 'CAPP', color="black", size=8, ha='center', va='top', rotation=90)
                plt.plot([8.3e-6, 6.79e-6], [1, 6], color='black', linewidth=0.5)
                plt.plot([8.3e-6, 1.07e-5], [1, 1.68], color='black', linewidth=0.5)
                plt.plot([8.3e-6, 1.33e-5], [1, 1.64], color='black', linewidth=0.5)
                plt.text(1.96e-5, 1.00, 'HAYSTAC', color="black", size=8, ha='center', va='top', rotation=90)
                plt.plot([2e-5, 1.71e-5], [1.12, 1.8], color='black', linewidth=0.5)
                plt.plot([2e-5, 2.38e-5], [1.12, 2.24], color='black', linewidth=0.5)

                plt.text(4.3e-5, 3.6, 'QUAX', color="black", size=8, ha='center', va='center', rotation=90)
                plt.text(1.2e-4, 45, 'ORGAN', color="black", size=8, ha='center', va='center', rotation=90)


# ==============================================================================#
# class to encapsulate the needed tools to plot sensitivities in the
# ALP g_ae versus m_a parameter space
class AxionGaePlot:

    # ==============================================================================#
    # build and plot...
    #
    def __init__(self, plottype="helioscopes", projections=False, showplot=True, saveplot=True):

        figx = 6
        figy = 5

        self.axplot = BasePlot(xlab='$m_a$ (eV)', ylab=r'$|g_{ae}g_{a\gamma}|^{1/2}$ (GeV$^{-1/2}$)',
                               figsizex=figx, figsizey=figy,
                               y_min=1.0e-13, y_max=1.0e-10,
                               x_min=1.0e-4, x_max=1.,
                               labelfontsize=13)

        self.axionDB = BuildGaeDB()
        self.PlotData(plottype, projections)
        self.PlotLabels(plottype, projections)
        if showplot:
            self.axplot.ShowPlot()
        if saveplot:
            self.axplot.SavePlot('AxionElectron_' + plottype)

    # ==============================================================================#
    # which lines & regions to plot here...
    #
    def PlotData(self, plottype, projections=False):
        for item in ['QCDband', 'DFSZ1_starhint', 'DFSZ2_starhint', 'AJ23_starhint',
                     'AJ53_starhint', 'AJ83_starhint', 'CAST_gae']:
            self.axionDB[item].DrawItem(self.axplot)

        if projections:
            for item in ['IAXO_gae', 'IAXOplus_gae', 'IAXO_gae_l', 'IAXOplus_gae_l']:
                self.axionDB[item].DrawItem(self.axplot)

    # ==============================================================================#
    # which labels to include in plot...
    #
    def PlotLabels(self, plottype, projections=False):
        plt.text(2e-4, 1.2e-11, r'{\bf CAST}', color="white", size=12)

        if projections:
            plt.text(2e-4, 6e-13, r'{\bf IAXO}', color="black", size=12)
            plt.text(2e-4, 3.2e-13, 'IAXO+', color="black", size=11)


# ==============================================================================#
# build a data base (dictionary) with all axion data (sensitivity/exclusion
# lines, etc.) for plots
#
def BuildDB():
    db = {}
    path = "data/axion/"
    db['qcdband'] = ExPltItem("qcdband", "band", path + "QCD_band.dat", facecolor="yellow")
    db['ksvz'] = ExPltItem("ksvz", "region", path + "ksvz.dat", facecolor="white", edgecolor="orange", linewidth=1)
    db['dfsz'] = ExPltItem("dfsz", "region", path + "dfsz.dat", facecolor="white", edgecolor="orange", linewidth=1)

    db['old_haloscopes'] = ExPltItem("old_haloscopes", "band", path + "MicrowaveCavities.txt", facecolor="limegreen",
                                     edgecolor="darkgreen", linewidth=0.2)
    db['admx'] = ExPltItem("admx", "band", path + "admx.txt", facecolor="limegreen", edgecolor="darkgreen",
                           linewidth=0.2)
    db['admx_hf_2016'] = ExPltItem("haystack", "band", path + "admx_hf_2016.dat", facecolor="limegreen",
                                   edgecolor="darkgreen", linewidth=0.2)
    db['ADMX2018'] = ExPltItem("ADMX2018", "band", path + "ADMX2018.txt", facecolor="limegreen", edgecolor="darkgreen",
                               linewidth=0.2)
    db['ADMX2019'] = ExPltItem("ADMX2019", "band", path + "ADMX2019.dat", facecolor="limegreen", edgecolor="darkgreen",
                               linewidth=0.2)
    # these two should become obsolete...
    db['ADMX2019_1'] = ExPltItem("ADMX2019_1", "band", path + "ADMX2019_1.txt", facecolor="limegreen",
                                 edgecolor="darkgreen", linewidth=0.2)
    db['ADMX2019_2'] = ExPltItem("ADMX2019_2", "band", path + "ADMX2019_2.txt", facecolor="limegreen",
                                 edgecolor="darkgreen", linewidth=0.2)

    db['ADMX_sidecar'] = ExPltItem("ADMX_sidecar", "band", path + "ADMX_sidecar.txt", facecolor="limegreen",
                                   edgecolor="darkgreen", linewidth=0.2)
    db['ADMX2021'] = ExPltItem("ADMX2021","band", path+"ADMX2021.txt",facecolor="limegreen",edgecolor="darkgreen",linewidth=0.2)
    db['CAPP-8TB'] = ExPltItem("CAPP-8TB", "band", path + "CAPP-8TB.txt", facecolor="limegreen", edgecolor="darkgreen",
                               linewidth=0.2)
    db['CAPP_multicell'] = ExPltItem("CAPP_multicell_2020", "band", path + "CAPP_multicell_2020.dat",
                                     facecolor="limegreen", edgecolor="darkgreen", linewidth=0.2)
    db['CAPP2021'] = ExPltItem("CAPP2021", "band", path + "CAPP2021.txt", facecolor="limegreen", edgecolor="darkgreen",
                               linewidth=0.2)
    db['HAYSTAC'] = ExPltItem("HAYSTAC", "band", path + "HAYSTAC.txt", facecolor="limegreen", edgecolor="darkgreen",
                              linewidth=0.2)
    db['HAYSTAC2020'] = ExPltItem("haystack2020", "band", path + "haystac2020.txt", facecolor="limegreen",
                                  edgecolor="darkgreen", linewidth=0.2)
    db['ORGAN'] = ExPltItem("ORGAN", "band", path + "ORGAN.txt", facecolor="limegreen", edgecolor="darkgreen",
                            linewidth=0.2)
    db['QUAX'] = ExPltItem("QUAX", "band", path + "QUAX.txt", facecolor="limegreen", edgecolor="darkgreen",
                           linewidth=0.2)
    db['QUAX2021'] = ExPltItem("QUAX", "band", path + "QUAX2021.txt", facecolor="limegreen", edgecolor="darkgreen",
                               linewidth=0.2)
    db['RADES2021'] = ExPltItem("RADES2021", "band", path + "RADES2021.txt", facecolor="limegreen",
                                edgecolor="darkgreen", linewidth=0.2)

    db['ABRA10cm'] = ExPltItem("ABRA10cm", "band", path + "ABRA10cm.txt", facecolor="limegreen", edgecolor="darkgreen",
                               linewidth=0.5, alpha=0.5)
    db['ABRA_2021'] = ExPltItem("ABRA_2021", "band", path + "ABRA_2021.txt", facecolor="limegreen",
                                edgecolor="darkgreen", linewidth=0.5, alpha=0.5)
    db['BASE_2021'] = ExPltItem("BASE2021", "band", path + "BASE2021.txt", facecolor="limegreen", edgecolor="darkgreen",
                                linewidth=0.5, alpha=0.5)
    db['ADMX_SLIC'] = ExPltItem("ADMX_SLIC", "band", path + "ADMX_SLIC.txt", facecolor="limegreen",
                                edgecolor="darkgreen", linewidth=0.5, alpha=0.5)

    db['SHAFT'] = ExPltItem("SHAFT", "band", path + "SHAFT.txt", facecolor="limegreen", edgecolor="darkgreen",
                            linewidth=0.5, alpha=0.5)

    db['hess'] = ExPltItem('HESS', 'band', path + 'hess.dat', facecolor="lightseagreen", edgecolor="darkgreen",
                           linewidth=0.5)
    db['mrk421'] = ExPltItem('mrk421', 'band', path + 'Mrk421.txt', facecolor="mediumturquoise", edgecolor="darkgreen",
                             linewidth=0.5, alpha=0.6)
    db['sn1987a_photon'] = ExPltItem('sn1987a_photon', 'band', path + 'sn1987a_photon.dat', facecolor="turquoise",
                                     edgecolor="darkgreen", linewidth=0.5)
    db['FERMI_NG1275'] = ExPltItem("FERMI_NG1275_region", 'region', path + "FERMI_NG1275_region.dat",
                                   facecolor="mediumturquoise", edgecolor="darkgreen", linewidth=0.5, alpha=0.6)

    db['SN1987energyloss'] = ExPltItem('SN1987energyloss', 'band', path + 'cosmoalp/SN1987energyloss.txt',
                                       facecolor="lightgreen", edgecolor="green", linewidth=0.5)
    db['Xray'] = ExPltItem('Xray', 'band', path + 'cosmoalp/Xray.txt', facecolor="green", edgecolor="darkgreen",
                           linewidth=0.5)
    db['Deut2016'] = ExPltItem('Deut2016', 'region', path + 'cosmoalp/Deut2016.txt', facecolor="limegreen",
                               edgecolor="darkgreen", linewidth=0.5)
    db['OpticalDepthTerm'] = ExPltItem('OpticalDepthTerm', 'band', path + 'cosmoalp/OpticalDepthTerm.txt',
                                       facecolor="yellowgreen", edgecolor="green", linewidth=0.5)
    db['gEBL1'] = ExPltItem('gEBL1', 'band', path + 'cosmoalp/gEBL1.txt', facecolor="lightgreen", edgecolor="green",
                            linewidth=0.5)
    db['EBL2'] = ExPltItem('EBL2', 'region', path + 'cosmoalp/EBL2.txt', facecolor="limegreen", edgecolor="darkgreen",
                           linewidth=0.5)
    db['cmb_mu'] = ExPltItem('cmb_mu', 'region', path + 'cosmoalp/CMB_mu.txt', facecolor="green", edgecolor="darkgreen",
                             linewidth=0.5)
    db['CMB_DEsuE'] = ExPltItem('CMB_DEsuE', 'band', path + 'cosmoalp/CMB_DEsuE.txt', facecolor="forestgreen",
                                edgecolor="darkgreen", linewidth=0.5)
    db['Overduin'] = ExPltItem('Overduin', 'region', path + 'cosmoalp/Overduin.txt', facecolor="lightgreen",
                               edgecolor="green", linewidth=0.5)
    db['Ressell'] = ExPltItem('Ressell', 'band', path + 'cosmoalp/Ressell.txt', facecolor="lightgreen",
                              edgecolor="green", linewidth=0.5)
    db['endlist2_gamma_projimprov'] = ExPltItem("endlist2_gamma_projimprov", "band",
                                                path + "endlist2_gamma_projimprov.txt", facecolor="gray",
                                                edgecolor="black", linewidth=0.5)

    db['telescopes'] = ExPltItem("telescopes", "band", path + "telescopes.dat", facecolor="green",
                                 edgecolor="darkgreen", linewidth=0.5)
    db['telescopes_new'] = ExPltItem("telescopes_new", "band", path + "telescopes_new.dat", facecolor="green",
                                     edgecolor="darkgreen", linewidth=0.5)

    db['HBalpbound'] = ExPltItem('HBalpbound', 'band', path + 'HBalpbound.txt', facecolor="skyblue", edgecolor="blue",
                                 linewidth=0.5)
    db['HBalpbound_l'] = ExPltItem('HBalpbound_l', 'line', path + 'HBalpbound.txt', color="blue", linewidth=0.5)
    db['solar_nu'] = ExPltItem('solar_nu', 'band', path + 'ALPSun_nu.txt', facecolor="steelblue", edgecolor="blue",
                               linewidth=0.5)

    db['CAST'] = ExPltItem('CAST', 'band', path + 'cast_env_2016.dat', facecolor="deepskyblue", edgecolor="blue",
                           linewidth=0.5)

    db['CROWS'] = ExPltItem("CROWS", "band", path + "CROWS.txt", facecolor="gray", edgecolor="white", linewidth=0.5)
    db['ALPSI'] = ExPltItem("ALPSI", "band", path + "ALPSI.dat", facecolor="gray", edgecolor="white", linewidth=0.5)
    db['OSCAR2015'] = ExPltItem('OSCAR2015', 'band', path + 'osqar2015.dat', facecolor="gray", edgecolor="black",
                                linewidth=0.5)
    db['PVLAS2015'] = ExPltItem('PVLAS2015', 'band', path + 'pvlas2015.dat', facecolor="gray", edgecolor="black",
                                linewidth=0.5)
    db['BeamDump'] = ExPltItem('BeamDump', 'region', path + 'llSLAC137.txt', facecolor="gray", edgecolor="black",
                               linewidth=0.5)

    # projecions
    db['BabyIAXO'] = ExPltItem('BAbyIAXO', 'band', path + 'miniIAXO.dat', facecolor="deepskyblue", linewidth=0.5,
                               alpha=0.1, linestyle="-")
    db['IAXO'] = ExPltItem('IAXO', 'band', path + 'IAXO_nominal.txt', facecolor="deepskyblue", linewidth=0.5, alpha=0.1,
                           linestyle="-")
    db['IAXOplus'] = ExPltItem('IAXOplus', 'band', path + 'IAXO_plus.txt', facecolor="deepskyblue", linewidth=0.5,
                               alpha=0.1, linestyle="-")
    db['ALPSII'] = ExPltItem('ALPSII', 'band', path + 'ALPSII.dat', facecolor="gray", linewidth=0.5, alpha=0.2,
                             linestyle=":")
    db['ORGANprosp'] = ExPltItem('ORGANprosp', 'line', path + 'ORGAN2.dat', color="darkgreen", linewidth=0.1,
                                 linestyle="-")
    db['castcapp2'] = ExPltItem('castcapp2', 'band', path + 'CASTCAPP2.dat', facecolor="limegreen", edgecolor="black",
                                linewidth=0.1, alpha=0.1, linestyle="-")
    db['CAPP4'] = ExPltItem('CAPP4', 'line', path + 'CAPP4.dat', color="darkgreen", linewidth=0.1, linestyle="-")
    db['MADMAX'] = ExPltItem('MADMAX', 'band', path + 'MADMAX.dat', facecolor="limegreen", edgecolor="black",
                             linewidth=0.1, alpha=0.1, linestyle="-")
    db['ADMXprosp_2GHz'] = ExPltItem('ADMXprosp_2GHz', 'band', path + 'ADMX_prospects_2GHz.dat', facecolor="limegreen",
                                     edgecolor="black", linewidth=0.1, alpha=0.1, linestyle="-")
    db['ADMXprosp_10GHz'] = ExPltItem('ADMXprosp_10GHz', 'band', path + 'ADMX_prospects_10GHz.dat',
                                      facecolor="limegreen", edgecolor="black", linewidth=0.1, alpha=0.1, linestyle="-")
    db['ABRA1'] = ExPltItem('ABRA1', 'band', path + 'ABRAres_1.dat', facecolor="limegreen", edgecolor="black",
                            linewidth=0.1, alpha=0.1, linestyle="-")
    db['ABRA1_l'] = ExPltItem('ABRA1', 'line', path + 'ABRAres_1.dat', color="green", linewidth=0.1, linestyle="-")
    db['ABRA2'] = ExPltItem('ABRA2', 'line', path + 'ABRAres_2.dat', color="green", linewidth=0.1, linestyle="-")
    db['ABRA3'] = ExPltItem('ABRA3', 'line', path + 'ABRAres_3.dat', color="green", linewidth=0.1, linestyle="-")
    db['KLASH'] = ExPltItem('KLASH', 'line', path + 'KLASH.dat', color="green", linewidth=0.1, linestyle="-")
    db['TOORAD'] = ExPltItem('TOORAD', 'line', path + 'TOORAD2.txt', color="green", linewidth=0.1, linestyle="-")
    db['BRASS'] = ExPltItem("BRASS", "line", path + "BRASS.txt", color="green", linewidth=0.1, linestyle="-")
    db['IAXODM'] = ExPltItem('IAXODM.dat', 'band', path + 'IAXODM.dat', facecolor="limegreen", edgecolor="black",
                             linewidth=0.1, alpha=0.1, linestyle="-")
    db['STAX1'] = ExPltItem('STAX1', 'line', path + 'STAX1.dat', color="black", linewidth=0.2, linestyle="-.")
    db['STAX2'] = ExPltItem('STAX2', 'line', path + 'STAX2.dat', color="black", linewidth=0.2, linestyle="-.")

    # "only_line" versions
    db['BabyIAXO_l'] = ExPltItem('BAbyIAXO', 'line', path + 'miniIAXO.dat', color="black", linewidth=0.6, alpha=1,
                                 linestyle="--")
    db['IAXO_l'] = ExPltItem('IAXO', 'line', path + 'IAXO_nominal.txt', color="black", linewidth=0.6, alpha=1,
                             linestyle="--")
    db['IAXOplus_l'] = ExPltItem('IAXOplus', 'line', path + 'IAXO_plus.txt', color="black", linewidth=0.6, alpha=1,
                                 linestyle="--")
    db['ALPSII_l'] = ExPltItem('ALPSII', 'line', path + 'ALPSII.dat', color="black", linewidth=0.5, alpha=1,
                               linestyle=":")
    db['CAPP4_l'] = ExPltItem('ORGANprosp', 'line', path + 'CAPP4.dat', color="darkgreen", linewidth=0.1, alpha=1,
                              linestyle="--")
    db['MADMAX_l'] = ExPltItem('MADMAX', 'line', path + 'MADMAX.dat', color="darkgreen", linewidth=0.3, alpha=1,
                               linestyle="--")
    db['ADMXprosp_2GHz_l'] = ExPltItem('ADMXprosp_2GHz', 'line', path + 'ADMX_prospects_2GHz.dat', color="darkgreen",
                                       linewidth=0.3, alpha=1, linestyle="--")
    db['ADMXprosp_10GHz_l'] = ExPltItem('ADMXprosp_10GHz', 'line', path + 'ADMX_prospects_10GHz.dat', color="darkgreen",
                                        linewidth=0.3, alpha=1, linestyle="--")
    db['ABRA1_l'] = ExPltItem('ABRA1', 'line', path + 'ABRAres_1.dat', color="darkgreen", linewidth=0.1, alpha=1,
                              linestyle="--")
    db['ABRA_2021_l'] = ExPltItem('ABRA_2021', 'line', path + 'ABRA_2021.txt', color="darkgreen", linewidth=0.1,
                                  alpha=1, linestyle="--")
    db['KLASH_l'] = ExPltItem('KLASH', 'line', path + 'KLASH.dat', color="darkgreen", linewidth=0.1, alpha=1,
                              linestyle="--")
    db['IAXODM_l'] = ExPltItem('IAXODM.dat', 'line', path + 'ORGAN2.dat', color="darkgreen", linewidth=0.1, alpha=1,
                               linestyle="--")
    db['AMELIE'] = ExPltItem('AMELIE', 'line', path + 'amelie_1m3_arXiv_1508.03006.txt', color="gray", linewidth=0.6, alpha=1,
                               linestyle="--")

    db['JURA'] = ExPltItem('JURA', 'line', path + 'ALPSIII.dat', color="black", linewidth=0.5, alpha=1, linestyle=":")

    # hints
    db['THintMayer'] = ExPltItem('THintMayer', 'region', path + 'Mayer_2013.dat', facecolor='yellow',
                                 edgecolor="orange", linewidth=0.5)
    db['THintCIBER'] = ExPltItem('THintCIBER', 'region', path + 'CIBER_contour_data.dat', facecolor='yellow',
                                 edgecolor="orange", linewidth=0.5)
    mpl.rcParams['hatch.linewidth'] = 0.1
    db['HBhint'] = ExPltItem('HBhint', 'region', path + 'hints/HB_hint.dat', facecolor='none', edgecolor='orangered',
                             linewidth=0.3, linestyle='-', hatch='////')

    return db


# ==============================================================================#
# renormalize data, to plot C_ag instead of g_ag
#
def RenormItem(item):
    for i in range(len(item.data)):
        # print(item.name)
        item.data[i, 1] = item.data[i, 1] / item.data[i, 0] * 5.172e9
        # print(item.data[i,0],item.data[i,1])
        # C_ag = g_ag / m_a * 5.172e9


# ==============================================================================#
# build a data base (dictionary) with all axion data (sensitivity/exclusion
# lines, etc.) for plots
#
def BuildGaeDB():
    db = {}

    path = "data/axion/hints/"
    db['DFSZ1_starhint'] = ExPltItem("DFSZ1_starhint", "region",
                                     path + "DFSZ1_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat",
                                     facecolor="springgreen", edgecolor="darkgreen", alpha=0.2)
    db['DFSZ2_starhint'] = ExPltItem("DFSZ2_starhint", "region",
                                     path + "DFSZ2_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat",
                                     facecolor="lime", edgecolor="darkgreen", alpha=0.2)
    db['AJ23_starhint'] = ExPltItem("AJ23_starhint", "region",
                                    path + "AJ23_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat",
                                    facecolor="orange", edgecolor="red", alpha=0.2)
    db['AJ53_starhint'] = ExPltItem("AJ53_starhint", "region",
                                    path + "AJ53_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat",
                                    facecolor="yellow", edgecolor="orange", alpha=0.2)
    db['AJ83_starhint'] = ExPltItem("AJ83_starhint", "region",
                                    path + "AJ83_ABC_dominant_No_SN_2sigma_hint_rootgaegag_vs_ma.dat", facecolor="red",
                                    edgecolor="red", alpha=0.2)

    path = "data/axion/gaegag/"
    db['QCDband'] = ExPltItem("QCDband", "band", path + "DFSZband_gaegag.dat", facecolor="lemonchiffon",
                              edgecolor="none", linewidth=1)
    # db['BabyIAXO'] = ExPltItem("BabyIAXO","band",path+"miniIAXO_gae_gag.dat",facecolor="white",edgecolor="orange",linewidth=1)
    db['IAXO_gae'] = ExPltItem("IAXO", "band", path + "sqrtgaagae_sc2.dat", facecolor="skyblue", edgecolor="black",
                               linewidth=0.5, alpha=0.3)
    db['IAXOplus_gae'] = ExPltItem("IAXOplus", "band", path + "sqrtgaagae_sc3.dat", facecolor="skyblue",
                                   edgecolor="black", linewidth=0.5, alpha=0.3)
    db['CAST_gae'] = ExPltItem("CAST", "band", path + "CAST_gae_gagg.dat", facecolor="steelblue", edgecolor="darkblue",
                               linewidth=0.5)
    db['IAXO_gae_l'] = ExPltItem("IAXO", "line", path + "sqrtgaagae_sc2.dat", color="black", linewidth=0.5,
                                 linestyle='--')
    db['IAXOplus_gae_l'] = ExPltItem("IAXOplus", "line", path + "sqrtgaagae_sc3.dat", color="black", linewidth=0.5,
                                     linestyle='--')

    return db

    # db['cooling_hint'] = ExPltItem("qcdband","band",path+"cooling_hint_gae_gag.dat",facecolor="yellow")
    # db['BabyIAXO'] = ExPltItem("ksvz","band",path+"miniIAXO_gae_gag.dat",facecolor="white",edgecolor="orange",linewidth=1)
    # db['IAXO'] = ExPltItem("IAXO","band", path+"IAXO_gae_gag.dat",facecolor="skyblue",edgecolor="black",linewidth=0.2,alpha=0.3)
    # db['IAXOplus'] = ExPltItem("IAXOplus","band", path+"IAXO_plus_gae_gag.dat",facecolor="skyblue",edgecolor="black",linewidth=0.2,alpha=0.3)
    # db['CAST'] = ExPltItem("CAST","band", path+"CAST_gae_vs_gag.dat",facecolor="steelblue",edgecolor="darkblue",linewidth=0.2)

    # <addPlotLine name="cooling_hint" file="cooling_hint_gae_gag.dat" active="on"
    #                   fill="1" fillcolor="kOrange" linewidth="1" linecolor="kYellow" drawoption="FL" />
    # <addPlotLine name="BabyIAXO" file="miniIAXO_gae_gag.dat" active="on"
    #           fill="1" fillcolor="kAzure+6" linewidth="2" linecolor="kBlack" style="7" alpha="0.3" drawoption="FL" />
    # <addPlotLine name="IAXO2" file="IAXO_gae_gag.dat" active="on"
    #              fill="1" fillcolor="kAzure+6" linewidth="2" linecolor="kBlack" style="7" alpha="0.2" drawoption="FL" />
    # <addPlotLine name="IAXO3" file="IAXO_plus_gae_gag.dat" active="on"
    #              fill="1" fillcolor="kAzure+6" linewidth="2" linecolor="kBlack" style="7" alpha="0.3" drawoption="FL" />
    # <addPlotLine name="CAST_gae_vs_gag" file="CAST_gae_vs_gag.dat" active="on"
    #            fill="1" fillcolor="kAzure-8" linewidth="1" linecolor="kBlue"  drawoption="FL" />
