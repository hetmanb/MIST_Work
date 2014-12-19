#!/usr/bin/env python

import argparse
import textwrap
import os
import sys
import json
import re


def parse_mist_json(mist_jsons):
    md_out = {}
    results_out = {}
    for mist_json in mist_jsons:
        j = json.load(open(mist_json, 'r'))
        results = j['Results']
        for result in results:
            strain = result['Strain']
            md_out[strain] = {}

            metadata_dict = result['Metadata']
            for test in metadata_dict:
                md_out[strain][test] = {} 
                for m in metadata_dict[test]:
                    md_dict = {}
                    for y in m:
                        md = m[y]
                        if md == '':
                            if y not in md_dict:
                                md_dict[y] = set()
                            continue
                        if y in md_dict:
                            md_dict[y].add(md)
                        else:
                            md_dict[y] = set([md])
                    for y in md_dict:
                        md_out[strain][test][y] = '|'.join(md_dict[y])
                        

            test_results_dict = result['TestResults']
            results_out[strain] = {}
            for test in test_results_dict:
                results_out[strain][test] = {}
                for marker in test_results_dict[test]:
                    results_out[strain][test][marker] = test_results_dict[test][marker]['MarkerCall']

    return (results_out, md_out)


def write_metadata(md_dict, filename):

    with open(filename, 'w') as outf:
        outf.write('Strain,Test,Metadata,Value\n')
        for strain in md_dict:
            md_strain = md_dict[strain]
            for test in md_strain:
                md_test = md_strain[test]
                for md_field in md_test:
                    outf.write('{strain},{test},{metadata},{value}\n'.format(
                        strain=strain,
                        test=test,
                        metadata=md_field,
                        value=md_test[md_field]))


def write_test_results(test_result_dict, filename):

    with open(filename, 'w') as outf:
        outf.write('Strain,Test,Marker,Call\n')
        for strain in test_result_dict:
            strain_result = test_result_dict[strain]
            for test in strain_result:
                test_result = strain_result[test]
                for marker in test_result:
                    outf.write('{strain},{test},{marker},{call}\n'.format(
                        strain=strain,
                        test=test,
                        marker=marker,
                        call=test_result[marker]))


prog_desc = '''
    Parse MIST JSON output files to CSV
    -----------------------------------

    Test results table will have the following fields:
    - Strain:   Strain name
    - Test:     Test name
    - Marker:   Marker name
    - Call:     In silico marker call

    Metadata table will have the following fields:
    - Strain:   Strain name
    - Test:     Test name
    - Metadata: Metadata name
    - Value:    Metadata value
'''

parser = argparse.ArgumentParser(prog='MIST JSON to CSV Parser',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(prog_desc))
parser.add_argument('-t', '--test_results_out', help='Test results CSV output filename')
parser.add_argument('-m', '--metadata_out', help='Metadata CSV output filename')
parser.add_argument('jsons', metavar='filename', nargs='+', help='MIST JSON files')

args = parser.parse_args()

if args.test_results_out is None:
    print 'You need to specify where to save the test results CSV!'
elif args.metadata_out is None:
    print 'You need to specify where to save the metadata results CSV!'
elif len(args.jsons) == 0:
    print 'You need to specify MIST JSON output files to parse!'
else:
    results_out, md_out = parse_mist_json(args.jsons)
    metadata_out = args.metadata_out
    if not re.match(r'^.*\.csv$', metadata_out):
        metadata_out += '.csv'
    test_results_out = args.test_results_out
    if not re.match(r'^.*\.csv$', test_results_out):
        test_results_out += '.csv'
    write_metadata(md_out, metadata_out)
    write_test_results(results_out, test_results_out)

    