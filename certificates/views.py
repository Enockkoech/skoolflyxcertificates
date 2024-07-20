from django.shortcuts import render, get_object_or_404, redirect
from .models import School, Student
from .forms import SchoolForm, StudentForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import qrcode
from io import BytesIO
import uuid
from datetime import datetime
import base64
from xhtml2pdf import pisa
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home(request):
    return render(request, 'certificates/home.html')

def create_school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SchoolForm()
    return render(request, 'certificates/create_school.html', {'form': form})

def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.certificate_number = uuid.uuid4()
            student.save()
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'certificates/create_student.html', {'form': form})

def generate_certificate(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    school = student.school

    # Generate QR code
    qr_data = f'{student.first_name} {student.second_name} - {school.name} - {student.certificate_number}'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Convert logo and profile picture to base64
    school_logo_base64 = base64.b64encode(school.logo.read()).decode()
    profile_picture_base64 = base64.b64encode(student.profile_picture.read()).decode()

    context = {
        'student': student,
        'school': school,
        'qr_code': qr_code_base64,
        'school_logo': school_logo_base64,
        'profile_picture': profile_picture_base64,
    }

    html = render_to_string('certificates/certificate.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{student.certificate_number}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# def verify_certificate(request):
#     certificate_number = request.GET.get('certificate_number')
#     try:
#         student = Student.objects.get(certificate_number=certificate_number)
#         return render(request, 'certificates/verify_certificate.html', {'student': student, 'valid': True})
#     except Student.DoesNotExist:
#         return render(request, 'certificates/verify_certificate.html', {'valid': False})

def verify_certificate(request):
    if request.method == 'POST':
        certificate_number = request.POST.get('certificate_number', None)
        if certificate_number:
            try:
                student = Student.objects.get(certificate_number=certificate_number)
                return JsonResponse({
                    'valid': True,
                    'student_name': f'{student.first_name} {student.second_name}',
                    'date_issued': student.date_created.strftime('%Y-%m-%d'),
                    'certificate_number': student.certificate_number
                })
            except Student.DoesNotExist:
                return JsonResponse({
                    'valid': False,
                    'error': 'Certificate number not found.'
                })
        else:
            return JsonResponse({
                'valid': False,
                'error': 'Certificate number not provided.'
            })
    return render(request, 'certificates/verify_certificate.html')

# def verify_certificate(request):
#     if request.method == 'POST':
#         certificate_number = request.POST.get('certificate_number', None)
#         if certificate_number:
#             try:
#                 student = Student.objects.get(certificate_number=certificate_number)
#                 return JsonResponse({
#                     'valid': True,
#                     'student_name': f'{student.first_name} {student.second_name}',
#                     'date_issued': student.date_created.strftime('%Y-%m-%d'),
#                 })
#             except Student.DoesNotExist:
#                 return JsonResponse({
#                     'valid': False,
#                     'error': 'Certificate number not found.'
#                 })
#         else:
#             return JsonResponse({
#                 'valid': False,
#                 'error': 'Certificate number not provided.'
#             })
#     return render(request, 'certificates/verify_certificate.html')

def certificate_list(request):
    school_name = request.GET.get('school_name')
    year = request.GET.get('year')
    certificates = Student.objects.all()

    if school_name:
        certificates = certificates.filter(school__name__icontains=school_name)
    if year:
        certificates = certificates.filter(date_created__year=year)

    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})
