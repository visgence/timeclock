FROM almalinux:9
LABEL description="Visgence Inc <info@visgence.com>"

RUN systemctl mask firewalld.service
RUN yum install -y epel-release
RUN yum install -y screen git
RUN yum install -y make automake gcc gcc-c++ && yum clean all
RUN yum install -y postgresql-devel
RUN yum install -y python3-devel python3-setuptools
RUN yum install -y postgresql && yum clean all

RUN dnf update -y && dnf clean all
RUN dnf install -y mlocate python3-pip
RUN dnf install -y nodejs
RUN updatedb

RUN adduser --uid 1000 timeclock

#PIP Stuff
RUN ln -fs /usr/bin/python3 /usr/bin/python
RUN ln -fs /usr/bin/pip3 /usr/bin/pip
COPY ./requirements.txt /tmp/
COPY ./run.sh /home/timeclock/timeclock/
RUN pip3 install -r /tmp/requirements.txt

## Set up files and local settings
RUN chmod u+x /home/timeclock/timeclock/run.sh
RUN chown -R timeclock:timeclock /home/timeclock/timeclock/*
RUN mkdir /home/timeclock/.npm
RUN chown -R timeclock:timeclock /home/timeclock/.npm

USER timeclock
WORKDIR /home/timeclock/timeclock/

VOLUME ["/home/timeclock/timeclock"]

EXPOSE 8000

USER timeclock
CMD ["/bin/bash"]
