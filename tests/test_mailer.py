#!/usr/bin/env python3
import pytest
import os
import config

import simplemailer

@pytest.fixture
def mailer():
    mailer = simplemailer.SimpleSMTP(config.mailer)
    return mailer

@pytest.fixture
def invalid_mailer():
    mailer = simplemailer.SimpleSMTP({
        'host'          : 'invalidmail.example.org',
        'port'          : 587,
        'smtp_user'     : 'invalid',
        'smtp_password' : 'invalid',
        'from'          : 'invalid',
        'to'            : 'invalid',
    })
    return mailer

def test_inline_variable_substitutions(mailer):
    mailer.setSubject('hello i am a {{test}}', **{'test': 'subject'})
    assert mailer.subject == 'hello i am a subject'
    mailer.setTextBody('hello i am a test {{email}}', **{'email' : 'letter'})
    assert mailer.textBody == 'hello i am a test letter'
    mailer.setHtmlBody('<html>{{html}} test </html>', **{'html' : 'HTML'})
    assert mailer.htmlBody == '<html>HTML test </html>'

def test_parse_files(mailer):
    mailer.setHtmlFile('mail.html', **{'fixture' : 'successful'})
    assert mailer.htmlBody == '''<html>
<h1>Mail title</h1>
<p>This is a successful email</p>
</html>'''

def test_failed_email(invalid_mailer):
    invalid_mailer.setTextBody('dang')
    with pytest.raises(simplemailer.SendMailError):
        invalid_mailer.send()

def test_invalid_config():
    with pytest.raises(simplemailer.ConfigError):
        mailer = simplemailer.SimpleSMTP({'host':'asf'})

#@pytest.mark.skip()
def test_send(mailer):
    mailer.setTextBody('This email body contains no {substitutions} at all')
    mailer.send() 
