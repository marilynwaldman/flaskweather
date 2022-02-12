install:
    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm -rf ~/miniconda3/miniconda.sh   
	~/miniconda3/bin/conda config --add channels conda-forge && ~/miniconda3/bin/conda update -y conda \
    && ~/miniconda3/bin/conda install -y geopandas flask urllib3
test:
	#python -m pytest -vv test_application.py

lint:
	#pylint --disable=R,C application.py

deploy:
	echo "Deploying app"
	#eb deploy dash-map-env

all:   install   
