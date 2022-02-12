install:

    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p $HOME/conda
    conda install -y geopandas flask urllib3
test:
	#python -m pytest -vv test_application.py

lint:
	#pylint --disable=R,C application.py

deploy:
	echo "Deploying app"
	#eb deploy dash-map-env

all:   install   
