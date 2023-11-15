from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import DataScrap, CSVFiles, Feedback
from django.core import serializers
from django.forms.models import model_to_dict
from django.views import View
from .forms import CSVUploadForm, FeedbackForm
import csv
import os
import zipfile
import tempfile
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
def data(request):
    return render(request, 'data/data.html')

@login_required(login_url='/login/')
def get_scrap_data(request):
    scrap_data = DataScrap.objects.all()
    data = [model_to_dict(s_data) for s_data in scrap_data]
    data = [{
        'id':s_data.id,
        'name': s_data.name,
        'designation': s_data.designation,
        'dep': s_data.dep,
        'address': s_data.address,
        'email': s_data.email,
        'phone_number': s_data.phone_number,
        'link':s_data.link,
        'desc':s_data.desc,
        'hierarchy': s_data.hierarchy,
        'image_name': s_data.image_name,
        'validation': None
    } for s_data in scrap_data]
    return JsonResponse({'scrap_data': data})

def get_data(request):
    scrap_data = DataScrap.objects.all()
    data = []

    for s_data in scrap_data:
        feedback = Feedback.objects.filter(data_scrap=s_data).first()
        feedback_data = feedback.feedback_data if feedback else ""

        data_entry = {
            'id': s_data.id,
            'name': s_data.name,
            'designation': s_data.designation,
            'dep': s_data.dep,
            'address': s_data.address,
            'email': s_data.email,
            'phone_number': s_data.phone_number,
            'link': s_data.link,
            'desc': s_data.desc,
            'hierarchy': s_data.hierarchy,
            'image_name': s_data.image_name,
            'validation': s_data.validation,
            'feedback_data': feedback_data,
        }

        data.append(data_entry)

    return JsonResponse({'scrap_data': data})


@login_required(login_url='/login/')
def accepted_data(request):
    if request.method == "GET":
        id = request.GET.get("id")
        try:
            data = DataScrap.objects.get(pk=id)
            data.validation = True
            print(f"Data with ID {id} marked as validated.")
            data.save()
            # Convert the Leadership model instance to a dictionary
            data_dict = model_to_dict(data)
            return JsonResponse({"status": "success", 'data':data_dict})
        except DataScrap.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Data record not found."}, status=404
            )

    return JsonResponse(
        {"status": "error", "message": "Invalid request method."}, status=400
    )


@login_required(login_url='/login/')
def accepted(request):
    return render(request, 'data/accepted.html')


@login_required(login_url='/login/')
def rejected_data(request):
    if request.method == "GET":
        id = request.GET.get("id")
        try:
            data = DataScrap.objects.get(pk=id)
            data.validation = False
            print(f"Data with ID {id} marked as validated.")
            data.save()
            # Convert the Leadership model instance to a dictionary
            data_dict = model_to_dict(data)
            return JsonResponse({"status": "success", 'data':data_dict})
        except DataScrap.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Data record not found."}, status=404
            )

    return JsonResponse(
        {"status": "error", "message": "Invalid request method."}, status=400
    )



@login_required(login_url='/login/')
def rejected(request):
    return render(request, 'data/rejected.html')


@login_required(login_url='/login/')
def upload_csv(request):
    if request.method == 'POST':
        csv_form = CSVUploadForm(request.POST, request.FILES)
        if csv_form.is_valid():
            csv_file = request.FILES['file']
            csv_file_name = csv_file.name

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

            data_count = 0

            for row in csv_data:
                # Check if a record with the same values already exists
                existing_record = DataScrap.objects.filter(
                    name=row[0],
                    designation=row[1],
                    dep=row[2],
                ).first()

                if existing_record:
                    # Update the existing record with new data
                    existing_record.address = row[3]
                    existing_record.email = row[4]
                    existing_record.phone_number = row[5]
                    existing_record.link = row[6]
                    existing_record.desc = row[7]
                    existing_record.hierarchy = row[8]
                    existing_record.image_name = row[9]
                    # existing_record.validation = None
                    existing_record.save()
                else:
                    # Create a new instance of DataScrap with appropriate field values
                    DataScrap.objects.create(              
                        name=row[0],
                        designation=row[1],
                        dep=row[2],
                        address=row[3],
                        email=row[4],
                        phone_number=row[5],
                        link=row[6],
                        desc=row[7],
                        hierarchy=row[8],
                        image_name=row[9],
                        validation=None
                    )
                    data_count += 1

            # Save the file name in the CSVFiles model
            csv_files_data = CSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            # Get user
            uploading_user = request.user.username

            logger.info(f'User {uploading_user} uploaded CSV file {csv_file_name}')
            logger.info(f'Total Uploaded Data: {data_count}')
            
            send_email_to_superuser(csv_file_name, data_count, uploading_user)
            return redirect('data:success_page')
    else:
        csv_form = CSVUploadForm()

    db_csv_files = CSVFiles.objects.all()

    return render(request, 'data/upload.html', {'form': csv_form, 'csv_files': db_csv_files})


@login_required(login_url='/login/')
def success_page(request):
    return render(request, 'data/success.html')


@login_required(login_url='/login/')
def feedback_data(request, data_id):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_text = form.cleaned_data['feedback_data']
            # Update the Feedback model associated with the DataScrap
            data_scrap = DataScrap.objects.get(id=data_id)
            feedback, created = Feedback.objects.get_or_create(data_scrap=data_scrap)
            feedback.feedback_data = feedback_text
            print(f"Feedback '{feedback_text}' submitted on ID {data_scrap.id}")
            feedback.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})


from django.core.mail import send_mail
from django.contrib.auth.models import User

def send_email_to_superuser(file_name, data_count, uploading_user):
    subject = 'CSV File Submitted'
    message = f'The user {uploading_user} has uploaded a CSV file \nFile Name: {file_name} \nData Uploaded: {data_count}.'
    from_email = os.environ.get("DEFAULT_FROM_EMAIL")
    to_email = User.objects.filter(is_superuser=True).values_list('email', flat=True)

    try:
        send_mail(subject, message, from_email, to_email, fail_silently=False)
        to_email_list = list(to_email)
        logger.info(f'Successfully sent email to superuser {to_email_list} for CSV file: {file_name}')
    except Exception as e:
        logger.error(f'Failed to send email to superuser for CSV file: {file_name}. Error: {e}')