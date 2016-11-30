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

def index(request):
    import os
    recognition_by_me = Recognition.objects.all().filter(recognition_by = request.META['USERNAME'])
    #recognition_for_me = Recognition.objects.all().filter(associate = request.META['USERNAME'])
    return render(request, 'randr/index.html', {'recognition_by_me':recognition_by_me})

#@login_required
def vote(request):
	if request.method == 'POST':
		form = RecognitionForm(request.POST)
		if form.is_valid():
			form.save()
			testMessage =  request.META['USERNAME'] + " voted for " + request.POST['associate'] + " with the following annotation " + request.POST['annotation_title'] 
			messages.success(request, 'Thank You. Your Recognition is successfully Created. ' + testMessage)
                        
			return HttpResponseRedirect('/randr/vote/')
	else:
		form = RecognitionForm()
		# also send names of manager along with associate id
		associates = {obj.employee_id:obj.manager.name if obj.manager else '' for obj in Associate.objects.all()}
		conn = sqlite3.connect('db.sqlite3')
                employees = conn.cursor()
                employees.execute('SELECT employee_id from randr_associate WHERE username = (?) LIMIT 1', (request.META['USERNAME'],))
                for employee in employees:
                    recognitionBy = employee[0]
		#username = {obj.username:obj.employee_id for obj in Associate.objects.all()}
	return render(request, 'randr/vote.html', {'form':form, 'associates':dumps(associates), 'recognitionBy': recognitionBy})


def data(request):
    XLS_FILE = os.getcwd() + "\\associates"
    ROW_SPAN = (1, 2)
    COL_SPAN = (1, 7)
    pythoncom.CoInitialize()
    app = Dispatch("Excel.Application")
    app.Visible = True
    ws = app.Workbooks.Open(XLS_FILE).Sheets(1)
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














