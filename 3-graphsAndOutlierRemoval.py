# GRAPHS AND OUTLIER REMOVAL
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# FUNCTIONS
# Movement Graph
def getMovement(dataset):  # Victoria-Only Function

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthStart = [13 - 1, 32 - 1, 61 - 1, 92 - 1, 122 - 1, 153 - 1, 183 - 1, 214 - 1, 245 - 1, 275 - 1, 306 - 1,
                  336 - 1]  # Jan is 13 because that's when they started recording data

    plt.xticks(monthStart, months)
    plt.yticks([20, 40, 60, 80, 100, 120], ['20%', '40%', '60%', '80%', '100%', '120%'])
    # plt.scatter(dataset['date'], dataset['driving'], c='b', label='driving')
    # plt.scatter(dataset['date'], dataset['transit'], c='r', label='transit')
    plt.scatter(dataset['date'], dataset['average'], c='g', label='average')
    plt.legend(loc="upper right")
    plt.title(f"Movement in 2020")
    plt.xlabel('month')
    plt.ylabel('movement (100 is baseline)')
    # plt.show()
    plt.savefig(f"graph-victoria-movement.png")
    plt.clf()

    # Saving a CSV for Stat Analysis ()
    movementStatAnalaysis = dataset[['date', 'average']]
    movementStatAnalaysis.to_csv('toMerge-Transport.csv', index=False)

    return


# Covid Case Graph
def getCovidCases(suburb='victoria'):
    if suburb == 'victoria':
        dataset = pd.read_csv('rawMergedVictoriaData.csv')
    else:
        dataset = pd.read_csv('rawMergedRegionalData.csv')

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthStart = [1 - 1, 32 - 1, 61 - 1, 92 - 1, 122 - 1, 153 - 1, 183 - 1, 214 - 1, 245 - 1, 275 - 1, 306 - 1,
                  336 - 1]  # refer to end of file
    plt.xticks(monthStart, months)
    if suburb != 'victoria':
        dataset = dataset.loc[dataset['suburb'] == suburb]  # filtering dataset to suburb

    plt.scatter(dataset['date'], dataset['covid cases'])
    plt.title(f"Confirmed Covid Cases in {suburb}")
    plt.xlabel('month')
    plt.ylabel('cases')
    # plt.show()
    plt.savefig(f"graph-{suburb}-covid.png")
    plt.clf()

    # toMerge Covid
    covidStatAnalysis = dataset[['date', 'covid cases']]
    covidStatAnalysis.to_csv(f"toMerge-{suburb}-Covid.csv", index=False)

    return


# Air Quality Graph
def getAirQuality(pollutant, suburb='victoria', indicatorLines=0):
    if suburb == 'victoria':
        dataset = pd.read_csv('rawMergedVictoriaData.csv')
    else:
        dataset = pd.read_csv('rawMergedRegionalData.csv')
        dataset = dataset.loc[dataset['suburb'] == suburb]  # filtering dataset to suburb

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthStart = [1 - 1, 32 - 1, 61 - 1, 92 - 1, 122 - 1, 153 - 1, 183 - 1, 214 - 1, 245 - 1, 275 - 1, 306 - 1,
                  336 - 1]
    # parameter numbers are quality indicators from EPA Victoria (refer to end of file)
    parameters = {'BPM2.5': ['Particulate Matter of <=2.5 microns', 'ug/m3', [25, 50, 100, 300]],
                  'PM10': ['Particulate Matter of <=10 microns', 'ug/m3', [40, 80, 120, 300]],
                  'O3': ['Ozone', 'ppb', [50, 100, 150, 300]],
                  'NO2': ['Nitrogen Dioxide', 'ppb', [60, 120, 180, 360]],
                  'SO2': ['Sulphur Dioxide', 'ppb', [100, 200, 300, 600]],
                  'CO': ['Carbon Monoxide', 'ppm', [30, 70]]}

    if pollutant in parameters.keys():
        filteredDataset = removePollutantOutliers(dataset, pollutant)  # Removes Outliers

        # Saves Outlier-less CSV
        filteredDataset.to_csv(f"toMerge-{suburb}-{pollutant}.csv", index=False)

        plt.xticks(monthStart, months)
        plt.scatter(filteredDataset['date'], filteredDataset[pollutant])
        plt.title(f"{parameters[pollutant][0]} in {suburb} in 2020")
        plt.xlabel('month')
        plt.ylabel(parameters[pollutant][1])
        if indicatorLines == 1:
            for i in range(len(parameters[pollutant][2])):  # every indicator line
                horizontalLineHeight = []
                for j in range(len(filteredDataset)):  # every day
                    horizontalLineHeight.append(parameters[pollutant][2][i])
                plt.scatter(filteredDataset['date'], horizontalLineHeight)

        # plt.show()
        plt.savefig(f"graph-{suburb}-{pollutant}.png")
        plt.clf()

    else:  # prints every other pollutant
        for param in parameters.keys():
            filteredDataset = removePollutantOutliers(dataset, param)  # removes Outliers

            if len(filteredDataset) == 0:  # Skipping if Empty Dataframe
                continue

            # saves Outlier-less CSV
            filteredDataset.to_csv(f"toMerge-{suburb}-{param}.csv", index=False)

            plt.xticks(monthStart, months)
            plt.scatter(filteredDataset['date'], filteredDataset[param])
            plt.title(f"{parameters[param][0]} in {suburb} in 2020")
            plt.xlabel('month')
            plt.ylabel(parameters[param][1])
            if indicatorLines == 1:
                for i in range(len(parameters[param][2])):  # every indicator line
                    horizontalLineHeight = []
                    for j in range(len(dataset)):  # every day
                        horizontalLineHeight.append(parameters[param][2][i])
                    plt.scatter(dataset['date'], horizontalLineHeight)

            # plt.show()
            plt.savefig(f"graph-{suburb}-{param}.png")
            plt.clf()
    return


