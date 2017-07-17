from django.shortcuts import render
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
                    return HttpResponseRedirect(reverse('system/student.html'))
                else:
                    return render(request, 'system/login.html', {'error': '你输入的密码错误'})
            else:
                return HttpResponse('没有这个用户！')
    return render(request,'')



def logoutAction(request):
    try:
        del request.session['studentID']
    except KeyError:
        pass
    return HttpResponse('你已经成功退出')

