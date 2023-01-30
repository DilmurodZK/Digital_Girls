from django.shortcuts import render, redirect
from app.models import *
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import ExtractDay, ExtractMonth
import calendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from xlutils.copy import copy
from xlrd import open_workbook
from django.http import HttpResponse
import os
from django.views.generic.base import TemplateView
from django.db.models import Q


def signin_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr = authenticate(username=username, password=password)
        if usr is not None:
            login(request,usr)
            return redirect('dashboard-url')
    return render(request, 'log-in.html')


def password_view(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('new')
        confirm = request.POST.get('confirm')
        if password is not None:
            if password == confirm:
                user.set_password(password)
            else:
                user.save()
        user.save()
        return redirect('password-url')
    context = {
        'user': request.user
    }
    return render(request, 'change-password.html' , context)


@login_required(login_url='login-url')
def logout_view(request):
    logout(request)
    return redirect('dashboard-url')

@login_required(login_url='login-url')
def home_view(request):
    application = Application.objects.all().order_by('-id')[:7]
    count = Application.objects.all().count()
    today = datetime.today() - timedelta(days=1)
    week = datetime.today() - timedelta(days=7)
    month = datetime.today() - timedelta(days=30)
    day = Application.objects.filter(created__gte=today).count()
    weeks = Application.objects.filter(created__gte=week).count()
    months = Application.objects.filter(created__gte=month).count()
    qs = Application.objects.filter(
        created__gte=month
    ).annotate(
        day=ExtractDay("created"),
        mon=ExtractMonth('created'),
    ).values(
        'day', 'mon'
    ).annotate(
        n=Count('pk')
    ).order_by('mon')
    mon_list = []
    for i in qs:
        i['mon']=(calendar.month_abbr[i['mon']])
        if len(mon_list) >= 30:
            del mon_list[0]
            mon_list.append(i)
        else:
            mon_list.append(i)
    context = {
        "all_apps": application,
        "count": count,
        "day": day,
        "week": weeks,
        "month": months,
        "qs": mon_list,
    }
    return render(request, 'dashboard-default.html', context)


# *********************** Contact **********************
@login_required(login_url='login-url')
def contact_view(request):
    context = {
        "contact":Contact.objects.last()
    }
    return render(request, "contact.html", context)


@login_required(login_url='login-url')
def create_contact_view(request):
    if request.method == "POST":
        website = request.POST.get("website")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        long = float(request.POST.get("long"))
        lat = float(request.POST.get("lat"))
        Contact.objects.create(
            website=website,
            phone=phone,
            email=email,
            address=address,
            long=long,
            lat=lat,
        )
        return redirect('contact-url')


@login_required(login_url='login-url')
def update_contact_view(request, pk):
    if request.method == "POST":
        contact = Contact.objects.get(id=pk)
        website = request.POST.get("website")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        long = float(request.POST.get("long"))
        lat = float(request.POST.get("lat"))
        contact.website=website
        contact.phone=phone
        contact.email=email
        contact.address=address
        contact.long=long
        contact.lat=lat
        contact.save()
        return redirect('contact-url')


@login_required(login_url='login-url')
def delete_contact_view(request, pk):
    contact = Contact.objects.get(id=pk)
    contact.delete()
    return redirect('contact-url')


# *********************** Info *************************
@login_required(login_url='login-url')
def info_view(request):
    context = {
        "info":Info.objects.last()
    }
    return render(request, "info.html", context)


@login_required(login_url='login-url')
def create_info_view(request):
    if request.method == "POST":
        name_uz = request.POST.get("name_uz")
        name_ru = request.POST.get("name_ru")
        logo = request.FILES.get("logo")
        instagram = request.POST.get("instagram")
        telegram = request.POST.get("telegram")
        youtube = request.POST.get("youtube")
        facebook = request.POST.get("facebook")
        Info.objects.create(
            name_uz=name_uz,
            name_ru=name_ru,
            logo=logo,
            instagram=instagram,
            telegram=telegram,
            youtube=youtube,
            facebook=facebook,
        )
        return redirect('info-url')


@login_required(login_url='login-url')
def update_info_view(request, pk):
    if request.method == "POST":
        info= Info.objects.get(id=pk)
        name_uz = request.POST.get("name_uz")
        name_ru = request.POST.get("name_ru")
        logo = request.FILES.get("logo")
        instagram = request.POST.get("instagram")
        telegram = request.POST.get("telegram")
        youtube = request.POST.get("youtube")
        facebook = request.POST.get("facebook")
        info.name_uz=name_uz
        info.name_ru=name_ru
        info.instagram=instagram
        info.telegram=telegram
        info.youtube=youtube
        info.facebook=facebook
        if logo is not None:
            info.logo = logo
        info.save()
        return redirect('info-url')


@login_required(login_url='login-url')
def delete_info_view(request, pk):
    info = Info.objects.get(id=pk)
    info.delete()
    return redirect('info-url')


# ********************* Application *******************

def PagenatorPage(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


@login_required(login_url='login-url')
def application_view(request):
    application = Application.objects.all().order_by('-id')
    context = {
        "application": PagenatorPage(application, 10, request)
    }
    return render(request, "application.html", context)


@login_required(login_url='login_url')
def search_view(request):
    if request.method == "POST":
        search = request.POST['search']
        info = Q(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search))
        result = Application.objects.filter(info)
        context = {
            "search": result #PagenatorPage(result, 3, request)
        }
        return render(request, 'search.html', context)


# ********************** Slider ***************************
@login_required(login_url='login-url')
def slider_view(request):
    context = {
        "slider" : Slider.objects.all().order_by('-status'),
    }
    return render(request, 'slider.html', context)


@login_required(login_url='login-url')
def edit_slider_view(request):
    if request.method == "POST":
        edit_id = request.POST['edit_id']
        edit= Slider.objects.get(pk=edit_id)
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        image = request.FILES.get('image')
        edit.title_uz=title_uz
        edit.title_ru=title_ru
        edit.text_uz=text_uz
        edit.text_ru=text_ru
        if image is not None:
            edit.image = image
        edit.save()
        return redirect("slider-url")
    return redirect("slider-url")


@login_required(login_url='login-url')
def activate_slider_view(request, pk):
    slider = Slider.objects.get(id=pk)
    active_slider = Slider.objects.filter(status=True)
    s_list = []
    for i in active_slider:
        if i.status:
            s_list.append(i)
    if len(s_list) == 0:
        slider.status = True
        slider.save()
    else:
        s_list[0].status = False
        s_list[0].save()
        slider.status = True
        slider.save()
    return redirect('slider-url')


@login_required(login_url='login-url')
def delete_slider_view(request, pk):
    slider = Slider.objects.get(id=pk)
    slider.delete()
    return redirect('slider-url')


@login_required(login_url='login-url')
def create_slider_view(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        image = request.FILES.get('image')
        Slider.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            text_uz=text_uz,
            text_ru=text_ru,
            image=image,
        )
        return redirect('slider-url')
    return redirect('slider-url')


@login_required(login_url='login-url')
def result_view(request):
    items = ResultItem.objects.filter(status=True).order_by('-id')
    s_list = []
    for i in items:
        s_list.append(i)
    context = {
        "result" : Result.objects.all(),
        "result_item" : ResultItem.objects.all().order_by("-status"),
        "active_items": items,
        's_len': len(s_list),
    }
    return render(request, "result.html", context)


@login_required(login_url='login-url')
def delete_result_view(request, pk):
    result = Result.objects.get(id=pk)
    result.delete()
    return redirect('result-url')


@login_required(login_url='login-url')
def create_result_view(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        Result.objects.create(
        title_uz=title_uz,
        title_ru=title_ru,
        text_uz=text_uz,
        text_ru=text_ru,
        )
        return redirect("result-url")
    return redirect("result-url")


@login_required(login_url='login-url')
def update_result_view(request):
    if request.method == "POST":
        result_id = request.POST['result_id']
        result= Result.objects.get(pk=result_id)
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        result.title_uz=title_uz
        result.title_ru=title_ru
        result.text_uz=text_uz
        result.text_ru=text_ru
        result.save()
        return redirect("result-url")
    return redirect("result-url")


@login_required(login_url='login-url')
def create_resultitem_view(request):
    if request.method == "POST":
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        icon = request.FILES.get("icon")
        ResultItem.objects.create(
            text_uz=text_uz,
            text_ru=text_ru,
            icon=icon,
        )
        return redirect("result-url")
    return redirect("result-url")


@login_required(login_url='login-url')
def update_resultitem_view(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        item = ResultItem.objects.get(pk=item_id)
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        icon = request.FILES.get("icon")
        item.text_uz = text_uz
        item.text_ru = text_ru
        if icon is not None:
            item.icon = icon
        item.save()
        return redirect("result-url")
    return redirect("result-url")


@login_required(login_url='login-url')
def delete_resultitem_view(request, pk):
    item = ResultItem.objects.get(id=pk)
    item.delete()
    return redirect('result-url')


@login_required(login_url='login-url')
def activate_resultitem_view(request, pk):
    item = ResultItem.objects.get(id=pk)
    if item.status:
        item.status = False
        item.save()
    else:
        item.status = True
        item.save()
    return redirect('result-url')


@login_required(login_url='login-url')
def resultitem_modal_view(request, pk):
    if request.method == "POST":
        modal_1 = request.POST["modal_id"]
        modal_item = ResultItem.objects.get(id=modal_1)
        item = ResultItem.objects.get(id=pk)
        item.status = True
        item.save()
        modal_item.status = False
        modal_item.save()
    return redirect('result-url')


@login_required(login_url='login-url')
def task_view(request):
    items = TaskItem.objects.filter(status=True).order_by('-id')
    t_list = []
    for i in items:
        t_list.append(i)
    context = {
        "task":Task.objects.all(),
        "active_t_item": items,
        "taskitem":TaskItem.objects.all().order_by('-status'),
        "t_len":len(t_list)
    }
    return render(request, "task.html", context)


@login_required(login_url='login-url')
def delete_task_view(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect("task-url")


@login_required(login_url='login-url')
def delete_taskitem_view(request, pk):
    item = TaskItem.objects.get(id=pk)
    item.delete()
    return redirect("task-url")


@login_required(login_url='login-url')
def create_task_view(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        Task.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            text_uz=text_uz,
            text_ru=text_ru,
        )
        return redirect("task-url")
    return redirect("task-url")


@login_required(login_url='login-url')
def create_taskitem_view(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        TaskItem.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
        )
        return redirect("task-url")
    return redirect("task-url")


@login_required(login_url='login-url')
def update_task_view(request):
    if request.method == "POST":
        task_id = request.POST["task_id"]
        task = Task.objects.get(pk=task_id)
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        task.title_uz = title_uz
        task.title_ru = title_ru
        task.text_uz = text_uz
        task.text_ru = text_ru
        task.save()
        return redirect("task-url")
    return redirect("task-url")


@login_required(login_url='login-url')
def update_taskitem_view(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        item = TaskItem.objects.get(pk=item_id)
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        item.title_uz = title_uz
        item.title_ru = title_ru
        item.save()
        return redirect("task-url")
    return redirect("task-url")


@login_required(login_url='login-url')
def activate_taskitem_view(request, pk):
    item = TaskItem.objects.get(id=pk)
    if item.status:
        item.status = False
        item.save()
    else:
        item.status = True
        item.save()
    return redirect('task-url')


@login_required(login_url='login-url')
def taskitem_modal_view(request, pk):
    if request.method == "POST":
        modal = request.POST["t_item_id"]
        modal_item = TaskItem.objects.get(id=modal)
        t_item = TaskItem.objects.get(id=pk)
        t_item.status = True
        t_item.save()
        modal_item.status = False
        modal_item.save()
    return redirect('task-url')


@login_required(login_url='login-url')
def course_view(request):
    context = {
        "course":Course.objects.all(),
    }
    return render(request, "course.html", context)


@login_required(login_url='login-url')
def course_item_view(request):
    items = CourseItem.objects.filter(status=True).order_by('-id')
    c_list = []
    for i in items:
        c_list.append(i)
    context = {
        "c_items": CourseItem.objects.all().order_by("-status"),
        "active_items": items,
        "c_len":len(c_list)
    }
    return render(request, "course-item.html", context)


@login_required(login_url='login-url')
def delete_course_view(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return redirect("course-url")


@login_required(login_url='login-url')
def delete_courseitem_view(request, pk):
    item = CourseItem.objects.get(id=pk)
    item.delete()
    return redirect("course-item-url")


@login_required(login_url='login-url')
def create_course_view(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        Course.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            text_uz=text_uz,
            text_ru=text_ru,
        )
        return redirect("course-url")
    return redirect("course-url")


@login_required(login_url='login-url')
def create_courseitem_view(request):
    if request.method == "POST":
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        icon = request.FILES.get("icon")
        CourseItem.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            icon=icon,
        )
        return redirect("course-item-url")
    return redirect("course-item-url")


@login_required(login_url='login-url')
def update_course_view(request):
    if request.method == "POST":
        course_id = request.POST["course_id"]
        course = Course.objects.get(pk=course_id)
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        course.title_uz = title_uz
        course.title_ru = title_ru
        course.text_uz = text_uz
        course.text_ru = text_ru
        course.save()
        return redirect("course-url")
    return redirect("course-url")


@login_required(login_url='login-url')
def update_courseitem_view(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        item = CourseItem.objects.get(pk=item_id)
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        icon = request.FILES.get("icon")
        item.title_uz = title_uz
        item.title_ru = title_ru
        if icon is not None:
            item.icon = icon
        item.save()
        return redirect("course-item-url")
    return redirect("course-item-url")


@login_required(login_url='login-url')
def activate_courseitem_view(request, pk):
    item = CourseItem.objects.get(id=pk)
    if item.status:
        item.status = False
        item.save()
    else:
        item.status = True
        item.save()
    return redirect('course-item-url')


@login_required(login_url='login-url')
def courseitem_modal_view(request, pk):
    if request.method == "POST":
        modal = request.POST["modal_id"]
        modal_item = CourseItem.objects.get(id=modal)
        item = CourseItem.objects.get(id=pk)
        item.status = True
        item.save()
        modal_item.status = False
        modal_item.save()
    return redirect('course-item-url')


# ********************** About ***************************
@login_required(login_url='login-url')
def about_view(request):
    context = {
        "about":About.objects.all(),
    }
    return render(request, "about.html", context)


@login_required(login_url='login-url')
def about_item_view(request):
    items = AboutItem.objects.filter(status=True).order_by('-id')
    a_list = []
    for i in items:
        a_list.append(i)
    context = {
        "a_items": AboutItem.objects.all().order_by("-status"),
        "active_items": items,
        "a_len":len(a_list)
    }
    return render(request, "about-item.html", context)


@login_required(login_url='login-url')
def delete_about_view(request, pk):
    about = About.objects.get(id=pk)
    about.delete()
    return redirect("about-url")


@login_required(login_url='login-url')
def delete_aboutitem_view(request, pk):
    item = AboutItem.objects.get(id=pk)
    item.delete()
    return redirect("about-item-url")


@login_required(login_url='login-url')
def create_about_view(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        About.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            text_uz=text_uz,
            text_ru=text_ru,
        )
        return redirect("about-url")
    return redirect("about-url")


@login_required(login_url='login-url')
def create_aboutitem_view(request):
    if request.method == "POST":
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        image = request.FILES.get("image")
        AboutItem.objects.create(
            text_uz=text_uz,
            text_ru=text_ru,
            image=image,
        )
        return redirect("about-item-url")
    return redirect("about-item-url")


@login_required(login_url='login-url')
def update_about_view(request):
    if request.method == "POST":
        about_id = request.POST["about_id"]
        about = About.objects.get(pk=about_id)
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        about.title_uz = title_uz
        about.title_ru = title_ru
        about.text_uz = text_uz
        about.text_ru = text_ru
        about.save()
        return redirect("about-url")
    return redirect("about-url")


@login_required(login_url='login-url')
def update_aboutitem_view(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        item = AboutItem.objects.get(pk=item_id)
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        image = request.FILES.get("image")
        item.text_uz = text_uz
        item.text_ru = text_ru
        if image is not None:
            item.icon = image
        item.save()
        return redirect("about-item-url")
    return redirect("about-item-url")


@login_required(login_url='login-url')
def activate_aboutitem_view(request, pk):
    item = AboutItem.objects.get(id=pk)
    if item.status:
        item.status = False
        item.save()
    else:
        item.status = True
        item.save()
    return redirect('about-item-url')


@login_required(login_url='login-url')
def aboutitem_modal_view(request, pk):
    if request.method == "POST":
        modal_about = request.POST["modal_id"]
        modal_item = AboutItem.objects.get(id=modal_about)
        item = AboutItem.objects.get(id=pk)
        item.status = True
        item.save()
        modal_item.status = False
        modal_item.save()
    return redirect('about-item-url')



class ExcelPageView(TemplateView):
    template_name = "application.html"


def export_write_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="applications.xls"'

    path = os.path.dirname(__file__)
    file = os.path.join(path, 'sample.xls')

    rb = open_workbook(file, formatting_info=True)

    wb = copy(rb)
    ws = wb.get_sheet(0)

    row_num = 0  # index start from 0
    rows = Application.objects.all().values_list('first_name', 'last_name', 'phone', 'email', 'birthday', 'address', 'created')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]))

    # wb.save(file) # will replace original file
    # wb.save(file + '.out' + os.path.splitext(file)[-1]) # will save file where the excel file is
    wb.save(response)
    return response