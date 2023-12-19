FROM debian:latest

RUN apt update -y && apt upgrade -y

RUN apt install -y john

COPY ./passwd .

CMD [ "john", "passwd" ]