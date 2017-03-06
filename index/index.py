#!/usr/bin/env python
from flask import Flask, render_template, request, url_for
import logging, json

app = Flask(__name__)


def sortbyKey(array, _key):
    return sorted(array, key=lambda x: x[_key])


def save_nginx_conf(idd, domain, listen_port, dst, remark):
    jo = sortbyKey(json.load(open('../nginx.json')), 'domain')
    for item in jo:
        if str(item['id']) == idd:
            item['domain'] = domain
            item['listen_port'] = int(listen_port)
            item['dst'] = dst
            item['remark'] = remark
            # rebuild id
            jo = sortbyKey(jo, 'domain')
            i = 0
            for item in jo:
                item['id'] = i
                i += 1
            f = open('../nginx.json', 'w')
            f.write(json.dumps(jo))
            f.close()
            return render_template('succeed.html', msg='edit succeed!')
    tmp = {'domain': domain, 'listen_port': listen_port, 'dst': dst, 'remark': remark}
    jo.append(tmp)

    # rebuild id
    jo = sortbyKey(jo, 'domain')
    i = 0
    for item in jo:
        item['id'] = i
        i += 1

    f = open('../nginx.json', 'w')
    f.write(json.dumps(jo))
    f.close()
    return render_template('succeed.html', msg='add succeed!')


def save_rinetd_conf(idd, bindaddress, bindport, connectaddress, connectport):
    jo = sortbyKey(json.load(open('../rinetd.json')), 'bindaddress')
    for item in jo:
        if str(item['id']) == idd:
            item['bindaddress'] = bindaddress
            item['bindport'] = bindport
            item['connectaddress'] = connectaddress
            item['connectport'] = connectport
            jo = sortbyKey(jo, 'bindaddress')
            i = 0
            for item in jo:
                item['id'] = i
                i += 1
            open('../rinetd.json', 'w').write(json.dumps(jo))
            return render_template('succeed.html', msg='succeed!')
    tmp = {'bindaddress': bindaddress, 'bindport': bindport, 'connectaddress': connectaddress,
           'connectport': connectport}
    jo.append(tmp)
    jo = sortbyKey(jo, 'bindaddress')
    i = 0
    for item in jo:
        item['id'] = i
        i += 1
    open('../rinetd.json', 'w').write(json.dumps(jo))
    return render_template('succeed.html', msg='succeed!')


@app.route('/')
def index():
    nv = []
    nv.append({'href': '/nginx-list', 'caption': 'View nginx Rules'})
    nv.append({'href': '/rinetd-list', 'caption': 'View rinetd Rules'})
    return render_template('index.html', a_variable='a', navigation=nv)


@app.route('/nginx-list')
def nginx_list():
    jo = sortbyKey(json.load(open('../nginx.json')), 'id')
    return render_template('nginx-list.html', rule_list=jo)


@app.route('/nginx-edit', methods=['GET'])
def nginx_edit():
    jo = sortbyKey(json.load(open('../nginx.json')), 'domain')
    for item in jo:
        if str(item['id']) == request.args.get('id'):
            return render_template('nginx-edit.html', id=item['id'], domain=item['domain'],
                                   listen_port=item['listen_port'], dst=item['dst'], remark=item['remark'],
                                   edit=item['domain'])
        else:
            continue
    return render_template('nginx-edit.html', add=request.args.get('domain'))


@app.route('/nginx-add')
def nginx_add():
    return render_template('nginx-edit.html', add='new rule')


@app.route('/nginx-delete', methods=['GET', 'POST'])
def nginx_delete():
    if request.method == 'GET':
        if request.args.get('id'):
            jo = sortbyKey(json.load(open('../nginx.json', 'r')), 'id')
            return render_template('nginx-delete.html', item=jo[int(request.args.get('id'))])
    if request.method == 'POST':
        jo = sortbyKey(json.load(open('../nginx.json')), 'id')
        for item in jo:
            if str(item['id']) == request.form['id']:
                jo.remove(item)
                # rebuild id
                jo = sortbyKey(jo, 'domain')
                i = 0
                for item in jo:
                    item['id'] = i
                    i += 1
                open('../nginx.json', 'w').write(json.dumps(jo))
                return render_template('succeed.html', msg='del succeed!')
        return 'rule not exist'


@app.route('/nginx-save', methods=['GET', 'POST'])
def nginx_save():
    if request.method == 'POST':
        # doamin listen_port dst remark]
        return save_rinetd_conf(request.form['id'], request.form['domain'], request.form['listen_port'],
                               request.form['dst'], request.form['remark'])


@app.route('/rinetd-list')
def rinetd_list():
    jo = sortbyKey(json.load(open('../rinetd.json')), 'connectaddress')
    return render_template('rinetd-list.html', rule_list=jo)


@app.route('/rinetd-edit', methods=['GET'])
def rinetd_edit():
    jo = sortbyKey(json.load(open('../rinetd.json')), 'connectaddress')
    for item in jo:
        if str(item['id']) == request.args.get('id'):
            return render_template('rinetd-edit.html', bindaddress=item['bindaddress'], bindport=item['bindport'],
                                   connectaddress=item['connectaddress'], connectport=item['connectport'],
                                   remark=item['remark'], id=item['id'], edit='%s:%s => %s:%s' % (
                    item['bindaddress'], item['bindport'], item['connectaddress'], item['connectport']))
    return render_template('rinetd-edit.html', add='new rule')


@app.route('/rinetd-add')
def rinetd_add():
    return render_template('rinetd-edit.html', add='new rule')


@app.route('/rinetd-delete', methods=['GET', 'POST'])
def rinetd_delete():
    # return ''
    if request.method == 'GET':
        jo = sortbyKey(json.load(open('../rinetd.json')), 'connectaddress')
        for item in jo:
            if str(item['id']) == request.args.get('id'):
                return render_template('rinetd-delete.html', item=item)
    if request.method == 'POST':
        jo = sortbyKey(json.load(open('../rinetd.json')), 'bindaddress')
        for item in jo:
            if str(item['id']) == request.form['id']:
                jo.remove(item)
                i = 0
                for item in jo:
                    item['id'] = i
                    i += 1
            open('../rinetd.json', 'w').write(json.dumps(jo))
            return render_template('succeed.html', msg='del succeed!')
        return 'rule not exist'


@app.route('/rinetd-save', methods=['GET', 'POST'])
def rinetd_save():
    if request.method == 'POST':
        return save_rinetd_conf(request.form['id'], request.form['bindaddress'], request.form['bindport'],
                                request.form['connectaddress'], request.form['connectport'])


@app.route('/log')
def log():
    return open('../auto_conf.log').read().replace('\n', '<br>')


if __name__ == '__main__':
    app.debug = True
    app.run()
