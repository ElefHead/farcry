import pandas as pd
from os import path, makedirs, listdir
from json import dump, load
import numpy as np
from geopy.geocoders import Nominatim

from transform_scripts.constants import Constants


def read_csv(loc='', filename='', sep=',', header='infer', encoding='ISO-8859-1', dtype=None):
    '''
    Function to read csv into a pandas data frame

    :param dirname: `String` location of file
    :param filename: `String` name of file
    :param sep: `String` separator for csv: defaults to ',' [comma]
    :param header: `int or list of ints`, Same as pandas header :default 'infer' can be set to None
    :param encoding: `String` encoding type: defaults to ISO-8859-1
    :param dtype: `type object` default data read in type: defaults to Noner
    :return: `pandas dataframe` containing the contents of the csv
    '''
    read_path = path.join(loc, filename)
    return pd.read_csv(read_path, encoding=encoding, header=header, sep=sep, dtype=dtype)


def read_json(loc='', filename=''):
    file_path = path.join(loc, filename)
    with open(file_path, 'r') as f:
        data = load(f)
    return data


def read_data():
    state_mortality = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.STATE_MORTALITY, dtype=str)
    state_incidence = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.STATE_INCIDENCE, dtype=str)
    cancer_centers = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.CANCER_CENTERS, dtype=str)
    cancer_centers_per10m = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.CANCER_CENTERS_PER10M,
                                     dtype=str)

    return cancer_centers, cancer_centers_per10m, state_mortality, state_incidence


def convert_to_dict(df, key_col):
    d = {}
    keys = df[key_col]
    df = df.drop(key_col, axis=1)
    val_dicts = df.to_dict(orient='records')
    for i in range(df.shape[0]):
        key = keys[i]
        d[key] = val_dicts[i]

    return d


def transform_data():
    cancer_centers, cancer_centers_per10m, state_mortality, state_incidence = read_data()

    state_mortality_dict = convert_to_dict(state_mortality, 'State')
    state_incidence_dict = convert_to_dict(state_incidence, 'State')
    cancer_centers_per10m = convert_to_dict(cancer_centers_per10m, 'State')

    data_dict = {}

    for i in range(cancer_centers.shape[0]):
        state_name = cancer_centers['State'][i]
        if state_name in Constants.STATE_NAME:
            state_name = Constants.STATE_NAME[state_name]
        else:
            continue
        if state_name in Constants.STATE_CODES:
            state = Constants.STATE_CODES[state_name]
        else:
            continue
        lat = cancer_centers['Latitude'][i]
        lon = cancer_centers['Longitude'][i]
        name = cancer_centers['Institution Name'][i]
        state_type = cancer_centers['Type'][i]
        link = cancer_centers['Link'][i]

        if state not in data_dict:
            data_dict[state] = {}
            data_dict[state]['state_name'] = state_name
            data_dict[state]['state_code'] = Constants.STATE_NAMES_SHORTEN[state_name]
            data_dict[state]['incidence'] = state_incidence_dict[state_name]['All cancer incidence 2011-2015'] if state_incidence_dict[state_name]['All cancer incidence 2011-2015'] != "None" else None
            data_dict[state]['incidence_rank'] = state_incidence_dict[state_name]['cancer incidence rank'] if state_incidence_dict[state_name]['cancer incidence rank'] != "None" else None
            data_dict[state]['mortality'] = state_mortality_dict[state_name]['Age-Adjusted cancer Death per 100K 2011-15']
            data_dict[state]['mortality_rank'] = state_mortality_dict[state_name]['cancer death rank']
            data_dict[state]['pop_2018'] = state_mortality_dict[state_name]['2018 Population']
            data_dict[state]['pop_2018_per1M'] =  state_mortality_dict[state_name]['pop per 1 M']
            data_dict[state]['num_des_cc'] = state_mortality_dict[state_name]['# designated cancer centers by state']
            data_dict[state]['people_per_cc'] = state_mortality_dict[state_name]['people (in million) per cancer center']
            data_dict[state]['cc_per10M'] = state_mortality_dict[state_name]['cancer centers per 10 million population']
            data_dict[state]['rank_cc_per1M'] = state_mortality_dict[state_name]['Rank of CC per 1 million people']
            data_dict[state]['growth_2018'] = state_mortality_dict[state_name]['2018 Growth']
            data_dict[state]['percent_US'] = state_mortality_dict[state_name]['% of US']
            data_dict[state]['cancer_centers'] = []

        data_dict[state]['cancer_centers'].append({
            'name': name,
            'type': state_type,
            'link': link,
            'lat': lat,
            'lon': lon
        })

    for i in range(state_mortality.shape[0]):
        state = state_mortality['State'][i]
        if type(state) == type(1.0) or state=='NaN' or state.strip().lower()=='us':
            continue
        state_name = state_mortality['State'][i].strip()
        state = Constants.STATE_CODES[state_name]

        if state not in data_dict:
            data_dict[state] = {}
            data_dict[state]['state_name'] = state_name
            data_dict[state]['state_code'] = Constants.STATE_NAMES_SHORTEN[state_name]
            data_dict[state]['incidence'] = state_incidence_dict[state_name]['All cancer incidence 2011-2015'] if state_name in state_incidence_dict else None
            data_dict[state]['incidence_rank'] = state_incidence_dict[state_name]['cancer incidence rank'] if state_name in state_incidence_dict else None
            data_dict[state]['mortality'] = state_mortality_dict[state_name]['Age-Adjusted cancer Death per 100K 2011-15'] if state_name in state_mortality_dict else None
            data_dict[state]['mortality_rank'] = state_mortality_dict[state_name]['cancer death rank'] if state_name in state_mortality_dict else None
            data_dict[state]['pop_2018'] = state_mortality_dict[state_name]['2018 Population'] if state_name in state_mortality_dict else None
            data_dict[state]['pop_2018_per1M'] = state_mortality_dict[state_name]['pop per 1 M'] if state_name in state_mortality_dict else None
            data_dict[state]['num_des_cc'] = state_mortality_dict[state_name]['# designated cancer centers by state'] if state_name in state_mortality_dict else None
            data_dict[state]['people_per_cc'] = state_mortality_dict[state_name]['people (in million) per cancer center'] if state_name in state_mortality_dict else None
            data_dict[state]['cc_per10M'] = state_mortality_dict[state_name]['cancer centers per 10 million population'] if state_name in state_mortality_dict else None
            data_dict[state]['rank_cc_per1M'] = state_mortality_dict[state_name]['Rank of CC per 1 million people'] if state_name in state_mortality_dict else None
            data_dict[state]['growth_2018'] = state_mortality_dict[state_name]['2018 Growth'] if state_name in state_mortality_dict else None
            data_dict[state]['percent_US'] = state_mortality_dict[state_name]['% of US'] if state_name in state_mortality_dict else None
            data_dict[state]['cancer_centers'] = []

    return data_dict


