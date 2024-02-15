import sys

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
    print_scanner_devices()


if __name__ == "__main__":
    main()
