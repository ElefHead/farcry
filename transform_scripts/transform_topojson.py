from transform_scripts.constants import Constants
from transform_scripts.state_data_transform import read_json, read_csv, write_json, makedirs
from transform_scripts.county_data_transform import read_county_fips

from os import path, listdir, makedirs
import numpy as np


if __name__ == '__main__':
    data = read_json(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.TOPOJSON_FILE)
    county_fips = read_county_fips(path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.UNFORMATTED_COUNTY_FIPS)

    states = data['objects']['states']['geometries']
    counties = data['objects']['counties']['geometries']
    count = 0
    print(data)
    for i, county in enumerate(counties):
        id = county['id']
        zfill_id = str(id).zfill(5)
        if zfill_id in county_fips:
            state_fips = int(county_fips[zfill_id]['state_fips'])
            for j, state in enumerate(states):
                if state_fips == state['id']:
                    if 'topo' in data['objects']['states']['geometries'][j]:
                        data['objects']['states']['geometries'][j]['topo']['geometries'].append(county)
                    else:
                        data['objects']['states']['geometries'][j]['topo'] = {
                        'type': 'GeometryCollection',
                        'geometries': [county]
                    }

    write_json(data, path.join(Constants.ROOT_DIR, Constants.DATA_DIR), Constants.TOPOJSON_DUMP_FILE, None)