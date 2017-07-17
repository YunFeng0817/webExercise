from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from system.models import *
# Create your views here.
studentID=0
teacherID=0
def login(request):
    return render(request,'system/login.html')
def loginAction(request):
    if request.method=='POST':
        ID = request.POST.get('ID').strip()
        Password = request.POST.get('Password').strip()
        if request.POST.get('select')=='0':
            if Student.objects.filter(StudentID=ID):
                student=Student.objects.get(pk=ID)
                if Password==student.password:
                    studentID=ID
                    return HttpResponseRedirect(reverse('system:login'))
                else:
                    return render(request,'system/login.html',{'error':'你输入的密码错误'})
            else:
                return HttpResponse('没有这个用户！')
        else:
            if Teacher.objects.filter(TeacherID=ID):
                teacher=Teacher.objects.get(pk=ID)
                if Password==teacher.password:
                    teacherID=ID
                    return HttpResponse('登陆成功')
                else:
                    return render(request, 'system/login.html', {'error': '你输入的密码错误'})
            else:
                return HttpResponse('没有这个用户！')
    return render(request,'')

