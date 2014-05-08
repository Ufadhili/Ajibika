#!/bin/bash

# abort on any error
set -e

find . -name '*.pyc' -delete

# run our tests
./manage.py test   \
    south_africa   \
    core           \
    images         \
    scorecards     \
    search         \
    tasks          \
    za_hansard

# This is a very ugly solution to running all the tests just for our own code.
# running './manage.py test' will cause all the django etc tests to run as well
# which is not wanted. Many of these tests fail - most likely due to the
# mzalendo settings being used.
#
# It would be much nicer to have a better way to run the tests.


# to generate the core/test_data.json fixture use:
#
# ./manage.py dumpdata --natural --indent 4 core auth.user > core/fixtures/test_data.json
