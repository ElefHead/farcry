import pandas as pd
from os import path, makedirs
from json import dump


class Constants:
    #   directories
    ROOT_DIR = path.dirname(path.abspath(path.join(__file__)))
    DATA_DIR = 'data'

    #   file names
    CANCER_CENTERS = 'cancer_center_list.csv'
    CANCER_CENTERS_PER10M = 'cancer_center_per10m.csv'
    STATE_INCIDENCE = 'state_incidence.csv'
    STATE_MORTALITY = 'state_mortality.csv'

    #   result file names
    JSON_DUMP_CANCER_CENTER = 'state_cancer_center.json'

    #   state names
    STATE_NAME = {
        'AL': 'Alabama', 'AK': "Alaska", 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
        'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida',
        'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
        'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
        'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
        'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin',
        'WY': 'Wyoming', 'AS': 'American Samoa', 'DC': 'District of Columbia',
        'FM': 'Federated States of Micronesia', 'GU': 'Guam', 'MH': 'Marshall Islands',
        'MP': 'Northern Mariana Islands', 'PW': 'Palau', 'PR': 'Puerto Rico', 'VI': 'Virgin Islands'
    }





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
        state = cancer_centers['State'][i]
        if state in Constants.STATE_NAME:
            state = Constants.STATE_NAME[state]
        else:
            continue
        lat = cancer_centers['Latitude'][i]
        lon = cancer_centers['Longitude'][i]
        name = cancer_centers['Institution Name'][i]
        state_type = cancer_centers['Type'][i]
        link = cancer_centers['Link'][i]

        if state not in data_dict:
            data_dict[state] = {}
            data_dict[state]['state_name'] = state
            data_dict[state]['state_code'] = cancer_centers['State'][i]
            data_dict[state]['incidence'] = state_incidence_dict[state]['All cancer incidence 2011-2015']
            data_dict[state]['incidence_rank'] = state_incidence_dict[state]['cancer incidence rank']
            data_dict[state]['mortality'] = state_mortality_dict[state]['Age-Adjusted cancer Death per 100K 2011-15']
            data_dict[state]['mortality_rank'] = state_mortality_dict[state]['cancer death rank']
            data_dict[state]['pop_2018'] = state_mortality_dict[state]['2018 Population']
            data_dict[state]['pop_2018_per1M'] =  state_mortality_dict[state]['pop per 1 M']
            data_dict[state]['num_des_cc'] = state_mortality_dict[state]['# designated cancer centers by state']
            data_dict[state]['people_per_cc'] = state_mortality_dict[state]['people (in million) per cancer center']
            data_dict[state]['cc_per10M'] = state_mortality_dict[state]['cancer centers per 10 million population']
            data_dict[state]['rank_cc_per1M'] = state_mortality_dict[state]['Rank of CC per 1 million people']
            data_dict[state]['growth_2018'] = state_mortality_dict[state]['2018 Growth']
            data_dict[state]['percent_US'] = state_mortality_dict[state]['% of US']
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
        if state not in data_dict:
            data_dict[state] = {}
            data_dict[state]['state_name'] = state
            data_dict[state]['state_code'] = cancer_centers['State'][i] if state.strip().lower() != 'us' else 'NaN'
            data_dict[state]['incidence'] = state_incidence_dict[state]['All cancer incidence 2011-2015']
            data_dict[state]['incidence_rank'] = state_incidence_dict[state]['cancer incidence rank']
            data_dict[state]['mortality'] = state_mortality_dict[state]['Age-Adjusted cancer Death per 100K 2011-15']
            data_dict[state]['mortality_rank'] = state_mortality_dict[state]['cancer death rank']
            data_dict[state]['pop_2018'] = state_mortality_dict[state]['2018 Population']
            data_dict[state]['pop_2018_per1M'] = state_mortality_dict[state]['pop per 1 M']
            data_dict[state]['num_des_cc'] = state_mortality_dict[state]['# designated cancer centers by state']
            data_dict[state]['people_per_cc'] = state_mortality_dict[state]['people (in million) per cancer center']
            data_dict[state]['cc_per10M'] = state_mortality_dict[state]['cancer centers per 10 million population']
            data_dict[state]['rank_cc_per1M'] = state_mortality_dict[state]['Rank of CC per 1 million people']
            data_dict[state]['growth_2018'] = state_mortality_dict[state]['2018 Growth']
            data_dict[state]['percent_US'] = state_mortality_dict[state]['% of US']
            data_dict[state]['cancer_centers'] = []

    return data_dict


def write_json(data, loc='', filename='', indent=2):
    if not path.exists(loc):
        makedirs(loc)
    assert filename, 'Please enter valid filename'
    json_filepath = path.join(loc, filename)
    with open(json_filepath, 'w') as jd:
        dump(data, jd, indent=indent)


if __name__ == '__main__':
    data_dict = transform_data()
    print(len(data_dict.items()))
    write_json(list(data_dict.values()), path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.JSON_DUMP_CANCER_CENTER)





