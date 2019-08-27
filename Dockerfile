FROM blitznote/debootstrap-amd64:16.04

RUN apt-get update
RUN apt-get check
RUN apt-get dist-upgrade -y
RUN apt-get install -y apache2

ENV APACHE_RUN_USER network
ENV APACHE_RUN_GROUP network
ENV APACHE_LOG_DIR /var/log/apache2

EXPOSE 80
ENTRYPOINT ["/usr/sbin/apache2"]
CMD ["-D","FOREGROUND"]
