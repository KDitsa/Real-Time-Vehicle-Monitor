#!/bin/bash
# the above line is called a "shebang" which tells the system to run
# the script using bash shell located at /bin/bash

set -e
# Exit immediately if any command fails
# This prevents the script from continuing in case of errors.

until pg_isready -h timescaleDB -p 5432 -U timescaleDB; do
    echo "Waiting for TimescaleDB to be ready..."
    sleep 2
done

echo "TimescaleDB is ready!"