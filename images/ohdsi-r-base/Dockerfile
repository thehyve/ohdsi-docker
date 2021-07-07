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

RUN R CMD javareconf \
    && ln -s /usr/local/lib/R/site-library/littler/examples/install.r /usr/local/bin/install.r \
    && install.r \
      devtools \
      base64enc \
      benchmarkme \
      benchmarkmeData \
      bit64 \
      checkmate \
      colorspace \
      curl \
      data.table \
      devtools \
      doParallel \
      dplyr \
      farver \
      fastmap \
      flextable \
      foreach \
      gdtools \
      generics \
      ggplot2 \
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
      plyr \
      RColorBrewer \
      readr \
      rJava \
      rjson \
      RJSONIO \
      rlang \
      rmarkdown \
      scales \
      shiny \
      snow \
      sourcetools \
      systemfonts \
      tidyr \
      tinytex \
      uuid \
      viridisLite \
      XML \
      xml2 \
      xtable \
      zip \
   && installGithub.r \
      OHDSI/ParallelLogger \
      OHDSI/SqlRender \
      OHDSI/DatabaseConnector \
      OHDSI/DatabaseConnectorJars