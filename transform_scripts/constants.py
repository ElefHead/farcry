from os import path, pardir


class Constants:
    #   directories
    ROOT_DIR = path.dirname(path.abspath(path.join(__file__, pardir)))
    DATA_DIR = 'data'
    UNFORMATTED_COUNTY_MORTALITY_RATES = 'Mortality rate by county'
    FORMATTED_COUNTY_MORTALITY_RATES = 'Formatted Mortality rates by county'
    TIME_VARYING_DATA = 'Time Varying Data'

    #   file names
    CANCER_CENTERS = 'cancer_center_list.csv'
    CANCER_CENTERS_PER10M = 'cancer_center_per10m.csv'
    STATE_INCIDENCE = 'state_incidence.csv'
    STATE_MORTALITY = 'state_mortality.csv'
    UNFORMATTED_COUNTY_FIPS = 'countyFIPScodes.txt'
    FORMATTED_COUNTY_FIPS = 'formatted_county_codes.json'
    FUNDING_BY_YEAR = 'funding_by_year.csv'
    GENDER_MORTALITY_BY_YEAR = 'gender_mortality_by_year.csv'
    MORTALITY_BY_YEAR = 'mortality_by_year.csv'
    RACE_MORTALITY_BY_YEAR = 'race_mortality_by_year.csv'
    TOPOJSON_FILE = 'us-counties.topojson'

    #   result file names
    JSON_DUMP_STATES_CANCER_CENTERS = 'state_cancer_center.json'
    JSON_DUMP_COUNTY_DATA = 'counties_cancer_data.json'
    JSON_DUMP_CANCER_CENTER = 'cancer_centers_list.json'
    TOPOJSON_DUMP_FILE = 'new-us-counties.topojson'

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
        'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI',
        'Wyoming': 'WY',
        'American Samoa': 'AS', 'District of Columbia': 'DC', 'Federated States of Micronesia': 'FM', 'Guam': 'GU',
        'Marshall Islands': 'MH', 'Northern Mariana Islands': 'MP', 'Palau': 'PW', 'Puerto Rico': 'PR',
        'U.S. Virgin Islands': 'VI'
    }

    #   state FIPS
    STATE_CODES = {
        'Alabama': 1, 'Alaska': 2, 'Arizona': 4, 'Arkansas': 5, 'California': 6, 'Colorado': 8, 'Connecticut': 9,
        'Delaware': 10, 'District of Columbia': 11,
        'Florida': 12, 'Georgia': 13, 'Hawaii': 15, 'Idaho': 16, 'Illinois': 17, 'Indiana': 18, 'Iowa': 19,
        'Kansas': 20, 'Kentucky': 21, 'Louisiana': 22, 'Maine': 23,
        'Maryland': 24, 'Massachusetts': 25, 'Michigan': 26, 'Minnesota': 27, 'Mississippi': 28, 'Missouri': 29,
        'Montana': 30, 'Nebraska': 31, 'Nevada': 32, 'New Hampshire': 33,
        'New Jersey': 34, 'New Mexico': 35, 'New York': 36, 'North Carolina': 37, 'North Dakota': 38, 'Ohio': 39,
        'Oklahoma': 40, 'Oregon': 41, 'Pennsylvania': 42, 'Rhode Island': 44,
        'South Carolina': 45, 'South Dakota': 46, 'Tennessee': 47, 'Texas': 48, 'Utah': 49, 'Vermont': 50,
        'Virginia': 51, 'Washington': 53, 'West Virginia': 54, 'Wisconsin': 55,
        'Wyoming': 56, 'American Samoa': 60, 'Guam': 66, 'Northern Mariana Islands': 69, 'Puerto Rico': 72,
        'U.S. Minor Outlying Islands': 74, 'U.S. Virgin Islands': 78
    }
