
# All nessesary imports
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect 

from django.contrib.auth.decorators import login_required


#importing user & messages forms
from .forms import MessageForm
from .forms import UserRegisterForm


from django.contrib import messages

from django.http import JsonResponse

#importing all nessesary models
from .models import Messages
from django.db.models import Q
from django.contrib.auth.models import User

#importing models for using WebRTC
from .models import VideoRoom, IceCandidate

#IDK what is it used for
import uuid

# uploading csrf 
from django.views.decorators.csrf import csrf_exempt

#using json to save data
import json

#getting current timezone
from django.utils import timezone
'''
it seems to be equal to

#from datetime import date
'''

#library previously used for loading templates now it's usually replaced by render()
from django.template import loader
#import string 


# Create your views here.


# Список пользователей

"""
old loader

def about(request):
    template=loader.get_template("users/about.html")
    return HttpResponse(template.render(cintext,request))

"""
#@login_required
def about(request):
    return render(request, "users/about.html")


@login_required            
def user_list(request):
    users=User.objects.all()

    context={"users":users}
    return render(request,"users/user_list.html",context)

@login_required
def get_and_send_user_messages(request, user_id):
    current_user = request.user
    for_user = get_object_or_404(User, pk=user_id)
    
    # Получаем сообщения из базы
    user_messages = Messages.objects.filter(
        (Q(sender=current_user.username, getter=for_user.username) | 
         Q(sender=for_user.username, getter=current_user.username))
    ).order_by('published')
    # sidebar user list (excluding current)
    users = User.objects.exclude(pk=current_user.pk)

    # ВАЖНО: Расшифровываем перед отправкой в шаблон
    for msg in user_messages:
        msg.decrypted_text = msg.get_decrypted()

    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = current_user.username
            message.getter = for_user.username
            # Поле .message зашифруется само внутри метода save() модели
            message.save() 
            return redirect('member', user_id=user_id)
    else:
        form = MessageForm()

    context = {
        "messages": user_messages, 
        "for_user": for_user, 
        "form": form,
        "users": users,
    }
    return render(request, "users/get_user.html", context)


# Удаляет сообщения
@login_required
def delete_message(request, post_id):
    # Удаляем только если пользователь — отправитель
    post_to_delete = get_object_or_404(Messages, id=post_id, sender=request.user.username)
    post_to_delete.delete()
    return redirect(request.META.get('HTTP_REFERER', 'us_lst'))




# Вход в аккаунт и регистрация
#Регистрируем пользлвателя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('us_lst')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

#

@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def view_profile(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    # try to get profile; if not, show placeholders
    profile = None
    try:
        profile = user_obj.profile
    except Exception:
        profile = None
    return render(request, 'users/other_profile.html', {'user_obj': user_obj, 'profile': profile})


# --- Video call views (basic HTTP-polling signaling) ---
@login_required
def video_call_create(request, user_id):
    # Initiator creates a room and gets a shareable link
    callee = get_object_or_404(User, pk=user_id)
    room = VideoRoom.objects.create(initiator=request.user.username, callee=callee.username)
    return render(request, 'users/video_call.html', {'room_id': room.id, 'role': 'initiator', 'peer': callee})


@login_required
def video_call_join(request, room_id):
    # Callee opens link and joins
    try:
        room = VideoRoom.objects.get(id=room_id)
    except VideoRoom.DoesNotExist:
        return HttpResponse('Room not found', status=404)
    return render(request, 'users/video_call.html', {'room_id': room.id, 'role': 'callee', 'peer': None})


@csrf_exempt
def video_offer(request, room_id):
    # GET returns offer, POST saves offer
    try:
        room = VideoRoom.objects.get(id=room_id)
    except VideoRoom.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'offer': room.offer})
    else:
        data = json.loads(request.body.decode('utf-8'))
        room.offer = data.get('sdp')
        room.save()
        return JsonResponse({'ok': True})


@csrf_exempt
def video_answer(request, room_id):
    try:
        room = VideoRoom.objects.get(id=room_id)
    except VideoRoom.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'answer': room.answer})
    else:
        data = json.loads(request.body.decode('utf-8'))
        room.answer = data.get('sdp')
        room.save()
        return JsonResponse({'ok': True})


@csrf_exempt
def video_candidate_post(request, room_id):
    try:
        room = VideoRoom.objects.get(id=room_id)
    except VideoRoom.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    data = json.loads(request.body.decode('utf-8'))
    sender = data.get('sender')
    candidate = data.get('candidate')
    if candidate:
        IceCandidate.objects.create(room=room, sender=sender, candidate=candidate)
    return JsonResponse({'ok': True})


def video_candidates_get(request, room_id):
    try:
        room = VideoRoom.objects.get(id=room_id)
    except VideoRoom.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    since = request.GET.get('since')
    qs = room.candidates.order_by('created')
    if since:
        try:
            since_dt = timezone.datetime.fromisoformat(since)
            qs = qs.filter(created__gt=since_dt)
        except Exception:
            pass

    items = [{'sender': c.sender, 'candidate': c.candidate, 'created': c.created.isoformat()} for c in qs]
    return JsonResponse({'candidates': items})

from .models import AcceptedIP


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt # Чтобы упростить отправку запроса из JS
def accept_cookies_view(request):
    if request.method == 'POST':
        user_ip = get_client_ip(request)
        # get_or_create гарантирует, что дубликатов не будет
        AcceptedIP.objects.get_or_create(ip_address=user_ip)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)