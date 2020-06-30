#!/bin/bash

echo "Linting code..."
pylint *.py **/*.py --disable=R || pylint-exit -wfail -efail -cfail $?
LINT_SUCCESS=$?
echo "Running tests..."
pytest
TEST_SUCCESS=$?

if [ $LINT_SUCCESS == 0 ] && [ $TEST_SUCCESS == 0 ]; then
    echo "Success!"
    exit
elif [ $LINT_SUCCESS == 0 ]; then
    echo "Linting passed, but tests failed."
elif [ $TEST_SUCCESS == 0 ]; then
    echo "Tests passed, but linting failed."
else
    echo "Both tests and linting failed :c"
fi
