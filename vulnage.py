#!/usr/bin/python3

import pyfiglet
import argparse
from csv import DictWriter, DictReader
from alive_progress import alive_it
from datetime import datetime
from os.path import exists

def main(args):

    print(TITLE)

    # Read in all Reports
    reports = []
    with open(args.csvFile, "r") as file:
        reader = DictReader(file)
        for line in alive_it(reader, title="Reading CSV File..."):
            reports.append(line)
        keys = reader.fieldnames

    # Converting String HOST_START to Date Object (Make Verbose Output)
    if args.verbose:
        for i in alive_it(reports, title="Modifying HOST_START Variables..."):
            scanDate = datetime.strptime(i["HOST_START"], "%a %b %d %H:%M:%S %Y")
            i["HOST_START"] = scanDate
    else:
        for i in reports:
            scanDate = datetime.strptime(i["HOST_START"], "%a %b %d %H:%M:%S %Y")
            i["HOST_START"] = scanDate

    # Sorted Reports by Date and Unique ID
    sortedReports = sorted(reports, key=lambda d: (d['uid'], d['HOST_START']))

    # Add Reports to UIDs
    UID_reports = {}
    if args.verbose:
        for report in alive_it(sortedReports, title="Creating UID Reports..."):
            if report["uid"] not in UID_reports:
                UID_reports[report["uid"]] = [report]
            else:
                UID_reports[report["uid"]].append(report)
    else:
        for report in sortedReports:
            if report["uid"] not in UID_reports:
                UID_reports[report["uid"]] = [report]
            else:
                UID_reports[report["uid"]].append(report)

    # Adding Age to Reports
    if args.verbose:
        for uid in alive_it(UID_reports, title="Adding Age to Reports..."):
            oldest_report = UID_reports[uid][0]["HOST_START"]
            newest_report = UID_reports[uid][-1]["HOST_START"]
            age = newest_report - oldest_report
            for rep in UID_reports[uid]:
                rep["vuln age"] = age
    else:
        for uid in UID_reports:
            oldest_report = UID_reports[uid][0]["HOST_START"]
            newest_report = UID_reports[uid][-1]["HOST_START"]
            age = newest_report - oldest_report
            for rep in UID_reports[uid]:
                rep["vuln age"] = age

    # Create Report Output List
    finalReports = []
    for uid in UID_reports:
        if args.compress:
            finalReports.append(UID_reports[uid][-1])
        else:
            for rep in UID_reports[uid]:
                finalReports.append(rep)

    # Add all Missing Keys
    for rep in finalReports:
        for key in rep.keys():
            if key not in keys:
                keys.append(key)

    # Write to output file
    if args.writeFile:
        if exists(args.writeFile):
            while True:
                if args.force:
                    break
                i = input("Overwrite (y/n): ")
                if i.lower() == "y":
                    pass
                    break
                elif i.lower() == "n":
                    print("Exiting")
                    exit()
        with open(args.writeFile, "w") as f:
            writer = DictWriter(f, keys)
            writer.writeheader()
            bar = alive_it(finalReports, title="Writing to file...")
            for rep in bar:
                writer.writerow(rep)

if __name__ == "__main__":
    
    __version__ = "1.0.0"
    NAME = "Vulnage"
    TITLE = pyfiglet.figlet_format(NAME, font="stop") + f"\n{NAME} {__version__}\n"

    parser = argparse.ArgumentParser(description=f"{TITLE}", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('csvFile', help='pyne csv output file')
    parser.add_argument('writeFile', help='path to write file')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    parser.add_argument('-f', '--force', action='store_true', help='force overwrite of write file')
    parser.add_argument('-c', '--compress', action='store_true', help='write the most recent version of each unique vulnerability')
    args = parser.parse_args()

    main(args)