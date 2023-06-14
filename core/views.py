import subprocess
import psutil
import xlwt

import datetime as dt
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import auth
from django.http.response import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.utils.timezone import datetime

from face_recognizer.headshot import FaceAdd
from .camera import VideoCamera, VideoCamera_2, gen
from .models import *


def index(request):
    if not is_running("/home/asus/PycharmProjects/Beta_version/face_recognizer/Camera.py"):
        subprocess.call('/home/asus/PycharmProjects/Beta_version/face_recognizer/start.sh', shell=True)
    return render(request, 'lock_screen.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home_page')
        else:
            messages.info(request, gettext('Maglumatlaryňyzy ýalnyş girizdiňiz!'))
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def homepage(request):
    return render(request, 'index.html')


def livefe(request):
    subprocess.call('/home/asus/PycharmProjects/Beta_version/face_recognizer/stop.sh', shell=True)
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


def livefe_2(request):
    subprocess.call('/home/asus/PycharmProjects/Beta_version/face_recognizer/stop.sh', shell=True)
    return StreamingHttpResponse(gen(VideoCamera_2()), content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url='login')
def register(request):
    if not is_running("/home/asus/PycharmProjects/Beta_version/face_recognizer/Camera.py"):
        subprocess.call('/home/asus/PycharmProjects/Beta_version/face_recognizer/start.sh', shell=True)
    if request.method == 'POST':
        name = request.POST['name']
        # name_en = request.POST['name_en']
        # name_ru = request.POST['name_ru']
        profession = request.POST['profession']
        # profession_en = request.POST['profession_en']
        # profession_ru = request.POST['profession_ru']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        person_user = Person.objects.create(name=name, profession=profession,
                                          mail=email, phone_number=phone_number)
        person_user.save()
        FaceAdd(person_user.name, person_user.id)
        return redirect('staff_members')
    else:
        return render(request, 'forms-advanced.html')


@login_required(login_url='login')
def face_add(request):
    return render(request, 'face_recognize.html')


class InputStatistics(LoginRequiredMixin, ListView,):
    model = Get_In
    template_name = 'giris_statistika.html'
    context_object_name = 'get_in'

    def get_queryset(self):
        qs = super(InputStatistics, self).get_queryset()
        today = self.request.GET.get('today')
        week = self.request.GET.get('week')
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        today_date = datetime.today()
        if today:
            qs = qs.filter(get_in_date__gte=today_date)
        if week:
            qs = qs.filter(get_in_date__gte=today_date - dt.timedelta(days=7))
        this_year = today_date.year
        if month:
            this_month = today_date.month
            qs = qs.filter(get_in_date__gte=datetime(this_year, this_month, 1))
        if year:
            qs = qs.filter(get_in_date__gte=datetime(this_year, 1, 1))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if not is_running("/home/asus/PycharmProjects/Beta_version/face_recognizer/Camera.py"):
            subprocess.call('/home/asus/PycharmProjects/Beta_version/face_recognizer/start.sh', shell=True)
        return super().get(request, *args, **kwargs)


class OutputStatistics(LoginRequiredMixin, ListView,):
    model = Get_Out
    template_name = 'cykys_stastika.html'
    context_object_name = 'get_out'

    def get_queryset(self):
        qs = super(OutputStatistics, self).get_queryset()

        today = self.request.GET.get('today')
        week = self.request.GET.get('week')
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        today_date = datetime.today()
        if today:
            qs = qs.filter(get_out_date__gte=today_date)
        if week:
            qs = qs.filter(get_out_date__gte=today_date - dt.timedelta(days=7))
        this_year = today_date.year
        if month:
            this_month = today_date.month
            qs = qs.filter(get_out_date__gte=datetime(this_year, this_month, 1))
        if year:
            qs = qs.filter(get_out_date__gte=datetime(this_year, 1, 1))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if not is_running("/home/asus/PycharmProjects/Beta_version/face_recognizer/Camera.py"):
            subprocess.call('/home/asus/PycharmProjects/Beta_version/face_recognizer/start.sh', shell=True)
        return super().get(request, *args, **kwargs)


