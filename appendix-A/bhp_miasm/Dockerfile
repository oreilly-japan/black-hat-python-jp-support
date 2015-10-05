FROM miasm/base
MAINTAINER bhp
USER root
RUN apt-get update \
    && apt-get -y --no-install-recommends install \
	locales \
        vim-nox \
	#git ca-certificates \
    && rm -r /var/cache/apt /var/lib/apt/lists

#RUN mkdir /opt/bhp && \
#    cd /opt/bhp && \
#    git clone https://github.com/cea-sec/miasm.git && \
#    cd miasm && \
#    git checkout dcc488ec39d9a96b70c728ccdbcd43e62b25ae99 && \
#    python setup.py install

RUN echo "ja_JP.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP.UTF-8 \
    LC_ALL=ja_JP.UTF-8

RUN mkdir -p /home/miasm2 && \
    chown miasm2.miasm2 /home/miasm2
USER miasm2
WORKDIR /home/miasm2
CMD ["/bin/bash"]
