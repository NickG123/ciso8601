import argparse
import csv
import importlib
import os
import pkg_resources
import pytz
import sys
import timeit
from datetime import datetime

ISO_8601_MODULES = {
    "aniso8601": ('import aniso8601', "aniso8601.parse_datetime('{timestamp}')"),
    "arrow": ('import arrow', "arrow.get('{timestamp}').datetime"),
    "ciso8601": ('import ciso8601', "ciso8601.parse_datetime('{timestamp}')"),
    "dateutil": ('import dateutil.parser', "dateutil.parser.parse('{timestamp}')"),
    "iso8601": ('import iso8601', "iso8601.parse_date('{timestamp}')"),
    "iso8601utils": ('from iso8601utils import parsers', "parsers.datetime('{timestamp}')"),
    "isodate": ('import isodate', "isodate.parse_datetime('{timestamp}')"),
    "maya": ('import maya', "maya.parse('{timestamp}').datetime()"),
    "moment": ('import moment', "moment.date('{timestamp}').date"),
    "pendulum": ('from pendulum.parsing.parser import parse_iso8601', "parse_iso8601('{timestamp}')"),
    "PySO8601": ('import PySO8601', "PySO8601.parse('{timestamp}')"),
    "str2date": ('from str2date import str2date', "str2date('{timestamp}')"),
    "zulu": ('import zulu', "zulu.parse('{timestamp}')"),
}

if os.name != 'nt':
    # udatetime doesn't support Windows.
    ISO_8601_MODULES["udatetime"] = ('import udatetime', "udatetime.from_string('{timestamp}')")


def get_module_version(module):
    # Based on 2 answers from https://stackoverflow.com/questions/20180543/how-to-check-version-of-python-modules
    # https://stackoverflow.com/a/32965521/6460914 and https://stackoverflow.com/a/20180564/6460914
    # While not perfect, it works for all of the modules we test.
    try:
        return pkg_resources.get_distribution(module).version
    except pkg_resources.DistributionNotFound:
        imported_module = importlib.import_module(module)
        return imported_module.__version__


def check_roughly_equivalent(dt1, dt2):
    # For the purposes of our benchmarking, we don't care if the datetime
    # has tzinfo=UTC or is naive.
    dt1 = dt1.replace(tzinfo=pytz.UTC) if isinstance(dt1, datetime) and dt1.tzinfo is None else dt1
    dt2 = dt2.replace(tzinfo=pytz.UTC) if isinstance(dt2, datetime) and dt2.tzinfo is None else dt2
    return dt1 == dt2


def run_tests(timestamp, results_directory, compare_to):
    # `Timer.autorange` only exists in Python 3.6+. We want the tests to run in a reasonable amount of time,
    # but we don't want to have to hard-code how many times to run each test.
    # So we make sure to call Python 3.6+ versions first. They output a file that the others use to know how many iterations to run.
    test_interation_counts = {}
    auto_range_file_obj = None
    auto_range_file_writer = None
    try:
        if (sys.version_info.major == 3 and sys.version_info.minor >= 6) or sys.version_info.major > 3:
            auto_range_file_obj = open(os.path.join(results_directory, "auto_range_counts.csv"), 'w')
            auto_range_file_writer = csv.writer(auto_range_file_obj, delimiter=',', quotechar='"', lineterminator='\n')
        else:
            with open(os.path.join(results_directory, "auto_range_counts.csv"), "r") as fin:
                reader = csv.reader(fin, delimiter=',', quotechar='"')
                for module, count in reader:
                    test_interation_counts[module] = int(count)

        exec(ISO_8601_MODULES[compare_to][0])
        expected_parse_result = eval(ISO_8601_MODULES[compare_to][1].format(timestamp=timestamp))

        with open(os.path.join(results_directory, "benchmark_timings_python{major}{minor}.csv".format(major=sys.version_info.major, minor=sys.version_info.minor)), 'w') as fout:
            writer = csv.writer(fout, delimiter=',', quotechar='"', lineterminator='\n')
            writer.writerow([sys.version_info.major, sys.version_info.minor, timestamp])
            for module, (setup, stmt) in ISO_8601_MODULES.items():
                count = None
                time_taken = None
                exception = None
                try:
                    exec(setup)
                    parse_result = eval(stmt.format(timestamp=timestamp))

                    if module in test_interation_counts:
                        count = test_interation_counts[module]
                        timer = timeit.Timer(stmt=stmt.format(timestamp=timestamp), setup=setup)
                        time_taken = timer.timeit(number=count)
                    else:
                        timer = timeit.Timer(stmt=stmt.format(timestamp=timestamp), setup=setup)
                        count, time_taken = timer.autorange()
                except Exception as exc:
                    parse_result = None
                    exception = type(exc)

                writer.writerow([module, setup, stmt.format(timestamp=timestamp), parse_result if parse_result is not None else "None", count, time_taken, check_roughly_equivalent(parse_result, expected_parse_result), exception])

                if auto_range_file_writer is not None:
                    auto_range_file_writer.writerow([module, count])
    finally:
        if auto_range_file_obj is not None:
            auto_range_file_obj.close()

    with open(os.path.join(results_directory, "module_versions_python{major}{minor}.csv".format(major=sys.version_info.major, minor=sys.version_info.minor)), 'w') as fout:
        module_version_writer = csv.writer(fout, delimiter=',', quotechar='"', lineterminator='\n')
        module_version_writer.writerow([sys.version_info.major, sys.version_info.minor])
        for module, (setup, stmt) in sorted(ISO_8601_MODULES.items(), key=lambda x: x[0]):
            module_version_writer.writerow([module, get_module_version(module)])


if __name__ == '__main__':
    TIMESTAMP_HELP = "Which ISO 8601 timestamp to parse"

    BASE_LIBRARY_DEFAULT = "ciso8601"
    BASE_LIBRARY_HELP = "The module to make correctness descisions relative to (default: \"{default}\").".format(default=BASE_LIBRARY_DEFAULT)

    RESULTS_DIR_DEFAULT = "benchmark_results"
    RESULTS_DIR_HELP = "Which directory the script should output benchmarking results. (default: \"{0}\")".format(RESULTS_DIR_DEFAULT)

    parser = argparse.ArgumentParser("Runs `timeit` to benchmark a variety of ISO 8601 parsers.")
    parser.add_argument("TIMESTAMP", help=TIMESTAMP_HELP)
    parser.add_argument("--base-module", required=False, default=BASE_LIBRARY_DEFAULT, help=BASE_LIBRARY_HELP)
    parser.add_argument("--results", required=False, default=RESULTS_DIR_DEFAULT, help=RESULTS_DIR_HELP)
    args = parser.parse_args()

    output_dir = os.path.join(args.results, args.TIMESTAMP.replace(":", ""))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    run_tests(args.TIMESTAMP, output_dir, args.base_module)
