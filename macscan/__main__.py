import sys
import argparse

from .browser import list_scanner_devices


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

    parsed_args = parser.parse_args(args if args else ["--help"])

    if parsed_args.subcommand == "list":
        print_scanner_devices()
        sys.exit(0)
    else:
        print("E: Unknown command '%s'." % parsed_args.subcommand)
        sys.exit(1)


if __name__ == "__main__":
    main()
