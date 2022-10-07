FROM quay.io/pypa/manylinux2014_x86_64 as base

RUN yum install -y make unzip wget libffi libffi-devel

COPY . /io

WORKDIR /io

RUN make clips_source

FROM base
RUN make install-clips

CMD "./manylinux/build-wheels.sh"
