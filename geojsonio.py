#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import json
import sys
import webbrowser

import github3
from github3 import login
from github3 import create_gist

import six
from six.moves import urllib

getCredentials = open('gitauth.txt').read().split("\n")
GIT_TOKEN = getCredentials[0]
MAX_URL_LEN = 150e3  # Size threshold above which a gist is created
DEFAULT_DOMAIN = 'http://geojson.io/'

def authToGit ():
    gh = login( GITUSER, GITPASS)
    return gh

def testauth(auth):
    return auth.me()

def display(contents, domain=DEFAULT_DOMAIN, force_gist=True):
    url = make_url(contents, domain, force_gist)
    webbrowser.open(url,  new = 2)
    return url
# display() used to be called to_geojsonio. Keep it around for now...
to_geojsonio = display


def embed(contents='', width='100%', height=512, *args, **kwargs):

    from IPython.display import HTML

    url = make_url(contents, *args, **kwargs)
    html = '<iframe src={url} width={width} height={height}></iframe>'.format(
        url=url, width=width, height=height)
    return HTML(html)

def make_url(contents, domain=DEFAULT_DOMAIN, force_gist=False,
             size_for_gist=MAX_URL_LEN):

    contents = make_geojson(contents)
    if len(contents) <= size_for_gist and not force_gist:
        url = data_url(contents, domain)
    else:
        gist = _make_gist(contents)
        url = gist_url(gist.id, domain)

    return url


def make_geojson(contents):

    if isinstance(contents, six.string_types):
        return contents

    if hasattr(contents, '__geo_interface__'):
        features = [_geo_to_feature(contents)]
    else:
        try:
            feature_iter = iter(contents)
        except TypeError:
            raise ValueError('Unknown type for input')

        features = []
        for i, f in enumerate(feature_iter):
            if not hasattr(f, '__geo_interface__'):
                raise ValueError('Unknown type at index {0}'.format(i))
            features.append(_geo_to_feature(f))

    data = {'type': 'FeatureCollection', 'features': features}
    return json.dumps(data)


def _geo_to_feature(ob):

    mapping = ob.__geo_interface__
    if mapping['type'] == 'Feature':
        return mapping
    else:
        return {'type': 'Feature',
                'geometry': mapping}


def data_url(contents, domain=DEFAULT_DOMAIN):

    url = (domain + '#data=data:application/json,' +
           urllib.parse.quote(contents))
    return url


def _make_gist(contents, description='', filename='data.geojson'):

    gh = login( token=GIT_TOKEN )
    files = {filename: {'content': contents}}
    gist = gh.create_gist(description, files)
    #print (gist.html_url)

    return gist


def gist_url(gist_id, domain=DEFAULT_DOMAIN):

    url = (domain + '#id=gist:/{0}'.format(gist_id))
    return url


def main():
    parser = argparse.ArgumentParser(
        description='Quickly visualize GeoJSON data on geojson.io')

    parser.add_argument('-p', '--print',
                        dest='do_print',
                        action='store_true',
                        help='print the URL')

    parser.add_argument('-d', '--domain',
                        dest='domain',
                        default=DEFAULT_DOMAIN,
                        help='Alternate URL instead of http://geojson.io/')

    parser.add_argument('filename',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="The file to send to geojson.io")

    args = parser.parse_args()

    contents = args.filename.read()
    url = make_url(contents, args.domain)
    if args.do_print:
        print(url)
    else:
        webbrowser.open(url,  new = 2)

if __name__ == '__main__':
    main()
