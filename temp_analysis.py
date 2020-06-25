"""temp_analysis - analyze data from temp sesors

The temp_analysis program analyzes the data files created by the
roomtemp_pi.py program.
"""
############################################################################
# temp_analysis.py - statistical aalysis of temperature data
#
# Author:      Phil Moyer (phil@moyer.ai)
# Date:        June 2020
#
# Copyright(c) 2020 Philip R. Moyer. All rights reserved.
#
############################################################################


######################
# Import Libraries
######################

# Standard libraries modules

import statistics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import polyfit


# Third-party modules

# Package/application modules


######################
# Globals
######################

# data_path = "/home/pi/src/roomtemp/roomtemp_pi/output/temperature_data.csv"
data_path = "/home/pi/src/roomtemp/roomtemp_pi/output/data_in.csv"
# output_path = "/home/pi/src/roomtemp/temp_analysis/output"
output_path = "./images/"


######################
# Pre-Main Setup
######################



######################
# Classes and Methods
######################



######################
# Functions
######################

def main():
    """Abstract main() into a function. Normally exits after execution.

    A function abstracting the main code in the module, which
    allows it to be used for libraries as well as testing (i.e., it can be
    called as a script for testing or imported as a library, without
    modification).
    """

    # Read the data into a matrix
    Col_Names = ["bme280","dps310","lps3x","pct2075","hts221","mean"]
    DataDF = pd.read_csv(data_path, names=Col_Names)

    #----------------------------------------------
    # Plot time series of all data points ####    |
    #----------------------------------------------

    x = np.arange(len(DataDF.iloc[:,1:1]))

    plt.style.use('dark_background')
    fig = plt.figure()
    fig.set_size_inches(12,5)
    fig.dpi = 300
    ax = fig.add_subplot(111)
    ax.set_ylabel('Temp F')
    ax.set_xlabel('Index')
    ax.set_title('Bedroom Temperature Sensor Comparison')

    ax.plot(x, DataDF.iloc[:,0:1], c='b', ls='-', label="BME280", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,1:2], c='g', ls='-', label="DPS310", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,2:3], c='c', ls='-', label="LPS3x", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,3:4], c='y', ls='-', label="PCT2075", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,4:5], c='m', ls='-', label="HTS221", linewidth=0.5)
