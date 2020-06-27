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
    Col_Names = ["bme280","dps310","pct2075","hts221","mcp9808","sht31d",
        "lps35hw","lps22","htu21","si7021","lps25","mean"]
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
    ax.set_xlabel('Observation')
    ax.set_title('Temperature Sensor Time Series Comparison')

    ax.plot(x, DataDF.iloc[:,0:1], c='b', ls='-', label="BME280", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,1:2], c='g', ls='-', label="DPS310", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,2:3], c='y', ls='-', label="PCT2075", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,3:4], c='m', ls='-', label="HTS221", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,4:5], c='xkcd:hot pink', ls='-', label="MCP9808", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,5:6], c='xkcd:light yellow', ls='-', label="SHT31", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,6:7], c='c', ls='-', label="LPS3x", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,7:8], c='xkcd:white', ls='-', label="LPS22", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,8:9], c='xkcd:seafoam', ls='-', label="HTU21", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,9:10], c='xkcd:light orange', ls='-', label="Si7021", linewidth=0.5)
    ax.plot(x, DataDF.iloc[:,10:11], c='xkcd:sky blue', ls='-', label="LPS25", linewidth=0.5)
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

    # Col_Names = ["bme280","dps310","pct2075","hts221","mcp9808","sht31d",
    #     "lps35hw","lps22","htu21","si7021","lps25","mean"]

    DF2 = pd.DataFrame()
    DF2['bme280'] = DataDF["bme280"] - DataDF['mean']
    DF2['dps310'] = DataDF["dps310"] - DataDF['mean']
    DF2['pct2075'] = DataDF["pct2075"] - DataDF['mean']
    DF2['hts221'] = DataDF["hts221"] - DataDF['mean']
    DF2['mcp9808'] = DataDF["mcp9808"] - DataDF['mean']
    DF2['sht31d'] = DataDF["sht31d"] - DataDF['mean']
    DF2['lps35hw'] = DataDF["lps35hw"] - DataDF['mean']
    DF2['lps22'] = DataDF["lps22"] - DataDF['mean']
    DF2['htu21'] = DataDF["htu21"] - DataDF['mean']
    DF2['si7021'] = DataDF["si7021"] - DataDF['mean']
    DF2['lps25'] = DataDF["lps25"] - DataDF['mean']

    # print(DF2.head(10))
   
    x = np.arange(len(DF2.iloc[:,1:1]))

    plt.style.use('dark_background')
    fig = plt.figure()
    fig.set_size_inches(12,5)
    fig.dpi = 300
    ax = fig.add_subplot(111)
    ax.set_ylabel('Variance')
    ax.set_xlabel('Observation')
    ax.set_title('Sensor Variance Around The Mean')

    # Colors:
    # BME280 	'b'
    # DPS310	'g'
    # PCT2075	'y'
    # HTS221	'm'
    # MCP9808	'xkcd:hot pink'
    # SHT31	'xkcd:light yellow'
    # LPS3x	'c''
    # LPS22	'xkcd:white'
    # HTU21	'xkcd:seafoam'
    # Si7021	'xkcd:light orange'
    # LPS25	'xkcd:sky blue'
