"""
/* This program is free software. It comes without any warranty, to
 * the extent permitted by applicable law. You can redistribute it
 * and/or modify it under the terms of the Do What The Fuck You Want
 * To Public License, Version 2, as published by Sam Hocevar. See
 * http://www.wtfpl.net/ for more details. */
"""
from datetime import date, datetime
from lxml import html
from requests import get

standard_github = [
    'https://github.com/bromite/bromite',
    'https://github.com/LibreOffice/core',
    'https://github.com/veler/DevToys',
    'https://github.com/git/git',
    'https://github.com/keepassxreboot/keepassxc',
    'https://github.com/microsoft/vscode',
    'https://github.com/mozilla/gecko-dev',
    'https://github.com/torproject/tor',
    'https://github.com/onionshare/onionshare',
    'https://github.com/ProtonVPN/win-app',
    'https://github.com/JetBrains/intellij-community',
    'https://github.com/qbittorrent/qBittorrent',
    'https://github.com/veracrypt/VeraCrypt',
    'https://github.com/wireshark/wireshark',
    'https://github.com/beemdevelopment/Aegis',
    'https://github.com/openboard-team/openboard',
    'https://github.com/signalapp/Signal-Android',
    'https://github.com/oxen-io/session-android',
    'https://github.com/gorhill/uBlock',
    'https://github.com/bitwarden/clients',
    'https://github.com/darkreader/darkreader',
    'https://github.com/szTheory/exifcleaner',
    'https://github.com/simple-login/app'
]


def danger_level(days: int) -> str:
    if days <= 150:
        return "is in active Development!"
    elif 150 < days <= 365:
        return "More than 5 months have elapsed since last commit, examine the repo."
    elif days >= 366:
        return "It has been more than a year, project has been orphaned! Stop using ASAP"


def sendmail(sender, receiver, subject):
    import smtplib
    import ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    body = f"Open-Software-Development update for : {datetime.today()}"
    password = "---"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "test.txt"  # In same directory as script

    # Open txt file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, text)
        server.quit()


for i in range(0, len(standard_github)):
    lst = []
    page = get(standard_github[i])
    tree = html.fromstring(page.content)
    last_commit = tree.xpath('//relative-time[@class="no-wrap"]/text()')[0].replace(",", "")
    name = tree.xpath('//a[@data-hovercard-type="organization"]/text()')[0] + \
        "/" + tree.xpath('//a[@data-pjax="#repo-content-pjax-container"]/text()')[0]
    today = date.today()
    datetime_object = datetime.strptime(last_commit, '%b %d %Y').date()

    res = today - datetime_object
    result = "Days since last commit:" + str(res.days) + f"; {name} " + danger_level(res.days) + "\n"
    f = open("test.txt", "a+")
    f.write(result)

sendmail("---", "---", "Test email")
