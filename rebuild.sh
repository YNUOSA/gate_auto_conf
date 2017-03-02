#!/usr/bin/env bash
t=`date "+%Y%m%d%H%M%S"`
sudo mv /etc/nginx/conf.d/vhosts.conf "/etc/nginx/conf.d/vhosts.conf.$t"
sudo python config_nginx.py > /etc/nginx/conf.d/vhosts.conf
sudo service nginx restart
sudo mv /etc/rinetd.conf "/etc/rinetd.conf.$t"
sudo python config_rinetd.py >> rinetd.conf
sudo mv rinetd.conf /etc/rinetd.conf
sudo service rinetd restart
