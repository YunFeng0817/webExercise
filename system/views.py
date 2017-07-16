from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from system.models import *
# Create your views here.
def login(request):
    if request.method=='POST':
        ID = request.POST.get('ID').strip()
        Password = request.POST.get('Password').strip()
        if request.POST.get('select')=='0':
            if Student.objects.filter(StudentID=ID):
                student=Student.objects.get(pk=ID)
                if Password==student.password:
                    return render(request,'',)
                else:
                    return render(request,'',{'error':'你输入的密码错误'})
            else:
                return HttpResponse('没有这个用户！')
        else:
            if Teacher.objects.filter(TeacherID=ID):
                teacher=Teacher.objects.get(pk=ID)
                if Password==teacher.password:
                    return render()
                else:
                    return render(request, '', {'error': '你输入的密码错误'})
            else:
                return HttpResponse('没有这个用户！')
    return render(request,'')
