## Installation

- `pip install git+https://github.com/chris-ca/smtpmailer.git#egg=smtpmailer`

## Configuration
- Mailer expects the following paramters  
```
mailer_config = {
    'save_file'      : 'data/last_email.data',
    'templatePath'   : './templates',
    'from'           : os.getenv('SMTP_SENDER'),
    'to'             : os.getenv('SMTP_RECIPIENT'),
    'port'           : os.getenv('SMTP_PORT', 587),
    'host'           : os.getenv('SMTP_HOST'),
    'smtp_user'      : os.getenv('SMTP_USER'),
    'smtp_password'  : os.getenv('SMTP_PASSWORD'),
}
```
- (Optionally) add parameters for SMTP client in `.env` file:
```
SMTP_HOST="smtp.example.com"
SMTP_USER="username"
SMTP_PASSWORD="hunter2"
SMTP_SENDER="sender@example.com"
SMTP_RECIPIENT="recipient@example.com"
```

## Usage
```
import config
from simplemailer import simplemailer
m = simplemailer.SimpleSMTP(mailer_config)
m.subject = subject
m.setHtmlBody("email.html", movies=movies, criteria=criteria)
m.setTextBody("email.txt", movies=movies, criteria=criteria)
m.send() 
