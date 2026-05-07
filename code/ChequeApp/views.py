from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
import json
from web3 import Web3, HTTPProvider
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import random
from datetime import date
import pyqrcode
import png
from pyqrcode import QRCode
import hashlib
import cv2
import smtplib

global uname, email, contract, web3
#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:8545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Cheque.json' #cheque contract file
    deployed_contract_address = '0x36B506167fAC2F1c25311C2Abd1224b2332787b4' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def format_tx_receipt(receipt, title):
    tx_hash = receipt['transactionHash'].hex()
    block_num = receipt['blockNumber']
    gas_used = receipt['gasUsed']
    from_addr = receipt['from']
    to_addr = receipt['to']
    html = f"""
    <div class="tx-receipt" style="margin-top: 10px;">
        <h4 style="margin-bottom: 12px; font-weight: 600; font-size: 1.1rem; color: var(--success);">✔ {title}</h4>
        <div style="background: rgba(0,0,0,0.25); padding: 15px; border-radius: 8px; font-family: 'Courier New', Courier, monospace; font-size: 0.95rem; overflow-x: auto; color: var(--text-main); border: 1px solid rgba(255,255,255,0.05);">
            <p style="margin-bottom: 8px;"><strong style="color: var(--text-muted); display: inline-block; width: 140px;">Transaction Hash:</strong> <span style="color: var(--accent-primary); word-break: break-all;">{tx_hash}</span></p>
            <p style="margin-bottom: 8px;"><strong style="color: var(--text-muted); display: inline-block; width: 140px;">Block Number:</strong> {block_num}</p>
            <p style="margin-bottom: 8px;"><strong style="color: var(--text-muted); display: inline-block; width: 140px;">Gas Used:</strong> {gas_used}</p>
            <p style="margin-bottom: 8px;"><strong style="color: var(--text-muted); display: inline-block; width: 140px;">From Address:</strong> {from_addr}</p>
            <p style="margin-bottom: 0;"><strong style="color: var(--text-muted); display: inline-block; width: 140px;">To Contract:</strong> {to_addr}</p>
        </div>
    </div>
    """
    return html


def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def BankLogin(request):
    if request.method == 'GET':
       return render(request, 'BankLogin.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        global contract
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        utype = request.POST.get('t6', False)
        count = contract.functions.getUserCount().call()
        status = "none"
        for i in range(0, count):
            user1 = contract.functions.getUsername(i).call()
            if username == user1:
                status = "exists"
                break
        if status == "none":
            msg = contract.functions.createUser(username, email, password, contact, address, utype).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            formatted_data = format_tx_receipt(tx_receipt, "Blockchain Receipt")
            context = {
                'success': True,
                'tx_html': formatted_data,
                'username': username,
                'contact': contact,
                'email': email,
                'address': address,
                'utype': utype
            }
            return render(request, 'Register.html', context)
        else:
            context= {'error': 'Given username already exists'}
            return render(request, 'Register.html', context)

def BankLoginAction(request):
    if request.method == 'POST':
        global uname, email, contract
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        count = contract.functions.getUserCount().call()
        status = "none"
        for i in range(0, count):
            user1 = contract.functions.getUsername(i).call()
            pass1 = contract.functions.getPassword(i).call()
            utype = contract.functions.getUsertype(i).call()
            email_id = contract.functions.getEmail(i).call()
            if user1 == username and pass1 == password and utype == "Bank":
                uname = username
                email = email_id
                status = "success"
                break
        if status == 'success':
            return redirect('BankDashboard')
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'BankLogin.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global uname, email, contract
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        count = contract.functions.getUserCount().call()
        status = "none"
        for i in range(0, count):
            user1 = contract.functions.getUsername(i).call()
            pass1 = contract.functions.getPassword(i).call()
            utype = contract.functions.getUsertype(i).call()
            email_id = contract.functions.getEmail(i).call()
            if user1 == username and pass1 == password and utype == "User":
                uname = username
                email = email_id
                status = "success"
                break
        if status == 'success':
            return redirect('UserDashboard')
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)

def UserDashboard(request):
    global uname
    output = 'Welcome '+uname
    context= {'data':output}
    return render(request, 'UserScreen.html', context)

