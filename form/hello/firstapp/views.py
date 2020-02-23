from django.shortcuts import render
from subprocess import run,PIPE
import sys

def button(request):
    return render(request, 'home.html')

def external(request):
    inp1 =  request.POST.get('mark')
    inp2 = request.POST.get('year')
    inp3 = request.POST.get('run')
    out = run([sys.executable, '//home//aliana//HiQo//test.py',inp1, inp2, inp3],shell=False,stdout=PIPE)

    return render(request,'home.html',{'data1':out.stdout})