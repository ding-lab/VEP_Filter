FROM python:3

WORKDIR /opt

RUN pip install PyVCF argparse pysam ConfigParser
RUN apt-get update && apt-get install -y \
    vim
ENV PYTHONPATH="/usr/local/lib/python3.7/site-packages:/opt/VEP_Filter/src"

COPY docker/vimrc /root/.vimrc
COPY . /opt/VEP_Filter
