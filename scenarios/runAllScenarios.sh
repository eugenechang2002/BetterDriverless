#!/bin/bash
# Usage: Under ~/Documents/cmpe295 Run ./scenarios/runAllScenarios.sh 

echo "running"

for py_file in $(find "./scenarios" -name "*.py")
do
    echo "Running $py_file"
    python3 $py_file
done