#coding=UTF-8
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
                    return render(request,'system/teacher.html',{'students':students,'teacher':teacher,'subject':'排名(按总分排名）'})
                else:
                    return render(request, 'system/login.html', {'error': '你输入的密码错误'})
            else:
                return HttpResponse('没有这个用户！')
    raise Http404



def changePassword(request):
    try:
        ID=request.session['studentID']
        return render(request, 'system/changePassword.html')
    except:
        raise Http404

def changeAction(request):
    try:
        ID = request.session['studentID']
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
                return redirect('/login/')
            else:
                return
        else:
            return HttpResponse('只支持post请求')
    except:
        raise Http404


def logoutAction(request):
    try:
        del request.session['studentID']
        return redirect('login/')
    except KeyError:
        del request.session['teacherID']
        return redirect('login/')
    except:
        raise Http404

def sorted(request,subjectID):
    try:
        ID = request.session['teacherID']
        teacher = Teacher.objects.get(pk=ID)
        if subjectID=='0':
            students = Student.objects.order_by('-sum')
            return render(request, 'system/teacher.html', {'students': students, 'teacher': teacher,'subject':'排名(按总分排名）'})
        elif subjectID=='1':
            students = Student.objects.order_by('-Chinese')
            return render(request, 'system/teacher.html', {'students': students, 'teacher': teacher,'subject':'排名(按语文排名）'})
        elif subjectID=='2':
            students = Student.objects.order_by('-Math')
            return render(request, 'system/teacher.html', {'students': students, 'teacher': teacher,'subject':'排名(按数学排名）'})
        elif subjectID=='3':
            students = Student.objects.order_by('-English')
            return render(request, 'system/teacher.html', {'students': students, 'teacher': teacher,'subject':'排名(按英语排名）'})
        elif subjectID=='4':
            students = Student.objects.order_by('-Physics')
            return render(request, 'system/teacher.html', {'students': students, 'teacher': teacher,'subject':'排名(按物理排名）'})
        elif subjectID=='5':
            students = Student.objects.order_by('-Chemistry')
            return render(request, 'system/teacher.html', {'students': students, 'teacher': teacher,'subject':'排名(按化学排名）'})
        else:
            raise Http404
    except:
        raise Http404


def delete(request):
    try:
        ID = request.session['teacherID']
        teacher = Teacher.objects.get(pk=ID)
        lst=request.POST.getlist('selected_student')
        for studentID in lst:
            Student.objects.get(pk=studentID).delete()
        students = Student.objects.order_by('-sum')
        return render(request, 'system/teacher.html', {'students': students, 'teacher': teacher, 'subject': '排名(按总分排名）'})
    except:
        raise Http404



def search(request):
    try:
        ID = request.session['teacherID']
        teacher = Teacher.objects.get(pk=ID)
        content=request.POST.get('search')
        if list(Student.objects.filter(StudentID__icontains=content))!=[]:
            students=Student.objects.filter(StudentID__icontains=content)
            return render(request,'system/teacher.html',{'students': students, 'teacher': teacher})
        elif list(Student.objects.filter(Name__icontains=content))!=[]:
            students=list(Student.objects.filter(Name__icontains=content))
            return render(request,'system/teacher.html',{'students': students, 'teacher': teacher})
        else:
            return HttpResponse('搜索无结果')
    except:
        raise Http404



def change(request,studentID):
    try:
        ID = request.session['teacherID']
        student=Student.objects.get(pk=studentID)
        return render(request,'system/ACStudent.html',{'student':student})
    except:
        raise Http404


def add(request):
    try:
        ID = request.session['teacherID']
        return render(request,'system/ACStudent.html')
    except:
        raise Http404


def ACaction(request):
    try:
        teacherID = request.session['teacherID']
        ID=request.POST.get('studentID')
        Name=request.POST.get('Name')
        Chinese=request.POST.get('Chinese')
        Math=request.POST.get('Math')
        English=request.POST.get('English')
        Physics=request.POST.get('Physics')
        Chemistry=request.POST.get('Chemistry')
        Password=request.POST.get('Password')
        try:
            student=Student.objects.get(pk=ID)
        except ObjectDoesNotExist:
            student=Student()
        except:
            return Http404
        student.StudentID=ID
        student.Name = Name
        student.Chinese = Chinese
        student.Math = Math
        student.English = English
        student.Physics = Physics
        student.Chemistry = Chemistry
        student.sum=float(Chinese)+float(Math)+float(English)+float(Physics)+float(Chemistry)
        student.password=Password
        student.save()
        return redirect('/change/Action/0/')
    except:
        raise Http404


def divided(request):
    try:
        ID = request.session['teacherID']
        teacher = Teacher.objects.get(pk=ID)
        start=request.POST.get('start')
        end=request.POST.get('end')
        subject=request.POST.get('subject')
        students = Student.objects.order_by('-' + subject)
        chooseStudent = []
        if subject=='Chinese':
            for student in students:
                if float(student.Chinese)>=float(start) and float(student.Chinese)<float(end):
                    chooseStudent.append(student)
            return render(request, 'system/teacher.html',{'students': chooseStudent, 'teacher': teacher, 'subject': '排名(按语文排名）','start':start,'end':end})
        elif subject=='Math':
            for student in students:
                if float(student.Math)>=float(start) and float(student.Math)<float(end):
                    chooseStudent.append(student)
            return render(request, 'system/teacher.html',{'students': chooseStudent, 'teacher': teacher, 'subject': '排名(按数学排名）','start':start,'end':end})
        elif subject=='English':
            for student in students:
                if float(student.English)>=float(start) and float(student.English)<float(end):
                    chooseStudent.append(student)
            return render(request, 'system/teacher.html',{'students': chooseStudent, 'teacher': teacher, 'subject': '排名(按英语排名）','start':start,'end':end})
        elif subject=='Physics':
            for student in students:
                if float(student.Physics)>=float(start) and float(student.Physics)<float(end):
                    chooseStudent.append(student)
            return render(request, 'system/teacher.html',{'students': chooseStudent, 'teacher': teacher, 'subject': '排名(按物理排名）','start':start,'end':end})
        elif subject=='Chemistry':
            for student in students:
                if float(student.Chemistry)>=float(start) and float(student.Chemistry)<float(end):
                    chooseStudent.append(student)
            return render(request, 'system/teacher.html',{'students': chooseStudent, 'teacher': teacher, 'subject': '排名(按化学排名）','start':start,'end':end})
        else:
            for student in students:
                if float(student.sum) >= float(start) and float(student.sum) < float(end):
                    chooseStudent.append(student)
            return render(request, 'system/teacher.html', {'students': chooseStudent, 'teacher': teacher, 'subject':'排名(按总分排名）','start':start,'end':end})
    except:
        raise Http404

