========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |downloads| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-tmsu-tag-assistant/badge/?style=flat
    :target: https://readthedocs.org/projects/python-tmsu-tag-assistant
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/jonjitsu/python-tmsu-tag-assistant.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jonjitsu/python-tmsu-tag-assistant

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/jonjitsu/python-tmsu-tag-assistant?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/jonjitsu/python-tmsu-tag-assistant

.. |requires| image:: https://requires.io/github/jonjitsu/python-tmsu-tag-assistant/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/jonjitsu/python-tmsu-tag-assistant/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/jonjitsu/python-tmsu-tag-assistant/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jonjitsu/python-tmsu-tag-assistant

.. |version| image:: https://img.shields.io/pypi/v/tmsu-tag-assistant.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/tmsu-tag-assistant

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonjitsu/python-tmsu-tag-assistant/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jonjitsu/python-tmsu-tag-assistant/compare/v0.1.0...master

.. |downloads| image:: https://img.shields.io/pypi/dm/tmsu-tag-assistant.svg
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/tmsu-tag-assistant

.. |wheel| image:: https://img.shields.io/pypi/wheel/tmsu-tag-assistant.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/tmsu-tag-assistant

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tmsu-tag-assistant.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/tmsu-tag-assistant

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/tmsu-tag-assistant.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/tmsu-tag-assistant


.. end-badges

An assistant for helping you TMSU tag your files.

* Free software: BSD license

Installation
============

::

    pip install tmsu-tag-assistant

Documentation
=============

https://python-tmsu-tag-assistant.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox