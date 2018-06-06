import argparse
import csv
import os
import platform
import pytablewriter
import re
import sys

from collections import defaultdict

FILENAME_REGEX_RAW = r"benchmark_timings_python(\d)(\d).csv"
FILENAME_REGEX = re.compile(FILENAME_REGEX_RAW)

MODULE_VERSION_FILENAME_REGEX_RAW = r"module_versions_python(\d)(\d).csv"
MODULE_VERSION_FILENAME_REGEX = re.compile(MODULE_VERSION_FILENAME_REGEX_RAW)

UNITS = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
SCALES = sorted([(scale, unit) for unit, scale in UNITS.items()], reverse=True)


def format_duration(duration):
    # Based on cPython's `timeit` CLI formatting
    scale, unit = next(((scale, unit) for scale, unit in SCALES if duration >= scale), SCALES[-1])
    precision = 3
    return "%.*g %s" % (precision, duration / scale, unit)


def format_relative(d1, d2):
    precision = 4
    return "%.*gx" % (precision + 1, d1 / d2)


def determine_used_module_versions(results_directory):
    module_versions_used = defaultdict(dict)
    for parent, _dirs, files in os.walk(results_directory):
        files_to_process = [f for f in files if MODULE_VERSION_FILENAME_REGEX.match(f)]
        for csv_file in files_to_process:
            with open(os.path.join(parent, csv_file), 'r') as fin:
                reader = csv.reader(fin, delimiter=",", quotechar='"')
                major, minor = next(reader)
                for module, version in reader:
                    if version not in module_versions_used[module]:
                        module_versions_used[module][version] = set()
                    module_versions_used[module][version].add('.'.join((major, minor)))
    return module_versions_used


def format_used_module_versions(module_versions_used):
    results = []
    for module, versions in sorted(module_versions_used.items(), key=lambda x: x[0]):
        if len(versions) == 1:
            results.append(f"{module}=={next(iter(versions.keys()))}")
        else:

            results.append(", ".join([f"{module}=={version} (on Python {', '.join(sorted(py_versions))})" for version, py_versions in versions.items()]))
    return results


def main(results_directory, output_file, compare_to, include_call, module_version_output):
    calling_code = {}
    timestamps = set()
    all_results = defaultdict(dict)

    for parent, _dirs, files in os.walk(results_directory):
        files_to_process = [f for f in files if FILENAME_REGEX.match(f)]
        for csv_file in files_to_process:
            with open(os.path.join(parent, csv_file), 'r') as fin:
                reader = csv.reader(fin, delimiter=",", quotechar='"')
                major, minor, timestamp = next(reader)
                timestamps.add(timestamp)
                for module, _setup, stmt, count, time_taken in reader:
                    all_results[(major, minor)][module] = float(time_taken) / int(count)
                    calling_code[module] = f"``{stmt.format(timestamp=timestamp)}``"

    if len(timestamps) > 1:
        raise NotImplementedError(f"Found a mix of files in the results directory. Found files that represent the parsing of {timestamps}. Support for handling multiple timestamps is not implemented.")

    all_modules = set([module for value in all_results.values() for module in value.keys()])
    python_versions_by_modernity = sorted(all_results.keys(), reverse=True)
    most_modern_python = python_versions_by_modernity[0]
    modules_by_modern_speed = sorted(all_modules, key=lambda module: all_results[most_modern_python][module])

    writer = pytablewriter.RstGridTableWriter()
    writer.header_list = ["Module"] + (["Call"] if include_call else []) + ["Python {}".format(".".join(key)) for key in python_versions_by_modernity] + [f"Relative Slowdown (versus {compare_to})"]
    writer.type_hint_list = [pytablewriter.String] * len(writer.header_list)
    writer.value_matrix = [
        [module] + ([calling_code[module]] if include_call else []) + [format_duration(all_results[python_version][module]) for python_version in python_versions_by_modernity] + ([format_relative(all_results[most_modern_python][module], all_results[most_modern_python][compare_to])] if module != compare_to else []) for module in modules_by_modern_speed
    ]

    with open(output_file, 'w') as fout:
        writer.stream = fout
        writer.write_table()

        if modules_by_modern_speed[0] == compare_to:
            fout.write(f"``{compare_to}`` takes {format_duration(all_results[most_modern_python][compare_to])}, which is **{format_relative(all_results[most_modern_python][modules_by_modern_speed[1]], all_results[most_modern_python][compare_to])}x faster than ``{modules_by_modern_speed[1]}``**, the next fastest ISO 8601 parser in this comparison.\n")
        else:
            fout.write(f"``{compare_to}`` takes {format_duration(all_results[most_modern_python][compare_to])}, which is **{format_relative(all_results[most_modern_python][compare_to], all_results[most_modern_python][modules_by_modern_speed[0]])}x slower than ``{modules_by_modern_speed[0]}``**, the fastest ISO 8601 parser in this comparison.\n")

    with open(os.path.join(os.path.dirname(output_file), module_version_output), 'w') as fout:
        fout.write(f"Tested on {platform.system()} {platform.release()} using the following modules:\n")
        fout.write('\n')
        fout.write(".. code:: python\n")
        fout.write('\n')
        for module_version_line in format_used_module_versions(determine_used_module_versions(results_directory)):
            fout.write(f"  {module_version_line}\n")


if __name__ == '__main__':
    OUTPUT_FILE_HELP = "The filepath to use when outputting the reStructuredText results."
    RESULTS_DIR_HELP = f"Which directory the script should look in to find benchmarking results. Will process any file that match the regexes '{FILENAME_REGEX_RAW}' and '{MODULE_VERSION_FILENAME_REGEX_RAW}'."

    BASE_LIBRARY_DEFAULT = "ciso8601"
    BASE_LIBRARY_HELP = f"The module to make all relative calculations relative to (default: \"{BASE_LIBRARY_DEFAULT}\")."

    INCLUDE_CALL_DEFAULT = False
    INCLUDE_CALL_HELP = f"Whether or not to include a column showing the actual code call (default: {INCLUDE_CALL_DEFAULT})."

    MODULE_VERSION_OUTPUT_FILE_DEFAULT = "benchmark_module_versions.rst"
    MODULE_VERSION_OUTPUT_FILE_HELP = "The filename to use when outputting the reStructuredText list of module versions. Written to the same directory as `OUTPUT`"

    parser = argparse.ArgumentParser("Formats the benchmarking results into a nicely formatted block of reStructuredText for use in the README.")
    parser.add_argument("RESULTS", help=RESULTS_DIR_HELP)
    parser.add_argument("OUTPUT", help=OUTPUT_FILE_HELP)
    parser.add_argument("--base-module", required=False, default=BASE_LIBRARY_DEFAULT, help=BASE_LIBRARY_HELP)
    parser.add_argument("--include-call", required=False, type=bool, default=INCLUDE_CALL_DEFAULT, help=INCLUDE_CALL_HELP)
    parser.add_argument("--module-version-output", required=False, default=MODULE_VERSION_OUTPUT_FILE_DEFAULT, help=MODULE_VERSION_OUTPUT_FILE_HELP)

    args = parser.parse_args()

    if not os.path.exists(args.RESULTS):
        raise ValueError(f'Results directory "{args.RESULTS}" does not exist.')

    main(args.RESULTS, args.OUTPUT, args.base_module, args.include_call, args.module_version_output)