@login_required(login_url='login')
def export_get_in_excel_file(request):
    gatnasyk = ""
    qs = Get_In.objects.all()
    if request.method == 'GET':
        today = request.GET.get('today')
        week = request.GET.get('week')
        month = request.GET.get('month')
        year = request.GET.get('year')
        today_date = datetime.today()
        if today:
            qs = qs.filter(get_in_date__gte=today_date)
            gatnasyk = '_su_sun'
        if week:
            qs = qs.filter(get_in_date__gte=today_date - dt.timedelta(days=7))
            gatnasyk = '_su_hepde'
        this_year = today_date.year
        if month:
            this_month = today_date.month
            gatnasyk = '_su_ay'
            qs = qs.filter(get_in_date__gte=datetime(this_year, this_month, 1))
        if year:
            gatnasyk = '_su_yyl'
            qs = qs.filter(get_in_date__gte=datetime(this_year, 1, 1))

    response = HttpResponse(content_type='application/ns-excel')
    response['Content-Disposition'] = f'attachment; filename="gatnasyk_giris{gatnasyk}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('base-detect')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold =True

    columns = [gettext('Ady, Familiýasy'), gettext('Wezipesi'), gettext('Giren güni'), gettext('Giren wagty'), gettext('Giren sany')]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = qs.values_list('person_id__name', 'person_id__profession', 'get_in_date', 'get_in_time', 'count')
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], dt.date):
                gun = row[col_num].strftime('%d.%m.%Y')
                ws.write(row_num, col_num, gun, font_style)
            elif isinstance(row[col_num], dt.time):
                wagt = row[col_num].strftime('%H:%M:%S')
                ws.write(row_num, col_num, wagt, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


@login_required(login_url='login')
def export_get_out_excel_file(request):
    gatnasyk = ""
    qs = Get_Out.objects.all()

    if request.method == 'GET':
        today = request.GET.get('today')
        week = request.GET.get('week')
        month = request.GET.get('month')
        year = request.GET.get('year')
        today_date = datetime.today()
        if today:
            gatnasyk="_su_gun"
            qs = qs.filter(get_out_date__gte=today_date)
        if week:
            gatnasyk="_su_hepde"
            qs = qs.filter(get_out_date__gte=today_date - dt.timedelta(days=7))
        this_year = today_date.year
        if month:
            gatnasyk="_su_ay"
            this_month = today_date.month
            qs = qs.filter(get_out_date__gte=datetime(this_year, this_month, 1))
        if year:
            gatnasyk="_su_yyl"
            qs = qs.filter(get_out_date__gte=datetime(this_year, 1, 1))

    response = HttpResponse(content_type='application/ns-excel')
    response['Content-Disposition'] = f'attachment; filename="gatnasyk_cykys{gatnasyk}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('base-detect')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold =True

    columns = [gettext('Ady, Familiýasy'), gettext('Wezipesi'), gettext('Çykan güni'), gettext('Çykan wagty'), gettext('Çykan sany')]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    font_style = xlwt.XFStyle()
    rows = qs.values_list('person_id__name', 'person_id__profession', 'get_out_date', 'get_out_time', 'count')
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], dt.date):
                gun = row[col_num].strftime('%d.%m.%Y')
                ws.write(row_num, col_num, gun, font_style)
            elif isinstance(row[col_num], dt.time):
                wagt = row[col_num].strftime('%H:%M:%S')
                ws.write(row_num, col_num, wagt, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


class StaffMembers(LoginRequiredMixin, ListView,):
    model = Person
    template_name = 'tables-data.html'
    context_object_name = 'people'
    # paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if not is_running("/home/asus/PycharmProjects/Beta_version/face_recognizer/Camera.py"):
            subprocess.call('/home/asus/PycharmProjects/Beta_version/face_recognizer/start.sh', shell=True)
        return super().get(request, *args, **kwargs)


class PersonView(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'ui-cards.html'
    context_object_name = 'people'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        get_out = Get_Out.objects.all()
        get_in = Get_In.objects.all()
        context['out'] = get_out
        context['get_in'] = get_in
        return context


class PersonDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'tables-data.html'
    success_message = gettext('ulgamdan aýryldy')
    success_url = reverse_lazy('staff_members')

    def get_object(self, queryset=None):
        _id = str(self.kwargs.get('slug'))
        address = get_object_or_404(Person, slug=_id)
        return address


class PersonUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'update.html'
    success_message = gettext('ulgamda maglumaty üýtgedildi')
    success_url = reverse_lazy('staff_members')
    model = Person
    fields = ['name', 'profession',  'mail', 'phone_number', 'image',]

    def get_object(self, queryset=None):
        _id = str(self.kwargs.get('slug'))
        address = get_object_or_404(Person, slug=_id)
        return address


def admin_logout(request):
    auth.logout(request)
    return redirect('/')


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(exception):
    data = {}
    return render('500.html', data)


def error_403(request, exception):
    data = {}
    return render(request, '403.html', data)


def error_400(request, exception):
    data = {}
    return render(request, '400.html', data)


def is_running(script):
    for q in psutil.process_iter():
        if q.name().startswith('python'):
            if len(q.cmdline()) > 1 and script in q.cmdline()[1] and q.pid != os.getpid():
                return True
    return False
