#!/usr/bin/env python3
import os
from dotenv import load_dotenv
load_dotenv()

mailer = {
    'templatePath'   : './tests/fixtures',
    'from'           : os.getenv('SMTP_SENDER'),
    'to'             : os.getenv('SMTP_RECIPIENT'),
    'port'           : os.getenv('SMTP_PORT', 587),
    'host'           : os.getenv('SMTP_HOST'),
    'smtp_user'      : os.getenv('SMTP_USER'),
    'smtp_password'  : os.getenv('SMTP_PASSWORD'),
}
