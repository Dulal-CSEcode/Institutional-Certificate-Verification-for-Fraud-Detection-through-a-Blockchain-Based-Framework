
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session,send_from_directory
import json
from web3 import Web3, HTTPProvider
import hashlib
from hashlib import sha256
#from hashlib import sha512 

import os
import datetime
import pyqrcode
import png
from pyqrcode import QRCode

app = Flask(__name__)

app.secret_key = 'welcome'
global uname, details, sid

def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:7545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CertificateVerification.json' #certification verification contract code
    deployed_contract_address = '0x9895084d88973BA054173364a87EF843DBCc9319' #hash address to access certification verification contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'company':
        details = contract.functions.getCompanyDetails().call()
    if contract_type == 'certificate':
        details = contract.functions.getCertificateDetails().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract

    details = ""
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))

    sender_address = web3.eth.accounts[0]
    web3.eth.defaultAccount = sender_address

    compiled_contract_path = 'CertificateVerification.json'
    deployed_contract_address = '0x9895084d88973BA054173364a87EF843DBCc9319'

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    readDetails(contract_type)

    # ✅ Append new data
    details += currentData

    # ✅ Contract write logic
    if contract_type == 'company':
        msg = contract.functions.setCompanyDetails(details).transact({'from': sender_address})
    elif contract_type == 'certificate':
        msg = contract.functions.setCertificateDetails(details).transact({'from': sender_address})
    else:
        raise ValueError("Invalid contract_type provided")

    # ✅ Confirm transaction
    tx_receipt = web3.eth.wait_for_transaction_receipt(msg)


from flask import redirect, url_for

@app.route('/')
def home():
    return redirect(url_for('index'))   


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', msg='')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
   return render_template('Login.html', msg='')

@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin():
   return render_template('AdminLogin.html', msg='')

@app.route('/AdminLoginAction', methods=['GET', 'POST'])
def AdminLoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        if user == "admin" and password == "admin":
            return render_template('AdminScreen.html', msg="Welcome "+user)
        else:
            return render_template('Login.html', msg="Invalid login details")

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    return render_template('Signup.html', msg='')

@app.route('/LoginAction', methods=['GET', 'POST'])
def LoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('company')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == user and array[1] == password:
                uname = user
                status = "success"
                break
        if status == "success":
            return render_template('UserScreen.html', msg="Welcome "+uname)
        else:
            return render_template('Login.html', msg="Invalid login details")

@app.route('/ViewCertificates', methods=['GET', 'POST'])
def ViewCertificates():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Student ID', 'Student Name', 'Department Name', 'Contact No', 'Address Details', 'Date & Time', 'Certificate Signature (Hashcode)', 'QR Code']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('certificate')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"
            output += "<td>"+font+array[5]+"</td>"
            output += "<td>"+font+array[6]+"</td>"
            output+='<td><img src="/static/qrcode/'+array[0]+'.png" width="200" height="200"></img></td>'
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewCertificates.html', msg=output)         

@app.route('/ViewCompanies', methods=['GET', 'POST'])
def ViewCompanies():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Company Username', 'Password', 'Phone No', 'Email ID', 'Company Address']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('company')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"            
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewCertificates.html', msg=output) 
        
        
@app.route('/SignupAction', methods=['GET', 'POST'])
def SignupAction():
    if request.method == 'POST':
        global details
        uname = request.form['t1']
        password = request.form['t2']
        phone = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        status = "none"
        readDetails('company')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == uname:
                status = uname+" Username already exists"
                break
        if status == "none":
            data = uname+"#"+password+"#"+phone+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"company")
            context = "Company signup task completed"
            return render_template('Signup.html', msg=context)
        else:
            return render_template('Signup.html', msg=status)

@app.route('/Logout')
def Logout():
    return render_template('index.html', msg='')



from flask import Flask, render_template, request
import pyqrcode
import datetime
from hashlib import sha256

#from hashlib import sha512

def readDetails(filename):
    global details
    try:
        with open(filename + ".txt", "r") as f:
            details = f.read()
    except FileNotFoundError:
        details = ""