def GenerateCheque(request):
    if request.method == 'GET':
        global uname
        count = contract.functions.getUserCount().call()
        banklist = []
        userlist = []
        for i in range(0, count):
            user1 = contract.functions.getUsername(i).call()
            utype = contract.functions.getUsertype(i).call()
            if utype == 'Bank':
                banklist.append(user1)
            else:
                userlist.append(user1)
        output = '<div class="form-group"><label for="t1">Bank Name</label>'
        output += '<select name="t1" id="t1" class="form-control">'
        for i in range(len(banklist)):
            output += '<option value="'+banklist[i]+'">'+banklist[i]+'</option>'
        output += '</select></div>'

        output += '<div class="form-group"><label for="t2">Receiver Name</label>'
        output += '<select name="t2" id="t2" class="form-control">'
        for i in range(len(userlist)):
            if userlist[i] != uname:
                output += '<option value="'+userlist[i]+'">'+userlist[i]+'</option>'
        output += '</select></div>'
        context= {'data1':output}
        return render(request, "GenerateCheque.html", context)

def GenerateChequeAction(request):
    if request.method == 'POST':
        global contract, uname
        bank = request.POST.get('t1', False)
        receiver = request.POST.get('t2', False)
        amount = request.POST.get('t3', False)
        today = str(date.today())
        url = pyqrcode.create(uname+"#"+bank+"#"+receiver+"#"+amount+"#"+today)
        if os.path.exists('ChequeApp/static/files/test.png'):
            os.remove('ChequeApp/static/files/test.png')
        url.png('ChequeApp/static/files/test.png', scale = 6)
        with open('ChequeApp/static/files/test.png', 'rb') as file:
            data = file.read()
        file.close()
        sha256hash = hashlib.sha256(data).hexdigest()
        if os.path.exists('ChequeApp/static/files/test.png'):
            os.remove('ChequeApp/static/files/test.png')
        with open('ChequeApp/static/files/'+sha256hash+".png", 'wb') as file:
            file.write(data)
        file.close()
        msg = contract.functions.createCheque(sha256hash, "Pending").transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        formatted_data = format_tx_receipt(tx_receipt, "Cheque Generation Completed")
        context= {'data': formatted_data}
        return render(request, 'UserScreen.html', context)
                

