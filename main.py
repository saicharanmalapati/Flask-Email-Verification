import os
import logging
import sys
import re
import requests
import smtplib
import dns.resolver
from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random'


@app.route('/')
def index():
    return render_template('email.html')

# port defines the port used by the api server


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        inputAddress = request.form['emailadd']
        fromAddress = 'corn@bt.com'

    # Simple Regex for syntax checking

        regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
        addressToVerify = str(inputAddress.lower())

        if inputAddress == '':
            print("NONE")
            flash("Enter Email Address")
            return redirect(url_for('index'))
        match = re.match(regex, addressToVerify)

        splitAddress = addressToVerify.split('@')
        domain = str(splitAddress[1])
        records = dns.resolver.query(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mxRecord)
        server.helo(server.local_hostname)
        server.mail(fromAddress)
        code, message = server.rcpt(str(addressToVerify))
        if code == 250:
            valid = "Email is valid"
            return render_template('valid.html', valid=valid, domain=domain)
        if code != 250:
            invalid = "Email is invalid"
            return render_template('invalid.html', invalid=invalid)
    return render_template('invalid.html', invalid="invalid email")


if __name__ == '__main__':
    app.run(debug=True)
