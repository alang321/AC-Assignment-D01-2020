import databaseAPI
import pandas as pd
from scipy.stats import linregress
import numpy as np

#database data
aircraftdata = databaseAPI.getdatafromsheet('Aircraft Reference Database')

#constants used
h_0 =0 #m
g_0 =9.80665 #m/s^2
r = 287
t_0 =288.15 #K
p_0 =101325 #Pa

#from empirical data and ADSEE slides
frac_resf = 0.05 #reserve fuel
frac_tfo = 0.01 #fraction trpped fuel and oil of total fuel
A = 8.45 #7-10 calculated by taking average from database
c_j = 0.582 * (0.45359 * 0.2248)/(3600) #0.5 - 0.9 * 0.45359 /3600 * 0.2248, for conversion
oswald_fact = 0.8 #0.7-0.85 Oswald factor
C_D0 = 0.018 #0.014-0.020
t_loiter = 1800 #s

#from requirements
#payload masses
M_harm = 66000 #kg
M_miss = 40000 #kg
M_maxi = 18000 #kg
M_ferr = 0 #kg
#ranges
R_harm = 4500 #km
R_miss = 7500 #km
R_maxi = 10500 #km
R_ferr = 11000 #km

Mach_cruise = 0.77
h_cruise = 9449 #m

#main function, rangemass should be of format (m, kg) [[range1, pl1], [range2, pl2]....]
def class1weight(rangemass):
    # General setup
    # calculations for atmosphere
    t, p, rho, a = atmospheredata(h_cruise) #K, Pa, kg/m^3, m/s
    v_cruise = Mach_cruise * a  # m/s

    # Step 1: Calculate k, d to express OEM as function of MTOW from statistical data
    reg_a, reg_b, reg_r, reg_p, reg_stderr = trenddata('MTOM (kg)', 'OEM (kg)') # y=a*x+b
    reg_b *= g_0 #since the aircraft databse is in kg, and we want newtons

    # variable to keep track of the most limiting mission
    mtow_max = 0
    mtow_max_index = 0

    #do next steps for each mission, to find the most limiting one
    for index, mission in enumerate(rangemass):
        # mission[0] = range in m, mission[1] = m_pl in kg:
        range = mission[0]
        W_pl = mission[1] * g_0

        # Step 2: Calculate Fuel mass fraction
        frac_usedf = fuelfracttransport(range, v_cruise)

        # Step 3: Calculate MTOW
        MTOW = (W_pl + reg_b) / (1 - (reg_a + frac_usedf * (1 + frac_tfo)))  # N  (1 + frac_resf + frac_tfo) accring to (3.11) from Aircraft Design, Raymer

        #check if largest mtow
        if MTOW > mtow_max:
            mtow_max_index = index
            mtow_max = MTOW

    # MTOW, OEW, mission index
    return mtow_max, reg_a * mtow_max + reg_b, mtow_max_index

#calculates Temp, press, density and SOS for altitude up to 11km according to ISA
def atmospheredata(h):
    a_atmo = -0.0065
    t = t_0 + (a_atmo * (h_cruise - h_0))  # K
    p = p_0 * (t / t_0) ** (-g_0 / a_atmo / r)  # Pa
    rho = p / (r * t)  # kg/m^3
    a = (1.4 * r * t)**0.5  # m/s
    return t, p, rho, a

#gets trendline data, returns: k, d, rval, pval, stderr (y=k*x+d)
def trenddata(x, y):
    x = pd.to_numeric(aircraftdata[x]).dropna()
    y = pd.to_numeric(aircraftdata[y]).dropna()
    return linregress(x, y)

def fuelfracttransport(range, v_cruise):
    #engine start and warm-up; taxi; take-off; Climb and acceleration to cruise; descent; landing, taxi and shut-down
    # calculations for w54 cruise
    LoverD1 = 3 / 4 * ((np.pi * A * oswald_fact) / (3 * C_D0))**0.5
    w54 = 1 / (np.exp((range * g_0 * c_j) / (v_cruise * LoverD1)))

    # calculations for w98 loiter
    LoverD2 = ((np.pi * A * oswald_fact * C_D0)**0.5) / (2 * C_D0)
    w98 = 1 / (np.exp((t_loiter * g_0 * c_j) / (LoverD2)))

    M_ff = 0.99 * 0.99 * 0.995 * 0.98 * 0.99 * 0.992 * 0.965 * w54 * w98
    return 1 - M_ff


#create a list of missions and their corresponding payloads, so the most limiting one can be deduced
rangemass = [[R_harm*1000, M_harm], [R_miss*1000, M_miss], [R_maxi*1000, M_maxi], [R_ferr*1000, M_ferr]]

MTOW, OEW, missionindex = class1weight(rangemass)

print("\nCLASS 1 WEIGHT ESTIMATION RESULTS \n")
print("Most limiting mission with range of", (rangemass[missionindex][0]/1000), "[m] and", rangemass[missionindex][1], "[kg] of payload.")
print("MTOW (N):", MTOW, " MTOM (kg):", (MTOW / g_0))
print("OEW (N):", OEW, " OEM (kg):", (OEW / g_0))