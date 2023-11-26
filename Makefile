# installation of environment for subimage
envname := env_subimage

env:
	python3 -m venv ${envname}
	source "./${envname}/bin/activate"
	pip install --upgrade pip
	pip install -r requirements.txt

# test environment
test:
	python3 -m venv ${envname}
	source "./${envname}/bin/activate"
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pytest