#   placeholder - SHTC3 - 'xkcd:goldenrod'
#   placeholder - AMT20 -  'xkcd:light violet'

    ax.plot(x, DF2["bme280"], c='b', ls='-', label="BME280", linewidth=0.5)
    ax.plot(x, DF2["dps310"], c='g', ls='-', label="DPS310", linewidth=0.5)
    ax.plot(x, DF2["pct2075"], c='y', ls='-', label="PCT2075", linewidth=0.5)
    ax.plot(x, DF2["hts221"], c='m', ls='-', label="HTS221", linewidth=0.5)
    ax.plot(x, DF2["mcp9808"], c='xkcd:hot pink', ls='-', label="MCP9808", linewidth=0.5)
    ax.plot(x, DF2["sht31d"], c='xkcd:light yellow', ls='-', label="SHT31", linewidth=0.5)
    ax.plot(x, DF2["lps35hw"], c='c', ls='-', label="LPS3x", linewidth=0.5)
    ax.plot(x, DF2["lps22"], c='xkcd:white', ls='-', label="LPS22", linewidth=0.5)
    ax.plot(x, DF2["htu21"], c='xkcd:seafoam', ls='-', label="HTU21", linewidth=0.5)
    ax.plot(x, DF2["si7021"], c='xkcd:light orange', ls='-', label="Si7021", linewidth=0.5)
    ax.plot(x, DF2["lps25"], c='xkcd:sky blue', ls='-', label="LPS25", linewidth=0.5)

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

    mcp_var_max = DF2["mcp9808"].max()
    mcp_var_min = DF2["mcp9808"].min()
    mcp_var_mean = DF2["mcp9808"].mean()
    mcp_var_median = DF2["mcp9808"].median()
    print("\tMCP9808\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (mcp_var_max,
        mcp_var_min,
        mcp_var_mean,
        mcp_var_median))

    sht_var_max = DF2["sht31d"].max()
    sht_var_min = DF2["sht31d"].min()
    sht_var_mean = DF2["sht31d"].mean()
    sht_var_median = DF2["sht31d"].median()
    print("\tSHT31D\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (sht_var_max,
        sht_var_min,
        sht_var_mean,
        sht_var_median))

    lps_var_max = DF2["lps35hw"].max()
    lps_var_min = DF2["lps35hw"].min()
    lps_var_mean = DF2["lps35hw"].mean()
    lps_var_median = DF2["lps35hw"].median()
    print("\tLPS3x\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (lps_var_max,
        lps_var_min,
        lps_var_mean,
        lps_var_median))

    lps22_var_max = DF2["lps22"].max()
    lps22_var_min = DF2["lps22"].min()
    lps22_var_mean = DF2["lps22"].mean()
    lps22_var_median = DF2["lps22"].median()
    print("\tLPS22\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (lps22_var_max,
        lps22_var_min,
        lps22_var_mean,
        lps22_var_median))

    htu_var_max = DF2["htu21"].max()
    htu_var_min = DF2["htu21"].min()
    htu_var_mean = DF2["htu21"].mean()
    htu_var_median = DF2["htu21"].median()
    print("\tHTU21\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (htu_var_max,
        htu_var_min,
        htu_var_mean,
        htu_var_median))

    si7021_var_max = DF2["si7021"].max()
    si7021_var_min = DF2["si7021"].min()
    si7021_var_mean = DF2["si7021"].mean()
    si7021_var_median = DF2["si7021"].median()
    print("\tSi7021\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (si7021_var_max,
        si7021_var_min,
        si7021_var_mean,
        si7021_var_median))

    lps25_var_max = DF2["lps25"].max()
    lps25_var_min = DF2["lps25"].min()
    lps25_var_mean = DF2["lps25"].mean()
    lps25_var_median = DF2["lps25"].median()
    print("\tLPS25\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (lps25_var_max,
        lps25_var_min,
        lps25_var_mean,
        lps25_var_median))

    print("")


    # Histograms of the variance

    out_file = "%s/variance_hist.jpg" % output_path
    plt.style.use('dark_background')
    hist = DF2.hist(bins=20, figsize=(12,5), layout=(3,5))
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

    ax.scatter(DataDF["pct2075"], DF2["pct2075"], c='y', s=0.1)
    b,m = polyfit(DataDF["pct2075"], DF2["pct2075"], 1)
    plt.plot(DataDF["pct2075"], b + m * DataDF["pct2075"], '-', c='y')

    ax.scatter(DataDF["hts221"], DF2["hts221"], c='m', s=0.1)
    b,m = polyfit(DataDF["hts221"], DF2["hts221"], 1)
    plt.plot(DataDF["hts221"], b + m * DataDF["hts221"], '-', c='m')

    ax.scatter(DataDF["mcp9808"], DF2["mcp9808"], c='xkcd:hot pink', s=0.1)
    b,m = polyfit(DataDF["mcp9808"], DF2["mcp9808"], 1)
    plt.plot(DataDF["mcp9808"], b + m * DataDF["mcp9808"], '-', c='xkcd:hot pink')

    ax.scatter(DataDF["sht31d"], DF2["sht31d"], c='xkcd:light yellow', s=0.1)
    b,m = polyfit(DataDF["sht31d"], DF2["sht31d"], 1)
    plt.plot(DataDF["sht31d"], b + m * DataDF["sht31d"], '-', c='xkcd:light yellow')

    ax.scatter(DataDF["lps35hw"], DF2["lps35hw"], c='c', s=0.1)
    b,m = polyfit(DataDF["lps35hw"], DF2["lps35hw"], 1)
    plt.plot(DataDF["lps35hw"], b + m * DataDF["lps35hw"], '-', c='c')

    ax.scatter(DataDF["lps22"], DF2["lps22"], c='xkcd:white', s=0.1)
    b,m = polyfit(DataDF["lps22"], DF2["lps22"], 1)
    plt.plot(DataDF["lps22"], b + m * DataDF["lps22"], '-', c='xkcd:white')

    ax.scatter(DataDF["htu21"], DF2["htu21"], c='xkcd:seafoam', s=0.1)
    b,m = polyfit(DataDF["htu21"], DF2["htu21"], 1)
    plt.plot(DataDF["htu21"], b + m * DataDF["htu21"], '-', c='xkcd:seafoam')

    ax.scatter(DataDF["si7021"], DF2["si7021"], c='xkcd:light orange', s=0.1)
    b,m = polyfit(DataDF["si7021"], DF2["si7021"], 1)
    plt.plot(DataDF["si7021"], b + m * DataDF["si7021"], '-', c='xkcd:light orange')

    ax.scatter(DataDF["lps25"], DF2["lps25"], c='xkcd:sky blue', s=0.1)
    b,m = polyfit(DataDF["lps25"], DF2["lps25"], 1)
    plt.plot(DataDF["lps25"], b + m * DataDF["lps25"], '-', c='xkcd:sky blue')

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
