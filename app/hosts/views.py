# encoding=UTF-8
import commands
import threading

import re
from flask import request
import shutil
import time
import os
import logging
from app.models import ansible_play
from app import app
from flask import render_template
from app.models import MysqlDb_Connection
from app.forms import HostsForm, AnsibleForm
from app.hosts.update_hosts import update_ansible_hosts

dbconfig = {'host': '192.168.1.220', 'port': 3306, 'user': 'root', 'passwd': 'Asd@1234', 'db': 'ansible_tools',
            'charset': 'utf8'}

def monitor_timer():
    play_book = update_ansible_hosts('/tools/ansible/test.yml')
    play_book.run()
    play_book.get_result()

    global timer
    timer = threading.Timer(30.0, monitor_timer)
    timer.start()


timer = threading.Timer(10.0, monitor_timer)
timer.start()


@app.route('/hosts_info', methods=['GET', 'POST'])
def hosts_list():
    db = MysqlDb_Connection(dbconfig)
    hostsform = HostsForm()

    if hostsform.validate_on_submit():
        ip_add = hostsform.ip_address.data
        sql = "select id, ip_eth0, host_name, cpu, sysinfo, disk, cpu_count, cpu_cores, mem, \
                  os_kernel, app_name_cn, app_platform, machine_addr, app_status,description \
                  from app_hosts_info where ip_eth0 = '%s'" % str(
            ip_add)
        db.query(sql)
        db_result = db.fetchAllRows()
        db.close()
        return render_template('hosts/hosts_list.html', db_result=db_result, hostsform=hostsform)
    else:
        sql = "select id, ip_eth0, host_name, cpu, sysinfo, disk, cpu_count, cpu_cores, mem, \
                  os_kernel, app_name_cn, app_platform, machine_addr, app_status,description \
                  from app_hosts_info"
        db.query(sql)
        db_result = db.fetchAllRows()
        db.close()
        return render_template('hosts/hosts_list.html', db_result=db_result, hostsform=hostsform)


@app.route('/hosts_info/update', methods=['GET', 'POST'])
def update_host():
    db = MysqlDb_Connection(dbconfig)
    hostsform = HostsForm()
    ip_add = request.form.get('ip_add')
    app_name_cn = request.form.get('app_name_cn')
    app_platform = request.form.get('app_platform')
    machine_addr = request.form.get('machine_addr')
    description = request.form.get('description')
    data = {}
    data['ip_add'] = ip_add.encode('utf-8')
    data['app_name_cn'] = app_name_cn.encode('utf-8')
    data['app_platform'] = app_platform.encode('utf-8')
    data['machine_addr'] = machine_addr.encode('utf-8')
    data['description'] = description.encode('utf-8')
    sql = "update app_hosts_info set app_name_cn = %(app_name_cn)s, \
              app_platform = %(app_platform)s, machine_addr = %(machine_addr)s, \
              description = %(description)s where ip_eth0 = %(ip_add)s"
    try:
        db.update(sql, data)
        db_result = db.fetchAllRows()
        db.commit()
    except:
        db.rollback()
    db.close()
    return render_template('hosts/hosts_list.html', db_result=db_result, hostsform=hostsform)


@app.route('/hosts_info/delhost', methods=['GET', 'POST'])
def del_host():
    db = MysqlDb_Connection(dbconfig)
    hostsform = HostsForm()
    del_ip_add = request.form.get('del_ip_add')
    data = {}
    data['del_ip_add'] = del_ip_add.encode('utf-8')
    sql = "delete from app_hosts_info where ip_eth0 = %(del_ip_add)s"
    try:
        db.insert(sql, data)
        db.commit()
    except:
        db.rollback()
    db.close()
    return render_template('hosts/hosts_list.html', hostsform=hostsform)


@app.route('/hosts_maintain', methods=['GET', 'POST'])
def hosts_maintain():
    ansibleform = AnsibleForm()

    hosts_file = '/tools/ansible/hosts'
    bak_hosts_file = '/data/appbak/hosts_' + time.strftime('%Y%m%d%H%M%S')
    file_dir = '/tools/ansible'
    file_object = open(hosts_file)
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()

    file_dir = os.listdir(file_dir)
    file_list = []
    for i in file_dir:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.yml':
            file_list.append(i)

    hosts_file_text = request.form.get('hosts_file_text')
    if hosts_file_text is not None:
        shutil.copyfile(hosts_file, bak_hosts_file)
        f = file('/tools/ansible/hosts', 'w+')
        f.writelines(hosts_file_text)
        f.close()
    else:
        print 'hosts文件内容未改变！'

    if ansibleform.validate_on_submit():
        ansible_groupname = ansibleform.ansible_groupname.data
        ansible_shell = ansibleform.ansible_shell.data
        (status, output) = commands.getstatusoutput('ansible ' + ansible_groupname + ' ' + ansible_shell)
        return render_template('hosts/hosts_maintain.html', ansibleform=ansibleform, all_the_text=all_the_text,
                               file_list=file_list, output=output)

    return render_template('hosts/hosts_maintain.html', ansibleform=ansibleform, all_the_text=all_the_text,
                           file_list=file_list)


@app.route('/ansible_add_hosts', methods=['GET', 'POST'])
def ansible_add_hosts():
    # if __name__ == '__main__':
    play_book = ansible_play('/tools/ansible/test.yml')
    play_book.run()
    play_book.get_result()

    db = MysqlDb_Connection(dbconfig)
    hostsform = HostsForm()
    sql = "select id, ip_eth0, host_name, cpu, sysinfo, disk, cpu_count, cpu_cores, mem, \
                      os_kernel, app_name_cn, app_platform, machine_addr, app_status,description \
                      from app_hosts_info"
    db.query(sql)
    db_result = db.fetchAllRows()
    db.close()
    return render_template('hosts/hosts_list.html', db_result=db_result, hostsform=hostsform)
