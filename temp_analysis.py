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
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import polyfit
import sklearn
import hashlib
from sklearn.model_selection import train_test_split


# Third-party modules

# Package/application modules


######################
# Globals
######################

data_path = "./TempData.csv"
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

def test_set_check(identifier, test_ratio, hash):
    return(hash(np.int64(identifier)).digets()[-1] < 256 * test_ratio)


def split_train_test_by_id(data, test_ratio, id_column, has=hashlib.md5):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio, hash))
    return(data.loc[~in_test_set], data.loc[in_test_set])


def main():

    # Read the data into a matrix
    # Col_Names = ["bme280","dps310","pct2075","hts221","mcp9808","sht31d",
    #     "lps35hw","lps22","htu21","si7021","lps25","mean"]
    Col_Names = ["dps310","pct2075","hts221","mcp9808","lps35hw","sht31d",
            "si7021","htu21d","shtc3","aht20","mean","pressure","rh"]
    tempDF = pd.read_csv(data_path, names=Col_Names)

    # Add an index column
    # DataDF = tempDF.reset_index()
    
    # Remove sensors with known-bad data
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
        if "pressure" != sensor and "rh" != sensor:
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
        if "pressure" != sensor and "rh" != sensor:
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
        if "pressure" != sensor and "rh" != sensor:
            ax.plot(x, DF2[sensor], c=color_data[sensor], ls='-', label=sensor, linewidth=0.5)

    plt.legend()
    out_file = "%s/variance_around_mean.jpg" % output_path
    # plt.show()
    plt.savefig(out_file)

    #----------------------------------------------
    # Statistics of the variance
    #----------------------------------------------

    print("\nSensor Variance Around The Mean\n")
    print("Sensor\tMax\tMin\tMean\tMedian")

    for sensor in DF2.keys():
        if "pressure" != sensor and "rh" != sensor:
            t_var_max = DF2[sensor].max()
            t_var_min = DF2[sensor].min()
            t_var_mean = DF2[sensor].mean()
            t_var_median = DF2[sensor].median()
            print("%s\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (sensor,
                t_var_max,
                t_var_min,
                t_var_mean,
                t_var_median))

    print("")


    # Histograms of the variance

    # out_file = "%s/variance_hist.jpg" % output_path
    # plt.style.use('dark_background')
    # hist = DF2.hist(bins=20, figsize=(12,5), layout=(3,5))
    # plt.savefig(out_file)

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
        if "pressure" != sensor and "rh" != sensor:
            ax.scatter(DataDF[sensor], DF2[sensor], c=color_data[sensor], s=0.1,
                label='_nolegend_')
            b,m = polyfit(DataDF[sensor], DF2[sensor], 1)
            plt.plot(DataDF[sensor], b + m * DataDF[sensor], '-', linewidth=0.4,
                c=color_data[sensor], label=sensor)

    plt.legend()
    out_file = "%s/VarxTemp.jpg" % output_path
    plt.savefig(out_file)

    # Temperature by pressure
    
    plt.style.use('dark_background')
    fig = plt.figure()
    fig.set_size_inches(12,5)
    fig.dpi = 300
    ax = fig.add_subplot(111)
    ax.set_ylabel('Temperature')
    ax.set_xlabel('Pressure')
    ax.set_title('Sensor Dependency on Pressure')

    for sensor in DataDF.keys():
        if "pressure" != sensor and "rh" != sensor:
            ax.scatter(DataDF["pressure"], DataDF[sensor], c=color_data[sensor], s=0.1,
                label='_nolegend_')
            b,m = polyfit(DataDF["pressure"], DataDF[sensor], 1)
            plt.plot(DataDF["pressure"], b + m * DataDF[sensor], '-', linewidth=0.4,
                c=color_data[sensor], label=sensor)

    plt.legend()
    out_file = "%s/TempxPress.jpg" % output_path
    plt.savefig(out_file)

    # Temperature by humidity
    
    plt.style.use('dark_background')
    fig = plt.figure()
    fig.set_size_inches(12,5)
    fig.dpi = 300
    ax = fig.add_subplot(111)
    ax.set_ylabel('Temperature')
    ax.set_xlabel('Humidity')
    ax.set_title('Sensor Dependency on Humidity')

    for sensor in DataDF.keys():
        if "pressure" != sensor and "rh" != sensor:
            ax.scatter(DataDF["rh"], DataDF[sensor], c=color_data[sensor], s=0.1,
                label='_nolegend_')
            b,m = polyfit(DataDF["rh"], DataDF[sensor], 1)
            plt.plot(DataDF["rh"], b + m * DataDF[sensor], '-', linewidth=0.4,
                c=color_data[sensor], label=sensor)

    plt.legend()
    out_file = "%s/TempxRH.jpg" % output_path
    plt.savefig(out_file)


    #################################################
    # 
    # Machine Learning Time
    #
    #################################################

    # Set aside a test set. Really want to use leave-one-out k-fold validation,
    # but we'll get to that.

    train_set, test_set = train_test_split(DataDF, test_size=0.2)

    # Correlation

    print("Correlation Matrix\n")    
    corr_matrix = DataDF.corr()
    print(corr_matrix)
    print("")

    # Correlation scatter matrix (not really useful)

    # plt.style.use('dark_background')
    # fig = plt.figure()
    # fig.set_size_inches(10,10)
    # fig.dpi = 300
    # ax = fig.add_subplot(111)
    # ax.set_title('Correlation Matrix Scatter Plots')

    # pd.plotting.scatter_matrix(corr_matrix)

    # out_file = "%s/CorrScatter.jpg" % output_path
    # plt.savefig(out_file)

  
######################
# Main
######################

# The main code call allows this module to be imported as a library or
# called as a standalone program because __name__ will not be properly
# set unless called as a program.

if __name__ == "__main__":
    main()
