## Installation

- `pip install git+https://github.com/chris-ca/simplemailer.git#egg=simplemailer`

## Configuration
- For configuration per user, create `$HOME/.config/simplemailer/config.ini` with credentials

## Usage
### Within Python programs
#### Quick mail
```
import simplemailer
simplemailer.SimpleSMTP.from_config() \
.subject('ehlo this is a test') \
.text('This email body contains no {substitutions} at all') \
.send()
```

#### Email using template and variable substitution 
```
import config
from simplemailer import simplemailer
m = simplemailer.SimpleSMTP(mailer_config)
m.subject = subject
m.setHtmlBody("email.html", movies=movies, criteria=criteria)
m.setTextBody("email.txt", movies=movies, criteria=criteria)
m.send() 
```
