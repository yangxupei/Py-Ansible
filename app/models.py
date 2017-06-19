# encoding=UTF-8
import MySQLdb
import time
import logging
import os
import json
import MySQLdb
# from collections import namedtuple
# from ansible.inventory import Inventory
# from ansible.vars import VariableManager
# from ansible.parsing.dataloader import DataLoader
# from ansible.executor.playbook_executor import PlaybookExecutor
# from ansible.plugins.callback import CallbackBase
# from ansible.errors import AnsibleParserError


class MysqlDb_Connection():
    u'''对MySQLdb常用函数进行封装的类'''

    error_code = ''  # MySQL错误号码

    _instance = None  # 本类的实例
    _conn = None  # 数据库conn
    _cur = None  # 游标

    _TIMEOUT = 30  # 默认超时30秒
    _timecount = 0

    def __init__(self, dbconfig):
        u'构造器：根据数据库连接参数，创建MySQL连接'
        try:
            self._conn = MySQLdb.connect(host=dbconfig['host'],
                                         port=dbconfig['port'],
                                         user=dbconfig['user'],
                                         passwd=dbconfig['passwd'],
                                         db=dbconfig['db'],
                                         charset=dbconfig['charset'])
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print error_msg

            # 如果没有超过预设超时时间，则再次尝试连接，
            if self._timecount < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                return self.__init__(dbconfig)
            else:
                raise Exception(error_msg)

        self._cur = self._conn.cursor()
        self._instance = MySQLdb

    def query(self, sql):
        u'执行 SELECT 语句'
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:", e.args[0], e.args[1]
            result = False
        return result

    def update(self, sql, data):
        u'执行 UPDATE 及 DELETE 语句'
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql, data)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:", e.args[0], e.args[1]
            result = False
        return result

    def insert(self, sql, data):
        u'执行 INSERT 语句。如主键为自增长int，则返回新生成的ID'
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql, data)
            self._conn.commit()
            return self._conn.insert_id()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            return False

    def fetchAllRows(self):
        u'返回结果列表'
        return self._cur.fetchall()

    def fetchOneRow(self):
        u'返回一行结果，然后游标指向下一行。到达最后一行以后，返回None'
        return self._cur.fetchone()

    def getRowCount(self):
        u'获取结果行数'
        return self._cur.rowcount

    def commit(self):
        u'数据库commit操作'
        self._conn.commit()

    def rollback(self):
        u'数据库回滚操作'
        self._conn.rollback()

    def __del__(self):
        u'释放资源（系统GC自动调用）'
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass

    def close(self):
        u'关闭数据库连接'
        self.__del__()


