#!/usr/bin/python

"""
copyright 2015 Seth Black
"""

import csv
import struct
import sys

BEGIN_IP_POS = 0
END_IP_POS = 1
LAT_POS = 5
LNG_POS = 6
INPUT_FORMAT = "I I f f"

def ipv4(ip):
    if '.' in ip:
        return True

    return False

def fast_ipv4_to_int(ip):
    o = ip.split('.')

    if len(o) != 4:
        return None

    return (int(o[0]) << 24) | (int(o[1]) << 16) | (int(o[2]) << 8) | (int(o[3]))

if __name__ == '__main__':
    s = struct.Struct(INPUT_FORMAT)

    with open('db.csv', 'rb') as csvfile:
        ip_reader = csv.reader(csvfile)

        for row in ip_reader:
            if ipv4(row[BEGIN_IP_POS]) and ipv4(row[END_IP_POS]):
                begin_ip = fast_ipv4_to_int(row[BEGIN_IP_POS])
                end_ip = fast_ipv4_to_int(row[END_IP_POS])
            elif ipv6(row[BEGIN_IP_POS]) and ipv6(row[END_IP_POS]):
                begin_ip = None
                end_ip = None

            if begin_ip is None:
                sys.stderr.write("Error converting {0} to integer\n".format(row[BEGIN_IP_POS]))
                continue

            if end_ip is None:
                sys.stderr.write("Error converting {0} to integer\n".format(row[END_IP_POS]))
                continue

            try:
                lat = float(row[LAT_POS])
                lng = float(row[LNG_POS])
            except ValueError:
                sys.stderr.write("Error converting {0}, {1} to binary values\n".format(row[LAT_POS], row[LNG_POS]))
                continue

            values = (begin_ip, end_ip, lat, lng)
            packed_row = s.pack(*values)

            sys.stdout.write(packed_row)

            