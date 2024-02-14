MacScan
=======

**MacScan** is a simple **Python library** and **CLI tool** to scan document on
**macOS** using the ImageCaptureCore_ API.

**IMPORTANT:** This library may not work with Apple Python (the Python version
distributed by Apple). Please use official Python version from python.org_ if
you encounter any issue.

.. _ImageCaptureCore: https://developer.apple.com/documentation/imagecapturecore
.. _python.org: https://www.python.org/downloads/macos/


Requirements
------------

* Apple macOS
* Python
* PyObjC


Development
-----------

Create / Activate / Install the virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the virtualenv::

    python3 -m venv __env__

Then activate the virtualenv::

    source __env__/bin/activate

Install dependencies and dev dependencies::

    pip install -e '.[dev]'

Lint
~~~~

To lint the code, run the following command (from virtualenv)::

    nox -s lint

To fix codding style, run::

    nox -s black_fix


Changelog
---------

* **[NEXT]** (changes on ``master``, but not released yet):

  * Nothing yet :)