# Checks if a student ID already exists in the file
def checkID(student_id):
    readDetails('certificate')
    arr = details.split("\n")
    for line in arr:
        parts = line.strip().split("#")
        if len(parts) > 0 and parts[0] == student_id:
            return True
    return False

# Checks if a digital signature already exists in the file
def is_duplicate_signature(signature, filename="certificate"):
    try:
        with open(filename + ".txt", "r") as file:
            for line in file:
                if signature in line:
                    return True
    except FileNotFoundError:
        return False
    return False

# Saves certificate data to the file (like a blockchain log)
def saveDataBlockChain(data, filename):
    with open(filename + ".txt", "a") as f:
        f.write(data)




@app.route('/AddCertificate')
def AddCertificate():
    return render_template('AddCertificate.html', msg='')


@app.route('/AddCertificateAction', methods=['POST'])
def AddCertificateAction():
    sid = request.form['t1']
    sname = request.form['t2']
    department = request.form['t3']
    contact = request.form['t4']
    address = request.form['t5']
    certificate = request.files['t6']
    filename = certificate.filename
    contents = certificate.read()
    current_time = datetime.datetime.now()

    # # Generate sha256 signature
    digital_signature = sha256(contents).hexdigest()



    # ✅ Step 2: Generate SHA-512 signature instead of SHA-256
    #digital_signature = sha512(contents).hexdigest()

    # Extract binary representation (first 64 bytes)
    binary_representation = ' '.join(format(byte, '08b') for byte in contents[:64])
    if len(contents) > 64:
        binary_representation += " ..."

    # Check for duplicate signature
    if is_duplicate_signature(digital_signature):
        context = (
            f"❌ Certificate already exists with this digital signature.<br/>"
            f"<b>Signature:</b> {digital_signature}<br/>"
            f"<b>Scanned Binary Bits (First 64 bytes):</b><br/><code>{binary_representation}</code>"
        )
        return render_template('Download.html', msg=context, sid=None)

    # Check for duplicate Student ID
    if checkID(sid):
        context = f"⚠️ Student ID {sid} already exists. Please use a different ID."
        return render_template('Download.html', msg=context, sid=None)

    # Prepare QR code
    qr_data = (
        f"Certificate Details:\n"
        f"ID: {sid}\n"
        f"Name: {sname}\n"
        f"Department: {department}\n"
        f"Contact: {contact}\n"
        f"Address: {address}\n"
        f"Timestamp: {current_time}\n"
        f"Digital Signature: {digital_signature}"
    )
    qr = pyqrcode.create(qr_data)
    qr.png(f'static/qrcode/{sid}.png', scale=6)

    # Save to Blockchain
    data = f"{sid}#{sname}#{department}#{contact}#{address}#{current_time}#{digital_signature}\n"
    saveDataBlockChain(data, "certificate")

    # Success message with binary bit display
    context = (
        f"✅ Certificate successfully added for <b>ID:</b> {sid}<br/>"
        f"<b>Digital Signature:</b> {digital_signature}<br/><br/>"
        f"<b>Scanned Binary Bits (First 64 bytes):</b><br/><code>{binary_representation}</code><br/><br/>"
        f"<b>Download your QR code below:</b>"
    )
    return render_template('Download.html', msg=context, sid=sid)



@app.route('/AuthenticateScan', methods=['GET', 'POST'])
def AuthenticateScan():
   return render_template('AuthenticateScan.html', msg='')


@app.route('/AuthenticateScanAction', methods=['GET', 'POST'])
def AuthenticateScanAction():
    if request.method == 'POST':
        barcode = request.files['t1']
        contents = barcode.read()
        digital_signature = sha256(contents).hexdigest();
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Student ID', 'Student Name', 'Department Name', 'Contact No', 'Address Details', 'Date & Time', 'Certificate Signature (Hash Code)', 'Status']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('certificate')
        arr = details.split("\n")
        flag = 0
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[6] == digital_signature:
                flag = 1
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
                output += "<td>"+font+array[6]+"</td>"
                output += "<td>"+font+"Authentication Successfull"+"</td>"
        if flag == 0:
            output += "<tr><td>Uploaded Certificate Authentication Failed</td></tr>"
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewDetails.html', msg=output)


    app.run()



if __name__ == '__main__':
    app.run(debug=True)