def getCode(hashcode):
    global uname
    image = cv2.imread('ChequeApp/static/files/'+hashcode+".png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    qr_codes = cv2.QRCodeDetector().detectAndDecode(gray)
    return qr_codes[0]

def ViewStatus(request):
    if request.method == 'GET':
        global uname
        output = '<div class="table-container"><table>'
        output+='<thead><tr><th>Sender Name</th>'
        output+='<th>Bank Name</th>'
        output+='<th>Receiver Name</th>'
        output+='<th>Amount</th>'
        output+='<th>Cheque Date</th>'
        output+='<th>Hashcode</th>'
        output+='<th>Status</th>'
        output+='<th>QR Code</th></tr></thead><tbody>'
        count = contract.functions.getChequeCount().call()
        for i in range(0, count):
            hashcode = contract.functions.getCode(i).call()
            status = contract.functions.getStatus(i).call()
            data = getCode(hashcode)
            print(type(data))
            arr = str(data).strip().split("#")
            if arr[0] == uname or arr[2] == uname:
                output+='<tr><td>'+arr[0]+'</td>'
                output+='<td>'+arr[1]+'</td>'
                output+='<td>'+str(arr[2])+'</td>'
                output+='<td>'+str(arr[3])+'</td>'
                output+='<td>'+str(arr[4])+'</td>'
                output+='<td>'+hashcode[0:30]+'</td>'
                output+='<td><span class="status-badge">'+status+'</span></td>'
                output+='<td><img src="/static/files/'+hashcode+'.png" width="100" height="100" style="border-radius: 8px;"></td></tr>'                    
        output+="</tbody></table></div>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)              
        
def sendMail(sender_email, receiver_email, amount, sender, receiver):
    em = []
    em.append(sender_email)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        email_address = 'kaleem202120@gmail.com'
        email_password = 'xyljzncebdxcubjq'
        connection.login(email_address, email_password)
        connection.sendmail(from_addr="kaleem202120@gmail.com", to_addrs=em, msg='Subject: {}\n\n{}'.format("Cheque Cleared Alert", "Your Cheque successfully cleared to receiver "+receiver+" of amount "+str(amount)))
    em1 = []
    em1.append(sender_email)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        email_address = 'kaleem202120@gmail.com'
        email_password = 'xyljzncebdxcubjq'
        connection.login(email_address, email_password)
        connection.sendmail(from_addr="kaleem202120@gmail.com", to_addrs=em1, msg='Subject: {}\n\n{}'.format("Cheque Cleared Alert", "Your Cheque successfully received from sender "+sender+" of amount "+str(amount)))


def ClearCheque(request):
    if request.method == 'GET':
        global uname
        cheque = request.GET['chequeno']
        sender = request.GET['sender']
        receiver = request.GET['receiver']
        amount = request.GET['amount']
        sender_email = "none"
        receiver_email = "none"
        contract.functions.updateStatus(int(cheque)).transact()
        count = contract.functions.getUserCount().call()
        for i in range(0, count):
            user1 = contract.functions.getUsername(i).call()
            email_id = contract.functions.getEmail(i).call()
            if user1 == sender:
                sender_email = email_id
            if user1 == receiver:    
                receiver_email = email_id
        sendMail(sender_email, receiver_email, amount, sender, receiver)         
        return BankDashboard(request, message='Cheque status successfully cleared')

def BankDashboard(request, message=None):
    global uname, contract
    if request.method == 'GET' or request.method == 'POST':
        # 1. Pending Cheques Table
        pending_rows = ""
        count = contract.functions.getChequeCount().call()
        for i in range(0, count):
            hashcode = contract.functions.getCode(i).call()
            status = contract.functions.getStatus(i).call()
            if status == "Pending":
                data = getCode(hashcode)
                arr = str(data).strip().split("#")
                if arr[1] == uname:
                    pending_rows+='<tr><td>'+arr[0]+'</td>'
                    pending_rows+='<td>'+arr[1]+'</td>'
                    pending_rows+='<td>'+str(arr[2])+'</td>'
                    pending_rows+='<td>'+str(arr[3])+'</td>'
                    pending_rows+='<td>'+str(arr[4])+'</td>'
                    pending_rows+='<td>'+hashcode[0:30]+'</td>'
                    pending_rows+='<td><span class="status-badge">'+status+'</span></td>'
                    pending_rows+='<td><img src="/static/files/'+hashcode+'.png" width="100" height="100" style="border-radius: 8px;"></td>'
                    pending_rows+='<td><a href=\'ClearCheque?chequeno='+str(i)+'&sender='+arr[0]+'&receiver='+arr[2]+'&amount='+arr[3]+'\' class="btn btn-primary" style="padding: 0.5rem; font-size: 0.85rem; margin-top: 0;">Clear</a></td></tr>'
        
        if pending_rows == "":
            output_pending = '<p style="color: var(--text-muted); font-size: 1.1rem;">There are no pending cheques to approve as of now.</p>'
        else:
            output_pending = '<div class="table-container"><table>'
            output_pending+='<thead><tr><th>Sender Name</th>'
            output_pending+='<th>Bank Name</th>'
            output_pending+='<th>Receiver Name</th>'
            output_pending+='<th>Amount</th>'
            output_pending+='<th>Cheque Date</th>'
            output_pending+='<th>Hashcode</th>'
            output_pending+='<th>Status</th>'
            output_pending+='<th>QR Code</th>'
            output_pending+='<th>Clear Cheque</th></tr></thead><tbody>'
            output_pending += pending_rows
            output_pending+="</tbody></table></div>"

        # 2. Daily Transactions Table
        transaction = {}
        for i in range(0, count):
            hashcode = contract.functions.getCode(i).call()
            status = contract.functions.getStatus(i).call()
            data = getCode(hashcode)
            arr = str(data).strip().split("#")
            if arr[1] == uname:
                if arr[4] not in transaction:
                    transaction[arr[4]] = float(arr[3])
                else:
                    transaction[arr[4]] += float(arr[3])
        
        if not transaction:
            output_daily = '<p style="color: var(--text-muted); font-size: 1.1rem;">There are no daily transactions as of now.</p>'
        else:
            output_daily = '<div class="table-container"><table>'
            output_daily+='<thead><tr><th>Bank Name</th>'
            output_daily+='<th>Date</th>'
            output_daily+='<th>Daily Transaction</th></tr></thead><tbody>'
            for key, value in transaction.items():
                output_daily+='<tr><td>'+uname+'</td>'
                output_daily+='<td>'+str(key)+'</td>'
                output_daily+='<td>'+str(value)+'</td></tr>'
            output_daily+="</tbody></table></div>"

        context= {'data': message, 'pending_cheques': output_pending, 'daily_transactions': output_daily}
        return render(request, 'BankScreen.html', context)

        
        
        
