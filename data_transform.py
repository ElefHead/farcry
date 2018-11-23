import pandas as pd
from os import path, makedirs, listdir
from json import dump, load


class Constants:
    #   directories
    ROOT_DIR = path.dirname(path.abspath(path.join(__file__)))
    DATA_DIR = 'data'
    UNFORMATTED_COUNTY_MORTALITY_RATES = 'Mortality rate by county'
    FORMATTED_COUNTY_MORTALITY_RATES = 'Formatted Mortality rates by county'

    #   file names
    CANCER_CENTERS = 'cancer_center_list.csv'
    CANCER_CENTERS_PER10M = 'cancer_center_per10m.csv'
    STATE_INCIDENCE = 'state_incidence.csv'
    STATE_MORTALITY = 'state_mortality.csv'
    UNFORMATTED_COUNTY_FIPS = 'countyFIPScodes.txt'
    FORMATTED_COUNTY_FIPS = 'formatted_county_codes.json'

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
        'MP': 'Northern Mariana Islands', 'PW': 'Palau', 'PR': 'Puerto Rico', 'VI': 'U.S. Virgin Islands'
    }

    STATE_NAMES_SHORTEN = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 
        'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 
        'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 
        'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 
        'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 
        'American Samoa': 'AS', 'District of Columbia': 'DC', 'Federated States of Micronesia': 'FM', 'Guam': 'GU', 
        'Marshall Islands': 'MH', 'Northern Mariana Islands': 'MP', 'Palau': 'PW', 'Puerto Rico': 'PR', 'U.S. Virgin Islands': 'VI'
    }

    #   state FIPS
    STATE_CODES = {
        'Alabama': 1, 'Alaska': 2, 'Arizona': 4, 'Arkansas': 5, 'California': 6, 'Colorado': 8, 'Connecticut': 9, 'Delaware': 10, 'District of Columbia': 11,
        'Florida': 12, 'Georgia': 13, 'Hawaii': 15, 'Idaho': 16, 'Illinois': 17, 'Indiana': 18, 'Iowa': 19, 'Kansas':20, 'Kentucky':21, 'Louisiana':22, 'Maine':23,
        'Maryland': 24, 'Massachusetts': 25, 'Michigan': 26, 'Minnesota':27, 'Mississippi':28, 'Missouri':29, 'Montana':30, 'Nebraska':31, 'Nevada':32, 'New Hampshire': 33,
        'New Jersey': 34, 'New Mexico': 35, 'New York': 36, 'North Carolina': 37, 'North Dakota': 38, 'Ohio': 39, 'Oklahoma': 40, 'Oregon':41, 'Pennsylvania':42, 'Rhode Island':44,
        'South Carolina': 45, 'South Dakota': 46, 'Tennessee': 47, 'Texas': 48, 'Utah': 49, 'Vermont': 50, 'Virginia': 51, 'Washington': 53, 'West Virginia': 54, 'Wisconsin': 55, 
        'Wyoming': 56, 'American Samoa': 60, 'Guam': 66, 'Northern Mariana Islands': 69, 'Puerto Rico': 72, 'U.S. Minor Outlying Islands': 74, 'U.S. Virgin Islands': 78
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
            data_dict[state]['incidence'] = state_incidence_dict[state_name]['All cancer incidence 2011-2015']
            data_dict[state]['incidence_rank'] = state_incidence_dict[state_name]['cancer incidence rank']
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


def write_json(data, loc='', filename='', indent=2):
    if not path.exists(loc):
        makedirs(loc)
    assert filename, 'Please enter valid filename'
    json_filepath = path.join(loc, filename)
    with open(json_filepath, 'w') as jd:
        dump(data, jd, indent=indent)


def rewrite_county_fips(loc, filename):
    file_path = path.join(loc, filename)
    fips_dict = {}
    with open(file_path, 'r') as cfc:
        for line in cfc:
            county_code, county, state_code = [i.strip() for i in line.split("\t")]
            state_name = Constants.STATE_NAME[state_code[:2].upper()]
            state_fips = Constants.STATE_CODES[state_name]
            if state_fips not in fips_dict:
                fips_dict[state_fips] = {
                    'state_name': state_name,
                    'state_code': state_code[:2].upper(),
                    'state_fips': state_fips,
                    'counties': {}
                }
            fips_dict[state_fips]['counties'][county_code] = county
    write_json(fips_dict, loc, Constants.FORMATTED_COUNTY_FIPS, indent=None)


def fix_mortality_csv():
    data_path = path.join(Constants.ROOT_DIR, Constants.DATA_DIR, Constants.UNFORMATTED_COUNTY_MORTALITY_RATES)
    out_data_path = path.join(Constants.ROOT_DIR, Constants.DATA_DIR, Constants.FORMATTED_COUNTY_MORTALITY_RATES)
    if not path.exists(out_data_path):
        makedirs(out_data_path)
    directories = listdir(data_path)
    for directory in directories:
        if directory[0] == '.' :
            continue
        data_folder = path.join(data_path, directory)
        out_data_folder = path.join(out_data_path, directory)
        if not path.exists(out_data_folder):
            makedirs(out_data_folder)
        for f in listdir(data_folder):
            if f[0] == '.':
                continue
            file_path = path.join(data_folder, f)
            out_file_path = path.join(out_data_folder, f)
            lines = []
            with open(file_path, 'r', encoding='ISO-8859-1') as t:
                for line in t:
                    if len(line.split(',')) >= 10:
                        lines.append(line)
            with open(out_file_path, 'w') as o:
                for line in lines:
                    o.write(line)


if __name__ == '__main__':
    fix_mortality_csv()
    # data_dict = transform_data()
    # rewrite_county_fips(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.UNFORMATTED_COUNTY_FIPS)
    # write_json(data_dict, path.join(Constants.ROOT_DIR, Constants.DATA_DIR),
    #            Constants.JSON_DUMP_CANCER_CENTER)





