# CODE FOR READING IN THE UBER FILES
import pandas as pd


# FUNCTIONS
# Selects Victorian data
def movementDataFilter(file):
    dataset = pd.read_csv(file, encoding='ISO-8859-1', dtype='unicode')  # Opens CSV

    # Gets Rows where Region is Victoria, and where Transportation Type is by Vehicle
    movement_data = dataset.loc[(dataset['region'] == 'Victoria')]
    movement_data = movement_data[dataset['transportation_type'].isin(['driving', 'transit'])]

    # Gets every Specific Columns, and those in a Range
    movement_data = movement_data.iloc[:,[2] + list(range(6, len(dataset.columns)))]  # External Code Reference 1

    # Setting up the Dataset for Transpose
    movement_data = movement_data.reset_index()
    movement_data = movement_data.drop(movement_data.columns[0], axis=1)
    movement_data.set_index('transportation_type', inplace=True)
    movement_data = movement_data.transpose()

    # Gets only 2020 dates
    year = 2020  # the Year in the Scope
    movement_data.index.name = 'date'
    movement_data = movement_data.reset_index()
    movement_data['date'] = pd.to_datetime(movement_data['date'], format="%Y-%m-%d")
    movement_data = movement_data[movement_data['date'].dt.year == year]  # to include a specific Year

    # Setting the other Datatype Values to Floats
    movement_data['driving'] = pd.to_numeric(movement_data['driving'])
    movement_data['transit'] = pd.to_numeric(movement_data['transit'])

    # Making an Averaged Column (idk, this might be needed)
    movement_data['average'] = movement_data[['driving','transit']].mean(axis=1)

    return movement_data


# MAIN
movementData = movementDataFilter('datasets/AppleMobilityTrend.csv')
print(movementData.head(5))
movementData.to_csv('processedMovementData.csv', index=False)  # Saving Database for Visualisation


"""
EXTERNAL CODE REFERENCES
    1. maciejwww, adapted from https://stackoverflow.com/a/64336534
    
"""
