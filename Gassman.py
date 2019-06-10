
import math
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
# from Wavelets import WaveletGenerator


######### CONSTANTS ######
# Calculating Voight Reuss Mixing

# Calculation method. User can only choose Gardner, Castagna_1, or Castagna_2
def getGraph(calculation_method, SP_shale_cutoff, K0_quartz, K0_plag_feldspar, K0_dolomite, K0_clay, Percent_quartz, Percent_plag_feldspar, Percent_dolomite, Percent_clay, K_brine, K_gas, rho_brine, rho_gas, Sw, Porosity, rhob_rock, grain_density, Vp_rock, Vs_rock, csv_file, wavelet_type, freq, dt):
    calculation_method = calculation_method

    K0_quartz = K0_quartz # 37
    K0_plag_feldspar = K0_plag_feldspar # 75.6
    K0_dolomite = K0_dolomite # 94.9
    K0_clay = K0_clay # 25

    # Calculating Minteralogy K Matrix
    # Assuming the mineralogy is 72% Quartz, 15% Plag Feldspar, 5% Dolomite, 8% Clay
    Percent_quartz = Percent_quartz # 0.72
    Percent_plag_feldspar = Percent_plag_feldspar # 0.15
    Percent_dolomite = Percent_dolomite # 0.05
    Percent_clay = Percent_clay # 0.08

    # Fluid Properties
    K_brine = K_brine # 3.1
    K_gas = K_gas # 0.25
    rho_brine = rho_brine # 1
    rho_gas = rho_gas # 0.25
    Sw = Sw # 1

    # Rock Properties

    Porosity = Porosity # 19.4
    rhob_rock = rhob_rock # 2.33
    grain_density = grain_density # 2.65
    Vp_rock = Vp_rock*3048 # 11437
    Vs_rock = Vs_rock*3048 # 5908

    SP_shale_cutoff = SP_shale_cutoff # -0.50

    ######## END OF CONSTANTS

    depth = []
    SP = []
    ILD = []
    DT = []
    GR = []
    DT_edited = []
    Vp_fts = []      # primary velocity in ft/sec
    Vp_kms = []      # primary velocity in km/sec
    bulk_density_gardner = []
    density_castagna_1 = []
    density_castagna_2 = []
    Vs_Greenburg_Cast = []
    Shear_Modulus_G = []
    Shear_Modulus_Castagna_1 = []
    Shear_Modulus_Castagna_2 = []
    Bulk_Modulus_Gardner = []
    Bulk_Modulus_Castagna_1 = []
    Bulk_Modulus_Castagna_2 = []

    index = 0

    if csv_file is None:
        with open('Texaco_Wilcox_original.csv',newline='') as csvfile:
            f = csv.reader(csvfile,delimiter=',', quotechar='|')
            for row in f:
                if index == 0:
                    index = 1
                else:
                    index += 1
                    #print(index)
                    if index > 0 and index < 30000:
                        depth.append(float(row[0]))
                        SP.append(float(row[1]))
                        #ILD.append(float(row[2]))
                        #DT.append(float(row[3]))
                        #GR.append(float(row[4]))
                        DT_edited.append(float(row[2]))
    else:
        print(csv_file)
        f = csv.reader(csv_file,delimiter=',', quotechar='|')
        for row in f:
            if index == 0:
                index = 1
            else:
                index += 1
                if index > 0 and index < 30000:
                    depth.append(float(row[0]))
                    SP.append(float(row[1]))
                    DT_edited.append(float(row[2]))

    for x in DT_edited:
        Vp_fts.append((1/x)*1000000) # calculate the primary velocity in ft/s
        Vp_kms.append(((1/x)*1000000)*0.0003048) # calculate the primary velocity in km/s

    for x in Vp_fts:
        bulk_density_gardner.append(0.23 * (x**0.25))

    depth_indexed = list(enumerate(depth))

    for x in depth_indexed:
        if SP[x[0]]<SP_shale_cutoff:
            #sand
            density_castagna_1.append(-0.0115 * (Vp_kms[x[0]] ** 2) + 0.261 * Vp_kms[x[0]] + 1.515)
            density_castagna_2.append(1.66 * (Vp_kms[x[0]] ** 0.261))
            Vs_Greenburg_Cast.append(0.7697*(Vp_kms[x[0]])-0.8673)
            Shear_Modulus_G.append(bulk_density_gardner[x[0]] * (Vs_Greenburg_Cast[x[0]] ** 2))
            Shear_Modulus_Castagna_1.append((Vs_Greenburg_Cast[x[0]]**2)*density_castagna_1[x[0]])
            Shear_Modulus_Castagna_2.append((Vs_Greenburg_Cast[x[0]] ** 2) * density_castagna_2[x[0]])
            Bulk_Modulus_Gardner.append(bulk_density_gardner[x[0]] * (Vp_kms[x[0]] ** 2) - (4 / 3) * Shear_Modulus_G[x[0]])
            Bulk_Modulus_Castagna_1.append(density_castagna_1[x[0]]*(Vp_kms[x[0]]**2)-(4/3)*Shear_Modulus_Castagna_1[x[0]])
            Bulk_Modulus_Castagna_2.append(density_castagna_2[x[0]]*(Vp_kms[x[0]]**2)-(4/3)*Shear_Modulus_Castagna_2[x[0]])
        else:
            #shale
            density_castagna_1.append(-0.0261 * (Vp_kms[x[0]] ** 2) + 0.373 * Vp_kms[x[0]] + 1.458)
            density_castagna_2.append(1.75 * (Vp_kms[x[0]] ** 0.265))
            Vs_Greenburg_Cast.append(0.8042*(Vp_kms[x[0]])-0.8559)
            Shear_Modulus_G.append(bulk_density_gardner[x[0]]*(Vs_Greenburg_Cast[x[0]]**2))
            Shear_Modulus_Castagna_1.append((Vs_Greenburg_Cast[x[0]] ** 2) * density_castagna_1[x[0]])
            Shear_Modulus_Castagna_2.append((Vs_Greenburg_Cast[x[0]] ** 2) * density_castagna_2[x[0]])
            Bulk_Modulus_Gardner.append(bulk_density_gardner[x[0]] * (Vp_kms[x[0]] ** 2) - (4 / 3) * Shear_Modulus_G[x[0]])
            Bulk_Modulus_Castagna_1.append(density_castagna_1[x[0]] * (Vp_kms[x[0]] ** 2) - (4 / 3) * Shear_Modulus_Castagna_1[x[0]])
            Bulk_Modulus_Castagna_2.append(density_castagna_2[x[0]] * (Vp_kms[x[0]] ** 2) - (4 / 3) * Shear_Modulus_Castagna_2[x[0]])




    # Calculating Reuss_Voight Mixing
    K_matrix_Reuss = 1 / (Percent_quartz/K0_quartz + Percent_plag_feldspar/K0_plag_feldspar + Percent_dolomite/K0_dolomite + Percent_clay/K0_clay )
    K_matrix_Voight = (Percent_quartz*K0_quartz + Percent_plag_feldspar*K0_plag_feldspar + Percent_dolomite*K0_dolomite + Percent_clay*K0_clay )
    K_matrix_YRH = 0.5 * (K_matrix_Voight+K_matrix_Reuss)


    def K_fluid(Sw):
        return (Sw / K_brine + (1-Sw)/K_gas )**-1

    def rho_fluid(Sw):
        return (Sw*rho_brine+(1-Sw)*rho_gas)




    rhob_dry = grain_density*(1-(Porosity/100))
    def rhob(rho_fluid_var):
        return (rhob_dry+Porosity/100*rho_fluid_var)

    K_star_Gardner = []
    K_star_Castagna_1 = []
    K_star_Castagna_2 = []
    Ksat_Gardner_0SW = []
    Ksat_Gardner_20SW = []
    Ksat_Gardner_40SW = []
    Ksat_Gardner_50SW = []
    Ksat_Gardner_60SW = []
    Ksat_Gardner_80SW = []
    Ksat_Gardner_100SW = []
    Ksat_Castagna_1_0SW = []
    Ksat_Castagna_1_20SW = []
    Ksat_Castagna_1_40SW = []
    Ksat_Castagna_1_50SW = []
    Ksat_Castagna_1_60SW = []
    Ksat_Castagna_1_80SW = []
    Ksat_Castagna_1_100SW = []
    Ksat_Castagna_2_0SW = []
    Ksat_Castagna_2_20SW = []
    Ksat_Castagna_2_40SW = []
    Ksat_Castagna_2_50SW = []
    Ksat_Castagna_2_60SW = []
    Ksat_Castagna_2_80SW = []
    Ksat_Castagna_2_100SW = []
    Vp_Gardner_0SW = []
    Vp_Gardner_20SW = []
    Vp_Gardner_40SW = []
    Vp_Gardner_50SW = []
    Vp_Gardner_60SW = []
    Vp_Gardner_80SW = []
    Vp_Gardner_100SW = []
    Vp_Castagna_1_0SW = []
    Vp_Castagna_1_20SW = []
    Vp_Castagna_1_40SW = []
    Vp_Castagna_1_50SW = []
    Vp_Castagna_1_60SW = []
    Vp_Castagna_1_80SW = []
    Vp_Castagna_1_100SW = []
    Vp_Castagna_2_0SW = []
    Vp_Castagna_2_20SW = []
    Vp_Castagna_2_40SW = []
    Vp_Castagna_2_50SW = []
    Vp_Castagna_2_60SW = []
    Vp_Castagna_2_80SW = []
    Vp_Castagna_2_100SW = []

    Vs_Gardner_0SW = []
    Vs_Gardner_20SW = []
    Vs_Gardner_40SW = []
    Vs_Gardner_50SW = []
    Vs_Gardner_60SW = []
    Vs_Gardner_80SW = []
    Vs_Gardner_100SW = []
    Vs_Castagna_1_0SW = []
    Vs_Castagna_1_20SW = []
    Vs_Castagna_1_40SW = []
    Vs_Castagna_1_50SW = []
    Vs_Castagna_1_60SW = []
    Vs_Castagna_1_80SW = []
    Vs_Castagna_1_100SW = []
    Vs_Castagna_2_0SW = []
    Vs_Castagna_2_20SW = []
    Vs_Castagna_2_40SW = []
    Vs_Castagna_2_50SW = []
    Vs_Castagna_2_60SW = []
    Vs_Castagna_2_80SW = []
    Vs_Castagna_2_100SW = []

    class Ksat:
        def __init__(self, K_star, K_matrix, Porosity, K_fluid):
            self.K_star = K_star
            self.K_matrix = K_matrix
            self.Porosity = Porosity
            self.K_fluid = K_fluid

        def calc_Ksat(self):
            K_sat = []
            for x in self.K_star:
                K_sat.append((((1 - x / self.K_matrix) ** 2) / (self.Porosity / 100 / self.K_fluid + (
                            1 - self.Porosity / 100) / self.K_matrix - x / self.K_matrix ** 2)) + x)
            self.Ksat = K_sat

    class Vp:
        def __init__(self, Ksat, Shear_Modulus, rhob, Porosity, rho_fluid):
            self.Ksat = Ksat
            self.Shear_Modulus = Shear_Modulus
            self.rhob = rhob
            self.Porosity = Porosity
            self.rho_fluid = rho_fluid

        def calc_Vp(self):
            Vp = []
            Vp_kms = []
            for counter, x in enumerate(self.Ksat):
                if 1000 * ((self.Ksat[counter] + 4 / 3 * self.Shear_Modulus[counter]) / (
                        self.rhob + self.Porosity / 100 * self.rho_fluid)) < 0:
                    # print(counter)
                    # print('The type should be complex')
                    Vp.append(3000)
                    Vp_kms.append(3)
                    # Vp.append(3280.83*((self.Ksat[counter-50]+4/3*self.Shear_Modulus[counter-50])/(self.rhob+self.Porosity/100*self.rho_fluid))**0.5)
                    # print(type(3280.83*((self.Ksat[counter-1]+4/3*self.Shear_Modulus[counter-1])/(self.rhob+self.Porosity/100*self.rho_fluid))**0.5))
                else:
                    Vp.append(1000 * ((self.Ksat[counter] + 4 / 3 * self.Shear_Modulus[counter]) / (
                                self.rhob + self.Porosity / 100 * self.rho_fluid)) ** 0.5)
                    Vp_kms.append(((self.Ksat[counter] + 4 / 3 * self.Shear_Modulus[counter]) / (
                                self.rhob + self.Porosity / 100 * self.rho_fluid)) ** 0.5)
                    # print(counter)
                    # print('The type should be float')
                    # print(type(3280.83*((self.Ksat[counter]+4/3*self.Shear_Modulus[counter])/(self.rhob+self.Porosity/100*self.rho_fluid))**0.5))
            self.Vp = Vp
            self.Vp_kms = Vp_kms

    class Vs:
        def __init__(self, Shear_Modulus, rhob, Porosity, rho_fluid):
            self.Shear_Modulus = Shear_Modulus
            self.rhob = rhob
            self.Porosity = Porosity
            self.rho_fluid = rho_fluid

        def calc_Vs(self):
            Vs = []
            Vs_kms = []
            for x in self.Shear_Modulus:
                Vs.append(1000 * (x / (self.rhob + self.Porosity / 100 * self.rho_fluid)) ** 0.5)
                Vs_kms.append((x / (self.rhob + self.Porosity / 100 * self.rho_fluid)) ** 0.5)
            self.Vs = Vs
            self.Vs_kms = Vs_kms

    for counter, x in enumerate(Bulk_Modulus_Gardner):
        K_star_Gardner.append((x * (Porosity / 100 * K_matrix_YRH / K_fluid(1) + 1 - Porosity / 100) - K_matrix_YRH) / (
                    Porosity / 100 * K_matrix_YRH / K_fluid(1) + x / Vp_rock - 1 - Porosity / 100))

    Ksat_Gardner_0SW = Ksat(K_star_Gardner, K_matrix_YRH, Porosity, K_fluid(0))
    Ksat_Gardner_0SW.calc_Ksat()
    Ksat_Gardner_20SW = Ksat(K_star_Gardner, K_matrix_YRH, Porosity, K_fluid(0.2))
    Ksat_Gardner_20SW.calc_Ksat()
    Ksat_Gardner_40SW = Ksat(K_star_Gardner, K_matrix_YRH, Porosity, K_fluid(0.4))
    Ksat_Gardner_40SW.calc_Ksat()
    Ksat_Gardner_50SW = Ksat(K_star_Gardner, K_matrix_YRH, Porosity, K_fluid(0.5))
    Ksat_Gardner_50SW.calc_Ksat()
    Ksat_Gardner_60SW = Ksat(K_star_Gardner, K_matrix_YRH, Porosity, K_fluid(0.6))
    Ksat_Gardner_60SW.calc_Ksat()
    Ksat_Gardner_80SW = Ksat(K_star_Gardner, K_matrix_YRH, Porosity, K_fluid(0.8))
    Ksat_Gardner_80SW.calc_Ksat()
    Ksat_Gardner_100SW = Ksat(K_star_Gardner, K_matrix_YRH, Porosity, K_fluid(1))
    Ksat_Gardner_100SW.calc_Ksat()

    Vp_Gardner_0SW = Vp(Ksat_Gardner_0SW.Ksat, Shear_Modulus_G, rhob(rho_fluid(0)), Porosity, rho_fluid(0))
    Vp_Gardner_0SW.calc_Vp()
    Vp_Gardner_20SW = Vp(Ksat_Gardner_20SW.Ksat, Shear_Modulus_G, rhob(rho_fluid(0.2)), Porosity, rho_fluid(0.2))
    Vp_Gardner_20SW.calc_Vp()
    Vp_Gardner_40SW = Vp(Ksat_Gardner_40SW.Ksat, Shear_Modulus_G, rhob(rho_fluid(0.4)), Porosity, rho_fluid(0.4))
    Vp_Gardner_40SW.calc_Vp()
    Vp_Gardner_50SW = Vp(Ksat_Gardner_50SW.Ksat, Shear_Modulus_G, rhob(rho_fluid(0.5)), Porosity, rho_fluid(0.5))
    Vp_Gardner_50SW.calc_Vp()
    Vp_Gardner_60SW = Vp(Ksat_Gardner_60SW.Ksat,Shear_Modulus_G,rhob(rho_fluid(0.6)),Porosity,rho_fluid(0.6))
    Vp_Gardner_60SW.calc_Vp()
    Vp_Gardner_80SW = Vp(Ksat_Gardner_80SW.Ksat, Shear_Modulus_G, rhob(rho_fluid(0.8)), Porosity, rho_fluid(0.8))
    Vp_Gardner_80SW.calc_Vp()
    Vp_Gardner_100SW = Vp(Ksat_Gardner_100SW.Ksat, Shear_Modulus_G, rhob(rho_fluid(1)), Porosity, rho_fluid(1))
    Vp_Gardner_100SW.calc_Vp()

    Vs_Gardner_0SW = Vs(Shear_Modulus_G, rhob(rho_fluid(0)), Porosity, rho_fluid(0))
    Vs_Gardner_0SW.calc_Vs()
    Vs_Gardner_20SW = Vs(Shear_Modulus_G, rhob(rho_fluid(0.2)), Porosity, rho_fluid(0.2))
    Vs_Gardner_20SW.calc_Vs()
    Vs_Gardner_40SW = Vs(Shear_Modulus_G, rhob(rho_fluid(0.4)), Porosity, rho_fluid(0.4))
    Vs_Gardner_40SW.calc_Vs()
    Vs_Gardner_50SW = Vs(Shear_Modulus_G, rhob(rho_fluid(0.6)), Porosity, rho_fluid(0.5))
    Vs_Gardner_50SW.calc_Vs()
    Vs_Gardner_60SW = Vs(Shear_Modulus_G, rhob(rho_fluid(0.6)), Porosity, rho_fluid(0.6))
    Vs_Gardner_60SW.calc_Vs()
    Vs_Gardner_80SW = Vs(Shear_Modulus_G, rhob(rho_fluid(0.8)), Porosity, rho_fluid(0.8))
    Vs_Gardner_80SW.calc_Vs()
    Vs_Gardner_100SW = Vs(Shear_Modulus_G, rhob(rho_fluid(1)), Porosity, rho_fluid(1))
    Vs_Gardner_100SW.calc_Vs()

    for counter, x in enumerate(Bulk_Modulus_Castagna_1):
        K_star_Castagna_1.append(
            (x * ((Porosity / 100) * (K_matrix_YRH / K_fluid(1)) + 1 - (Porosity / 100)) - K_matrix_YRH) / (
                        (Porosity / 100) * K_matrix_YRH / K_fluid(1) + x / Vp_rock - 1 - (Porosity / 100)))

    Ksat_Castagna_1_0SW = Ksat(K_star_Castagna_1, K_matrix_YRH, Porosity, K_fluid(0))
    Ksat_Castagna_1_0SW.calc_Ksat()
    Ksat_Castagna_1_20SW = Ksat(K_star_Castagna_1, K_matrix_YRH, Porosity, K_fluid(0.2))
    Ksat_Castagna_1_20SW.calc_Ksat()
    Ksat_Castagna_1_40SW = Ksat(K_star_Castagna_1, K_matrix_YRH, Porosity, K_fluid(0.4))
    Ksat_Castagna_1_40SW.calc_Ksat()
    Ksat_Castagna_1_50SW = Ksat(K_star_Castagna_1, K_matrix_YRH, Porosity, K_fluid(0.5))
    Ksat_Castagna_1_50SW.calc_Ksat()
    Ksat_Castagna_1_60SW = Ksat(K_star_Castagna_1, K_matrix_YRH, Porosity, K_fluid(0.6))
    Ksat_Castagna_1_60SW.calc_Ksat()
    Ksat_Castagna_1_80SW = Ksat(K_star_Castagna_1, K_matrix_YRH, Porosity, K_fluid(0.8))
    Ksat_Castagna_1_80SW.calc_Ksat()
    Ksat_Castagna_1_100SW = Ksat(K_star_Castagna_1, K_matrix_YRH, Porosity, K_fluid(1))
    Ksat_Castagna_1_100SW.calc_Ksat()

    Vp_Castagna_1_0SW = Vp(Ksat_Castagna_1_0SW.Ksat, Shear_Modulus_Castagna_1, rhob(rho_fluid(0)), Porosity,
                           rho_fluid(0))
    Vp_Castagna_1_0SW.calc_Vp()
    Vp_Castagna_1_20SW = Vp(Ksat_Castagna_1_20SW.Ksat, Shear_Modulus_Castagna_1, rhob(rho_fluid(0.2)), Porosity,
                            rho_fluid(0.2))
    Vp_Castagna_1_20SW.calc_Vp()
    Vp_Castagna_1_40SW = Vp(Ksat_Castagna_1_40SW.Ksat, Shear_Modulus_Castagna_1, rhob(rho_fluid(0.4)), Porosity,
                            rho_fluid(0.4))
    Vp_Castagna_1_40SW.calc_Vp()
    Vp_Castagna_1_50SW = Vp(Ksat_Castagna_1_50SW.Ksat, Shear_Modulus_Castagna_1, rhob(rho_fluid(0.5)), Porosity,
                            rho_fluid(0.5))
    Vp_Castagna_1_50SW.calc_Vp()
    Vp_Castagna_1_60SW = Vp(Ksat_Castagna_1_60SW.Ksat, Shear_Modulus_Castagna_1, rhob(rho_fluid(0.6)), Porosity,
                            rho_fluid(0.6))
    Vp_Castagna_1_60SW.calc_Vp()
    Vp_Castagna_1_80SW = Vp(Ksat_Castagna_1_80SW.Ksat, Shear_Modulus_Castagna_1, rhob(rho_fluid(0.8)), Porosity,
                            rho_fluid(0.8))
    Vp_Castagna_1_80SW.calc_Vp()
    Vp_Castagna_1_100SW = Vp(Ksat_Castagna_1_100SW.Ksat, Shear_Modulus_Castagna_1, rhob(rho_fluid(1)), Porosity,
                             rho_fluid(1))
    Vp_Castagna_1_100SW.calc_Vp()

    Vs_Castagna_1_0SW = Vs(Shear_Modulus_Castagna_1, rhob(rho_fluid(0)), Porosity, rho_fluid(0))
    Vs_Castagna_1_0SW.calc_Vs()
    Vs_Castagna_1_20SW = Vs(Shear_Modulus_Castagna_1, rhob(rho_fluid(0.2)), Porosity, rho_fluid(0.2))
    Vs_Castagna_1_20SW.calc_Vs()
    Vs_Castagna_1_40SW = Vs(Shear_Modulus_Castagna_1, rhob(rho_fluid(0.4)), Porosity, rho_fluid(0.4))
    Vs_Castagna_1_40SW.calc_Vs()
    Vs_Castagna_1_50SW = Vs(Shear_Modulus_Castagna_1, rhob(rho_fluid(0.6)), Porosity, rho_fluid(0.5))
    Vs_Castagna_1_50SW.calc_Vs()
    Vs_Castagna_1_60SW = Vs(Shear_Modulus_Castagna_1, rhob(rho_fluid(0.6)), Porosity, rho_fluid(0.6))
    Vs_Castagna_1_60SW.calc_Vs()
    Vs_Castagna_1_80SW = Vs(Shear_Modulus_Castagna_1, rhob(rho_fluid(0.8)), Porosity, rho_fluid(0.8))
    Vs_Castagna_1_80SW.calc_Vs()
    Vs_Castagna_1_100SW = Vs(Shear_Modulus_Castagna_1, rhob(rho_fluid(1)), Porosity, rho_fluid(1))
    Vs_Castagna_1_100SW.calc_Vs()

    for counter, x in enumerate(Bulk_Modulus_Castagna_2):
        K_star_Castagna_2.append(
            (x * ((Porosity / 100) * (K_matrix_YRH / K_fluid(1)) + 1 - (Porosity / 100)) - K_matrix_YRH) / (
                        (Porosity / 100) * K_matrix_YRH / K_fluid(1) + x / Vp_rock - 1 - (Porosity / 100)))

    Ksat_Castagna_2_0SW = Ksat(K_star_Castagna_2, K_matrix_YRH, Porosity, K_fluid(0))
    Ksat_Castagna_2_0SW.calc_Ksat()
    Ksat_Castagna_2_20SW = Ksat(K_star_Castagna_2, K_matrix_YRH, Porosity, K_fluid(0.2))
    Ksat_Castagna_2_20SW.calc_Ksat()
    Ksat_Castagna_2_40SW = Ksat(K_star_Castagna_2, K_matrix_YRH, Porosity, K_fluid(0.4))
    Ksat_Castagna_2_40SW.calc_Ksat()
    Ksat_Castagna_2_50SW = Ksat(K_star_Castagna_2, K_matrix_YRH, Porosity, K_fluid(0.5))
    Ksat_Castagna_2_50SW.calc_Ksat()
    Ksat_Castagna_2_60SW = Ksat(K_star_Castagna_2, K_matrix_YRH, Porosity, K_fluid(0.6))
    Ksat_Castagna_2_60SW.calc_Ksat()
    Ksat_Castagna_2_80SW = Ksat(K_star_Castagna_2, K_matrix_YRH, Porosity, K_fluid(0.8))
    Ksat_Castagna_2_80SW.calc_Ksat()
    Ksat_Castagna_2_100SW = Ksat(K_star_Castagna_2, K_matrix_YRH, Porosity, K_fluid(1))
    Ksat_Castagna_2_100SW.calc_Ksat()

    Vp_Castagna_2_0SW = Vp(Ksat_Castagna_2_0SW.Ksat, Shear_Modulus_Castagna_2, rhob(rho_fluid(0)), Porosity,
                           rho_fluid(0))
    Vp_Castagna_2_0SW.calc_Vp()
    Vp_Castagna_2_20SW = Vp(Ksat_Castagna_2_20SW.Ksat, Shear_Modulus_Castagna_2, rhob(rho_fluid(0.2)), Porosity,
                            rho_fluid(0.2))
    Vp_Castagna_2_20SW.calc_Vp()
    Vp_Castagna_2_40SW = Vp(Ksat_Castagna_2_40SW.Ksat, Shear_Modulus_Castagna_2, rhob(rho_fluid(0.4)), Porosity,
                            rho_fluid(0.4))
    Vp_Castagna_2_40SW.calc_Vp()
    Vp_Castagna_2_50SW = Vp(Ksat_Castagna_2_50SW.Ksat, Shear_Modulus_Castagna_2, rhob(rho_fluid(0.5)), Porosity,
                            rho_fluid(0.5))
    Vp_Castagna_2_50SW.calc_Vp()
    Vp_Castagna_2_60SW = Vp(Ksat_Castagna_2_60SW.Ksat, Shear_Modulus_Castagna_2, rhob(rho_fluid(0.6)), Porosity, 
                            rho_fluid(0.6))
    Vp_Castagna_2_60SW.calc_Vp()
    Vp_Castagna_2_80SW = Vp(Ksat_Castagna_2_80SW.Ksat, Shear_Modulus_Castagna_2, rhob(rho_fluid(0.8)), Porosity,
                            rho_fluid(0.8))
    Vp_Castagna_2_80SW.calc_Vp()
    Vp_Castagna_2_100SW = Vp(Ksat_Castagna_2_100SW.Ksat, Shear_Modulus_Castagna_2, rhob(rho_fluid(1)), Porosity,
                             rho_fluid(1))
    Vp_Castagna_2_100SW.calc_Vp()

    Vs_Castagna_2_0SW = Vs(Shear_Modulus_Castagna_2, rhob(rho_fluid(0)), Porosity, rho_fluid(0))
    Vs_Castagna_2_0SW.calc_Vs()
    Vs_Castagna_2_20SW = Vs(Shear_Modulus_Castagna_2, rhob(rho_fluid(0.2)), Porosity, rho_fluid(0.2))
    Vs_Castagna_2_20SW.calc_Vs()
    Vs_Castagna_2_40SW = Vs(Shear_Modulus_Castagna_2, rhob(rho_fluid(0.4)), Porosity, rho_fluid(0.4))
    Vs_Castagna_2_40SW.calc_Vs()
    Vs_Castagna_2_50SW = Vs(Shear_Modulus_Castagna_2, rhob(rho_fluid(0.6)), Porosity, rho_fluid(0.5))
    Vs_Castagna_2_50SW.calc_Vs()
    Vs_Castagna_2_60SW = Vs(Shear_Modulus_Castagna_2, rhob(rho_fluid(0.6)), Porosity, rho_fluid(0.6))
    Vs_Castagna_2_60SW.calc_Vs()
    Vs_Castagna_2_80SW = Vs(Shear_Modulus_Castagna_2, rhob(rho_fluid(0.8)), Porosity, rho_fluid(0.8))
    Vs_Castagna_2_80SW.calc_Vs()
    Vs_Castagna_2_100SW = Vs(Shear_Modulus_Castagna_2, rhob(rho_fluid(1)), Porosity, rho_fluid(1))
    Vs_Castagna_2_100SW.calc_Vs()

    # This starts an adaptation of a wavelet from
    # https://github.com/rowanc1/Seismogram

    ## WAVELET DEFINITIONS
    pi = np.pi

    def getRicker(f, t):
        """
        Retrieves a Ricker wavelet with center frequency f.
        See: http://www.subsurfwiki.org/wiki/Ricker_wavelet
        """
        # assert len(f) == 1, 'Ricker wavelet needs 1 frequency as input'
        # f = f[0]
        pift = pi * f * t
        wav = (1 - 2 * pift ** 2) * np.exp(-pift ** 2)
        return wav

    def getOrmsby(f, t):
        """
        Retrieves an Ormsby wavelet with low-cut frequency f[0], low-pass frequency f[1], high-pass frequency f[2] and high-cut frequency f[3]
        See: http://www.subsurfwiki.org/wiki/Ormsby_filter
        """
        assert len(f) == 4, 'Ormsby wavelet needs 4 frequencies as input'
        f = np.sort(f)  # Ormsby wavelet frequencies must be in increasing order
        pif = pi * f
        den1 = pif[3] - pif[2]
        den2 = pif[1] - pif[0]
        term1 = (pif[3] * np.sinc(pif[3] * t)) ** 2 - (pif[2] * np.sinc(pif[2])) ** 2
        term2 = (pif[1] * np.sinc(pif[1] * t)) ** 2 - (pif[0] * np.sinc(pif[0])) ** 2

        wav = term1 / den1 - term2 / den2;
        return wav

    def getKlauder(f, t):
        T = 5
        """
        Retrieves a Klauder Wavelet with upper frequency f[0] and lower frequency f[1].
        See: http://www.subsurfwiki.org/wiki/Ormsby_filter
        """
        assert len(f) == 2, 'Klauder wavelet needs 2 frequencies as input'

        k = np.diff(f) / T
        f0 = np.sum(f) / 2.0
        wav = np.real(np.sin(pi * k * t * (T - t)) / (pi * k * t) * np.exp(2 * pi * 1j * f0 * t))
        return wav

    def normalize(v):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm

    class Seis:
        def __init__(self, pvel, D, wavelet_type, freq, dt):
            self.pvel = pvel
            self.D = D
            self.wavelet_type = wavelet_type
            self.freq = freq
            self.dt = dt

        def calc_Seis(self):
            RC = []

            for x, index in enumerate(self.pvel):
                if x > 0:
                    RC.append((self.pvel[x - 1] - self.pvel[x]) / (self.pvel[x - 1] + self.pvel[x]))

            twt = []
            for x, index in enumerate(self.pvel):
                if x == 0:
                    twt.append(2 * self.D[x] / self.pvel[x])
                else:
                    twt.append((2 * (self.D[x] - self.D[x - 1]) / self.pvel[x]) + twt[x - 1])

            R = np.zeros(round(twt[-1] / self.dt) + 10)

            for x, index in enumerate(RC):
                n = twt[x] / self.dt
                n = round(n)
                R[n] = RC[x]

            twav = np.arange(-2.0 / np.min(self.freq), 2.0 / np.min(self.freq), self.dt)
            if self.wavelet_type == 'Ricker':
                wt = getRicker(self.freq, twav)
            elif self.wavelet_type == 'Ormsby':
                wt = getOrmsby(self.freq, twav)
            elif self.wavelet_type == 'Klauder':
                wt = getKlauder(self.freq, twav)

            seis = np.convolve(wt, R)
            tseis = np.min(twav) + self.dt * np.arange(len(seis))
            index = np.logical_and(tseis >= np.min(twt), tseis <= np.max(twt))
            tseis = tseis[index]
            seis = seis[index]
            self.Seis = seis
            self.tSeis = tseis

    if calculation_method == 'Gardner':
        Seis_0SW = Seis(Vp_Gardner_0SW.Vp, depth, wavelet_type, freq, dt)
        Seis_0SW.calc_Seis()
        Seis_50SW = Seis(Vp_Gardner_50SW.Vp, depth, wavelet_type, freq, dt)
        Seis_50SW.calc_Seis()
        Seis_100SW = Seis(Vp_Gardner_100SW.Vp, depth, wavelet_type, freq, dt)
        Seis_100SW.calc_Seis()
    elif calculation_method == 'Castagna_1':
        Seis_0SW = Seis(Vp_Castagna_1_0SW.Vp, depth, wavelet_type, freq, dt)
        Seis_0SW.calc_Seis()
        Seis_50SW = Seis(Vp_Castagna_1_50SW.Vp, depth, wavelet_type, freq, dt)
        Seis_50SW.calc_Seis()
        Seis_100SW = Seis(Vp_Castagna_1_100SW.Vp, depth, wavelet_type, freq, dt)
        Seis_100SW.calc_Seis()
    elif calculation_method == 'Castagna_2':
        Seis_0SW = Seis(Vp_Castagna_2_0SW.Vp, depth, wavelet_type, freq, dt)
        Seis_0SW.calc_Seis()
        Seis_50SW = Seis(Vp_Castagna_2_50SW.Vp, depth, wavelet_type, freq, dt)
        Seis_50SW.calc_Seis()
        Seis_100SW = Seis(Vp_Castagna_2_100SW.Vp, depth, wavelet_type, freq, dt)
        Seis_100SW.calc_Seis()

    # Making the plot

    f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharey=True)

    ax1.plot(SP, depth)
    ax1.set_xlabel('SP or GR')
    ax1.set_ylabel('Depth (Ft)')
    ax1.invert_yaxis()
    ax1.legend(['SP or GR'], loc=9, bbox_to_anchor=(0.5, 1.25))

    if calculation_method == 'Gardner':
        ax2.plot(Vp_Gardner_0SW.Vp_kms, depth, Vp_Gardner_50SW.Vp_kms, depth, Vp_Gardner_100SW.Vp_kms, depth)
        ax3.plot(Vs_Gardner_0SW.Vs_kms, depth, Vs_Gardner_50SW.Vs_kms, depth, Vs_Gardner_100SW.Vs_kms, depth)
        ax4.plot(Ksat_Gardner_0SW.Ksat, depth, Ksat_Gardner_50SW.Ksat, depth, Ksat_Gardner_100SW.Ksat, depth)

    elif calculation_method == 'Castagna_1':
        ax2.plot(Vp_Castagna_1_0SW.Vp_kms, depth, Vp_Castagna_1_50SW.Vp_kms, depth, Vp_Castagna_1_100SW.Vp_kms, depth)
        ax3.plot(Vs_Castagna_1_0SW.Vs_kms, depth, Vs_Castagna_1_50SW.Vs_kms, depth, Vs_Castagna_1_100SW.Vs_kms, depth)
        ax4.plot(Ksat_Castagna_1_0SW.Ksat, depth, Ksat_Castagna_1_50SW.Ksat, depth, Ksat_Castagna_1_100SW.Ksat, depth)
    else:
        ax2.plot(Vp_Castagna_2_0SW.Vp_kms, depth, Vp_Castagna_2_50SW.Vp_kms, depth, Vp_Castagna_2_100SW.Vp_kms, depth)
        ax3.plot(Vs_Castagna_2_0SW.Vs_kms, depth, Vs_Castagna_2_50SW.Vs_kms, depth, Vs_Castagna_2_100SW.Vs_kms, depth)
        ax4.plot(Ksat_Castagna_2_0SW.Ksat, depth, Ksat_Castagna_2_50SW.Ksat, depth, Ksat_Castagna_2_100SW.Ksat, depth)

    ax2.legend(['Vp 0% Sw', 'Vp 50% Sw', 'Vp 100% Sw'], loc=9, bbox_to_anchor=(0.5, 1.25))
    ax2.set_xlabel('Velocity (km/s)')
    ax2.invert_yaxis()
    ax2.get_yaxis().set_visible(False)

    ax3.legend(['Vs 0% Sw', 'Vs 50% Sw', 'Vs 100% Sw'], loc=9, bbox_to_anchor=(0.5, 1.25))
    ax3.set_xlabel('Velocity (km/s)')
    ax3.invert_yaxis()
    ax3.get_yaxis().set_visible(False)

    ax4.legend(['Ksat 0% Sw', 'Ksat 50% Sw', 'Ksat 100% Sw'], loc=9, bbox_to_anchor=(0.5, 1.25))
    ax4.set_xlabel('Bulk Modulus (GPa)')
    ax4.invert_yaxis()
    ax4.get_yaxis().set_visible(False)
    plt.tight_layout()
    plt.show()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_one_url = 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

    # Making the second plot

    f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, sharey=False)

    ax1.plot(SP, depth, 'k')
    ax1.set_xlabel('SP or GR')
    ax1.set_ylabel('Depth (Ft)')
    ax1.invert_yaxis()
    ax1.legend(['SP or GR'], loc=9, bbox_to_anchor=(0.5, 1.15))

    ax2.plot(DT_edited, depth, 'r')
    ax2.set_xlabel('dt (s)')
    ax2.invert_yaxis()
    ax2.legend(['Sonic'], loc=9, bbox_to_anchor=(0.5, 1.15))
    ax2.get_yaxis().set_visible(False)
    ax3.plot(Seis_0SW.Seis, Seis_0SW.tSeis, 'y')
    ax3.legend(['0% Sw'], loc=9, bbox_to_anchor=(0.5, 1.15))
    ax3.get_yaxis().set_visible(False)
    ax3.set_xlabel('Amplitude', fontsize=9)
    ax3.xaxis.set_major_locator(plt.MaxNLocator(2))
    ax3.set_autoscale_on(False)
    plt.ylim(top=max(Seis_0SW.tSeis[-1], Seis_50SW.tSeis[-1], Seis_100SW.tSeis[-1]))
    ax3.invert_yaxis()

    ax4.plot(Seis_50SW.Seis, Seis_50SW.tSeis, 'g')
    ax4.legend(['50% Sw'], loc=9, bbox_to_anchor=(0.5, 1.15))
    ax4.set_xlabel('Amplitude', fontsize=9)
    ax4.xaxis.set_major_locator(plt.MaxNLocator(2))
    plt.ylim(top=max(Seis_0SW.tSeis[-1], Seis_50SW.tSeis[-1], Seis_100SW.tSeis[-1]))
    ax4.set_autoscale_on(False)
    ax4.invert_yaxis()
    ax4.get_yaxis().set_visible(False)

    ax5.plot(Seis_100SW.Seis, Seis_100SW.tSeis)
    ax5.legend(['100% Sw'], loc=9, bbox_to_anchor=(0.5, 1.15))
    ax5.xaxis.set_major_locator(plt.MaxNLocator(2))
    ax5.set_xlabel('Amplitude', fontsize=9)
    ax5.set_autoscale_on(False)
    plt.ylim(top=max(Seis_0SW.tSeis[-1], Seis_50SW.tSeis[-1], Seis_100SW.tSeis[-1]))
    ax5.invert_yaxis()
    ax5.tick_params(axis='y', right=1, left=0, labelright=1, labelleft=0)
    ax5.set_ylabel('Relative Time (s)')
    ax5.yaxis.set_label_position('right')

    plt.subplots_adjust(left=0.125)
    plt.show()
    

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_two_url = 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
    # plt.close()

    with open('./static/csv/las_export.csv','w',newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['This CSV file was written with from https://rockphysics.herokuapp.com/'])
        thewriter.writerow(['Contact Jacob Anderson with questions/comments. jacob.anderson10@gmail.com'])
        thewriter.writerow(['Calculation Method','Bulk Modulus Quartz (K0 GPa)','Bulk Modulus Plag Feldspar (K0 GPa)',
                            'Bulk Modulus Dolomite (K0 GPa)','Bulk Modulus Clay (K0 GPa)','Fraction Quartz',
                            'Fraction Plag Feldspar','Fraction Dolomite','Fraction Clay','Bulk Modulus of Pore Fluid (Kfl GPa)',
                            'Bulk Modulus of Gas (Kgas GPa)','Density of Pore Fluid (g/cc)','Density of Gas (g/cc)','Porosity','Density of Rock (g/cc)',
                            'Grain Density (g/cc)','Primary Velocity of Rock (Km/s)','Shear Velocity of Rock (km/s)','SP Cutoff',
                            'Wavelet Type','Sampling Interval (time)','Frequency (Hz)'])
        Vs_rock=Vs_rock/3048
        Vp_rock=Vp_rock/3048
        thewriter.writerow([calculation_method,str(K0_quartz),str(K0_plag_feldspar),str(K0_dolomite),str(K0_clay),
                            str(Percent_quartz),str(Percent_plag_feldspar),str(Percent_dolomite),str(Percent_clay),
                            str(K_brine),str(K_gas),str(rho_brine),str(rho_gas),str(Porosity),str(rhob_rock),str(rhob_dry),
                            str(Vp_rock),str(Vs_rock),str(SP_shale_cutoff),wavelet_type,str(dt),str(freq)])
        thewriter.writerow(['Depth','SP','Sonic','Vp 0% Sw (m/s)','Vp 20% Sw (m/s)', 'Vp 40% Sw (m/)','Vp 50% Sw (m/s)','Vp 60% Sw (m/s)','Vp 80% Sw (m/s)',
                            'Vp 100% Sw (m/s)','Vs 0% Sw (m/s)','Vs 20% Sw (m/s)','Vs 40% Sw (m/s)',
                            'Vs 50% Sw (m/s)','Vs 60% Sw (m/s)','Vs 80% Sw (m/s)','Vs 100% Sw (m/s)','Ksat 0% Sw (GPa)',
                            'Ksat 20% Sw (GPa)','Ksat 40% Sw (GPa)','Ksat 50% Sw (GPa)','Ksat 60% Sw (GPa)','Ksat 80% Sw (GPa)',
                            'Ksat 100% Sw (GPa)','Seismic Time 0% Sw (s)','Amplitude 0% Sw','Seismic Time 50% Sw (s)',
                            'Amplitude 50% Sw','Seismic Time 100% Sw','Amplitude 100% Sw'])



        for i,x in enumerate(depth):

            if calculation_method=='Gardner':
                thewriter.writerow([str(depth[i]), str(SP[i]), str(DT_edited[i]), str(Vp_Gardner_0SW.Vp[i]), str(Vp_Gardner_20SW.Vp[i]),
                            str(Vp_Gardner_40SW.Vp[i]),str(Vp_Gardner_50SW.Vp[i]),str(Vp_Gardner_60SW.Vp[i]),str(Vp_Gardner_80SW.Vp[i]),
                            str(Vp_Gardner_100SW.Vp[i]), str(Vs_Gardner_0SW.Vs[i]), str(Vs_Gardner_20SW.Vs[i]),str(Vs_Gardner_40SW.Vs[i]),
                            str(Vs_Gardner_50SW.Vs[i]),str(Vs_Gardner_60SW.Vs[i]),str(Vs_Gardner_80SW.Vs[i]),
                            str(Vs_Gardner_100SW.Vs[i]), str(Ksat_Gardner_0SW.Ksat[i]),str(Ksat_Gardner_20SW.Ksat[i]),str(Ksat_Gardner_40SW.Ksat[i]),
                            str(Ksat_Gardner_50SW.Ksat[i]),str(Ksat_Gardner_60SW.Ksat[i]),str(Ksat_Gardner_80SW.Ksat[i]),str(Ksat_Gardner_100SW.Ksat[i]),
                            str(Seis_0SW.tSeis[i]) if i<len(Seis_0SW.tSeis) else None,str(Seis_0SW.Seis[i]) if i<len(Seis_0SW.Seis) else None,
                            str(Seis_50SW.tSeis[i]) if i<len(Seis_50SW.tSeis) else None,str(Seis_50SW.Seis[i]) if i<len(Seis_50SW.Seis) else None,
                            str(Seis_100SW.tSeis[i]) if i<len(Seis_100SW.tSeis) else None,str(Seis_100SW.Seis[i]) if i<len(Seis_100SW.Seis) else None])
            elif calculation_method=='Castagna_1':
                thewriter.writerow([str(depth[i]), str(SP[i]), str(DT_edited[i]), str(Vp_Castagna_1_0SW.Vp[i]), str(Vp_Castagna_1_20SW.Vp[i]),
                            str(Vp_Castagna_1_40SW.Vp[i]),str(Vp_Castagna_1_50SW.Vp[i]),str(Vp_Castagna_1_60SW.Vp[i]),str(Vp_Castagna_1_80SW.Vp[i]),
                            str(Vp_Castagna_1_100SW.Vp[i]), str(Vs_Castagna_1_0SW.Vs[i]), str(Vs_Castagna_1_20SW.Vs[i]),str(Vs_Castagna_1_40SW.Vs[i]),
                            str(Vs_Castagna_1_50SW.Vs[i]),str(Vs_Castagna_1_60SW.Vs[i]),str(Vs_Castagna_1_80SW.Vs[i]),
                            str(Vs_Castagna_1_100SW.Vs[i]), str(Ksat_Castagna_1_0SW.Ksat[i]),str(Ksat_Castagna_1_20SW.Ksat[i]),str(Ksat_Castagna_1_40SW.Ksat[i]),
                            str(Ksat_Castagna_1_50SW.Ksat[i]), str(Ksat_Castagna_1_60SW.Ksat[i]),str(Ksat_Castagna_1_80SW.Ksat[i]),str(Ksat_Gardner_100SW.Ksat[i]),
                            str(Seis_0SW.tSeis[i]) if i<len(Seis_0SW.tSeis) else None,str(Seis_0SW.Seis[i]) if i<len(Seis_0SW.Seis) else None,
                            str(Seis_50SW.tSeis[i]) if i<len(Seis_50SW.tSeis) else None,str(Seis_50SW.Seis[i]) if i<len(Seis_50SW.Seis) else None,
                            str(Seis_100SW.tSeis[i]) if i<len(Seis_100SW.tSeis) else None,str(Seis_100SW.Seis[i]) if i<len(Seis_100SW.Seis) else None])
            else:
                thewriter.writerow([str(depth[i]), str(SP[i]), str(DT_edited[i]), str(Vp_Castagna_2_0SW.Vp[i]), str(Vp_Castagna_2_20SW.Vp[i]),
                            str(Vp_Castagna_2_40SW.Vp[i]),str(Vp_Castagna_2_50SW.Vp[i]),str(Vp_Castagna_2_60SW.Vp[i]),str(Vp_Castagna_2_80SW.Vp[i]),
                            str(Vp_Castagna_2_100SW.Vp[i]), str(Vs_Castagna_2_0SW.Vs[i]), str(Vs_Castagna_2_20SW.Vs[i]),str(Vs_Castagna_2_40SW.Vs[i]),
                            str(Vs_Castagna_2_50SW.Vs[i]),str(Vs_Castagna_2_60SW.Vs[i]),str(Vs_Castagna_2_80SW.Vs[i]),
                            str(Vs_Castagna_2_100SW.Vs[i]), str(Ksat_Castagna_2_0SW.Ksat[i]),str(Ksat_Castagna_2_20SW.Ksat[i]),str(Ksat_Castagna_2_40SW.Ksat[i]),
                            str(Ksat_Castagna_2_50SW.Ksat[i]), str(Ksat_Castagna_2_60SW.Ksat[i]),str(Ksat_Castagna_2_80SW.Ksat[i]),str(Ksat_Gardner_100SW.Ksat[i]),
                            str(Seis_0SW.tSeis[i]) if i<len(Seis_0SW.tSeis) else None,str(Seis_0SW.Seis[i]) if i<len(Seis_0SW.Seis) else None,
                            str(Seis_50SW.tSeis[i]) if i<len(Seis_50SW.tSeis) else None,str(Seis_50SW.Seis[i]) if i<len(Seis_50SW.Seis) else None,
                            str(Seis_100SW.tSeis[i]) if i<len(Seis_100SW.tSeis) else None,str(Seis_100SW.Seis[i]) if i<len(Seis_100SW.Seis) else None])
    
    graph_urls = {
        "url_1": graph_one_url,
        "url_2": graph_two_url
    }
    return graph_urls