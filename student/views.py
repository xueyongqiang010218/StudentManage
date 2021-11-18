from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from student.models import Student


# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/index')
        else:
            return render(request, 'login.html', context={'errmsg': '账号或密码错误'})


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request, request.user)
        return redirect('/')


class Index(LoginRequiredMixin, View):
    def get(self, request):
        page_size = int(request.GET.get('pagesize', 1))
        page_index = int(request.GET.get('pageindex', 1))
        nick_name = request.user.nick_name
        stus = Student.objects.all()
        start = (page_index - 1) * page_size  # 开始数
        end = page_index * page_size  # 截止数
        total = (stus.count() + page_size - 1) / page_size  # 总页数
        stus = stus[start:end]
        return render(request, 'index.html', context={'data': stus, 'nickname': nick_name})

    def post(self, request):
        nick_name = request.user.nick_name
        stus = Student.objects.all()
        name = request.POST.get('search_name')
        if name:
            stus = stus.filter(name__contains=name)
        school = request.POST.get('search_school')
        if school:
            stus = stus.filter(school__contains=school)
        class_name = request.POST.get('search_class')
        if class_name:
            stus = stus.filter(class_name__contains=class_name)
        return render(request, 'index.html',
                      context={'data': stus, 'nickname': nick_name, 'search_name': name, 'search_school': school,
                               'search_class': class_name})


class AddStudent(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add.html')

    def post(self, request):
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        school = request.POST.get('school')
        class_name = request.POST.get('class_name')
        class_position = request.POST.get('class_position')
        phone = request.POST.get('phone')
        admission = request.POST.get('admission')

        stu = Student.objects.create(name=name, gender=gender, school=school, class_name=class_name,
                                     class_position=class_position, phone=phone, admission=admission)
        if stu:
            return redirect('/index')
        else:
            return render(request, 'add.html',
                          context={'name': name, 'gender': gender, 'school': school, 'class_name': class_name,
                                   'class_position': class_position
                              , 'phone': phone, 'admission': admission})


class EditStudent(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Exception as e:
            print(e)
        else:
            return render(request, 'edit.html', context={'student': student})

    def post(self, request, id):
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        school = request.POST.get('school')
        class_name = request.POST.get('class_name')
        class_position = request.POST.get('class_position')
        phone = request.POST.get('phone')
        admission = request.POST.get('admission')
        try:
            student = Student.objects.get(id=id)
        except Exception as e:
            print(e)
        else:
            student.name = name
            student.gender = gender
            student.school = school
            student.class_name = class_name
            student.class_position = class_position
            student.phone = phone
            student.admission = admission
            student.save()
            return redirect('/index')


class DeleteStudent(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            Student.objects.get(id=id).delete()
        except Exception as e:
            print(e)
        return redirect('/index')
