from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

d = {'name': 'Prachaw', 'university': 'Daffodil International University', 'semester': 5, 'department': 'CSE', 'result': 3.63,'courses': [
        {
            'id': 1,
            'course_name': 'Algorithm',
            'teacher': 'Nahid',
            'credit': 3
        },
        {
            'id': 2,
            'course_name': 'Algorithm_Lab',
            'teacher': 'Nahid',
            'credit': 1
        },
        {
            'id': 3,
            'course_name': 'Data Stucture',
            'teacher': 'Zohara Zaman',
            'credit': 3
        },
        {
            'id': 4,
            'course_name': 'Data Stucture_Lab',
            'teacher': 'Zohara Zaman',
            'credit': 1
        },
        {
            'id': 5,
            'course_name': 'Numerical Mathod',
            'teacher': 'Anuz Kumar Chakrabarty',
            'credit': 3
        },
        {
            'id': 6,
            'course_name': 'Statistic',
            'teacher': 'Shirin Shorna',
            'credit': 3
        },
        {
            'id': 7,
            'course_name': 'Economics',
            'teacher': 'Shakiul Hossain',
            'credit': 3
        },
        {
            'id': 8,
            'course_name': 'Software Development 1',
            'teacher': 'Ashraful Islam',
            'credit': 1
        }
    ]}

def Home(request):
    return render(request, 'first_app/home.html', d)

def Result(request):
    return render(request, 'first_app/result.html', d)

def Courses(request):
    return render(request, 'first_app/courses.html', d)
