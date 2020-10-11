#!/usr/bin/env bash
# Builds Expecto Botronum's Rust code.

cargo build --release

# macOS
if [ -f target/release/librust_chatlogger.dylib ]
then
    mv target/release/librust_chatlogger.dylib ./rust_chatlogger.so
fi

# Linux
if [ -f target/release/librust_chatlogger.so ]
then
    mv target/release/librust_chatlogger.so ./rust_chatlogger.so
fi

# Windows
if [ -f target/release/librust_chatlogger.dylib ]
then
    mv target/release/librust_chatlogger.dll ./rust_chatlogger.pyd
fi

echo "Rust code built!"
