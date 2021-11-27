sudo docker run -d -p 9002:9002 -v /home/pi/Documents/dnsmasq-configs:/opt/hostfile --name pingbot \
-e HOSTS='hosts' \
-e GITROOT='/opt/hostfile/' \
-e GITURL='http://gitlab/jarrance/dnsmasq-configs.git' \
-e INTERVAL=60 \
pingbot