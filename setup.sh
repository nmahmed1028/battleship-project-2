# setup.sh

# Specify the path to the desired Python version
PYTHON_VERSION="$(which python3.11)"  # Change this to the path of the desired Python version

# Create a virtual environment with the specified Python version
$PYTHON_VERSION -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Virtual environment setup complete and dependencies installed!"