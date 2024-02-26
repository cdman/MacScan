import os
import sys
import argparse
from functools import partial

from .browser import list_scanner_devices
from .scanner import scan_document, FILE_EXT_TO_OUTPUT_FORMATS
from .exceptions import DeviceUnavailableError


def _type_path(mode, string):
    if os.path.isfile(string):
        if os.access(string, mode):
            return string
        raise argparse.ArgumentTypeError("can't access '%s'" % string)
    else:
        path = os.path.dirname(os.path.abspath(string))
        if os.access(path, mode):
            return string
        raise argparse.ArgumentTypeError("the '%s' folder does not exist" % path)


def print_scanner_devices():
    """Prints scanner device list in human readable format."""
    devices = list(list_scanner_devices())
    if devices:
        print("Scanner ID                            Scanner Name")
        print("==========                            ============")
        for device in devices:
            print(
                "%s  %s"
                % (
                    device["persistentIDString"],
                    device["name"],
                )
            )
        print()
    print("%i scanner(s) found." % len(devices))


def scan_to_file(parsed_args):
    print("Scanning to '%s'..." % parsed_args.output)
    try:
        scan_document(parsed_args.output)
    except DeviceUnavailableError as error:
        print("E: %s" % str(error))
        sys.exit(1)
    except ValueError as error:
        print("E: %s" % str(error))
        sys.exit(1)


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="macscan",
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    subparsers.add_parser(
        "list",
        prog="macscan list",
        help="list available scanner devices",
    )

    scan_parser = subparsers.add_parser(
        "scan",
        prog="macscan scan",
        help="scan a document to a file",
    )
    scan_parser.add_argument(
        "output",
        help="output file path (file's extension must be one of %s)"
        % ", ".join(['"%s"' % k for k in FILE_EXT_TO_OUTPUT_FORMATS.keys()]),
        type=partial(_type_path, os.W_OK),
    )

    parsed_args = parser.parse_args(args if args else ["--help"])

    if parsed_args.subcommand == "list":
        print_scanner_devices()
        sys.exit(0)
    elif parsed_args.subcommand == "scan":
        scan_to_file(parsed_args)
        sys.exit(0)


if __name__ == "__main__":
    main()
