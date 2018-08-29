FROM python:3.6

RUN apt update && apt install git

RUN git clone https://github.com/nesfit/Lemmiwinks.git && cd Lemmiwinks && git checkout origin/dev && python3 setup.py install

RUN git clone https://github.com/nesfit/MultiFIST.git
