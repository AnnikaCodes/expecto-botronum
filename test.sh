#!/bin/bash

echo "Linting Python code..."
if ! pylint ./*.py ./*/*.py ./*/*/*.py --disable=R,fixme || pylint-exit -wfail -efail -cfail $?;
then
    echo "Python linting failed!"
    exit 1
fi

echo "Checking types in Python..."
if ! MYPYPATH="$MYPYPATH:stubs/" mypy ./*.py ./*/*.py ./*/*/*.py --disallow-untyped-calls \
    --disallow-untyped-defs \
    --disallow-incomplete-defs \
    --warn-redundant-casts \
    --warn-unused-ignores \
    --warn-unreachable;
then
    echo "Python type checking failed!"
    exit 1
fi

echo "Running Python tests..."
if ! pytest tests/;
then
    echo "Python tests failed!"
    exit 1
fi

echo "Running Rust tests..."
if ! cargo test; # smh cargo won't let me exit on warning :((((((
then
    echo "Rust tests failed!"
    exit 1
fi

echo "All checks passed!"
