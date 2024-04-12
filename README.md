# pylint-requests

[![pypi](https://badge.fury.io/py/pylint-requests.svg)](https://pypi.org/project/pylint-requests)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://pypi.org/project/pylint-requests)
[![Downloads](https://img.shields.io/pypi/dm/pylint-requests.svg)](https://pypistats.org/packages/pylint-requests)
[![Build Status](https://github.com/m-burst/pylint-requests/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/m-burst/pylint-requests/actions/workflows/ci.yml)
[![Code coverage](https://codecov.io/gh/m-burst/pylint-requests/branch/master/graph/badge.svg)](https://codecov.io/gh/m-burst/pylint-requests)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Description

A `pylint` plugin to check for common issues with usage of `requests`.

Currently the following errors are reported:

* `F7801 (requests-not-available)`  
Reported if this plugin failed to import `requests`.
This means that: (a) you are running `pylint` with incorrect `PYTHONPATH`,
(b) you forgot to install `requests`, or (c) you aren't using `requests` and don't
need the plugin.
* `E7801 (request-without-timeout)`  
Reported if a HTTP call (e.g. `requests.get`) without a timeout is detected.

## Installation

    pip install pylint-requests

## Usage

Use pylint's `--load-plugins` option to enable the plugin:

    pylint --load-plugins=pylint_requests <your_code>

## For developers

### Install deps and setup pre-commit hook

    make init

### Run linters, autoformat, tests etc.

    make format lint test

### Bump new version

    make bump_major
    make bump_minor
    make bump_patch

## License

MIT

## Change Log

**Unreleased**

* require at least Python 3.8.1

**0.1.1 - 2020-05-07**

* fix crash with `AttributeInferenceError` on optional function parameters

**0.1.0 - 2019-04-14**

* initial
