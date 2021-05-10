"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []

    with open(neo_csv_path, 'r') as infile:
        neo_reader = csv.DictReader(infile)
        for row in neo_reader:
            new_neo = NearEarthObject(row['pdes'], name=row['name'], diameter=row['diameter'], hazardous=row['pha'])
            neos.append(new_neo)
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    cads = []

    with open(cad_json_path, 'r') as infile:
        cad_dict = json.load(infile)
        for cad in cad_dict['data']:
            new_cad = CloseApproach(cad[0], cad[3], cad[5], cad[7])
            cads.append(new_cad)
    return cads
