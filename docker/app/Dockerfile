FROM centos:7
MAINTAINER Visgence Inc <info@visgence.com>

RUN systemctl mask firewalld.service
#RUN systemctl stop firewalld.service

#RUN yum install -y iptables-services
#RUN systemctl enable iptables
#ADD iptables.conf /etc/sysconfig/iptables

#RUN vim /etc/sysconfig/iptables
#    #required sniffer ports
#    -A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
#    -A INPUT -m state --state NEW -m tcp -p tcp --dport 8000 -j ACCEPT
#    -A INPUT -m state --state NEW -m udp -p udp --dport 6343 -j ACCEPT

# TODO: vim /etc/sysconfig/selinux <- set to "disabled"

RUN yum install -y epel-release
#yum install -y fail2ban
#vim /etc/fail2ban/jail.d/sshd.local
##    [ssh-iptables]
#    enabled  = true
#    filter   = sshd
#    action   = iptables[name=SSH, port=ssh, protocol=tcp]
#    logpath  = /var/log/secure
#    maxretry = 5
#    bantime = 3600

#systemctl enable fail2ban
#systemctl start fail2ban

#reboot

RUN yum install -y screen && yum clean all
RUN yum install -y git && yum clean all

RUN yum install -y python-setuptools && yum clean all
RUN easy_install pip

RUN yum install -y postgresql && yum clean all

RUN yum install -y make automake gcc gcc-c++ && yum clean all
RUN yum install -y python-devel && yum clean all
RUN yum install -y postgresql-devel && yum clean all

#PIP Stuff
COPY pip-requirements.txt /tmp/
RUN pip install -r /tmp/pip-requirements.txt

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

expose 8000

USER timeclock
CMD ["/bin/bash"]
