#!/bin/bash

# 1. Activate the project virtual environment safely
# Using the standard local path for Windows virtual environments
source venv/Scripts/activate

# 2. Execute the Pytest test suite
echo "Running automated test suite..."
pytest test_app.py

# 3. Capture the exit status of the pytest command
# $? captures the return code of the last executed command
TEST_EXIT_CODE=$?

# 4. Evaluate the results and return explicit exit codes
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "SUCCESS: All automated tests passed successfully!"
    exit 0
else
    echo "FAILURE: Test suite encountered errors or failed assertions!"
    exit 1
fi