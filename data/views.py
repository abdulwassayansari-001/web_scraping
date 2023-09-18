from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Products, Leadership
from django.core import serializers
from django.forms.models import model_to_dict

def products(request):

    products = Products.objects.all()
    product_data = serializers.serialize('json', products)
    return JsonResponse({'products': product_data}, safe=False)
    # return render(request, 'data/products.html', {'products':products})

def products_page(request):
    return render(request, 'data/products.html')


def data(request):
    return render(request, 'data/data.html')


def get_leadership_data(request):
    leadership_data = Leadership.objects.all()
    data = [model_to_dict(leader) for leader in leadership_data]
    data = [{
        'id':leader.id,
        'name': leader.name,
        'dep': leader.dep,
        'title': leader.title,
        'email': leader.email,
        'phone_number': leader.phone_number,
        'validate': True
    } for leader in leadership_data]
    return JsonResponse({'leadership_data': data})

def get_data(request):
    leadership_data = Leadership.objects.all()
    data = [model_to_dict(leader) for leader in leadership_data]
    data = [{
        'id':leader.id,
        'name': leader.name,
        'dep': leader.dep,
        'title': leader.title,
        'email': leader.email,
        'phone_number': leader.phone_number,
        'validate': leader.validate
    } for leader in leadership_data]
    return JsonResponse({'leadership_data': data})

# def validated(request):
#     if request.method == "GET":
#         id = request.GET.get("id")
#         try:
#             data = Leadership.objects.get(pk=id)
#             data.validate = False
#             print(f"Data with ID {id} marked as validated.")
#             data.save()
#             # Convert the Leadership model instance to a dictionary
#             data_dict = model_to_dict(data)
#             return JsonResponse({"status": "success", 'data':data_dict})
#         except Leadership.DoesNotExist:
#             return JsonResponse(
#                 {"status": "error", "message": "Leadership record not found."}, status=404
#             )

#     return JsonResponse(
#         {"status": "error", "message": "Invalid request method."}, status=400
#     )


def accepted_data(request):
    if request.method == "GET":
        id = request.GET.get("id")
        try:
            data = Leadership.objects.get(pk=id)
            data.validate = True
            print(f"Data with ID {id} marked as validated.")
            data.save()
            # Convert the Leadership model instance to a dictionary
            data_dict = model_to_dict(data)
            return JsonResponse({"status": "success", 'data':data_dict})
        except Leadership.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Leadership record not found."}, status=404
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
            data = Leadership.objects.get(pk=id)
            data.validate = False
            print(f"Data with ID {id} marked as validated.")
            data.save()
            # Convert the Leadership model instance to a dictionary
            data_dict = model_to_dict(data)
            return JsonResponse({"status": "success", 'data':data_dict})
        except Leadership.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Leadership record not found."}, status=404
            )

    return JsonResponse(
        {"status": "error", "message": "Invalid request method."}, status=400
    )

def rejected(request):
    return render(request, 'data/rejected.html')