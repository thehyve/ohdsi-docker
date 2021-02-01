FROM openjdk:11-jre-slim

WORKDIR /code

ARG SYNTHEA_VERSION=2.6.1

RUN curl -LO# https://github.com/synthetichealth/synthea/archive/v${SYNTHEA_VERSION}.tar.gz \
  && tar --strip-components=1 -xzf v${SYNTHEA_VERSION}.tar.gz \
  && rm v${SYNTHEA_VERSION}.tar.gz \
  && ./gradlew classes

COPY synthea.properties /code/src/main/resources/

CMD ["./run_synthea"]