#   placeholder - HTU21D-F - 'xkcd:seafoam'
#   placeholder - Si7021 - 'xkcd:light orange'
#   placeholder - SHT31-D - 'xkcd:light yellow'
#   placeholder - LPS22 - 'xkcd:white'
#   placeholder - LPS25 - 'xkcd:sky blue'
#   placeholder - PT1000/ADS1115 - 'xkcd:hot pink'
#   placeholder - SHTC3 - 'xkcd:goldenrod'
#   placeholder - AMT20 -  'xkcd:light violet'
    ax.plot(x, DataDF.iloc[:,5:6], c='r', ls='-', label="Mean", linewidth=0.5)

    plt.legend()
    out_file = "%s/time_series_001.jpg" % output_path
    # plt.show()
    plt.savefig(out_file)

    #----------------------------------------------
    # Deviation from the mean
    #----------------------------------------------

    # Remove the curve so we see only data around the mean
    # Data format:
    # BME280 value, DPS310 value, LPS3x value, mean

    # New data frame format is distance from the mean for each
    # observed value.

    DF2 = pd.DataFrame()
    DF2['bme280'] = DataDF["bme280"] - DataDF['mean']
    DF2['dps310'] = DataDF["dps310"] - DataDF['mean']
    DF2['lps3x'] = DataDF["lps3x"] - DataDF['mean']
    DF2['pct2075'] = DataDF["pct2075"] - DataDF['mean']
    DF2['hts221'] = DataDF["hts221"] - DataDF['mean']
    # print(DF2.head(10))
   
    x = np.arange(len(DF2.iloc[:,1:1]))

    plt.style.use('dark_background')
    fig = plt.figure()
    fig.set_size_inches(12,5)
    fig.dpi = 300
    ax = fig.add_subplot(111)
    ax.set_ylabel('Variance')
    ax.set_xlabel('Index')
    ax.set_title('Sensor Variance Around The Mean')

    ax.plot(x, DF2["bme280"], c='b', ls='-', label="BME280", linewidth=0.5)
    ax.plot(x, DF2["dps310"], c='g', ls='-', label="DPS310", linewidth=0.5)
    ax.plot(x, DF2["lps3x"], c='c', ls='-', label="LPS3x", linewidth=0.5)
    ax.plot(x, DF2["pct2075"], c='y', ls='-', label="PCT2075", linewidth=0.5)
    ax.plot(x, DF2["hts221"], c='m', ls='-', label="HTS221", linewidth=0.5)

    plt.legend()
    out_file = "%s/variance_around_mean.jpg" % output_path
    # plt.show()
    plt.savefig(out_file)

    #----------------------------------------------
    # Statistics of the variance
    #----------------------------------------------

    print("\nSensor Variance Around The Mean:")
    print("\tSensor\tMax\tMin\tMean\tMedian")

    bme_var_max = DF2["bme280"].max()
    bme_var_min = DF2["bme280"].min()
    bme_var_mean = DF2["bme280"].mean()
    bme_var_median = DF2["bme280"].median()
    print("\tBME280\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (bme_var_max,
        bme_var_min,
        bme_var_mean,
        bme_var_median))

    dps_var_max = DF2["dps310"].max()
    dps_var_min = DF2["dps310"].min()
    dps_var_mean = DF2["dps310"].mean()
    dps_var_median = DF2["dps310"].median()
    print("\tDPS310\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (dps_var_max,
        dps_var_min,
        dps_var_mean,
        dps_var_median))

    lps_var_max = DF2["lps3x"].max()
    lps_var_min = DF2["lps3x"].min()
    lps_var_mean = DF2["lps3x"].mean()
    lps_var_median = DF2["lps3x"].median()
    print("\tLPS3x\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (lps_var_max,
        lps_var_min,
        lps_var_mean,
        lps_var_median))

    pct_var_max = DF2["pct2075"].max()
    pct_var_min = DF2["pct2075"].min()
    pct_var_mean = DF2["pct2075"].mean()
    pct_var_median = DF2["pct2075"].median()
    print("\tPTC2075\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (pct_var_max,
        pct_var_min,
        pct_var_mean,
        pct_var_median))

    hts_var_max = DF2["hts221"].max()
    hts_var_min = DF2["hts221"].min()
    hts_var_mean = DF2["hts221"].mean()
    hts_var_median = DF2["hts221"].median()
    print("\tHTS221\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (hts_var_max,
        hts_var_min,
        hts_var_mean,
        hts_var_median))

    print("")

    # Histograms of the variance

    out_file = "%s/variance_hist.jpg" % output_path
    plt.style.use('dark_background')
    hist = DF2.hist(bins=20, figsize=(12,5), layout=(1,3))
    plt.savefig(out_file)

    # Variance by temperature
    
    plt.style.use('dark_background')
    fig = plt.figure()
    fig.set_size_inches(12,5)
    fig.dpi = 300
    ax = fig.add_subplot(111)
    ax.set_ylabel('Variance')
    ax.set_xlabel('Temperature')
    ax.set_title('Sensor Variance by Temperature')

    ax.scatter(DataDF["bme280"], DF2["bme280"], c='b', s=0.1)
    b,m = polyfit(DataDF["bme280"], DF2["bme280"], 1)
    plt.plot(DataDF["bme280"], b + m * DataDF["bme280"], '-', c='b')

    ax.scatter(DataDF["dps310"], DF2["dps310"], c='g', s=0.1)
    b,m = polyfit(DataDF["dps310"], DF2["dps310"], 1)
    plt.plot(DataDF["dps310"], b + m * DataDF["dps310"], '-', c='g')

    ax.scatter(DataDF["lps3x"], DF2["lps3x"], c='c', s=0.1)
    b,m = polyfit(DataDF["lps3x"], DF2["lps3x"], 1)
    plt.plot(DataDF["lps3x"], b + m * DataDF["lps3x"], '-', c='c')

    ax.scatter(DataDF["pct2075"], DF2["pct2075"], c='y', s=0.1)
    b,m = polyfit(DataDF["pct2075"], DF2["pct2075"], 1)
    plt.plot(DataDF["pct2075"], b + m * DataDF["pct2075"], '-', c='y')

    ax.scatter(DataDF["hts221"], DF2["hts221"], c='m', s=0.1)
    b,m = polyfit(DataDF["hts221"], DF2["hts221"], 1)
    plt.plot(DataDF["hts221"], b + m * DataDF["hts221"], '-', c='m')

    plt.legend()
    out_file = "%s/VarxTemp.jpg" % output_path
    plt.savefig(out_file)
    

  
######################
# Main
######################

# The main code call allows this module to be imported as a library or
# called as a standalone program because __name__ will not be properly
# set unless called as a program.

if __name__ == "__main__":
    main()
