sudo docker run -d -p 9002:9002 --name pingbot \
-e HOSTS='hosts' \
-e GITROOT='/root/dnsdir/' \
-e GITURL='http://gitlab/jarrance/dnsmasq-configs.git' \
-e INTERVAL=60 \
-e CLONEREPO=True \
pingbot