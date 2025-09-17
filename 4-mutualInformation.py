# MUTUAL INFORMATION ANALYSI
import pandas as pd
from sklearn.metrics import mutual_info_score
import math
import numpy as np

# Calculates Mutual Information Value
def calc_MI(x, y, bins):
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    mi = mi / math.log(2)  # Conversion to log2 from loge
    return mi

# Calculates Mutual Information from a Dataset
def calcMIDataFrame(dataset, column1, column2, bins=3):  # 3 was arbitrarily chosen, refer to Report
    filteredDataset = dataset[[column1, column2]]
    filteredDataset = filteredDataset.dropna()  # to Match number of Data Points
    return calc_MI(filteredDataset[column1], filteredDataset[column2], bins)


# MAIN
datasetVictoria = pd.read_csv('finalVictoriaData.csv')
datasetRegional = pd.read_csv('finalfootscrayData.csv')
with open('statisticalAnalysisResults.txt', 'w') as f:
    # Victoria
    # Movement vs Pollutants
    print('Movement vs Pollutants in Victoria')
    f.write('Movement vs Pollutants in Victoria\n')
    print(
        f"\tMovement & BPM2.5: {calcMIDataFrame(datasetVictoria, 'average', 'BPM2.5')}")  # average == averageMovement
    f.write(f"\tMovement & BPM2.5: {calcMIDataFrame(datasetVictoria, 'average', 'BPM2.5')}\n")
    print(f"\tMovement & PM10: {calcMIDataFrame(datasetVictoria, 'average', 'PM10')}")
    f.write(f"\tMovement & PM10: {calcMIDataFrame(datasetVictoria, 'average', 'PM10')}\n")
    print(f"\tMovement & O3: {calcMIDataFrame(datasetVictoria, 'average', 'O3')}")
    f.write(f"\tMovement & O3: {calcMIDataFrame(datasetVictoria, 'average', 'O3')}\n")
    print(f"\tMovement & NO2: {calcMIDataFrame(datasetVictoria, 'average', 'NO2')}")
    f.write(f"\tMovement & NO2: {calcMIDataFrame(datasetVictoria, 'average', 'NO2')}\n")
    print(f"\tMovement & CO: {calcMIDataFrame(datasetVictoria, 'average', 'CO')}")
    f.write(f"\tMovement & CO: {calcMIDataFrame(datasetVictoria, 'average', 'CO')}\n")
    print(f"\tMovement & SO2: {calcMIDataFrame(datasetVictoria, 'average', 'SO2')}")
    f.write(f"\tMovement & SO2: {calcMIDataFrame(datasetVictoria, 'average', 'SO2')}\n")

    # Covid Cases vs Pollutants
    print('Covid Cases vs Pollutants in Victoria')
    f.write('Covid Cases vs Pollutants in Victoria\n')
    print(f"\tCovid Cases & BPM2.5: {calcMIDataFrame(datasetVictoria, 'covid cases', 'BPM2.5')}")
    f.write(f"\tCovid Cases & BPM2.5: {calcMIDataFrame(datasetVictoria, 'covid cases', 'BPM2.5')}\n")
    print(f"\tCovid Cases & PM10: {calcMIDataFrame(datasetVictoria, 'covid cases', 'PM10')}")
    f.write(f"\tCovid Cases & PM10: {calcMIDataFrame(datasetVictoria, 'covid cases', 'PM10')}\n")
    print(f"\tCovid Cases & O3: {calcMIDataFrame(datasetVictoria, 'covid cases', 'O3')}")
    f.write(f"\tCovid Cases & O3: {calcMIDataFrame(datasetVictoria, 'covid cases', 'O3')}\n")
    print(f"\tCovid Cases & NO2: {calcMIDataFrame(datasetVictoria, 'covid cases', 'NO2')}")
    f.write(f"\tCovid Cases & NO2: {calcMIDataFrame(datasetVictoria, 'covid cases', 'NO2')}\n")
    print(f"\tCovid Cases & CO: {calcMIDataFrame(datasetVictoria, 'covid cases', 'CO')}")
    f.write(f"\tCovid Cases & CO: {calcMIDataFrame(datasetVictoria, 'covid cases', 'CO')}\n")
    print(f"\tCovid Cases & SO2: {calcMIDataFrame(datasetVictoria, 'covid cases', 'SO2')}")
    f.write(f"\tCovid Cases & SO2: {calcMIDataFrame(datasetVictoria, 'covid cases', 'SO2')}\n")

    # Regional
    print('Covid Cases vs Pollutants in Region')
    f.write('Covid Cases vs Pollutants in Region\n')
    print(f"\tCovid Cases & BPM2.5: {calcMIDataFrame(datasetRegional, 'covid cases', 'BPM2.5')}")
    f.write(f"\tCovid Cases & BPM2.5: {calcMIDataFrame(datasetRegional, 'covid cases', 'BPM2.5')}\n")
    print(f"\tCovid Cases & PM10: {calcMIDataFrame(datasetRegional, 'covid cases', 'PM10')}")
    f.write(f"\tCovid Cases & PM10: {calcMIDataFrame(datasetRegional, 'covid cases', 'PM10')}\n")
    print(f"\tCovid Cases & O3: {calcMIDataFrame(datasetRegional, 'covid cases', 'O3')}")
    f.write(f"\tCovid Cases & O3: {calcMIDataFrame(datasetRegional, 'covid cases', 'O3')}\n")
    print(f"\tCovid Cases & NO2: {calcMIDataFrame(datasetRegional, 'covid cases', 'NO2')}")
    f.write(f"\tCovid Cases & NO2: {calcMIDataFrame(datasetRegional, 'covid cases', 'NO2')}\n")
    print(f"\tCovid Cases & CO: {calcMIDataFrame(datasetRegional, 'covid cases', 'CO')}")
    f.write(f"\tCovid Cases & CO: {calcMIDataFrame(datasetRegional, 'covid cases', 'CO')}\n")
    # print(f"\tCovid Cases & SO2: {calcMIDataFrame(datasetRegional, 'covid cases', 'SO2')}")
    # f.write(f"\tCovid Cases & SO2: {calcMIDataFrame(datasetRegional, 'covid cases', 'SO2')}\n")

f.close()

"""
EXTERNAL CODE REFERENCES:
    - calc_MI by Warren Weckesser, from https://stackoverflow.com/a/20505476
    
"""
