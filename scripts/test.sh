#!/usr/bin/env bash
# Tests Expecto Botronum and runs linting

set -o errexit
set -o errtrace
set -o pipefail

echo -e "\033[0;32mLinting Python code...\033[0m"
if ! pylint ./*.py ./*/*.py ./*/*/*.py --disable=R,fixme --extension-pkg-whitelist=rust_chatlogger || pylint-exit -wfail -efail -cfail $?;
then
    echo -e "\033[0;31mPython linting failed!\033[0m"
    exit 1
fi

echo -e "\033[0;32mChecking types in Python...\033[0m"
if [ -z "${MYPYPATH}" ]
then
    MYPYPATH="stubs/"
fi

if ! MYPYPATH="$MYPYPATH:stubs/" mypy ./*.py ./*/*.py ./*/*/*.py --disallow-untyped-calls \
    --disallow-untyped-defs \
    --disallow-incomplete-defs \
    --warn-redundant-casts \
    --warn-unused-ignores \
    --warn-unreachable;
then
    echo -e "\033[0;31mPython type checking failed!\033[0m"
    exit 1
fi

echo -e "\033[0;32mRunning Python tests...\033[0m"
if ! py.test --cov-report=xml --cov=./ tests/;
then
    echo -e "\033[0;31mPython tests failed!\033[0m"
    exit 1
fi

echo -e "\033[0;32mRunning Rust tests..."
if ! cargo test --no-default-features; # smh cargo won't let me exit on warning :((((((
then
    echo -e "\033[0;31mRust tests failed!\033[0m"
    exit 1
fi

echo -e "\033[0;32mAll checks passed!\033[0m"
