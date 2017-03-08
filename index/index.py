#!/usr/bin/env python
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, validators, DecimalField, HiddenField

import logging, json


class nginxForm(FlaskForm):
    id = HiddenField('id')
    domain = StringField('domain', [validators.DataRequired()])
    listen_port = IntegerField('listen_port', [validators.DataRequired(), validators.NumberRange(min=0, max=65535)])
    dst = StringField('dst', [validators.DataRequired()])
    remark = StringField('remark', [validators.DataRequired()])
    submit = SubmitField('Save')


class rinetdForm(FlaskForm):
    id = HiddenField('id')
    bindaddress = StringField('bindaddress', [validators.DataRequired(), validators.IPAddress()])
    bindport = IntegerField('bindport', [validators.DataRequired(), validators.NumberRange(min=0, max=65535)])
    connectaddress = StringField('connectaddress', [validators.DataRequired(), validators.IPAddress()])
    connectport = IntegerField('connectport', [validators.DataRequired(), validators.NumberRange(min=0, max=65535)])
    submit = SubmitField('Save')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'what a testing project'
Bootstrap(app)


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
    return render_template('index.html', navigation=nv)


@app.route('/nginx-list')
def nginx_list():
    jo = sortbyKey(json.load(open('../nginx.json')), 'id')
    return render_template('nginx-list.html', rule_list=jo)


@app.route('/nginx-edit', methods=['GET'])
def nginx_edit():
    jo = sortbyKey(json.load(open('../nginx.json')), 'domain')
    ngf = nginxForm()
    for item in jo:
        if str(item['id']) == request.args.get('id'):
            ngf.id.data = item['id']
            ngf.domain.data = item['domain']
            ngf.listen_port.data = item['listen_port']
            ngf.dst.data = item['dst']
            ngf.remark.data = item['remark']
            return render_template('nginx-edit.html', form=ngf)
        else:
            continue
    return render_template('nginx-edit.html', add=request.args.get('domain'))


@app.route('/nginx-add')
def nginx_add():
    form = nginxForm()
    return render_template('nginx-edit.html', form=form)


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
        form = nginxForm()
        if form.validate_on_submit():
            return save_nginx_conf(request.form['id'], request.form['domain'], request.form['listen_port'],
                                   request.form['dst'], request.form['remark'])
        else:
            return render_template('succeed.html', title='faild', msg='argument error', msgdetail=form.errors)
            # doamin listen_port dst remark]
            # return save_nginx_conf(request.form['id'], request.form['domain'], request.form['listen_port'],
            #                        request.form['dst'], request.form['remark'])


@app.route('/rinetd-list')
def rinetd_list():
    jo = sortbyKey(json.load(open('../rinetd.json')), 'connectaddress')
    return render_template('rinetd-list.html', rule_list=jo)


@app.route('/rinetd-edit', methods=['GET'])
def rinetd_edit():
    jo = sortbyKey(json.load(open('../rinetd.json')), 'connectaddress')
    for item in jo:
        if str(item['id']) == request.args.get('id'):
            form = rinetdForm()
            form.id.data = item['id']
            form.bindaddress.data = item['bindaddress']
            form.bindport.data = item['bindport']
            form.connectaddress.data = item['connectaddress']
            form.connectport.data = item['connectport']
            return render_template('rinetd-edit.html', form=form)
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
        form = rinetdForm()
        if form.validate_on_submit():
            return save_rinetd_conf(request.form['id'], request.form['bindaddress'], request.form['bindport'],
                                    request.form['connectaddress'], request.form['connectport'])
        else:
            return render_template('succeed.html', title='faild', msg='argument error', msgdetail=form.errors)


@app.route('/log')
def log():
    return open('../auto_conf.log').read().replace('\n', '<br>')


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


if __name__ == '__main__':
    app.debug = True
    app.run()
