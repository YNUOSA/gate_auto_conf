from jinja2 import Template
import json

rinetd_conf_file = "/etc/rinetd.conf"


def createArinetd(_bindaddress, _bindport, _connectaddress, _connectport, _remark):
    t = open("rinetd.conf.template", 'r')
    T = Template(t.read())
    return T.render(bindaddress=_bindaddress, bindport=_bindport, connectaddress=_connectaddress,
                    connectport=_connectport, remark=_remark)


def buildrinetd():
    rinetd_result = "#auto config\n"
    solid = open("solid-rinetd")
    f = open("rinetd.json", 'r')
    jo = json.load(f)
    lines = []
    for line in solid:
        lines.append(line)
    solid.close()

    for i in jo:
        lines.insert(19,
                     createArinetd(i["bindaddress"], i["bindport"], i["connectaddress"], i["connectport"],
                                   i["remark"]) + "\n\n")
    print "".join(lines)


buildrinetd()
