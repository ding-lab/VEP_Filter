FROM python:3

WORKDIR /opt

RUN pip install PyVCF argparse pysam ConfigParser
RUN apt-get update && apt-get install -y \
    vim
ENV PYTHONPATH="/usr/local/lib/python3.8/site-packages:/opt/VEP_Filter/src/python"

COPY docker/vimrc /root/.vimrc
COPY . /opt/VEP_Filter