def add_time_varying_data(data_dict):
    funding_by_year = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR, Constants.TIME_VARYING_DATA), Constants.FUNDING_BY_YEAR, dtype=str)
    mortality_by_year = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR, Constants.TIME_VARYING_DATA), Constants.MORTALITY_BY_YEAR, dtype=str)
    gender_mortality_by_year = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR, Constants.TIME_VARYING_DATA), Constants.GENDER_MORTALITY_BY_YEAR, dtype=str)
    race_mortality_by_year = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR, Constants.TIME_VARYING_DATA), Constants.RACE_MORTALITY_BY_YEAR, dtype=str)

    years = list(range(2000, 2016))

    for i in range(funding_by_year.shape[0]):
        state_name = funding_by_year['StateName'][i]
        if state_name not in Constants.STATE_CODES:
            print("funding", state_name)
            continue
        state = Constants.STATE_CODES[state_name]
        if state not in data_dict:
            continue
        state_funding = {
            'GrantsNo': [],
            'GrantsAmount': [],
            'ContractsNo': [],
            'ContractsAmount': [],
            'TotalNo': [],
            'TotalAmount': []
        }
        cols = ['GrantsNo', 'GrantsAmount', 'ContractsNo', 'ContractsAmount', 'TotalNo', 'TotalAmount']
        for year in years:
            for col in cols:
                val = funding_by_year[col+str(year)][i]
                if val is None or type(val) == type(1.0):
                    state_funding[col].append(None)
                else:
                    state_funding[col].append(val)
        data_dict[state]['funding_by_year'] = state_funding

    for i in range(mortality_by_year.shape[0]):
        state_name = mortality_by_year['StateName'][i]
        if state_name not in Constants.STATE_CODES:
            print("mortality", state_name)
            continue
        state = Constants.STATE_CODES[state_name]
        if state not in data_dict:
            continue
        state_funding = {
            'Rate': [],
            'Count': [],
            'Pop': []
        }
        cols = ['Rate', 'Count', 'Pop']
        for year in years:
            for col in cols:
                val = mortality_by_year[col + str(year)][i]
                if val is None or type(val) == type(1.0):
                    state_funding[col].append(None)
                else:
                    state_funding[col].append(val)
        data_dict[state]['mortality_by_year'] = state_funding

    for i in range(race_mortality_by_year.shape[0]):
        state_name = race_mortality_by_year['StateName'][i]
        if state_name not in Constants.STATE_CODES:
            print("race_mortality", state_name)
            continue
        state = Constants.STATE_CODES[state_name]
        if state not in data_dict:
            continue
        state_funding = {
            'RateAll': [],
            'CountAll': [],
            'PopAll': [],
            'RateWhite': [],
            'CountWhite': [],
            'PopWhite': [],
            'RateBlack': [],
            'CountBlack': [],
            'PopBlack': [],
            'RateOther': [],
            'CountOther': [],
            'PopOther': []
        }
        cols = ['RateAll', 'CountAll', 'PopAll', 'RateWhite', 'CountWhite', 'PopWhite', 'RateBlack', 'CountBlack', 'PopBlack', 'RateOther', 'CountOther', 'PopOther']
        for year in years:
            for col in cols:
                val = race_mortality_by_year[col + str(year)][i]
                if val is None or type(val) == type(1.0):
                    state_funding[col].append(None)
                else:
                    state_funding[col].append(val)
        data_dict[state]['race_mortality_by_year'] = state_funding

        for i in range(gender_mortality_by_year.shape[0]):
            state_name = gender_mortality_by_year['StateName'][i]
            if state_name not in Constants.STATE_CODES:
                print("gender", state_name)
                continue
            state = Constants.STATE_CODES[state_name]
            if state not in data_dict:
                continue
            state_funding = {
                'RateTotal': [],
                'CountTotal': [],
                'PopTotal': [],
                'RateMale': [],
                'CountMale': [],
                'PopMale': [],
                'RateFemale': [],
                'CountFemale': [],
                'PopFemale': []
            }
            cols = ['RateTotal', 'CountTotal', 'PopTotal', 'RateMale', 'CountMale', 'PopMale', 'RateFemale', 'CountFemale', 'PopFemale']
            for year in years:
                for col in cols:
                    val = gender_mortality_by_year[col + str(year)][i]
                    if val is None or type(val) == type(1.0):
                        state_funding[col].append(None)
                    else:
                        state_funding[col].append(val)
            data_dict[state]['gender_mortality_by_year'] = state_funding


