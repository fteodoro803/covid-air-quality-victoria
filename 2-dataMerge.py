# MERGES ALL PROCESSED DATA
import pandas as pd


# FUNCTIONS
# Merges Datasets based on a particular Region
def regionalDataMerge(dataAirQuality, dataCovid, dataPostcode):
    # Merge Postcode and Air Quality
    dataset = dataAirQuality.set_index('suburb').join(dataPostcode.set_index('suburb'))
    dataset.reset_index(drop=False, inplace=True)

    # Merge Postcode and Covid
    dataset['postcode'] = pd.to_numeric(dataset['postcode'])  # Refer to end of file (1)
    dataCovid['postcode'] = pd.to_numeric(dataCovid['postcode'])
    dataset = pd.merge(dataset, dataCovid, how='left')

    return dataset

# Merges Datasets based on Victoria
def victoriaDataMerge(dataAirQuality, dataCovid, dataMovement):
    dataset = pd.merge(dataAirQuality, dataMovement, how='outer')
    dataset = pd.merge(dataset, dataCovid, how='outer')
    return dataset


# MAIN
# Reading Regional Files
airQualityDataRegional = pd.read_csv('processedAirQualityDataRegional.csv', encoding='ISO-8859-1', dtype='unicode')
covidDataRegional = pd.read_csv('processedCovidDataRegional.csv', encoding='ISO-8859-1', dtype='unicode')
postcodeSuburbData = pd.read_csv('processedSuburbPostcodeData.csv', encoding='ISO-8859-1', dtype='unicode')

# Reading General Victoria Files
airQualityDataVictoria = pd.read_csv('processedAirQualityDataVictoria.csv', encoding='ISO-8859-1', dtype='unicode')
covidDataVictoria = pd.read_csv('processedCovidDataVictoria.csv', encoding='ISO-8859-1', dtype='unicode')
movementData = pd.read_csv('processedMovementData.csv', encoding='ISO-8859-1', dtype='unicode')

# Merging Datasets
regionalData = regionalDataMerge(airQualityDataRegional, covidDataRegional, postcodeSuburbData)
print(regionalData.head(5))
regionalData.to_csv('rawMergedRegionalData.csv', index=False)

victoriaData = victoriaDataMerge(airQualityDataVictoria, covidDataVictoria, movementData)
print(victoriaData.head(5))
victoriaData.to_csv('rawMergedVictoriaData.csv', index=False)

# Dataset for Merging Later on
dateData = airQualityDataVictoria['date']
dateData.to_csv('toMerge-Dates.csv', index=False)

"""
    1. fix from https://stackoverflow.com/questions/39582984/pandas-merging-on-string-columns-not-working-bug
        - i was running into issues where i would get NaN when I wasn't expecting it
"""
