# CODE FOR READING IN THE EPA AIRWATCH FILE
import pandas as pd
import os


# FUNCTIONS
# Filters through the Air Quality Files
def airQualityDataFilter2020():
    datasetPresence = 0

    # Go through every Dataset in the Folder (must be csv)
    files = []
    directory = os.listdir('datasets/AirQuality2020')
    for i in range(len(directory)):
        files.append(f"datasets/AirQuality2020/{directory[i]}")

    # DataFrame Merge Loop
    for i in range(len(files)):
        if (datasetPresence == 0):  # Initialising Merged DataFrame
            dataset = pd.read_csv(files[i], encoding='ISO-8859-1', dtype='unicode')
            datasetPresence = 1
        else:
            newDataset = pd.read_csv(files[i], encoding='ISO-8859-1', dtype='unicode')
            dataset = pd.concat([dataset, newDataset])

    # Choosing the Pollutants that matter to Air Quality: https://www.epa.vic.gov.au/for-community/monitoring-your-environment/about-epa-airwatch/calculate-air-quality-categories
    #   - According to site: PM2.5, PM10, Ozone, Nitrogen Dioxide, Sulfur Dioxide
    #   - In the sheet, that would be: 'BAM  Particles < 2.5 micron', 'TEOM Particles <10micron', 'Ozone', 'Nitrogen Dioxide', 'Sulfur Dioxide'
    air_quality_data = dataset.loc[:, ('location_name', 'datetime_local', 'BPM2.5', 'PM10', 'O3', 'NO2', 'SO2',
                                       'CO')]

    # Consistency Preprocessing
    air_quality_data.columns = ['suburb', 'date', 'BPM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO']  # Renaming Column
    air_quality_data['suburb'] = air_quality_data['suburb'].str.lower()

    # get only 2020 (some data points go into last day of 2019, start of 2021)
    year = 2020
    air_quality_data['date'] = pd.to_datetime(air_quality_data['date'], format="%Y-%m-%d")
    air_quality_data = air_quality_data[air_quality_data['date'].dt.year == year]  # to include a specific Year

    # Changing Datatypes
    # datetime
    air_quality_data['date'] = pd.to_datetime(air_quality_data['date']).dt.date

    # float
    air_quality_data['BPM2.5'] = pd.to_numeric(air_quality_data['BPM2.5'])
    air_quality_data['PM10'] = pd.to_numeric(air_quality_data['PM10'])
    air_quality_data['O3'] = pd.to_numeric(air_quality_data['O3'])
    air_quality_data['NO2'] = pd.to_numeric(air_quality_data['NO2'])
    air_quality_data['SO2'] = pd.to_numeric(air_quality_data['SO2'])
    air_quality_data['CO'] = pd.to_numeric(air_quality_data['CO'])

    # GroupBy
    air_quality_data = air_quality_data.groupby(['suburb', 'date'])[['BPM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO']].mean()

    return air_quality_data

# Generalises everything from every Location to an average Victoria
def generateVictoriaData(file):
    air_quality_data = file
    air_quality_data = air_quality_data.groupby(['date'])[['BPM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO']].mean()
    return air_quality_data


# MAIN
pd.set_option('display.max_columns', None)  # test

AirQualityData2020 = airQualityDataFilter2020()
print(AirQualityData2020.head(5))
AirQualityData2020.to_csv('processedAirQualityDataRegional.csv')

AirQualityVictoriaData = generateVictoriaData(airQualityDataFilter2020())
print(AirQualityVictoriaData.head(5))
AirQualityVictoriaData.to_csv('processedAirQualityDataVictoria.csv')

"""
    1. Air Pollutant Categories from
https://www.epa.vic.gov.au/for-community/monitoring-your-environment/about-epa-airwatch/calculate-air-quality-categories
"""
