#Description : This Dockerfile will build a container which will record a 5 second voice clip, decode and if possible run the associated docker command.

# Build : docker build -t thshaw/okdocker .

# Demo : docker run -it --privileged --device /dev/snd -v `pwd`/wav:/opt/okdocker/wav --group-add audio thshaw/okdocker --demo

# Record : docker run -it --privileged --device /dev/snd -v `pwd`/wav:/opt/okdocker/wav --group-add audio thshaw/okdocker --record test.wav

# Playback : docker run -it --privileged --device /dev/snd -v `pwd`/wav:/opt/okdocker/wav --group-add audio thshaw/okdocker --play wav/test.wav

# Translate Recording to text : docker run -it --privileged --device /dev/snd -v `pwd`/wav:/opt/okdocker/wav --group-add audio thshaw/okdocker --decode wav/test.wav
 

FROM ubuntu:15.10

MAINTAINER thshaw

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y

#Install dependencies
RUN apt-get install -y python-dev bison python-pyaudio pocketsphinx-hmm-wsj1 pocketsphinx-lm-wsj libasound-dev jackd

#Install build dependencies
RUN apt-get install -y make build-essential

RUN mkdir -p /opt/okdocker

#Install SphinxBase : http://sourceforge.net/projects/cmusphinx/files/sphinxbase/0.8/

ADD sphinxbase-0.8.tar.gz /opt/okdocker
WORKDIR /opt/okdocker/sphinxbase-0.8
RUN ./configure;make clean all;make install
RUN cd python;python setup.py install

#Install PocketSphinx : http://sourceforge.net/projects/cmusphinx/files/pocketsphinx/0.8/
ADD pocketsphinx-0.8.tar.gz /opt/okdocker
WORKDIR /opt/okdocker/pocketsphinx-0.8
RUN ./configure;make clean all;make install
RUN cd python;python setup.py install

#Add US English Generic Language Model : 
ADD cmusphinx-en-us-5.2.tar.gz /opt/okdocker/hmm/

#Add US English Generic Acoustic Model
ADD cmusphinx-5.0-en-us.lm /opt/okdocker/lm/

#Add in dictionary
COPY cmu07a.dic /opt/okdocker/dict/cmu07a.dic

RUN mkdir /opt/okdocker/wav
RUN chmod 777 /opt/okdocker/wav

#Setup for jackd
COPY audio.conf /etc/security/limits.d/audio.conf
RUN mv /etc/security/limits.d/audio.conf.disabled /etc/security/limits.d/audio.conf

#Copy in python script
COPY okdocker.py /opt/okdocker/okdocker.py

WORKDIR /opt/okdocker/

ENTRYPOINT ["python", "/opt/okdocker/okdocker.py"]

CMD ["--usage"]

