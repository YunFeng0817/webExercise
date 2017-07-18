from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from system.models import *
# Create your views here.

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
                    request.session['studentID']=ID
                    lst=list(Student.objects.order_by('-sum'))
                    Ranking=lst.index(Student.objects.get(pk=ID))+1
                    return render(request,'system/student.html',{'student_score': student,'Ranking':Ranking})
                else:
                    return render(request,'system/login.html',{'error':'你输入的密码错误'})
            else:
                return HttpResponse('没有这个用户！')
        else:
            if Teacher.objects.filter(TeacherID=ID):
                teacher=Teacher.objects.get(pk=ID)
                if Password==teacher.password:
                    request.session['teacherID']=ID
                    students=Student.objects.order_by('-sum')
                    teacher=Teacher.objects.get(pk=ID)
                    return render(request,'system/teacher.html',{'students':students,'teacher':teacher})
                else:
                    return render(request, 'system/login.html', {'error': '你输入的密码错误'})
            else:
                return HttpResponse('没有这个用户！')
    return HttpResponse('只支持post请求')



def changePassword(request):
    try:
        ID=request.session['studentID']
    except:
        ID=request.session['teacherID']
    else:
        return render(request, 'system/changePassword.html')
    raise Http404

def changeAction(request):
    if request.method=='POST':
        Password=request.POST['newPassword']
        RepeatPassword=request.POST['repeatPassword']
        if Password==RepeatPassword:
            ID=request.session['studentID']
            del request.session['studentID']
            student=Student.objects.get(pk=ID)
            student.password = Password
            student.save()
            Student.objects.get(pk=ID).save()
            return render(request,'system/login.html',{'changePassword':'修改密码成功，请重新登录'})
        else:
            return
    else:
        return HttpResponse('只支持post请求')


def logoutAction(request):
    try:
        del request.session['studentID']
        return redirect('login/')
    except KeyError:
        raise Http404

