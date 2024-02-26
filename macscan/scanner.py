import pathlib

import objc
import ImageCaptureCore
from Cocoa import NSObject
from Cocoa import NSURL
from Cocoa import CGRect, CGPoint
from PyObjCTools import AppHelper

from .browser import list_scanner_devices
from .exceptions import DeviceUnavailableError


FILE_EXT_TO_OUTPUT_FORMATS = {
    ".tiff": "public.tiff",
    ".png": "public.png",
    ".jpeg": "public.jpeg",
}


class DeviceBrowserDelegate2(NSObject):

    scanner_id = None
    output_dir_url = None
    output_file_name = None
    output_format_uti = None

    def init(self):
        self = objc.super(DeviceBrowserDelegate2, self).init()
        self._scanner_device = None
        self._scanner_device_delegate = None
        return self

    def deviceBrowser_didAddDevice_moreComing_(
        self, browser, device, moreComing
    ):  # required?
        if device.persistentIDString() == self.scanner_id:
            self._scanner_device_delegate = ScannerDeviceDelegate.alloc().init()

            self._scanner_device = device
            self._scanner_device.setDelegate_(self._scanner_device_delegate)
            self._scanner_device.setDownloadsDirectory_(self.output_dir_url)
            self._scanner_device.setDocumentName_(self.output_file_name)
            self._scanner_device.setDocumentUTI_(self.output_format_uti)

            self._scanner_device.requestOpenSession()

    def deviceBrowser_didRemoveDevice_moreGoing(
        self, browser, device, moreGoing
    ):  # required?
        pass

    def deviceBrowserDidEnumerateLocalDevices_(self, browser):
        browser.stop()
        if not self._scanner_device:
            AppHelper.stopEventLoop()
            raise DeviceUnavailableError(
                "No scanner found with id '%s'" % self.scanner_id
            )


class ScannerDeviceDelegate(NSObject):

    # ICDeviceDelegate

    def device_didOpenSessionWithError_(self, device, error):  # required
        # TODO handle errors
        pass

    def device_didCloseSessionWithError_(self, device, error):  # requried
        # TODO handle errors
        AppHelper.stopEventLoop()

    def didRemove_(self, device):  # required
        AppHelper.stopEventLoop()

    def deviceDidBecomeReady_(self, device):
        device.requestSelectFunctionalUnit_(
            ImageCaptureCore.ICScannerFunctionalUnitTypeFlatbed
        )

    def device_didEncounterError_(self, device, error):
        # TODO
        AppHelper.stopEventLoop()

    # ICScannerDeviceDelegate

    def scannerDevice_didSelectFunctionalUnit_error_(
        self, scanner_device, functional_unit, error
    ):
        if error:
            pass  # TODO handle errors

        if functional_unit:
            size = functional_unit.physicalSize()
            area = CGRect(CGPoint(0, 0), size)
            functional_unit.setScanArea_(area)

            scanner_device.requestScan()

    def scannerDevice_didCompleteScanWithError_(self, scanner_device, error):
        # TODO handle errors
        scanner_device.requestCloseSession()


def scan_document(
    output_file_path,
    scanner_id=None,
):
    """Scan a document using a flatbed scanner.

    :param str output_file_path: The path of the output file.
    :param str scanner_id: The ID of the scanner to use (the
        ``persistentIDString`` from :py:func:`browser.list_scanner_devices`;
        optional, by default the first device found will be used).

    :raises DeviceUnavailableError: if requested device is not available or if
        no device are available at all.
    :raises ValueError: if file extiension/format is not supported.
    """

    # Find the id of the first available scanner if none is requested
    if not scanner_id:
        scanners = list(list_scanner_devices())
        if not scanners:
            raise DeviceUnavailableError("No scanner device available.")
        scanner_id = scanners[0]["persistentIDString"]

    # Output folder and file name
    output_file_path = pathlib.Path(output_file_path)

    if output_file_path.is_file():
        # Remove file if already exists as the output file will be named
        # "<name> 1.ext" else...
        output_file_path.unlink()

    output_dir_url = NSURL.alloc().initFileURLWithPath_(
        output_file_path.absolute().parent.as_posix()
    )

    output_file_name = output_file_path.with_suffix("").name

    # Output file format
    if output_file_path.suffix in FILE_EXT_TO_OUTPUT_FORMATS:
        output_format_uti = FILE_EXT_TO_OUTPUT_FORMATS[output_file_path.suffix]
    else:
        raise ValueError(
            "Unsupported file extension '%s'. The extension must be one of %s."
            % (
                output_file_path.suffix,
                ", ".join(['"%s"' % k for k in FILE_EXT_TO_OUTPUT_FORMATS.keys()]),
            )
        )

    browser_delegate = DeviceBrowserDelegate2.alloc().init()
    browser_delegate.scanner_id = scanner_id
    browser_delegate.output_dir_url = output_dir_url
    browser_delegate.output_file_name = output_file_name
    browser_delegate.output_format_uti = output_format_uti

    browser = ImageCaptureCore.ICDeviceBrowser.alloc().init()
    browser.setDelegate_(browser_delegate)
    browser.setBrowsedDeviceTypeMask_(
        ImageCaptureCore.ICDeviceTypeMaskScanner
        | ImageCaptureCore.ICDeviceLocationTypeMaskLocal
        | ImageCaptureCore.ICDeviceLocationTypeMaskBonjour
        | ImageCaptureCore.ICDeviceLocationTypeMaskShared
    )

    browser.start()
    AppHelper.runConsoleEventLoop()
