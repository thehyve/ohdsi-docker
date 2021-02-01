ARG BASE_CONTAINER=jupyter/datascience-notebook
FROM $BASE_CONTAINER

USER $NB_UID

ENV CONDA_DIR=$HOME/.conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Custom packages
RUN conda install --quiet --yes \
    'openjdk' \
    'r-rjava' \
    'psycopg2' \
    'matplotlib' && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions $HOME && \
    echo ${CONDA_DIR} > ${CONDA_DIR}/environments.txt && \
    conda config --system --set root_prefix ${CONDA_DIR} && \
    conda create --prefix ${CONDA_DIR} --yes && \
    conda clean --all -f -y
