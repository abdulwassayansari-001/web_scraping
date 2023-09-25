from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import DataScrap, CSVFiles
from django.core import serializers
from django.forms.models import model_to_dict
from django.views import View
from .forms import CSVUploadForm
import csv

def data(request):
    return render(request, 'data/data.html')


def get_scrap_data(request):
    scrap_data = DataScrap.objects.all()
    data = [model_to_dict(s_data) for s_data in scrap_data]
    data = [{
        'id':s_data.id,
        'name': s_data.name,
        'dep': s_data.dep,
        'designation': s_data.designation,
        'email': s_data.email,
        'phone_number': s_data.phone_number,
        'link':s_data.link,
        'hierarchy': s_data.hierarchy,
        'validation': None
    } for s_data in scrap_data]
    return JsonResponse({'scrap_data': data})

def get_data(request):
    scrap_data = DataScrap.objects.all()
    data = [model_to_dict(s_data) for s_data in scrap_data]
    data = [{
        'id':s_data.id,
        'name': s_data.name,
        'dep': s_data.dep,
        'designation': s_data.designation,
        'email': s_data.email,
        'phone_number': s_data.phone_number,
        'link':s_data.link,
        'hierarchy': s_data.hierarchy,
        'validation': s_data.validation
    } for s_data in scrap_data]
    return JsonResponse({'scrap_data': data})

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

def accepted(request):
    return render(request, 'data/accepted.html')

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

def rejected(request):
    return render(request, 'data/rejected.html')


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            csv_file_name = csv_file.name

             # Save the file name in the CSVFiles model
            csv_files_data = CSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

            for row in csv_data:
                # Check if a record with the same values already exists
                existing_record = DataScrap.objects.filter(
                    name=row[0],
                    dep=row[1],
                    designation=row[2],
                    email=row[3],
                    phone_number=row[4],
                ).first()

                if not existing_record:
                    # Create an instance of DataScrap with appropriate field values
                    DataScrap.objects.create(              
                        name=row[0],
                        dep=row[1],
                        designation=row[2],
                        email=row[3],
                        phone_number=row[4],
                        link= row[5] ,
                        hierarchy= row[6],
                        validation=True  # Assuming you want to set 'validation' to True for all rows
                    )
            print(request.FILES['file'])

            return redirect('data:success_page')
    else:
        form = CSVUploadForm()

    db_csv_files = CSVFiles.objects.all()
    
    return render(request, 'data/upload.html', {'form': form,'csv_files':db_csv_files})



def success_page(request):
    return render(request, 'data/success.html')
