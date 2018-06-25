FROM amazonlinux:2

RUN yum install -y awscli unzip

WORKDIR /opt/jobs

COPY builds/*.zip /opt/jobs/

CMD unzip ${JOB_TO_EXECUTE}.zip \
  && find . -name *.sh -exec chmod +x {} \; \
  && find . -name *.sh -exec {} \;
