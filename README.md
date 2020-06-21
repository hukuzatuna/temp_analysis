# Analytic Comparison of Temperature Sensor Chips

Philip R. Moyer (phil@moyer.ai)
June 2020

## Abstract

This analysis compares the performance characteristics of commonly-available
temperature sensing chipsets.

## Keywords

## Introduction

Many electronic temperature sensors are available on the market. Each
of these chips have associated Data Sheets that document the performance
characteristics of each chipset. When selectng a temperature sensor, system
designers will need to read cnd ompare each Data Sheet in order to select
the right component. Other considerations, not in scope for this analysis,
are associated sensors (e.g., pressure, humidity), electrical characteristics,
physical dimensions, sampling rate, and interafces available (e.g., I2C, SPI).
This analysis, though wll be of interest because temperature performance
will be presented in on the same graphs.

## Materials and Methods

This analysis uses the following hardware:

- [Raspberry Pi 4 8GB](https://www.adafruit.com/product/4564)
- ICE Tower cooling system
- Raspberry Pi mouse and keyboard
- Samsung HDTV as a monitor
- [Adafruit BME280]{https://www.adafruit.com/product/2652) temperature sensor
- [Adafruit DPS310](https://www.adafruit.com/product/4494) temperature sensor
- [Adafruit LPS35HW](https://www.adafruit.com/product/4258) temperatuere sensor
- [Adafruit Sensiron SHTC3](https://www.adafruit.com/product/4636) temperatue sensor
- [Adafruit AHT20](https://www.adafruit.com/product/4566) temperature sensor
- [Adafruit LPS22](https://www.adafruit.com/product/4633) temperature sensor
- [Adafruit LPS25](https://www.adafruit.com/product/4530) temperature sensor
- [Adafruit PCT2075](https://www.adafruit.com/product/4566) temperature sensor
- [Adafruit HTS221](https://www.adafruit.com/product/4535)temperature sensor
- 1/4 breadboard
- DuPont jumpers
- 60 watt power supply

## Results and Discussion

![Time Series](/images/time_series_001.jpg)

![Variance around the mean](/images/variance_around_mean.jpg)

![Histogram of variance around the mean](/images/variance_hist.jpg)

![Variance by temperature, with regression](/images/VarxTemp.jpg)

## Conclusions

## Acknowledgements

## References

- [Bosch Sensortec BME280](https://ae-bst.resource.bosch.com/media/_tech/media/product_flyer/BST-BME280-FL000.pdf)
- [BME280 Data Sheet](https://ae-bst.resource.bosch.com/media/_tech/media/datasheets/BST-BME280-DS002.pdf)
- Infineon Technologies DPS310
- [DPS310 Data Sheet](https://www.infineon.com/dgdl/Infineon-DPS310-DS-v01_00-EN.pdf?fileId=5546d462576f34750157750826c42242)
- STMicroelectronics LPS35HW
- [LPS35HW Data Sheet](http://www.st.com/content/ccc/resource/technical/document/datasheet/group3/61/1f/dc/f4/51/bc/49/82/DM00280413/files/DM00280413.pdf/jcr:content/translations/en.DM00280413.pdf)
- Sensiron SHTC3 temperature sensor
- [Sensirion AG Data Sheet](https://media.digikey.com/pdf/Data%20Sheets/Sensirion%20PDFs/HT_DS_SHTC3_D1.pdf]
- AHT20 temperature sensor
- [AHT20 Data Sheet](https://cdn-learn.adafruit.com/assets/assets/000/091/676/original/AHT20-datasheet-2020-4-16.pdf?1591047915)
- LPS22 temperature sensor
- Data Sheet
- LPS25 temperature sensor
- Data Sheet
- PCT2075 temperature sensor
- Data Sheet
- HTS221 temperature sensor
- Data Sheet

