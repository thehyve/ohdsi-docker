ARG JUPYTERHUB_VERSION=0.9.2
FROM jupyterhub/jupyterhub-onbuild:${JUPYTERHUB_VERSION}

RUN /opt/conda/bin/conda update -n root conda && \
    /opt/conda/bin/conda install -yq psycopg2 ruamel.yaml && \
    /opt/conda/bin/conda clean -tipsy && \
    /opt/conda/bin/pip install --no-cache-dir \
        dockerspawner \
        oauthenticator
