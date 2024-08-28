#!/usr/bin/env sh

if [ -f ./installed ]; then
    exit 0
fi

dependencies="openssl-v1.0.1e.zip stonesoup-vm-v3.0.zip"

for dep in $dependencies; do
    curl -L "https://samate.nist.gov/SARD/downloads/dependencies/$dep" --output dependency.zip
    unzip -n dependency.zip
    rm dependency.zip
done

touch .installed
