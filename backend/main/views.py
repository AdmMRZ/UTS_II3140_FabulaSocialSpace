import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .services import MenuService, OrderService, TenantService
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings

@csrf_exempt
def auth_google(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "method not allowed"}, status=405)
    try:
        body = json.loads(request.body)
        credential = body.get('credential') or body.get('token')
        if not credential:
            return HttpResponseBadRequest('missing credential')

        try:
            idinfo = id_token.verify_oauth2_token(credential, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
        except ValueError as e:
            return HttpResponseBadRequest('invalid token: ' + str(e))

        user_data = {
            'name': idinfo.get('name'),
            'email': idinfo.get('email'),
            'picture': idinfo.get('picture')
        }

        request.session['user'] = user_data

        return JsonResponse({'status': 'success', 'user': user_data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def logout(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "method not allowed"}, status=405)
    
    request.session.flush()
    return JsonResponse({"status": "success", "message": "logged out successfully"})

@csrf_exempt
def menu_list(request):
    if request.method == "GET":
        try:
            data = MenuService.list_menus()
            return JsonResponse({"status": "success", "data": data})
        except Exception as e:
            print(f"DEBUG: Error in menu_list: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "invalid json"}, status=400)

        if isinstance(body, list):
            created_menus = []
            for menu_data in body:
                name = menu_data.get("name")
                description = menu_data.get("description", "")
                price = menu_data.get("price")
                image_url = menu_data.get("image_url", "")
                category = menu_data.get("category")
                
                created = MenuService.create_menu(
                    name=name,
                    description=description,
                    price=price,
                    image_url=image_url,
                    category=category
                )
                created_menus.append(created)
            return JsonResponse({"status": "success", "data": created_menus}, status=201)
        
        name = body.get("name")
        description = body.get("description", "")
        price = body.get("price")
        image_url = body.get("image_url", "")
        category = body.get("category")

        try:
            created = MenuService.create_menu(
                name=name,
                description=description,
                price=price,
                image_url=image_url,
                category=category)
            return JsonResponse({"status": "success", "data": created}, status=201)
        except ValueError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "method not allowed"}, status=405)

@csrf_exempt
def order_create(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "method not allowed"}, status=405)
    try:
        body = json.loads(request.body)
        table_number = body.get("table_number")
        items = body.get("items", [])
        result = OrderService.create_order(table_number, items)
        return JsonResponse({"status": "success", "message": "Order berhasil dibuat", "data": result})
    except ValueError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def tenant_create(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "method not allowed"}, status=405)
    try:
        body = json.loads(request.body)
        tr = TenantService.create_tenant_request(
            body.get("tenant_name"),
            body.get("contact"),
            body.get("type"),
            body.get("description", "")
        )
        return JsonResponse({"status": "success", "message": "Request tenant berhasil dikirim", "data": tr})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
