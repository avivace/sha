# This resets everything related to the deployed instance
# It cleans installed Node and Python dependencies and deletes the virtual env
# You need to rerun the deploy commands after this 
# (create venv, activate it, install python dependencies, install node dependencies)

cd backend
rm -rf bin
rm -rf include
rm -rf lib
rm lib64
rm -rf share
rm pyvenv.cfg
rm -rf __pycache__
cd frontend
rm node_modules