# class mycallback(CallbackBase):
#     # 这里是状态回调，各种成功失败的状态,里面的各种方法其实都是从写于CallbackBase父类里面的，其实还有很多，可以根据需要拿出来用
#     def __init__(self, *args):
#         super(mycallback, self).__init__(display=None)
#         self.status_ok = json.dumps({})
#         self.status_fail = json.dumps({})
#         self.status_unreachable = json.dumps({})
#         self.status_playbook = ''
#         self.status_no_hosts = False
#         self.host_ok = {}
#         self.host_failed = {}
#         self.host_unreachable = {}
#
#     def v2_runner_on_ok(self, result):
#         host = result._host.get_name()
#         self.runner_on_ok(host, result._result)
#         # self.status_ok=json.dumps({host:result._result},indent=4)
#         self.host_ok[host] = result
#
#     def v2_runner_on_failed(self, result, ignore_errors=False):
#         host = result._host.get_name()
#         self.runner_on_failed(host, result._result, ignore_errors)
#         # self.status_fail=json.dumps({host:result._result},indent=4)
#         self.host_failed[host] = result
#
#     def v2_runner_on_unreachable(self, result):
#         host = result._host.get_name()
#         self.runner_on_unreachable(host, result._result)
#         # self.status_unreachable=json.dumps({host:result._result},indent=4)
#         self.host_unreachable[host] = result
#
#     def v2_playbook_on_no_hosts_matched(self):
#         self.playbook_on_no_hosts_matched()
#         self.status_no_hosts = True
#
#     def v2_playbook_on_play_start(self, play):
#         self.playbook_on_play_start(play.name)
#         self.playbook_path = play.name
#
#
# class ansible_play():
#     # 这里是ansible运行
#     # 初始化各项参数，大部分都定义好，只有几个参数是必须要传入的
#     def __init__(self, playbook, extra_vars={},
#                  host_list='/tools/ansible/hosts',
#                  connection='ssh',
#                  become=False,
#                  become_user=None,
#                  module_path=None,
#                  fork=50,
#                  ansible_cfg=None,  # os.environ["ANSIBLE_CONFIG"] = None
#                  passwords={},
#                  check=False):
#         self.playbook_path = playbook
#         self.passwords = passwords
#         self.extra_vars = extra_vars
#         Options = namedtuple('Options',
#                              ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path',
#                               'forks', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
#                               'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
#         self.options = Options(listtags=False, listtasks=False,
#                                listhosts=False, syntax=False,
#                                connection=connection, module_path=module_path,
#                                forks=fork, private_key_file=None,
#                                ssh_common_args=None, ssh_extra_args=None,
#                                sftp_extra_args=None, scp_extra_args=None,
#                                become=become, become_method=None,
#                                become_user=become_user,
#                                verbosity=None, check=check)
#         if ansible_cfg != None:
#             os.environ["ANSIBLE_CONFIG"] = ansible_cfg
#         self.variable_manager = VariableManager()
#         self.loader = DataLoader()
#         self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=host_list)
#
#     # 定义运行的方法和返回值
#     def run(self):
#         complex_msg = {}
#         if not os.path.exists(self.playbook_path):
#             code = 1000
#             results = {'playbook': self.playbook_path, 'msg': self.playbook_path + ' playbook is not exist',
#                        'flag': False}
#         pbex = PlaybookExecutor(playbooks=[self.playbook_path],
#                                 inventory=self.inventory,
#                                 variable_manager=self.variable_manager,
#                                 loader=self.loader,
#                                 options=self.options,
#                                 passwords=self.passwords)
#         self.results_callback = mycallback()
#         pbex._tqm._stdout_callback = self.results_callback
#         try:
#             code = pbex.run()
#         except AnsibleParserError:
#             code = 1001
#             results = {'playbook': self.playbook_path, 'msg': self.playbook_path + ' playbook have syntax error',
#                        'flag': False}
#             # results='syntax error in '+self.playbook_path #语法错误
#             return code, results
#         if self.results_callback.status_no_hosts:
#             code = 1002
#             results = {'playbook': self.playbook_path, 'msg': self.results_callback.status_no_hosts, 'flag': False,
#                        'executed': False}
#             # results='no host match in '+self.playbook_path
#             return code, results
#
#     def get_result(self):
#         self.result_all = {'success': {}, 'fail': {}, 'unreachable': {}}
#         for host, result in self.results_callback.host_ok.items():
#             self.result_all['success'][host] = result._result
#
#         for host, result in self.results_callback.host_failed.items():
#             self.result_all['failed'][host] = result._result['msg']
#             print host, self.result_all['failed'][host]
#
#         for host, result in self.results_callback.host_unreachable.items():
#             self.result_all['unreachable'][host] = result._result['msg']
#             print host, self.result_all['unreachable'][host]
#
#         data = {}
#         for i in self.result_all['success'].keys():
#             datastructure = self.result_all['success'][i]
#             host_name = datastructure['ansible_facts']['ansible_hostname']
#             description = datastructure['ansible_facts']['ansible_distribution']
#             description_version = datastructure['ansible_facts']['ansible_distribution_version']
#             ansible_machine = datastructure['ansible_facts']['ansible_machine']
#             sysinfo = '%s %s %s' % (description, description_version, ansible_machine)
#             kernel = datastructure['ansible_facts']['ansible_kernel']
#             cpu = datastructure['ansible_facts']['ansible_processor'][1]
#             cpu_count = datastructure['ansible_facts']['ansible_processor_count']
#             cpu_cores = datastructure['ansible_facts']['ansible_processor_cores']
#             mem = datastructure['ansible_facts']['ansible_memtotal_mb']
#             ipadd_in = datastructure['ansible_facts']['ansible_all_ipv4_addresses'][0]
#             disk = datastructure['ansible_facts']['ansible_devices']['sda']['size']
#             ansible_mounts = datastructure['ansible_facts']['ansible_mounts']
#             ansible_memory_mb_nocache = datastructure['ansible_facts']['ansible_memory_mb']['nocache']
#             ansible_memory_mb_real = datastructure['ansible_facts']['ansible_memory_mb']['real']
#             ansible_memory_mb_swap = datastructure['ansible_facts']['ansible_memory_mb']['swap']
#
#             mem_total = ansible_memory_mb_real['total']
#             mem_free = ansible_memory_mb_nocache['free']
#             swap_total = ansible_memory_mb_swap['total']
#             swap_free = ansible_memory_mb_swap['free']
#             for am in ansible_mounts:
#                 if am['mount'] == '/':
#                     disk_total = am['size_total']/1024/1024
#                     disk_free = am['size_available']/1024/1024
#                 else:
#                     pass
#
#             mem_rate = "%.1f" % ((1 - (mem_free/mem_total))*100)
#             swap_rate = "%.1f" % ((1 - (swap_free / swap_total))*100)
#             disk_rate = "%.1f" % ((1 - (disk_free / disk_total))*100)
#
#             data['mem_rate'] = mem_rate
#             data['swap_rate'] = swap_rate
#             data['disk_rate'] = disk_rate
#             data['mem_total'] = mem_total
#             data['mem_free'] = mem_free
#             data['swap_total'] = swap_total
#             data['swap_free'] = swap_free
#             data['disk_total'] = disk_total
#             data['disk_free'] = disk_free
#             data['sysinfo'] = str(sysinfo)
#             data['cpu'] = str(cpu)
#             data['cpu_count'] = cpu_count
#             data['cpu_cores'] = cpu_cores
#             data['mem'] = mem
#             data['disk'] = str(disk)
#             data['ipadd_in'] = str(ipadd_in)
#             data['kernel'] = str(kernel)
#             data['host_name'] = str(host_name)
#
#             db = MySQLdb.connect("192.168.1.220", "root", "Asd@1234", "ansible_tools")
#             cursor = db.cursor()
#
#             #print data
#             sql = "INSERT INTO app_hosts_info (ip_eth0, host_name, cpu, sysinfo, disk, cpu_count, cpu_cores, \
#                         mem, os_kernel, mem_total, mem_free, swap_total, swap_free, disk_total, disk_free, mem_rate, swap_rate, \
#                         disk_rate) VALUES (%(ipadd_in)s, %(host_name)s, %(cpu)s, %(sysinfo)s, %(disk)s, %(cpu_count)s, %(cpu_cores)s, \
#                         %(mem)s, %(kernel)s, %(mem_total)s, %(mem_free)s, %(swap_total)s, %(swap_free)s, %(disk_total)s, %(disk_free)s, \
#                         %(mem_rate)s, %(swap_rate)s, %(disk_rate)s)"
#
#             try:
#                 cursor.execute(sql, data)
#                 db.commit()
#             except:
#                 db.rollback()
#
#                 # 关闭数据库连接
#             db.close()

# if __name__ == '__main__':
#     play_book = ansible_play('/tools/ansible/test.yml')
#     play_book.run()
#     play_book.get_result()
