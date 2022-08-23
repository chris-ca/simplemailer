#!/usr/bin/env python3
from os.path import expanduser
from pathlib import Path
import smtplib
import datetime
import logging

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import jinja2
import configparser

class SendMailError(Exception):
    pass

class ConfigError(Exception):
    pass

class SimpleSMTP:
    subject = '[no subject]'
    
    @classmethod
    def from_config(cls, app_name='DEFAULT'):
        """ read config from config.ini in $HOME/.config
            Returns:
                instance of SimpleSMTP
        """
        config = configparser.ConfigParser()
        if not config.read(cls.get_config_file()):
            config_file = cls.create_default_config()
            raise ConfigError(f"Config file not found. New file created at '{config_file}', please edit")

        if not app_name in config:
            raise ConfigError(f'Section "{app_name}" not found in mailer configuration')
        return cls(config[app_name])

    @classmethod
    def create_default_config(cls):
        """ create empty config file """
        path = cls.get_config_file()
        contents = """[DEFAULT]
port           = 587
host           = mail.example.com
smtp_user      = email_login@example.com
smtp_password  = hunter2
from           = My Mailer <mymailer@example.com>
to             = Recipient <recipient@example.com>"""

        with open(path, 'w') as f:
            f.write(contents) 
        return path

    def get_config_file():
        """ Return path to user config file """
        config_dir  = expanduser("~")+'/.config/simplemailer'
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        return config_dir + '/config.ini'

    def __init__(self, config):
        self.bodies = {}

        self.msg = MIMEMultipart('alternative')
        try:
            self.host = config['host']
            self.port = config['port']
            self.mail_user = config['smtp_user']
            self.mail_password = config['smtp_password']
        except Exception as e:
            raise ConfigError('invalid configuration') from e

        self.From = config.get('from', None)
        self.To = config.get('to', None)

        templatePath = config.get('templatePath', './templates')
        templateLoader = jinja2.FileSystemLoader(searchpath=templatePath)
        self.templateEnv = jinja2.Environment(loader=templateLoader)

    """ save the email to file """
    def save_as(self, file):
        with open(file, 'w') as f:
            email = f"Subject: {self.subject}\n"
            email += str(self.msg)
            if self.textBody is not None:
                email += self.textBody
            if self.htmlBody is not None:
                email += self.htmlBody
            f.write(email)

    def setTo(self, s):
        self.To = s

    def setFrom(self, s):
        self.From = s

    def getSubject(self):
        return self.subject

    def setSubject(self, s, **kwargs):
        s = jinja2.Environment(loader=jinja2.BaseLoader).from_string(s)
        self.subject = s.render(**kwargs)

    def setTextFile(self, filename, **kwargs):
        self.setFile('text', filename, **kwargs)

    def setHtmlFile(self, filename, **kwargs):
        self.setFile('html', filename, **kwargs)

    def setFile(self, type_, filename, **kwargs):
        if type_ in self.bodies:
            raise ValueError(f"A {type_} template is already set")
        s = self.templateEnv.get_template(filename)
        s.globals['_now'] = datetime.datetime.utcnow
        self.bodies[type_] = s.render(**kwargs)

    def setBody(self, type_, s, **kwargs):
        if type_ in self.bodies:
            raise ValueError(f"A {type_} template is already set")
        s = jinja2.Environment(loader=jinja2.BaseLoader).from_string(s)
        s.globals['_now'] = datetime.datetime.utcnow
        self.bodies[type_] = s.render(**kwargs)
        
    def setTextBody(self, s, **kwargs):
        self.setBody('text', s, **kwargs)

    def setHtmlBody(self, s, **kwargs):
        self.setBody('html', s, **kwargs)

    def subject(self, s):
        self.subject = s
        return self

    def text(self, s):
        self.setBody('text', s)
        return self

    def to(self, s):
        self.setTo(s)
        return self

    def from_(self, s):
        self.setFrom(s)
        return self

    @property
    def textBody(self):
        return self.bodies['text']

    @property
    def htmlBody(self):
        return self.bodies['html']

    def setParameters(self, **kwargs):
        self.kwargs = kwargs
        body.globals['now'] = datetime.datetime.utcnow

    def _send_email(self, msg):
        """ initiate connection to SMTP server and send email """
        try:
            self.server = smtplib.SMTP(self.host, self.port)
            self.server.ehlo()
            self.server.starttls()
            self.server.login(self.mail_user, self.mail_password)
            self.server.sendmail(msg['From'], msg['To'], msg.as_string())
            self.server.close()
        except Exception as e:
            raise SendMailError('Error while sending email: '+str(e)) from e
             
    def send(self, **kwargs):
        """ validate inputs and send email """
        if self.From is None or self.To is None:
            raise ConfigError('Invalid From/To')

        msg = self.msg
        msg['From']     = self.From
        msg['To']       = self.To
        msg['Subject']  = self.subject

        try:
            msg.attach(MIMEText(self.htmlBody, 'html'))
        except KeyError:
            pass
        try:
            msg.attach(MIMEText(self.textBody, 'plain'))
        except KeyError:
            pass

        self._send_email(msg)
