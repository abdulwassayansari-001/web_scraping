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

def data(request):
    return render(request, 'data/data.html')


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

from django.core.paginator import Paginator, EmptyPage
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)

def get_data(request, validation_status=None):
    try:
        if request.method == 'POST':
            # Handle POST request parameters
            validation_status = request.GET.get('validation_status')
            # modification = request.GET.get('modification')
            draw = int(request.POST.get('draw', 1))
            start = int(request.POST.get('start', 0))
            length = int(request.POST.get('length', 10000))

            # Assuming you want to order by 'id', adjust this based on your requirements
            order_column_index = int(request.POST.get('order[0][column]', 0))
            order_direction = request.POST.get('order[0][dir]', '')
            order_column_name = request.POST.get(f'columns[{order_column_index}][data]', 'id')
            ordering = f"{'' if order_direction == 'asc' else '-'}{order_column_name}"

            # Get the search value from the DataTables request
            search_value = request.POST.get('search[value]', '')

            # Get the hierarchy value from the DataTables request
            hierarchy_value = request.POST.get('columns[10][search][value]', '')

            # Use hierarchy_value as the search_value if it is not empty
            final_search_value = hierarchy_value if hierarchy_value else search_value

            # Define the filter conditions based on the columns you want to search
            filter_conditions = Q(id__iexact=final_search_value) | Q(name__icontains=final_search_value) | Q(designation__icontains=final_search_value) | Q(dep__icontains=final_search_value) | Q(hierarchy__icontains=final_search_value)
            
            print('Search value:', search_value)
            print('Hierarchy value:', hierarchy_value)
            if validation_status == 'null':
                scrap_data = DataScrap.objects.filter(validation__isnull=True).filter(filter_conditions).order_by(ordering)
            elif validation_status == 'true':
                scrap_data = DataScrap.objects.filter(validation=True).filter(filter_conditions).order_by(ordering)
            elif validation_status == 'false':
                scrap_data = DataScrap.objects.filter(validation=False).filter(filter_conditions).order_by(ordering)

            # elif validation_status == 'true' and modification == 'true':
            #     # scrap_data = DataScrap.objects.filter(validation=True).filter(filter_conditions).filter(feedback__feedback_data__isnull=False, feedback__feedback_data = '').order_by(ordering)
            #     scrap_data = DataScrap.objects.filter(
            #         filter_conditions,
            #         validation=True,
            #         ).exclude(
            #         Q(feedback__feedback_data__isnull=True) | Q(feedback__feedback_data='')
            #         ).order_by(ordering)
            else:
                # Default case: all data
                print("default")
                scrap_data = DataScrap.objects.filter(filter_conditions).order_by(ordering)

            paginator = Paginator(scrap_data, length)
            page = (start // length) + 1

            try:
                paginated_data = paginator.page(page)
            except EmptyPage:
                paginated_data = []

            data = []

            for s_data in paginated_data:
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

            response = {
                'draw': draw,
                'recordsTotal': scrap_data.count(),
                'recordsFiltered': scrap_data.count(),
                'data': data,
            }

            return JsonResponse(response)
    except Exception as e:
        logging.error(f"Error in get_data view: {e}")
        return JsonResponse({'error': 'An error occurred while processing the request.'}, status=500)


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

def accepted_modification(request):
    return render(request, 'data/modification.html')

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

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

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
                    existing_record.validation = existing_record.validation
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

            # Save the file name in the CSVFiles model
            csv_files_data = CSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            return redirect('data:success_page')
    else:
        csv_form = CSVUploadForm()

    db_csv_files = CSVFiles.objects.all()

    return render(request, 'data/upload.html', {'form': csv_form, 'csv_files': db_csv_files})



def success_page(request):
    return render(request, 'data/success.html')

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
