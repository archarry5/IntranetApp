from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from json import dumps


import os
import sqlite3
from win32com.client import constants, Dispatch
import pythoncom

from django.contrib.auth.decorators import login_required
from .models import Associate
from .forms import RecognitionForm
from .models import Recognition
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def index(request):
    import os
    recognition_by_me = Recognition.objects.all().filter(recognition_by = request.META['USERNAME'])
    return render(request, 'randr/index.html', {'recognition_by_me':recognition_by_me})

def vote(request):
    if request.method == 'POST':
        form = RecognitionForm(request.POST)
        if form.is_valid():
            fromaddr = Associate.objects.all().filter(username = request.META['USERNAME'])[0].email
            toAssociateObj =  Associate.objects.all().filter(employee_id = request.POST['associate'])[0]
            toaddr = toAssociateObj.email
            cc = Associate.objects.all().filter(employee_id = toAssociateObj.manager_id)[0].email

            attachment = 'template'
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr 
            msg['Subject'] = "R and R Test MAIL"
            #msg["Cc"] =  cc
            rcpt = cc.split(",")+ [toaddr]
            body = request.POST['annotation_title']
            #msgText = MIMEText('<b>%s</b><br><img src="cid:%s"><br>' % (body, attachment), 'html')
            html = """\
            <html>
            <head>
                <style>
                    #div1 {
                        margin-left: ''50%'';
                        background-color: ''green'';
                    }
                </style>
                </head>
               <body>
                 <div id=""div1""> Hello  %s </div>
               </body>
            </html>
            """ % (body)
            msgText = MIMEText(html , 'html')
            msg.attach(msgText)

            #fp = open(attachment, 'rb')
            #img = MIMEImage(fp.read())
            #fp.close()
            #img.add_header('Content-ID', '<{}>'.format(attachment))
            #msg.attach(img)
            #msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('dsrelay.hoffman.ds.adp.com',25)
            server.ehlo()
            text = msg.as_string()
            server.sendmail(fromaddr,rcpt , text)
            server.quit()
            
            testMessage =  request.META['USERNAME'] + " voted for " + request.POST['associate'] + " with the following annotation " + request.POST['annotation_title'] 
            messages.success(request, 'Thank You. Your Recognition is successfully Created. ' + testMessage)
           
        return HttpResponseRedirect('/randr/vote/')
    else:
        form = RecognitionForm()
        # also send names of manager along with associate id
        associates = {obj.employee_id:obj.manager.name if obj.manager else '' for obj in Associate.objects.all()}
        recognitionBy = Associate.objects.all().filter(username = request.META['USERNAME'])[0].employee_id;
       
    return render(request, 'randr/vote.html', {'form':form, 'associates':dumps(associates), 'recognitionBy': recognitionBy})

@login_required
def data(request):
    XLS_FILE = os.getcwd() + "\\associates"
    pythoncom.CoInitialize()
    app = Dispatch("Excel.Application")
    app.Visible = True
    ws = app.Workbooks.Open(XLS_FILE).Sheets(1)

    used = ws.UsedRange
    nrows = used.Row + used.Rows.Count - 1
    ncols = used.Column + used.Columns.Count - 1
    # alternative way
    # lastCol = ws.UsedRange.Columns.Count
    # lastRow = ws.UsedRange.Rows.Count
    ROW_SPAN = (1, nrows+1)
    COL_SPAN = (1, ncols+1)
    
    exceldata = [[ws.Cells(row, col).Value 
             for col in xrange(COL_SPAN[0], COL_SPAN[1])] 
             for row in xrange(ROW_SPAN[0], ROW_SPAN[1])]

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    for row in exceldata:
        c.execute('INSERT OR REPLACE INTO randr_associate (employee_id, username, name, email, is_manager, manager_id) VALUES (?,?,?,?,?,?)', row) 
    conn.commit()

    c.execute('SELECT * FROM randr_associate')
    for row in c:
        print row
    return HttpResponse("Records Inserted Successfully")







