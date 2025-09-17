# CODE FOR READING IN THE VICTORIA COVID DATA FILE
import pandas as pd


# Filters through Covid Data
def CovidDataFilter(dataset):
    filtered_data = dataset.loc[:, ["diagnosis_date", "Postcode"]]

    # Getting only 2020 dates
    year = 2020
    filtered_data['diagnosis_date'] = pd.to_datetime(filtered_data['diagnosis_date'], format="%Y-%m-%d")
    filtered_data = filtered_data[filtered_data['diagnosis_date'].dt.year == year]  # to include a specific Year

    # adds a Column to count each Case
    filtered_data["case_count"] = 1

    # Groups by the Postcode and adds counts the Cases on each Date
    filtered_data.columns = ['date', 'postcode', 'covid cases']
    filtered_data = filtered_data.groupby(["postcode", "date"]).sum()

    return filtered_data

# Generalises the Data to Victoria overall
def covidDataVictoria(dataset):
    filtered_data = dataset

    filtered_data = filtered_data.groupby(['date']).sum()

    return filtered_data


# Main
covid_data = pd.read_csv(r"datasets/CovidCases.csv")
covid_data = CovidDataFilter(covid_data)
print(covid_data.head(5))
covid_data.to_csv('processedCovidDataRegional.csv')  # Saving Database for Visualisation

covid_data_victoria = covidDataVictoria(covid_data)
print(covid_data_victoria.head(5))
covid_data_victoria.to_csv('processedCovidDataVictoria.csv')
