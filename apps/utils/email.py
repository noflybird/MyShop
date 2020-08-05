# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from django.conf import settings


class SendEmail(object):

    def send(self, code, email):
        email_title = '注册验证码'
        email_body = '验证码'
        email_to = email
        msg = "您好: <br/>  感谢您的注册，您的注册验证码为:{}请在10分钟内输入使用。".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email_to], html_message=msg)
        ret = {}
        if send_status:
            ret = {
                'success': True,
                'retCode': 200,
                'retMsg': "邮件添发送成功！"
            }
        else:
            ret = {
                'success':False,
                'retCoode': 400,
                'retMsg': "邮件发送失败"
            }
        return ret
