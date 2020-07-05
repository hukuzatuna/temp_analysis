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

# data_path = "/home/pi/src/roomtemp/roomtemp_pi/output/data_in.csv"
data_path = "./data_in.csv"
output_path = "./images/"

color_data = {
    'bme280'   : 'b',
    'dps310'   : 'g',
    'pct2075'  : 'y',
    'hts221'   : 'm',
    'mcp9808'  : 'xkcd:hot pink',
    'sht31d'   : 'xkcd:light yellow',
    'htu21d'   : 'xkcd:seafoam',
    'si7021'   : 'xkcd:light orange',
    'shtc3'    : 'xkcd:goldenrod',
    'aht20'    : 'xkcd:light violet',
    'mean'     : 'r',
}
    # 'lps35hw'  : 'c',


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
    # Col_Names = ["bme280","dps310","pct2075","hts221","mcp9808","sht31d",
    #     "lps35hw","lps22","htu21","si7021","lps25","mean"]
    Col_Names = ["dps310","pct2075","hts221","mcp9808","lps35hw","sht31d",
            "si7021","htu21d","shtc3","aht20","mean","press","rh"]
    tempDF = pd.read_csv(data_path, names=Col_Names)

    DataDF = tempDF.drop("lps35hw",1)

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

    for sensor in DataDF.keys():
        if "press" != sensor and "rh" != sensor:
            ax.plot(x, DataDF[sensor], c=color_data[sensor], ls='-', label=sensor, linewidth=0.5)

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
    for sensor in DataDF.keys():
        if "press" != sensor and "rh" != sensor:
            DF2[sensor] = DataDF[sensor] - DataDF['mean']

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

    for sensor in DF2.keys():
        if "press" != sensor and "rh" != sensor:
            ax.plot(x, DF2[sensor], c=color_data[sensor], ls='-', label=sensor, linewidth=0.5)

    plt.legend()
    out_file = "%s/variance_around_mean.jpg" % output_path
    # plt.show()
    plt.savefig(out_file)

    #----------------------------------------------
    # Statistics of the variance
    #----------------------------------------------

    print("\nSensor Variance Around The Mean:")
    print("\tSensor\tMax\tMin\tMean\tMedian")

    for sensor in DF2.keys():
        t_var_max = DF2[sensor].max()
        t_var_min = DF2[sensor].min()
        t_var_mean = DF2[sensor].mean()
        t_var_median = DF2[sensor].median()
        print("\t%s\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (sensor,
            t_var_max,
            t_var_min,
            t_var_mean,
            t_var_median))

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

    for sensor in DataDF.keys():
        if "press" != sensor and "rh" != sensor:
            ax.scatter(DataDF[sensor], DF2[sensor], c=color_data[sensor], s=0.1,
                label='_nolegend_')
            b,m = polyfit(DataDF[sensor], DF2[sensor], 1)
            plt.plot(DataDF[sensor], b + m * DataDF[sensor], '-', linewidth=0.4,
                c=color_data[sensor], label=sensor)

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
