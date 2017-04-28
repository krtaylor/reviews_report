#!/usr/bin/python

#
# Author: Kurt Taylor <kurt.r.taylor@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import requests
from sys import stderr

""" This tool gathers review stats to the OpenStack project from Stackalytics
and reports in a nicer format for a company and its employees

There is a python wrapper library available for the Stackalytics API called
"pystackalytics"[1]. It is good for simple queries, but I found it to be
limiting, so, I thought it would be fun to write my own.

The possible parameters for the API are:
release
project_type
module
company
user_id
metric
start_date
end_date

Not all parameters are valid for a given query. For example, with the 
"engineers" query, "company" is not valid. Experiment with the query to see
the valid parameters and choose one that fits what you want to filter on.

[1]https://pypi.python.org/pypi/pystackalytics
"""

base_url = 'http://stackalytics.com/api/1.0/stats'

projects = '{url}/modules'.format(url=base_url)
companies = '{url}/companies'.format(url=base_url)
engineers = '{url}/engineers'.format(url=base_url)
activity = '{url}/activity'.format(url=base_url)
contribution = '{url}/contribution'.format(url=base_url)

company = 'ibm'
releases = [
           'austin',
           'bexar',
           'cactus',
           'diablo',
           'essex',
           'folsom',
           'grizzly',
           'havana',
           'icehouse',
           'juno',
           'kilo',
           'liberty',
           'mitaka',
           'newton',
           'ocata',
           'pike',
           'queens'
           ]

launchpad_ids = [
                'krtaylor', 
                'mjturek', 
                'edleafe', 
                'mlavalle'
                ]

def get_release( releases ):
    print(" ".join(rel for rel in releases))
    print('Enter the review stats release name in lower case '
          + '(for example: ocata): ')
    while True:
        release = raw_input('')
        if release in releases:
            break
        else:
            print('{typo} is not a valid release, try again'.format(typo=release))
    return release

def get_engineers( release ):
    for launchpad_id in launchpad_ids:
        url = (engineers + '?user_id={user}&release={rel}'
               .format(user=launchpad_id,rel=release))
        request = requests.get(url)
        try:
            request.raise_for_status()
            data = request.json()
            if data['stats']:
                print(data['stats'][0]['name'])
                print('-2|-1|+1|+2|Approve|Abandon (Positive Ratio)')
                print(data['stats'][0]['mark_ratio'])
            else:
                print('{user} had no reviews for {rel}'
                      .format(user=launchpad_id,rel=release))
        except requests.exceptions.HTTPError as error:
            #print('HTTPError:', error.message, file=sys.stderr)
            print('**************************************')
            print('"{user}" launchpad id not found'
                  .format(user=launchpad_id))
            print('**************************************')
        except ValueError as error:
            print('**************************************')
            print('Wrong parameters:', error.message)
            print('**************************************')

if __name__ == '__main__':
    release = get_release(releases)
    get_engineers (release)

