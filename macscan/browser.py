import ImageCaptureCore
from Cocoa import NSObject
from PyObjCTools import AppHelper


class DeviceBrowserDelegate(NSObject):
    def deviceBrowserDidEnumerateLocalDevices_(self, browser):
        browser.stop()
        AppHelper.stopEventLoop()


def list_scanner_devices():
    """Lists scanner devices.

    :rtype: generator<dict>

    E.g.::

        {
            "persistentIDString": "00000000-0000-0000-0000-000000000000",
            "name": "My Super Scanner",
            "transportType": "ICTransportTypeUSB",
            "usbVendorID": 0x0000,   # USB devices only
            "usbProductID": 0x0000,  # USB devices only
        }
    """
    browser_delegate = DeviceBrowserDelegate.alloc().init()

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

    for device in browser.devices():
        yield {
            "persistentIDString": device.persistentIDString(),
            "name": device.name(),
            "transportType": device.transportType(),
            "usbVendorID": (
                device.usbVendorID()
                if device.transportType() == ImageCaptureCore.ICTransportTypeUSB
                else 0x0000
            ),
            "usbProductID": (
                device.usbProductID()
                if device.transportType() == ImageCaptureCore.ICTransportTypeUSB
                else 0x0000
            ),
        }
