# Set base image (host OS)
FROM continuumio/miniconda3

RUN /opt/conda/bin/conda config --add channels conda-forge && /opt/conda/bin/conda update -y conda \
    && /opt/conda/bin/conda install -y geopandas flask urllib3

WORKDIR /app

EXPOSE 8000

COPY . .

CMD ["python", "wsgi.py"]



