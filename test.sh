#!/bin/bash

echo "Linting code..."
pylint *.py */*.py */*/*.py --disable=R,fixme || pylint-exit -wfail -efail -cfail $?
LINT_SUCCESS=$?
echo "Checking types..."
MYPYPATH="$MYPYPATH:stubs/" mypy *.py */*.py */*/*.py --disallow-untyped-calls \
    --disallow-untyped-defs \
    --disallow-incomplete-defs \
    --warn-redundant-casts \
    --warn-unused-ignores \
    --warn-unreachable
TYPE_CHECK_SUCCESS=$?
echo "Running tests..."
pytest .
TEST_SUCCESS=$?

if [ $LINT_SUCCESS == 0 ] && [ $TEST_SUCCESS == 0 ] && [ $TYPE_CHECK_SUCCESS == 0 ]; then
    echo "All checks passed!"
    exit 0
elif [ $LINT_SUCCESS == 0 ] && [ $TYPE_CHECK_SUCCESS == 0 ]; then
    echo "Linting and type checking passed, but tests failed."
    exit 1
elif [ $LINT_SUCCESS == 0 ] && [ $TEST_SUCCESS == 0 ]; then
    echo "Linting and tests passed, but type checking failed."
    exit 1
elif [ $TEST_SUCCESS == 0 ] && [ $TYPE_CHECK_SUCCESS == 0 ]; then
    echo "Tests and type checking passed, but linting failed."
    exit 1
elif [ $LINT_SUCCESS == 0 ]; then
    echo "Linting passed, but tests and type checking failed."
    exit 2
elif [ $TEST_SUCCESS == 0 ]; then
    echo "Tests passed, but linting and type checking failed."
    exit 2
elif [ $TYPE_CHECK_SUCCESS == 0 ]; then
    echo "Type checking passed, but linting and tests failed."
    exit 2
else
    echo "Everything failed, but you didn't!"
    exit 3
fi