def write_json(data, loc='', filename='', indent=2):
    assert filename, 'Please enter valid filename'
    json_filepath = path.join(loc, filename)
    with open(json_filepath, 'w') as jd:
        dump(data, jd, indent=indent, default=str)


def get_lat_long(data):
    geolocator = Nominatim(user_agent='elefhead')
    lat = []
    long = []
    for i in range(data.shape[0]):
        address = data['Address'][i]
        try:
            location = geolocator.geocode(address)
            if location:
                lat.append(location.latitude)
                long.append(location.longitude)
            else:
                lat.append(None)
                long.append(None)
        except:
            lat.append(None)
            long.append(None)

    data['latitude'] = lat
    data['longitude'] = long

    data.to_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR, Constants.CANCER_CENTERS))


def isolate_cancer_centers(data):
    cancer_centers = {}
    for i in range(data.shape[0]):
        type = data['Type'][i]
        address = data['Address'][i]
        lat = data['latitude'][i]
        long = data['longitude'][i]
        year_nci = data['Achieved NCI cancer center designation'][i]
        name = data['Center Name'][i]
        link = data['Link'][i]
        state_short = data['State'][i]
        state_name = Constants.STATE_NAME[state_short]
        state_fips = Constants.STATE_CODES[state_name]
        cancer_centers[name] = {"type": type, "name": name, "address": address, "lat": lat, "long": long,
                               "year": year_nci, "state_short": state_short, "state_name": state_name,
                               "state_fips": state_fips, "link": link}
    return cancer_centers


def get_mean(data):
    column_datas = []
    for i in list(data):
        funding_through_years = data[i]['funding_by_year']['TotalAmount']
        column_datas.append([float(x) if x else 0 for x in funding_through_years])
    column_datas = np.asarray(column_datas, dtype=np.float64)
    return np.mean(column_datas, axis=0)


if __name__ == '__main__':
    data = read_csv(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.CANCER_CENTERS)
    cancer_centers = isolate_cancer_centers(data)

    write_json(list(cancer_centers.values()), path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.JSON_DUMP_CANCER_CENTER, None)





