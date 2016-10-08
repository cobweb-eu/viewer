#!/usr/bin/python3
"""Filter JSON dumps from PCAPI."""

import sys, csv, json


def fetch_key(d, k, fail=False):
    """Access dictionary keys while checking if they exist."""
    if k in d:
        return d[k]
    else:
        print ("Key: {} not found".format(k))
        if fail:
            sys.exit(1)
        return None

if len(sys.argv) == 4:
    json_in_fname = sys.argv[1]
    csv_out_fname = sys.argv[2]
    uuid = sys.argv[3]
else:
    print ("Usage: filter_json.py in.json out.csv UUID")

with open(csv_out_fname, 'w') as csvfile:
    fieldnames = ['Geometry Type', 'Geometry', 'Timestamp', 'UUID', 'SurveyID',
                  'Title', 'Obsevation Name']
    writer = csv.DictWriter(csvfile, dialect="excel", fieldnames=fieldnames)
    # writer.writeheader()

    with open(json_in_fname, "r") as jfile:
        sumo = json.load(jfile)
        # reader = csv.DictReader( open("iRecord_ExampleData.csv","r"))
        # header
        # reader.fieldnames

        for f in sumo["features"]:
            props = fetch_key(f, "properties")
            name = fetch_key(f, "name")
            timestamp = fetch_key(props, "timestamp")
            title = fetch_key(props, "title")
            editor = fetch_key(props, "editor")
            if (editor.endswith(".json") or editor.endswith(".edtr")):
                editor = editor[:-5]
            geom = fetch_key(f, "geometry", fail=True)
            geom_type = fetch_key(geom, "type", fail=True)
            geom_lonlat = repr(fetch_key(geom, "coordinates", fail=True))
            print (geom_type)
            print (geom_lonlat)
            print (timestamp)
            print (editor)
            print (title)
            print (name)

            # SAVE TO CSV
            writer.writerow({'Geometry Type': geom_type,
                             'Geometry': geom_lonlat,
                             'Timestamp': timestamp,
                             'UUID': uuid,
                             'SurveyID': editor,
                             'Title': title,
                             'Obsevation Name': name,
                             })
