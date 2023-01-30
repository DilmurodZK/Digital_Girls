from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view


@api_view(['GET'])
def contact(request):
    contacts = Contact.objects.last()
    ser = ContactSerializer(contacts)
    return Response(ser.data)


@api_view(['GET'])
def course(request):
    courses = Course.objects.last()
    ser = CourseSerializer(courses)
    return Response(ser.data)


@api_view(['GET'])
def info(request):
    info = Info.objects.last()
    ser = InfoSerializer(info)
    return Response(ser.data)


@api_view(['GET'])
def slider(request):
    slider = Slider.objects.filter(status=True)
    ser = SliderSerializer(slider)
    return Response(ser.data)


@api_view(['GET'])
def about(request):
    about = About.objects.last()
    ser = AboutSerializer(about)
    return Response(ser.data)


@api_view(['GET'])
def about_item(request):
    about_item = AboutItem.objects.filter(status=True)
    ser = AboutItemSerializer(about_item, many=True)
    return Response(ser.data)


@api_view(['GET'])
def course_item(request):
    course_item = CourseItem.objects.filter(status=True)
    ser = CourseItemSerializer(course_item, many=True)
    return Response(ser.data)


@api_view(['GET'])
def task(request):
    tasks = Task.objects.last()
    ser = TaskSerializer(tasks)
    return Response(ser.data)


@api_view(['GET'])
def task_item(request):
    task_item = TaskItem.objects.all()
    ser = TaskItemSerializer(task_item, many=True)
    return Response(ser.data)


@api_view(['GET'])
def result(request):
    results = Result.objects.last()
    ser = ResultSerializer(results)
    return Response(ser.data)


@api_view(['GET'])
def result_item(request):
    result_item = ResultItem.objects.filter(status=True)
    ser = ResultItemSerializer(result_item, many=True)
    return Response(ser.data)


@api_view(['POST'])
def create_application(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    birthday = request.POST.get("birthday")
    email = request.POST.get("email")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    try:
        Application.objects.create(
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            email=email,
            address=address,
            phone=phone,
        )
        return Response('Success')
    except:
        return Response(f'{email} yoki {phone} oldin ishlatilgan')