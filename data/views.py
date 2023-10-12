from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import DataScrap, CSVFiles, DataScrapImages
from django.core import serializers
from django.forms.models import model_to_dict
from django.views import View
from .forms import CSVUploadForm, ImageUploadForm
import csv
import os
import zipfile
import tempfile

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
        image_name = f"{s_data.name}{s_data.designation}"
        matching_images = DataScrapImages.objects.filter(data_scrap=s_data, image__contains=image_name)
        
        if matching_images.exists():
            data.append({
                'id': s_data.id,
                'name': s_data.name,
                'dep': s_data.dep,
                'designation': s_data.designation,
                'address': s_data.address,
                'email': s_data.email,
                'phone_number': s_data.phone_number,
                'link':s_data.link,
                'desc':s_data.desc,
                'hierarchy': s_data.hierarchy,
                'image_name': s_data.image_name,
                'validation': s_data.validation,
            })

        else:
            data.append({
                'id': s_data.id,
                'name': s_data.name,
                'dep': s_data.dep,
                'designation': s_data.designation,
                'address': s_data.address,
                'email': s_data.email,
                'phone_number': s_data.phone_number,
                'link':s_data.link,
                'desc':s_data.desc,
                'hierarchy': s_data.hierarchy,
                'image_name': s_data.image_name,
                'validation': s_data.validation,
            })

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
        csv_form = CSVUploadForm(request.POST, request.FILES)
        if csv_form.is_valid():
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
                ).first()

                if not existing_record:
                    # Create an instance of DataScrap with appropriate field values
                    DataScrap.objects.create(              
                        name=row[0],
                        dep=row[1],
                        designation=row[2],
                        address = row[3],
                        email=row[4],
                        phone_number=row[5],
                        link= row[6],
                        desc = row[7],
                        hierarchy= row[8],
                        image_name = row[9],
                        validation=None  # Assuming you want to set 'validation' to True for all rows
                    )
            print(request.FILES['file'])

            return redirect('data:success_page')
    else:
        csv_form = CSVUploadForm()

    db_csv_files = CSVFiles.objects.all()
    
    return render(request, 'data/upload.html', {'form': csv_form,'csv_files':db_csv_files})



def success_page(request):
    return render(request, 'data/success.html')


# def image_upload(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('data:image_list')  # Redirect to the image list page after successful upload
#     else:
#         form = ImageUploadForm()

#     return render(request, 'data/image_upload.html', {'form': form})


def image_list(request):
    images = DataScrapImages.objects.all()
    return render(request, 'data/image_list.html', {'images': images})


def image_upload(request):
    if request.method == 'POST':
        img_form = ImageUploadForm(request.POST, request.FILES)
        if img_form.is_valid():
            zip_file = img_form.cleaned_data.get('zip_file')  # Access 'zip_file' field correctly

            if zip_file:
                # Check if the uploaded file is a ZIP archive
                if not zip_file.name.lower().endswith('.zip'):
                    return HttpResponseBadRequest("Invalid file format. Please upload a ZIP archive.")

                # Extract the ZIP archive to a temporary folder
                with zipfile.ZipFile(zip_file, 'r') as archive:
                    tmp_dir = tempfile.mkdtemp()
                    archive.extractall(tmp_dir)

                # Process and save the valid images from the extracted folder
                for root, _, files in os.walk(tmp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as img_file:
                            # Check if the file is an image
                            if img_file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):

                                # Generate the image filename
                                filename = os.path.basename(file)

                                # Check if an image with the same name already exists in the database
                                existing_image = DataScrapImages.objects.filter(image=f'images/{filename}').first()

                                if not existing_image:
                                    # If it doesn't exist, save the image to the database
                                    image_instance = DataScrapImages(image=f'images/{filename}')
                                    image_instance.save()
                                else:
                                    # If it exists, skip saving and print a message
                                    print(f"Image with filename '{filename}' already exists. Skipping.")

                return redirect('data:image_list')  # Make sure 'image_list' is defined in your urls.py

    else:
        img_form = ImageUploadForm()

    return render(request, 'data/image_upload.html', {'img_form': img_form})

