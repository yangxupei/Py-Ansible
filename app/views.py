# encoding=UTF-8
from flask import url_for
from app import app, login_manager
from flask import render_template, flash, redirect
from .forms import LoginForm

dbconfig = {'host': '192.168.1.220', 'port': 3306, 'user': 'root', 'passwd': 'Asd@1234', 'db': 'ansible_tools',
            'charset': 'utf8'}

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.route('/')
def index_login():
    return redirect(url_for('login'))

@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        username = str(form.user_name.data)
        password = str(form.password.data)
        if username == 'admin' and password == 'test123':
            flash("Logged in successfully.")
            return redirect(url_for("index"))
        else:
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

@app.route('/system_about')
def about():
    return render_template('about.html')

#
# @app.route('/hosts_info', methods=['GET', 'POST'])
# def hosts_list():
#     db = MysqlDb_Connection(dbconfig)
#     hostsform = HostsForm()
#
#     if hostsform.validate_on_submit():
#         ip_add = hostsform.ip_address.data
#         sql = "select id, ip_eth0, host_name, cpu, sysinfo, disk, cpu_count, cpu_cores, mem, \
#                   os_kernel, app_name_cn, app_platform, machine_addr, app_status,description \
#                   from app_hosts_info where ip_eth0 = '%s'" % str(
#             ip_add)
#         db.query(sql)
#         db_result = db.fetchAllRows()
#         db.close()
#         return render_template('hosts_list.html', db_result=db_result, hostsform=hostsform)
#     else:
#         sql = "select id, ip_eth0, host_name, cpu, sysinfo, disk, cpu_count, cpu_cores, mem, \
#                   os_kernel, app_name_cn, app_platform, machine_addr, app_status,description \
#                   from app_hosts_info"
#         db.query(sql)
#         db_result = db.fetchAllRows()
#         db.close()
#         return render_template('hosts_list.html', db_result=db_result, hostsform=hostsform)
#
#
# @app.route('/hosts_info/update', methods=['GET', 'POST'])
# def update_host():
#     db = MysqlDb_Connection(dbconfig)
#     hostsform = HostsForm()
#     ip_add = request.form.get('ip_add')
#     app_name_cn = request.form.get('app_name_cn')
#     app_platform = request.form.get('app_platform')
#     machine_addr = request.form.get('machine_addr')
#     description = request.form.get('description')
#     data = {}
#     data['ip_add'] = ip_add.encode('utf-8')
#     data['app_name_cn'] = app_name_cn.encode('utf-8')
#     data['app_platform'] = app_platform.encode('utf-8')
#     data['machine_addr'] = machine_addr.encode('utf-8')
#     data['description'] = description.encode('utf-8')
#     sql = "update app_hosts_info set app_name_cn = %(app_name_cn)s, \
#               app_platform = %(app_platform)s, machine_addr = %(machine_addr)s, \
#               description = %(description)s where ip_eth0 = %(ip_add)s"
#     try:
#         db.update(sql, data)
#         db_result = db.fetchAllRows()
#         db.commit()
#     except:
#         db.rollback()
#     db.close()
#     return render_template('hosts_list.html', db_result=db_result, hostsform=hostsform)
#
#
# @app.route('/hosts_info/update_app', methods=['GET', 'POST'])
# def update_app():
#     db = MysqlDb_Connection(dbconfig)
#     hostsform = HostsForm()
#     ip_add = request.form.get('ip_add')
#     app_name_en = request.form.get('app_name_en')
#     app_owner = request.form.get('app_owner')
#     app_platform = request.form.get('app_platform')
#     description = request.form.get('description')
#     data = {}
#     data['ip_add'] = ip_add.encode('utf-8')
#     data['app_name_en'] = app_name_en.encode('utf-8')
#     data['app_owner'] = app_owner.encode('utf-8')
#     data['app_platform'] = app_platform.encode('utf-8')
#     data['description'] = description.encode('utf-8')
#     sql = "update app_hosts_info set app_name_en = %(app_name_en)s, \
#               owner = %(app_owner)s, app_platform = %(app_platform)s, \
#               description = %(description)s where ip_eth0 = %(ip_add)s"
#     try:
#         db.update(sql, data)
#         db_result = db.fetchAllRows()
#         db.commit()
#     except:
#         db.rollback()
#     db.close()
#     return render_template('hosts_list.html', db_result=db_result, hostsform=hostsform)
#
#
# @app.route('/hosts_info/addhost', methods=['GET', 'POST'])
# def add_host():
#     db = MysqlDb_Connection(dbconfig)
#     hostsform = HostsForm()
#     ip_add = request.form.get('ip_add')
#     app_name_en = request.form.get('app_name_en')
#     app_owner = request.form.get('app_owner')
#     app_platform = request.form.get('app_platform')
#     description = request.form.get('description')
#     data = {}
#     data['ip_add'] = ip_add.encode('utf-8')
#     data['app_name_en'] = app_name_en.encode('utf-8')
#     data['app_owner'] = app_owner.encode('utf-8')
#     data['app_platform'] = app_platform.encode('utf-8')
#     data['description'] = description.encode('utf-8')
#     sql = "insert into app_hosts_info  (ip_eth0, app_name_en, owner, app_platform, description) \
#               VALUE (%(ip_add)s, %(app_name_en)s, %(app_owner)s, %(app_platform)s, %(description)s)"
#     try:
#         db.insert(sql, data)
#         db.commit()
#     except:
#         db.rollback()
#     db.close()
#     return render_template('paycloud_list.html',  hostsform=hostsform)
#
#
# @app.route('/hosts_info/delhost', methods=['GET', 'POST'])
# def del_host():
#     db = MysqlDb_Connection(dbconfig)
#     hostsform = HostsForm()
#     del_ip_add = request.form.get('del_ip_add')
#     data = {}
#     data['del_ip_add'] = del_ip_add.encode('utf-8')
#     sql = "delete from app_hosts_info where ip_eth0 = %(del_ip_add)s"
#     try:
#         db.insert(sql, data)
#         db.commit()
#     except:
#         db.rollback()
#     db.close()
#     return render_template('hosts_list.html',  hostsform=hostsform)
#
#
# @app.route('/hosts_monitor', methods=['GET', 'POST'])
# def hosts_monitor():
#     db = MysqlDb_Connection(dbconfig)
#     hostsform = HostsForm()
#
#     online = "SELECT count(*) AS nu FROM app_hosts_info WHERE app_status=0"
#     db.query(online)
#     online_nu = db.fetchAllRows()
#
#     offline = "SELECT count(*) AS nu FROM app_hosts_info WHERE app_status=1"
#     db.query(offline)
#     offline_nu = db.fetchAllRows()
#
#     mem_rate = "SELECT count(*) AS nu FROM app_hosts_info WHERE mem_rate > 75"
#     db.query(mem_rate)
#     mem_rate_nu = db.fetchAllRows()
#
#     disk_rate = "SELECT count(*) AS nu FROM app_hosts_info WHERE disk_rate > 75"
#     db.query(disk_rate)
#     disk_rate_nu = db.fetchAllRows()
#
#     swap_rate = "SELECT count(*) AS nu FROM app_hosts_info WHERE swap_rate > 75"
#     db.query(swap_rate)
#     swap_rate_nu = db.fetchAllRows()
#
#     if hostsform.validate_on_submit():
#         ip_add = hostsform.ip_address.data
#         sql = "select ip_eth0, host_name, mem_total, mem_free, disk_total, disk_free, \
#                   swap_total, swap_free, mem_rate, swap_rate, disk_rate, app_status from \
#                   app_hosts_info where ip_eth0 = '%s'" % str(
#             ip_add)
#         db.query(sql)
#         db_result = db.fetchAllRows()
#         db.close()
#         return render_template('hosts_monitor.html', db_result=db_result, online_nu=online_nu, offline_nu=offline_nu,
#                                mem_rate_nu=mem_rate_nu, disk_rate_nu=disk_rate_nu, swap_rate_nu=swap_rate_nu,
#                                hostsform=hostsform)
#     else:
#         sql = "select ip_eth0, host_name, mem_total, mem_free, disk_total, disk_free, swap_total, \
#                   swap_free, mem_rate, swap_rate, disk_rate, app_status from app_hosts_info"
#         db.query(sql)
#         db_result = db.fetchAllRows()
#         db.close()
#         return render_template('hosts_monitor.html', db_result=db_result, online_nu=online_nu, offline_nu=offline_nu,
#                                mem_rate_nu=mem_rate_nu, disk_rate_nu=disk_rate_nu, swap_rate_nu=swap_rate_nu,
#                                hostsform=hostsform)
#
#
# @app.route('/hosts_graph', methods=['GET', 'POST'])
# def hosts_graph():
#     db = MysqlDb_Connection(dbconfig)
#
#     # pay_count, customer_count, bill_count, rz_count
#     platform_count = "select count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '80.1.1.%' OR ahi.ip_eth0 LIKE '80.1.4.%' UNION ALL \
#                     select count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '80.2.%' UNION ALL select count(*) FROM \
#                     app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '10.27.%' UNION ALL select count(*) FROM app_hosts_info ahi WHERE \
#                     ahi.ip_eth0 LIKE '80.1.11.%' OR ahi.ip_eth0 LIKE '80.1.12.%'"
#     # pay_warning, customer_warning, bill_warning, rz_warning
#     app_status_warning = "SELECT count(*) FROM app_hosts_info ahi WHERE (ahi.ip_eth0 LIKE '80.1.1.%' OR ahi.ip_eth0 LIKE '80.1.4.%') AND \
#                                               ahi.app_status = 1 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '80.2.%'AND \
#                                               ahi.app_status = 1 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '10.27.%' AND \
#                                               ahi.app_status = 1 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE (ahi.ip_eth0 LIKE '80.1.11.%' OR \
#                                               ahi.ip_eth0 LIKE '80.1.12.%') AND ahi.app_status = 1"
#
#     mem_warning = "SELECT count(*) FROM app_hosts_info ahi WHERE (ahi.ip_eth0 LIKE '80.1.1.%' OR ahi.ip_eth0 LIKE '80.1.4.%') AND \
#                                   ahi.mem_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '80.2.%'AND \
#                                   ahi.mem_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '10.27.%' AND \
#                                   ahi.mem_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE (ahi.ip_eth0 LIKE '80.1.11.%' OR \
#                                   ahi.ip_eth0 LIKE '80.1.12.%') AND ahi.mem_rate > 85"
#
#     disk_warning = "SELECT count(*) FROM app_hosts_info ahi WHERE (ahi.ip_eth0 LIKE '80.1.1.%' OR ahi.ip_eth0 LIKE '80.1.4.%') AND \
#                                   ahi.disk_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '80.2.%'AND \
#                                   ahi.disk_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '10.27.%' AND \
#                                   ahi.disk_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE (ahi.ip_eth0 LIKE '80.1.11.%' OR \
#                                   ahi.ip_eth0 LIKE '80.1.12.%') AND ahi.disk_rate > 85"
#
#     swap_warning = "SELECT count(*) FROM app_hosts_info ahi WHERE (ahi.ip_eth0 LIKE '80.1.1.%' OR ahi.ip_eth0 LIKE '80.1.4.%') AND \
#                                   ahi.swap_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '80.2.%'AND \
#                                   ahi.swap_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '10.27.%' AND \
#                                   ahi.swap_rate > 85 UNION ALL SELECT count(*) FROM app_hosts_info ahi WHERE (ahi.ip_eth0 LIKE '80.1.11.%' OR \
#                                   ahi.ip_eth0 LIKE '80.1.12.%') AND ahi.swap_rate > 85"
#
#     db.query(platform_count)
#     platform_count_result = db.fetchAllRows()
#     graph4 = []
#     for pcr in platform_count_result:
#         graph4.append(str(pcr[0]))
#
#     db.query(app_status_warning)
#     app_status_result = db.fetchAllRows()
#     asr_r = 0
#     asr_r_p = []
#     for asr in app_status_result:
#         asr_r_p.append(int(asr[0]))
#         asr_r += int(asr[0])
#
#     db.query(mem_warning)
#     mem_result = db.fetchAllRows()
#     mr_r = 0
#     mr_r_p = []
#     for mr in mem_result:
#         mr_r_p.append(int(mr[0]))
#         mr_r += int(mr[0])
#
#     db.query(disk_warning)
#     disk_result = db.fetchAllRows()
#     dr_r = 0
#     dr_r_p = []
#     for dr in disk_result:
#         dr_r_p.append(int(dr[0]))
#         dr_r += int(dr[0])
#
#     db.query(swap_warning)
#     swap_result = db.fetchAllRows()
#     sr_r = 0
#     sr_r_p = []
#     for sr in swap_result:
#         sr_r_p.append(int(sr[0]))
#         sr_r += int(sr[0])
#
#     db.close()
#
#     # 处理传入js数值
#     graph1 = '{0},{1},{2},{3}'.format(str(asr_r), str(mr_r), str(dr_r), str(sr_r))
#     graph2 = [str(asr_r_p[0] + mr_r_p[0] + dr_r_p[0] + sr_r_p[0]), str(asr_r_p[1] + mr_r_p[1] + dr_r_p[1] + sr_r_p[1]),
#               str(asr_r_p[2] + mr_r_p[2] + dr_r_p[2] + sr_r_p[2]), str(asr_r_p[3] + mr_r_p[3] + dr_r_p[3] + sr_r_p[3])]
#     graph3 = [str(asr_r_p[0]) + ',' + str(asr_r_p[1]) + ',' + str(asr_r_p[2]) + ',' + str(asr_r_p[3]), str(mr_r_p[0]) +
#               ',' + str(mr_r_p[1]) + ',' + str(mr_r_p[2]) + ',' + str(mr_r_p[3]), str(dr_r_p[0]) + ',' + str(dr_r_p[1])
#               + ',' + str(dr_r_p[2]) + ',' + str(dr_r_p[3]), str(sr_r_p[0]) + ',' + str(sr_r_p[1]) + ',' +
#               str(sr_r_p[2]) + ',' + str(sr_r_p[3])]
#
#     return render_template('hosts_graph.html', graph1=graph1,
#                            graph2=graph2, graph3=graph3, graph4=graph4)
#
#
# @app.route('/hosts_maintain', methods=['GET', 'POST'])
# def hosts_maintain():
#     hosts_file = '/tools/ansible/hosts'
#     bak_hosts_file = '/data/appbak/hosts_' + time.strftime('%Y%m%d%H%M%S')
#     file_dir = '/tools/ansible'
#     file_object = open(hosts_file)
#     try:
#         all_the_text = file_object.read()
#     finally:
#         file_object.close()
#
#     file_dir = os.listdir(file_dir)
#     file_list = []
#     for i in file_dir:
#         # os.path.splitext():分离文件名与扩展名
#         if os.path.splitext(i)[1] == '.yml':
#             file_list.append(i)
#
#     hosts_file_text = request.form.get('hosts_file_text')
#     if hosts_file_text is not None:
#         shutil.copyfile(hosts_file, bak_hosts_file)
#         f = file('/tools/ansible/hosts', 'w+')
#         f.writelines(hosts_file_text)
#         f.close()
#     else:
#         print 'hosts文件内容未改变！'
#
#     return render_template('hosts_maintain.html', all_the_text=all_the_text, file_list=file_list)
#
#
# @app.route('/paycloud', methods=['GET', 'POST'])
# def paycloud():
#     db = MysqlDb_Connection(dbconfig)
#     hostsform = HostsForm()
#     if hostsform.validate_on_submit():
#         ip_add = hostsform.ip_address.data
#         sql = "select id, ip_eth0, app_name_en, owner, app_platform, description from \
#                   app_hosts_info where ip_eth0 = '%s'" % str(ip_add)
#         db.query(sql)
#         db_result = db.fetchAllRows()
#         db.close()
#         return render_template('paycloud_list.html', db_result=db_result, hostsform=hostsform)
#     else:
#         sql = "select id, ip_eth0, app_name_en, owner, app_platform, description from \
#                   app_hosts_info ahi WHERE ahi.ip_eth0 LIKE '80.1.1.%' OR ahi.ip_eth0 LIKE '80.1.4.%'"
#         db.query(sql)
#         db_result = db.fetchAllRows()
#         db.close()
#     return render_template('paycloud_list.html', hostsform=hostsform, db_result=db_result)