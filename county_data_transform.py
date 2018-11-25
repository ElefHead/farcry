from os import path, listdir
from constants import Constants

from state_data_transform import read_json, read_csv, write_json, makedirs

import numpy as np


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


def transform_county_data():
    county_data_directory = path.join(Constants.ROOT_DIR, Constants.DATA_DIR, Constants.FORMATTED_COUNTY_MORTALITY_RATES)

    county_cancer_folders = {
        'breast': None,
        'cervix': None,
        'colon': None,
        'stomach': None
    }

    for f in listdir(county_data_directory):
        if 'breast' in f.lower():
            county_cancer_folders['breast'] = path.join(county_data_directory, f)
        if 'cervix' in f.lower():
            county_cancer_folders['cervix'] = path.join(county_data_directory, f)
        if 'colon' in f.lower():
            county_cancer_folders['colon'] = path.join(county_data_directory, f)
        if 'stomach' in f.lower():
            county_cancer_folders['stomach'] = path.join(county_data_directory, f)

    county_fips = read_json(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.FORMATTED_COUNTY_FIPS)

    county_data = {}

    for f in listdir(county_cancer_folders['breast']):

        breast_cancer_data = np.empty((0, 0))
        cervical_cancer_data = np.empty((0, 0))
        colon_cancer_data = np.empty((0, 0))
        stomach_cancer_data = np.empty((0, 0))

        if path.exists(path.join(county_cancer_folders['breast'], f)):
            breast_cancer_data = read_csv(county_cancer_folders['breast'], f)

        if path.exists(path.join(county_cancer_folders['cervix'], f)):
            cervical_cancer_data = read_csv(county_cancer_folders['cervix'], f)

        if path.exists(path.join(county_cancer_folders['colon'], f)):
            colon_cancer_data = read_csv(county_cancer_folders['colon'], f)

        if path.exists(path.join(county_cancer_folders['stomach'], f)):
            stomach_cancer_data = read_csv(county_cancer_folders['stomach'], f)

        state_name = f[:-10].strip()
        state_name = state_name[0].upper() + state_name[1:]
        state_fips = str(Constants.STATE_CODES[state_name])
        state_short_name = Constants.STATE_NAMES_SHORTEN[state_name]
        state_county_fips = county_fips[state_fips]['counties']

        for i in range(breast_cancer_data.shape[0]):
            fips = str(breast_cancer_data[' FIPS'][i]).zfill(5)

            if fips in state_county_fips:
                county_name = state_county_fips[fips]
                if fips not in county_data:
                    county_data[fips] = {
                        'county_fips': fips,
                        'state_name': state_name,
                        'state_code': state_short_name,
                        'county_name': county_name,
                        'state_fips': state_fips,
                        'breast_death_rate': None,
                        'breast_recent_trend': None,
                        'breast_recent_5_year': None,
                        'cervical_death_rate': None,
                        'cervical_recent_trend': None,
                        'cervical_recent_5_year': None,
                        'colon_death_rate': None,
                        'colon_recent_trend': None,
                        'colon_recent_5_year': None,
                        'stomach_death_rate': None,
                        'stomach_recent_trend': None,
                        'stomach_recent_5_year': None
                    }

                death_rate = str(breast_cancer_data["Age-Adjusted Death Rate(Â\x86) - deaths per 100,000"][i]).replace('*', '').strip()
                recent_trend = str(breast_cancer_data['Recent Trend'][i]).replace('*', '').strip()
                recent_5_year = str(breast_cancer_data['Recent 5-Year Trend (Â\x87) in Death Rates'][i]).replace('*', '').strip()
                annual_count = str(breast_cancer_data['Average Annual Count'][i]).replace('*', '').strip()

                if len(annual_count.split(" ")) > 1:
                    annual_count = '0'

                county_data[fips]['breast_death_rate'] = death_rate if death_rate else None
                county_data[fips]['breast_recent_trend'] = recent_trend if recent_trend else None
                county_data[fips]['breast_recent_5_year'] = recent_5_year if recent_5_year else None
                county_data[fips]['breast_annual_average_count'] = annual_count if annual_count else None

        for i in range(cervical_cancer_data.shape[0]):
            fips = str(cervical_cancer_data[' FIPS'][i]).zfill(5)

            if fips in state_county_fips:
                county_name = state_county_fips[fips]
                if fips not in county_data:
                    county_data[fips] = {
                        'county_fips': fips,
                        'state_name': state_name,
                        'state_code': state_short_name,
                        'county_name': county_name,
                        'state_fips': state_fips,
                        'breast_death_rate': None,
                        'breast_recent_trend': None,
                        'breast_recent_5_year': None,
                        'cervical_death_rate': None,
                        'cervical_recent_trend': None,
                        'cervical_recent_5_year': None,
                        'colon_death_rate': None,
                        'colon_recent_trend': None,
                        'colon_recent_5_year': None,
                        'stomach_death_rate': None,
                        'stomach_recent_trend': None,
                        'stomach_recent_5_year': None
                    }

                death_rate = str(cervical_cancer_data["Age-Adjusted Death Rate(Â\x86) - deaths per 100,000"][i]).replace('*', '').strip()
                recent_trend = str(cervical_cancer_data['Recent Trend'][i]).replace('*', '').strip()
                recent_5_year = str(cervical_cancer_data['Recent 5-Year Trend (Â\x87) in Death Rates'][i]).replace('*', '').strip()
                annual_count = str(cervical_cancer_data['Average Annual Count'][i]).replace('*', '').strip()

                if len(annual_count.split(" ")) > 1:
                    annual_count = '0'

                county_data[fips]['cervical_death_rate'] = death_rate if death_rate else None
                county_data[fips]['cervical_recent_trend'] = recent_trend if recent_trend else None
                county_data[fips]['cervical_recent_5_year'] = recent_5_year if recent_5_year else None
                county_data[fips]['cervical_annual_average_count'] = annual_count if annual_count else None

        for i in range(colon_cancer_data.shape[0]):
            fips = str(colon_cancer_data[' FIPS'][i]).zfill(5)

            if fips in state_county_fips:
                county_name = state_county_fips[fips]
                if fips not in county_data:
                    county_data[fips] = {
                        'county_fips': fips,
                        'state_name': state_name,
                        'state_code': state_short_name,
                        'county_name': county_name,
                        'state_fips': state_fips,
                        'breast_death_rate': None,
                        'breast_recent_trend': None,
                        'breast_recent_5_year': None,
                        'cervical_death_rate': None,
                        'cervical_recent_trend': None,
                        'cervical_recent_5_year': None,
                        'colon_death_rate': None,
                        'colon_recent_trend': None,
                        'colon_recent_5_year': None,
                        'stomach_death_rate': None,
                        'stomach_recent_trend': None,
                        'stomach_recent_5_year': None
                    }

                death_rate = str(colon_cancer_data["Age-Adjusted Death Rate(Â\x86) - deaths per 100,000"][i]).replace('*', '').strip()
                recent_trend = str(colon_cancer_data['Recent Trend'][i]).replace('*', '').strip()
                recent_5_year = str(colon_cancer_data['Recent 5-Year Trend (Â\x87) in Death Rates'][i]).replace('*', '').strip()
                annual_count = str(colon_cancer_data['Average Annual Count'][i]).replace('*', '').strip()

                if len(annual_count.split(" ")) > 1:
                    annual_count = '0'

                county_data[fips]['colon_death_rate'] = death_rate if death_rate else None
                county_data[fips]['colon_recent_trend'] = recent_trend if recent_trend else None
                county_data[fips]['colon_recent_5_year'] = recent_5_year if recent_5_year else None
                county_data[fips]['colon_annual_average_count'] = annual_count if annual_count else None

        for i in range(stomach_cancer_data.shape[0]):
            fips = str(stomach_cancer_data[' FIPS'][i]).zfill(5)

            if fips in state_county_fips:
                county_name = state_county_fips[fips]
                if fips not in county_data:
                    county_data[fips] = {
                        'county_fips': fips,
                        'state_name': state_name,
                        'state_code': state_short_name,
                        'county_name': county_name,
                        'state_fips': state_fips,
                        'breast_death_rate': None,
                        'breast_recent_trend': None,
                        'breast_recent_5_year': None,
                        'cervical_death_rate': None,
                        'cervical_recent_trend': None,
                        'cervical_recent_5_year': None,
                        'colon_death_rate': None,
                        'colon_recent_trend': None,
                        'colon_recent_5_year': None,
                        'stomach_death_rate': None,
                        'stomach_recent_trend': None,
                        'stomach_recent_5_year': None
                    }

                death_rate = str(stomach_cancer_data["Age-Adjusted Death Rate(Â\x86) - deaths per 100,000"][i]).replace('*', '').strip()
                recent_trend = str(stomach_cancer_data['Recent Trend'][i]).replace('*', '').strip()
                recent_5_year = str(stomach_cancer_data['Recent 5-Year Trend (Â\x87) in Death Rates'][i]).replace('*', '').strip()
                annual_count = str(stomach_cancer_data['Average Annual Count'][i]).replace('*', '').strip()

                if len(annual_count.split(" ")) > 1:
                    annual_count = '0'

                county_data[fips]['stomach_death_rate'] = death_rate if death_rate else None
                county_data[fips]['stomach_recent_trend'] = recent_trend if recent_trend else None
                county_data[fips]['stomach_recent_5_year'] = recent_5_year if recent_5_year else None
                county_data[fips]['stomach_annual_average_count'] = annual_count if annual_count else None

    return county_data


if __name__ == '__main__':
    county_data = transform_county_data()
    write_json(county_data, path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.JSON_DUMP_COUNTY_DATA, indent=None)