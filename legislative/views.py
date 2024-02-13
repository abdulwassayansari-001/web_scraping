from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import *
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)


def success_page(request):
    return render(request, 'legislative/success_page.html')


def data(request):
    return render(request, 'data.html')



def data_json(request):
    try:
        draw = int(request.POST.get('draw', 1))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10000))

        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_direction = request.POST.get('order[0][dir]', '')
        order_column_name = request.POST.get(f'columns[{order_column_index}][data]', 'id')
        ordering = f"{'' if order_direction == 'asc' else '-'}{order_column_name}"

        search_value = request.POST.get('search[value]', '')

        # Debugging to check the received search value
        print('Search value:', search_value)

        filter_conditions = (
            Q(member__name__icontains=search_value) |
            Q(committee__name__icontains=search_value) |
            Q(subcommittee__name__icontains=search_value) |
            Q(title__title__icontains=search_value) |
            Q(hierarchy__hierarchy__icontains=search_value)
        )

        data_list = Data.objects.filter(filter_conditions).order_by(ordering)

        paginator = Paginator(data_list, length)
        page = (start // length) + 1

        try:
            paginated_data = paginator.page(page)
        except EmptyPage:
            paginated_data = []

        data = []

        for item in paginated_data:
            data_entry = {
                'id': item.id,
                'member': None,
                'committee': None,
                'subcommittee': None,
                'title': None,
            }

            # Serialize related objects
            # Member
            if item.member:
                data_entry['member'] = {
                    'id': item.member.id,
                    'name': item.member.name,
                    'state': item.member.state,
                    'district': item.member.district,
                    'party': item.member.party,
                    'member_title': item.member.member_title,
                    'employer': item.member.employer,
                    'email': item.member.email,
                    'phone': item.member.phone_number,
                    'address': item.member.address,
                    'desc': item.member.desc,
                    'link':item.member.link,
                    'image_name':item.member.image_name,
                }

            # Committee
            if item.committee:
                data_entry['committee'] = {
                    'id': item.committee.id,
                    'name': item.committee.name,
                    'link':item.committee.link
                }

            # Sub Committee
            if item.subcommittee:
                data_entry['subcommittee'] = {
                    'id': item.subcommittee.id,
                    'name': item.subcommittee.name,
                    'link':item.subcommittee.link
                }

            # Title
            if item.title:
                data_entry['title'] = {
                    'id': item.title.id,
                    'name': item.title.title,
                }

            # Hierarchy
            if item.hierarchy:
                data_entry['hierarchy'] = {
                    'id': item.hierarchy.id,
                    'name': item.hierarchy.hierarchy,
                }

            data.append(data_entry)

        response = {
            'draw': draw,
            'recordsTotal': data_list.count(),
            'recordsFiltered': data_list.count(),
            'data': data,
        }

        return JsonResponse(response)

    except Exception as e:
        logging.error(f"Error in data_json view: {e}")
        return JsonResponse({'error': 'An error occurred while processing the request.'}, status=500)



import csv

def upload_member_csv(request):
    if request.method == 'POST':
        csv_form = CSVMemberForm(request.POST, request.FILES)
        if csv_form.is_valid():
            csv_file = request.FILES['file']
            csv_file_name = csv_file.name

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

            for row in csv_data:
                # Check if a record with the same values already exists
                existing_record = Members.objects.filter(
                    name=row[0],
                ).first()

                if existing_record:
                    # Update the existing record with new data
                    existing_record.state = row[1]
                    existing_record.district = row[2]
                    existing_record.party = row[3]
                    existing_record.member_title = row[4]
                    existing_record.employer = row[5]
                    existing_record.email = row[6]
                    existing_record.phone_number = row[7]
                    existing_record.address = row[8]
                    existing_record.desc = row[9]
                    existing_record.image_name = row[10]
                    existing_record.link = row[11]
                    existing_record.save()
                else:
                    # Create a new instance of DataScrap with appropriate field values
                    Members.objects.create(              
                        name=row[0],
                        state=row[1],
                        district=row[2],
                        party=row[3],
                        employer=row[4],
                        email=row[5],
                        phone_number=row[6],
                        address=row[7],
                        desc=row[8],
                        image_name=row[9],
                        link = row[10]
                    )

            # Save the file name in the CSVFiles model
            csv_files_data = LegislativeCSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            return redirect('data:success_page')
    else:
        csv_form = CSVMemberForm()

    db_csv_files = LegislativeCSVFiles.objects.all()

    return render(request, 'upload.html', {'member_form': csv_form, 'csv_files': db_csv_files})


def upload_combine_data_csv(request):
    if request.method == 'POST':
        csv_form = CombineDataForm(request.POST, request.FILES)
        if csv_form.is_valid():
            csv_file = request.FILES['file']
            csv_file_name = csv_file.name

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

            for row in csv_data:
                # # Check if a record with the same values already exists
                # existing_record = CombineData.objects.filter(
                #     name=row[0],
                #     committee=row[11],
                #     subcommittee=row[12],
                #     member_title=row[9],
                #     employer=row[4]
                # ).first()

                # if existing_record:
                #     # Update the existing record with new data
                #     existing_record.state = row[1],
                #     existing_record.district = row[2],
                #     existing_record.party = row[3],
                #     existing_record.email = row[5],
                #     existing_record.phone_number = row[6],
                #     existing_record.address = row[7],
                #     existing_record.desc = row[8],
                #     existing_record.committee_title=row[10],
                #     existing_record.hierarchy=row[13],
                #     existing_record.image_name = row[14],
                #     existing_record.subcommittee_link = row[15],
                #     existing_record.committee_link = row[16],
                #     existing_record.member_link = row[17]
                #     existing_record.save()
                # else:
                    # Create a new instance of DataScrap with appropriate field values
                    CombineData.objects.create(
                    name=row[0],
                    state = row[1],
                    district = row[2],
                    party = row[3],
                    employer=row[4],      
                    email = row[5],
                    phone_number = row[6],
                    address = row[7],
                    desc = row[8],
                    member_title=row[9],
                    committee_title=row[10],
                    committee=row[11],
                    subcommittee=row[12],
                    hierarchy=row[13],
                    image_name = row[14],
                    subcommittee_link = row[15],
                    committee_link = row[16],
                    member_link = row[17]
                    )

            # Save the file name in the CSVFiles model
            csv_files_data = LegislativeCSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            return redirect('data:success_page')
    else:
        csv_form = CombineDataForm()

    db_csv_files = LegislativeCSVFiles.objects.all()

    return render(request, 'upload.html', {'combine_form': csv_form, 'csv_files': db_csv_files})


def upload_committee_csv(request):
    if request.method == 'POST':
        csv_form = CSVCommitteeForm(request.POST, request.FILES)
        if csv_form.is_valid():
            csv_file = request.FILES['file']
            csv_file_name = csv_file.name

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

            for row in csv_data:
                Committees.objects.create(              
                    name=row[0],
                    link=row[1]
                )

            # Save the file name in the CSVFiles model
            csv_files_data = LegislativeCSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            return redirect('data:success_page')
    else:
        csv_form = CSVMemberForm()

    db_csv_files = LegislativeCSVFiles.objects.all()

    return render(request, 'upload.html', {'committee_form': csv_form, 'csv_files': db_csv_files})

def upload_subcommittee_csv(request):
    if request.method == 'POST':
        csv_form = CSVSubCommitteeForm(request.POST, request.FILES)
        if csv_form.is_valid():
            csv_file = request.FILES['file']
            csv_file_name = csv_file.name

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

            for row in csv_data:
                SubCommittees.objects.create(              
                    name=row[0],
                    link=row[1]
                )

            # Save the file name in the CSVFiles model
            csv_files_data = LegislativeCSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            return redirect('data:success_page')
    else:
        csv_form = CSVSubCommitteeForm()

    db_csv_files = LegislativeCSVFiles.objects.all()

    return render(request, 'upload.html', {'subcommittee_form': csv_form, 'csv_files': db_csv_files})



def upload_title_csv(request):
    if request.method == 'POST':
        csv_form = CSVTitleForm(request.POST, request.FILES)
        if csv_form.is_valid():
            csv_file = request.FILES['file']
            csv_file_name = csv_file.name

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

            for row in csv_data:
                Title.objects.create(              
                    title=row[0],
                )

            # Save the file name in the CSVFiles model
            csv_files_data = LegislativeCSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            return redirect('data:success_page')
    else:
        csv_form = CSVTitleForm()

    db_csv_files = LegislativeCSVFiles.objects.all()

    return render(request, 'upload.html', {'title_form': csv_form, 'csv_files': db_csv_files})

def upload_hierarchy_csv(request):
    if request.method == 'POST':
        csv_form = CSVHierarchyForm(request.POST, request.FILES)
        if csv_form.is_valid():
            csv_file = request.FILES['file']
            csv_file_name = csv_file.name

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            # Skip the header row
            next(csv_data)

            for row in csv_data:
                Hierarchy.objects.create(              
                    hierarchy=row[0],
                )

            # Save the file name in the CSVFiles model
            csv_files_data = LegislativeCSVFiles(file_name=csv_file_name)
            csv_files_data.save()

            return redirect('data:success_page')
    else:
        csv_form = CSVHierarchyForm()

    db_csv_files = LegislativeCSVFiles.objects.all()

    return render(request, 'upload.html', {'hierarchy_form': csv_form, 'csv_files': db_csv_files})


def success_page(request):
    return render(request, 'data/success.html')

from django.forms.models import model_to_dict
from django.contrib import messages

def upload_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            # Store the data in the session for later use
            request.session['last_submitted_data'] = model_to_dict(data)

            # Add a success message for the alert
            messages.success(request, 'Form submitted successfully!')

            return redirect('legislative:upload_data')
        
        else:
            # Add an error message for the alert if the form is not valid
            messages.error(request, 'Form submission failed. Please check your input.')

    else:
        # Check if there is last submitted data in the session
        last_submitted_data = request.session.get('last_submitted_data')
        form = DataForm(initial=last_submitted_data) if last_submitted_data else DataForm()

    return render(request, 'upload_data.html', {'form': form})


# def delete_data(request, id):
#     if request.method == "GET":
#         id = request.GET.get("id")
#         print(id)
#         try:
#             data = Data.objects.get(id=id)
#             data.delete()
#             return JsonResponse({"status": "success", 'data':data})
#         except Data.DoesNotExist:
#             return JsonResponse(
#                 {"status": "error", "message": "Data record not found."}, status=404
#             )
        
#     return JsonResponse(
#         {"status": "error", "message": "Invalid request method."}, status=400
#     )

def delete_data(request, id):
  print(id)
  data = Data.objects.get(pk=id)
  data.delete()
  return JsonResponse({"status": "success"})



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def combine_data_json(request):
    try:
        draw = int(request.POST.get('draw', 1))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10000))

        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_direction = request.POST.get('order[0][dir]', '')
        order_column_name = request.POST.get(f'columns[{order_column_index}][data]', 'id')
        ordering = f"{'' if order_direction == 'asc' else '-'}{order_column_name}"

        search_value = request.POST.get('search[value]', '')

        filter_conditions = (
            Q(name__icontains=search_value) |
            Q(committee__icontains=search_value) |
            Q(subcommittee__icontains=search_value) |
            Q(member_title__icontains=search_value) |
            Q(hierarchy__icontains=search_value)
        )

        data_list = CombineData.objects.filter(filter_conditions).order_by(ordering)

        paginator = Paginator(data_list, length)
        page = (start // length) + 1

        try:
            paginated_data = paginator.page(page)
        except EmptyPage:
            paginated_data = []

        data = []

        for item in paginated_data:
            data_entry = {
                'id': item.id,
                'name': item.name,
                'state': item.state,
                'district': item.district,
                'party': item.party,
                'employer': item.employer,
                'email': item.email,
                'phone_number': item.phone_number,
                'address': item.address,
                'desc': item.desc,
                'member_title': item.member_title,
                'committee_title': item.committee_title,
                'committee': item.committee,
                'subcommittee': item.subcommittee,
                'hierarchy': item.hierarchy,
                'image_name': item.image_name,
                'subcommittee_link': item.subcommittee_link,
                'committee_link': item.committee_link,
                'member_link': item.member_link,
            }
            data.append(data_entry)

        response = {
            'draw': draw,
            'recordsTotal': data_list.count(),
            'recordsFiltered': data_list.count(),
            'data': data,
        }

        return JsonResponse(response)

    except Exception as e:
        logging.error(f"Error in data_json view: {e}")
        return JsonResponse({'error': 'An error occurred while processing the request.'}, status=500)
    

def combine_data(request):
    return render(request, 'combine_data.html')