FROM rocker/r-ver:4.1.0

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      libbz2-dev \
      liblzma-dev \
      libcairo2-dev \
      libcurl4-openssl-dev \
      libfontconfig1-dev \
      libpcre3-dev \
      libssl-dev \
      libxml2 \
      libxml2-dev \
      openjdk-11-jdk-headless \
      zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 \
  LD_LIBRARY_PATH=/usr/lib/jvm/java-11-openjdk-amd64/lib/server

ARG GITHUB_PAT
ENV GITHUB_PAT=$GITHUB_PAT

ARG CDM5_POSTGRESQL_USER
ARG CDM5_POSTGRESQL_PASSWORD
ARG CDM5_POSTGRESQL_SERVER
ARG CDM5_POSTGRESQL_CDM_SCHEMA
ARG CDM5_POSTGRESQL_OHDSI_SCHEMA

ENV CDM5_POSTGRESQL_USER=$CDM5_POSTGRESQL_USER
ENV CDM5_POSTGRESQL_PASSWORD=$CDM5_POSTGRESQL_PASSWORD
ENV CDM5_POSTGRESQL_SERVER=$CDM5_POSTGRESQL_SERVER
ENV CDM5_POSTGRESQL_CDM_SCHEMA=$CDM5_POSTGRESQL_CDM_SCHEMA
ENV CDM5_POSTGRESQL_OHDSI_SCHEMA=$CDM5_POSTGRESQL_OHDSI_SCHEMA

COPY localdata /localdata

RUN R CMD javareconf \
    && ln -s /usr/local/lib/R/site-library/littler/examples/install.r /usr/local/bin/install.r \
    && install.r \
      devtools \
      Andromeda \
      base64enc \
      benchmarkme \
      benchmarkmeData \
      bit64 \
      checkmate \
      colorspace \
      curl \
      clock \
      data.table \
      devtools \
      doParallel \
      DT \
      dplyr \
      digest \
      farver \
      fastmap \
      flextable \
      foreach \
      gdtools \
      generics \
      ggplot2 \
      ggiraph \
      gtable \
      hms \
      httpuv \
      isoband \
      iterators \
      labeling \
      lubridate \
      munsell \
      officer \
      openxlsx \
      pool \
      plyr \
      plotly \
      RColorBrewer \
      readr \
      rJava \
      rjson \
      RJSONIO \
      RSQLite \
      rlang \
      rmarkdown \
      scales \
      shiny \
      shinydashboard \
      shinyWidgets \
      snow \
      sourcetools \
      systemfonts \
      tidyr \
      tinytex \
      tsibble \
      uuid \
      viridisLite \
      withr \
      XML \
      xml2 \
      xtable \
      zip \
   && installGithub.r \
      OHDSI/CohortDiagnostics \
      OHDSI/CirceR \
      OHDSI/Eunomia \
      OHDSI/FeatureExtraction \
      OHDSI/ParallelLogger \
      OHDSI/ROhdsiWebApi \
      OHDSI/SqlRender \
      OHDSI/DatabaseConnector \
      OHDSI/DatabaseConnectorJars