# Removes Pollutant Outliers from Dataset
def removePollutantOutliers(dataset, pollutant):
    reducedDataset = dataset[['date', pollutant]]
    reducedDataset = reducedDataset.dropna()  # ignoring NaN values

    # Breaks if Dataset after Filtering is Empty
    if len(reducedDataset) == 0:
        return pd.DataFrame()  # return empty dataframe

    # Box Plot
    # boxPlot = plt.boxplot(reducedDataset[pollutant])
    # plt.show()

    # get points with outliers
    firstQuartile = np.percentile(reducedDataset[pollutant], 25)
    thirdQuartile = np.percentile(reducedDataset[pollutant], 75)

    iqr = thirdQuartile - firstQuartile
    upperBound = thirdQuartile + (1.5 * iqr)
    lowerBound = firstQuartile - (1.5 * iqr)
    # print(f"Lower Bound: {lowerBound}")
    # print(f"Upper Bound: {upperBound}")

    upperBoundDataset = reducedDataset[reducedDataset[pollutant] < upperBound]  # Everything Less than Upper Bound
    lowerBoundDataset = reducedDataset[reducedDataset[pollutant] > lowerBound]  # Everything Greater than Lower Bound

    # Inner Merge
    noOutlierDataset = pd.merge(upperBoundDataset, lowerBoundDataset, how='inner')

    return noOutlierDataset

# Re-Merges all the CSVs
def refinedMergeRegional(suburb):
    # Manually comment which Datasets are Available
    dataDates = pd.read_csv('toMerge-Dates.csv')
    dataCovid = pd.read_csv(f'toMerge-{suburb}-Covid.csv')
    dataBPM25 = pd.read_csv(f'toMerge-{suburb}-BPM2.5.csv')
    dataPM10 = pd.read_csv(f'toMerge-{suburb}-PM10.csv')
    dataO3 = pd.read_csv(f'toMerge-{suburb}-O3.csv')
    dataNO2 = pd.read_csv(f'toMerge-{suburb}-NO2.csv')
    dataCO = pd.read_csv(f'toMerge-{suburb}-CO.csv')
    # dataSO2 = pd.read_csv(f'toMerge-{suburb}-SO2.csv')

    # Manually comment which Datasets are Available (must correspond to one above)
    dataset = pd.merge(dataDates, dataCovid, how='outer')
    dataset = pd.merge(dataset, dataBPM25, how='outer')
    dataset = pd.merge(dataset, dataPM10, how='outer')
    dataset = pd.merge(dataset, dataO3, how='outer')
    dataset = pd.merge(dataset, dataNO2, how='outer')
    dataset = pd.merge(dataset, dataCO, how='outer')
    # dataset = pd.merge(dataset, dataSO2, how='outer')

    # print(dataset)
    dataset.to_csv(f'final{suburb}Data.csv', index=False)

    return

# Re-Merges all the CSVs
def refinedMergeVictoria():
    dataDates = pd.read_csv('toMerge-Dates.csv')
    dataTransport = pd.read_csv('toMerge-Transport.csv')
    dataCovid = pd.read_csv('toMerge-victoria-Covid.csv')
    dataBPM25 = pd.read_csv('toMerge-victoria-BPM2.5.csv')
    dataPM10 = pd.read_csv('toMerge-victoria-PM10.csv')
    dataO3 = pd.read_csv('toMerge-victoria-O3.csv')
    dataNO2 = pd.read_csv('toMerge-victoria-NO2.csv')
    dataCO = pd.read_csv('toMerge-victoria-CO.csv')
    dataSO2 = pd.read_csv('toMerge-victoria-SO2.csv')

    dataset = pd.merge(dataDates, dataCovid, how='outer')
    dataset = pd.merge(dataset, dataTransport, how='outer')
    dataset = pd.merge(dataset, dataBPM25, how='outer')
    dataset = pd.merge(dataset, dataPM10, how='outer')
    dataset = pd.merge(dataset, dataO3, how='outer')
    dataset = pd.merge(dataset, dataNO2, how='outer')
    dataset = pd.merge(dataset, dataCO, how='outer')
    dataset = pd.merge(dataset, dataSO2, how='outer')

    # print(dataset)
    dataset.to_csv('finalVictoriaData.csv', index=False)

    return


# MAIN
dataRegional = pd.read_csv('rawMergedRegionalData.csv')
dataVictoria = pd.read_csv('rawMergedVictoriaData.csv')

# Victoria
getMovement(dataVictoria)  # Victoria-only Function
getCovidCases(suburb='victoria')  # leave blank for victoria
getAirQuality('all', suburb='victoria',
              indicatorLines=0)  # Parameters: 'BPM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO'. If not in list, graphs all

# Particular Region
location = 'footscray'  # Change This to get Others
getCovidCases(suburb=location)
getAirQuality('all', suburb=location, indicatorLines=0)

# Inner Merging on Date, for all Regional and Victorian Data
refinedMergeVictoria()
refinedMergeRegional('footscray')

"""
REFERENCES

- EPA Air Quality Indicators from 
https://www.epa.vic.gov.au/for-community/monitoring-your-environment/about-epa-airwatch/calculate-air-quality-categories

- Cumulative Number of Days at the end of each Month from https://cals.arizona.edu/azmet/julian.html

"""
