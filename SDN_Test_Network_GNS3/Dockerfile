FROM python:3.8-slim

WORKDIR /gns3/

RUN apt-get update \
 && apt-get install -y --no-install-recommends iputils-ping telnet openssh-client build-essential\
 && pip3 install --upgrade --no-cache-dir setuptools pip paramiko pyats genie ansible gns3fy netaddr pexpect \
 && ansible-galaxy collection install davidban77.gns3  \
 && apt-get remove -y curl build-essential\
 && apt-get autoremove -y\
 && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

#COPY taf /taf
ENV ANSIBLE_HOST_KEY_CHECKING false

CMD ["/bin/sh"]
