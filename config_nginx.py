#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Template
import json

nginx_conf_file = "/etc/nginx/conf.d/vhosts.conf"


def createAproxy(_domain, _listen_port, _dst, _remark):
    t = open("vhost.conf.template", 'r')
    T = Template(t.read())
    return T.render(listen_port=_listen_port, domain=_domain, dst=_dst, remark=_remark) + "\n\n"


def buildnginx():
    nginx_result = "#auto config\n"
    f = open("nginx.json", 'r')
    jo = json.load(f)
    for i in jo:
        nginx_result += createAproxy(i["domain"], i["listen_port"], i["dst"], i["remark"])
    print nginx_result


buildnginx()
