#encoding=UTF-8
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class HostsForm(Form):
    ip_address = StringField('ip_address', validators=[DataRequired(message=u'IP地址不能为空'), Length(1, 64)])


class Md_HostsForm(Form):
    ip_address = StringField('md_ip_address', validators=[DataRequired(message=u'IP地址不能为空'), Length(1, 64)])
    app_name_cn = StringField('md_app_name_cn', validators=[DataRequired(message=u'应用名称不能为空'), Length(1, 64)])
    app_platform = StringField('md_app_platform', validators=[DataRequired(message=u'所属平台不能为空'), Length(1, 64)])
    machine_addr = StringField('md_machine_addr', validators=[DataRequired(message=u'机房位置不能为空'), Length(1, 64)])
    description = StringField('md_description', validators=[DataRequired(), Length(1, 64)])


class LoginForm(Form):
    user_name = StringField('username', validators=[DataRequired(message=u'用户名不能为空'), Length(1, 64)])
    password = StringField('password', validators=[DataRequired(message=u'密码不能为空'), Length(1, 64)])


class AnsibleForm(Form):
    ansible_groupname = StringField('ansible_groupname', validators=[DataRequired(message=u'组名不能为空'), Length(1, 64)])
    ansible_shell = StringField('ansible_shell', validators=[DataRequired(message=u'命令不能为空'), Length(1, 64)])