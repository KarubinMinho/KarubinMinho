#!/usr/bin/env python

import csv
import sys
from datetime import datetime
from functools import wraps
from pathlib import Path

from netaddr import cidr_merge


def time_logger(wrapped):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        ret = wrapped(*args, **kwargs)
        delta = (datetime.now() - start).total_seconds()
        print('Function {} took {}s.'.format(wrapped.__name__, delta))
        return ret

    return wrapper


@time_logger
def get_geonames(locale_file, country_code, state=None):
    """
    :param locale_file: locale csv file
    :param country_code: e.g. US|AU...
    :param state: state of country_iso_code default: None
    :return: list: geonames of country_iso_code|state
    """
    with open(locale_file, newline='', encoding='utf8') as srcfile:
        content = csv.reader(srcfile, delimiter=',')
        if state is not None:
            return [row[0] for row in content if row[6] == state]
        return [row[0] for row in content if row[4] == country_code]


@time_logger
def create_cidr_dict():
    """
    :return: dict {'geonames_id': [cidr]}
    """
    ipv4_dict = {}
    with open(ipv4_csv, newline='', encoding='utf8') as srcfile:
        content = csv.reader(srcfile, delimiter=',')
        # return dict([(row[0], row[1]) for row in content])
        for row in content:
            if row[1] in ipv4_dict:
                ipv4_dict[row[1]].append(row[0])
            else:
                ipv4_dict[row[1]] = [row[0]]
        return ipv4_dict


@time_logger
def get_cidr(*, state, country_code=None):
    """
    :param state: str state name of country_code
    :param country_code: str 2bit_iso_code default: US
    :return: list of all state cidr
    """
    if country_code is None:
        country_code = 'US'
    genomes_id = get_geonames(locale_csv, country_code, state=state)
    ipv4_dict = create_cidr_dict()
    lst = []
    for i in genomes_id:
        lst.extend(ipv4_dict.get(i, []))
    return lst


@time_logger
def write2file(lst, save_path):
    line = '\n'.join(map(str, cidr_merge(lst)))
    with open(save_path, 'w') as save_file:
        save_file.write(line)


if __name__ == '__main__':
    locale_csv = r'D:/GeoIP2-City-CSV_20201215/GeoIP2-City-Locations-en.csv'
    ipv4_csv = r'D:/GeoIP2-City-CSV_20201215/GeoIP2-City-Blocks-IPv4.csv'
    if len(sys.argv) == 3:
        cidr = get_cidr(state=sys.argv[1], country_code=sys.argv[2])
    elif len(sys.argv) == 2:
        cidr = get_cidr(state=sys.argv[1])
    else:
        print("Usage: python {} state_name [country_code]".format(sys.argv[0]))
        sys.exit(1)
    # WriteFile
    save_name = Path('D:/GeoIP2-City-CSV_20201215') / \
        '{}.ip'.format(sys.argv[1]).lower()
    write2file(cidr, save_name)
