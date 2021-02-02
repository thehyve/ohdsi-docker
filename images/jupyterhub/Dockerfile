ARG JUPYTERHUB_VERSION=1.3.0
FROM jupyterhub/jupyterhub:${JUPYTERHUB_VERSION}

ENV PATH=/opt/conda/condabin:/opt/conda/bin:$PATH

RUN curl -O# https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    conda install -yq psycopg2 ruamel.yaml && \
    conda clean -tipsy && \
    pip install --no-cache-dir \
        dockerspawner \
        oauthenticator

RUN useradd jovyan

COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]
