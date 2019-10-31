#!/usr/bin/env python

import json
from os import environ
from sys import exit
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


def load_zones(path='zones.json'):
    """ load zones from json file
    returns python object """
    try:
        with open(path) as config:
            zones = json.load(config)
            return zones
    except ValueError as detail:
        raise detail


def load_templates(dir='templates'):
    """ load jinja2 templates """
    file_loader = FileSystemLoader(dir)
    return Environment(loader=file_loader)

def create_file(name, content):
    """ creates a file with content """
    with open(name, 'w') as file:
        file.write(content)

def generate_zones(zones, templates):
    """ create zone file and reverse zone """

    try:
        serial = environ['BUILD_NUMBER']
    except KeyError:
        print('$BUILD_NUMBER env variable not available, not running from Jenkins ?')
        exit(1)

    for zone, config in zones.items():
        config['domain'] = zone
        config['serial'] = serial
        config['file'] = 'db.{}'.format(zone)
        config['reverse'] =  {}
        config['reverse']['file'] = 'db' + ''.join(map(
                                            lambda x: '.{}'.format(x),
                                            config['network'].split('.')[:3]))
        reversed_octets = ''.join(map(
                            lambda x: '{}.'.format(x),
                            config['network'].split('.')[::-1][-3:]))
        config['reverse']['domain'] = "{}in-addr.arpa".format(reversed_octets)
        config['raw'] = templates.get_template('zone.jinja2').render(zone=config)
        config['reverse']['raw'] = templates.get_template('reverse-zone.jinja2').render(zone=config)
    return zones

if __name__ == "__main__":
    zones = load_zones()
    templates = load_templates()
    generate_zones(zones, templates)
    config_yaml = templates.get_template('config.yaml.jinja2').render(zones=zones)
    create_file('manifests/config.yaml', config_yaml)