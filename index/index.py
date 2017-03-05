#!/usr/bin/env python
from flask import Flask, render_template, request, url_for
import logging, json

app = Flask(__name__)


def sortbyKey(array):
    return sorted(array, key=lambda x: x["domain"])


def save_nginx_conf(domain, listen_port, dst, remark):
    jo = sortbyKey(json.load(open('../nginx.json')))
    for item in jo:
        if item['domain'] == domain:
            item['listen_port'] = listen_port
            item['dst'] = dst
            item['remark'] = remark
            f = open('../nginx.json', 'w')
            f.write(json.dumps(jo))
            f.close()
            return render_template('succeed.html', msg='edit succeed!')
        else:
            continue
    tmp = {'domain': domain, 'listen_port': listen_port, 'dst': dst, 'remark': remark}
    jo.append(tmp)
    f = open('../nginx.json', 'w')
    f.write(json.dumps(jo))
    f.close()
    return render_template('succeed.html', msg='add succeed!')


@app.route('/')
def index():
    nv = []
    nv.append({'href': '/nginx-list', 'caption': 'View nginx Rules'})
    nv.append({'href': '/rinetd-list', 'caption': 'View rinetd Rules'})
    return render_template('index.html', a_variable='a', navigation=nv)


@app.route('/nginx-list')
def nginx_list():
    jo = sortbyKey(json.load(open('../nginx.json')))
    return render_template('nginx-list.html', rule_list=jo)


@app.route('/nginx-edit', methods=['GET'])
def nginx_edit():
    domain = request.args.get('domain')
    jo = sortbyKey(json.load(open('../nginx.json')))
    for item in jo:
        if item['domain'] == domain:
            return render_template('nginx-edit.html', domain=item['domain'], listen_port=item['listen_port'],
                                   dst=item['dst'], remark=item['remark'], edit=domain)
        else:
            continue
    return render_template('nginx-edit.html', add=domain)


@app.route('/nginx-add')
def nginx_add():
    return render_template('nginx-edit.html', add='new rule')


@app.route('/nginx-delete', methods=['GET', 'POST'])
def nginx_delete():
    if request.method == 'GET':
        return render_template('nginx-delete.html', domain=request.args.get('domain'))
    if request.method == 'POST':
        jo = sortbyKey(json.load(open('../nginx.json')))
        for item in jo:
            if item['domain'] == request.form['domain']:
                jo.remove(item)
                open('../nginx.json', 'w').write(json.dumps(jo))
                return render_template('succeed.html', msg='del succeed!')
            else:
                continue
        return 'rule not exist'


@app.route('/nginx-save', methods=['GET', 'POST'])
def nginx_save():
    if request.method == 'POST':
        # doamin listen_port dst remark
        return save_nginx_conf(request.form['domain'], request.form['listen_port'], request.form['dst'],
                               request.form['remark'])


@app.route('/rinetd-list')
def rinetd_list():
    return render_template('rinetd-list.html')


@app.route('/log')
def log():
    return open('../auto_conf.log').read().replace('\n', '<br>')


if __name__ == '__main__':
    app.debug = True
    app.run()
