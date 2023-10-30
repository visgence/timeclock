FROM almalinux:9
LABEL Visgence Inc <info@visgence.com>

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

#PIP Stuff
RUN ln -fs /usr/bin/python3 /usr/bin/python
RUN ln -fs /usr/bin/pip3 /usr/bin/pip
COPY pip-requirements.txt /tmp/
RUN pip3 install -r /tmp/pip-requirements.txt

## Set up files and local settings
RUN adduser timeclock

USER timeclock
WORKDIR /home/timeclock/timeclock/docker/app

USER root
ADD gen_pgpass.sh /home/timeclock
RUN chmod u+x /home/timeclock/gen_pgpass.sh
RUN chown timeclock:timeclock /home/timeclock/gen_pgpass.sh
USER timeclock

RUN echo "~/gen_pgpass.sh > ~/.pgpass" >> ~/.bashrc
RUN echo "chmod 0600 ~/.pgpass" >> ~/.bashrc
RUN echo "cd /home/timeclock/" >> ~/.bashrc
RUN echo "export DOCKER=true" >> ~/.bashrc

VOLUME ["/home/timeclock/timeclock"]

EXPOSE 8000

USER timeclock
CMD ["/bin/bash"]
