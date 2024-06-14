from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone
from django.template import loader
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import time
import json
import csv


# Create your views here.
from .models import AvailableSlot, Subject, CustomUser, Schedule

from .forms import SlotForm, SubjectUploadForm

@login_required
def HomeView(request):
    user = request.user
    schedules = Schedule.objects.filter(teacher=user) | Schedule.objects.filter(learner=user)
    return render(request, 'myapp/home.html', {'schedules': schedules})

# def ProfileView(request):
#     user = request.user
#     return render(request, "myapp/profile.html", {'user': user})

def ProfileView(request):
    user = request.user
    if request.method == 'POST':
        form = SubjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)
                for row in reader:
                    subject_number = row[2]
                    try:
                        subject = Subject.objects.get(subject_number=subject_number)
                        user.subjects_teach.add(subject)
                        messages.success(request, f'Successfully added subject: {subject.name}')
                    except Subject.DoesNotExist:
                        messages.warning(request, f'Subject with number {subject_number} does not exist')
            except Exception as e:
                messages.error(request, f'Error processing file: {e}')
            return redirect('profile')
    else:
        form = SubjectUploadForm()

    return render(request, "myapp/profile.html", {'user': user, 'form': form})

def SlotsView(request):
    get_token(request)

    template = loader.get_template("myapp/slots.html")
    return HttpResponse(template.render())

def AddSlotView(request):
    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # UNIXタイムスタンプを文字列形式の日時に変換
    formatted_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas["start_time"] / 1000))
    formatted_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas["end_time"] / 1000))

    # 登録処理
    available_slot = AvailableSlot(
        teacher=request.user,  # ログイン中のユーザーを取得
        start_time=formatted_start_time,
        end_time=formatted_end_time,
    )
    available_slot.save()

    # 新しく追加したスロットのIDを返却
    return JsonResponse({"id": available_slot.id})

def DeleteSlotView(request):
    if request.method == "POST":
        datas = json.loads(request.body)
        slot_id = datas.get("id")

        print("Received Slot ID:", slot_id)
        # スロットを取得し、削除する
        try:
            slot = AvailableSlot.objects.get(id=slot_id, teacher=request.user)
            slot.delete()
            return HttpResponse("")
        except AvailableSlot.DoesNotExist:
            return HttpResponse("スロットが見つかりません", status=404)

def GetSlotView(request):
    if request.method == "GET":
        # GETは対応しない
        raise Http404()
    
    # JSONの解析
    datas = json.loads(request.body)

    # UNIXタイムスタンプを文字列形式の日時に変換
    formatted_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas["start_time"] / 1000))
    formatted_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas["end_time"] / 1000))

    # FullCalendarの表示範囲のみ表示
    slots = AvailableSlot.objects.filter(
        teacher=request.user,
        start_time__lt=formatted_end_time, end_time__gt=formatted_start_time
    )

    # fullcalendarのため配列で返却
    slot_list = []
    for slot in slots:
        slot_list.append(
            {
                "id": slot.id,
                "title": "slot",
                "start": slot.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end": slot.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return JsonResponse(slot_list, safe=False)
    
def GetSlotView2(request):
    if request.method == "GET":
        # GETは対応しない
        raise Http404()
    
    # JSONの解析
    datas = json.loads(request.body)

    # UNIXタイムスタンプを文字列形式の日時に変換
    formatted_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas["start_time"] / 1000))
    formatted_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas["end_time"] / 1000))

    # 検索条件を取得
    subject_query = datas.get("subject", "")
    print(f"domo~{subject_query}")
    


    # FullCalendarの表示範囲のみ表示
    slots = AvailableSlot.objects.filter(
        start_time__lt=formatted_end_time,
        end_time__gt=formatted_start_time
    ).exclude(teacher=request.user)

    print(f"Filtered slots by time range (before subject filter): {slots}")

    filtered_slots = []
    for slot in slots:
        print(f"Checking slot: {slot.id}, teacher: {slot.teacher.username}")
        subjects = slot.teacher.subjects_teach.all()
        for subject in subjects:
            # print(f"Teacher: {slot.teacher.username}, Subject: {subject.name}, Subject Number: {subject.subject_number}")
            if subject_query.lower() == subject.name.lower() or subject_query.lower() == subject.subject_number.lower():
                filtered_slots.append(slot)
                break

    print(f"Filtered slots by subject: {filtered_slots}")



    # fullcalendarのため配列で返却
    slot_list = []
    for slot in filtered_slots:
        slot_list.append(
            {
                "id": slot.id,
                "title": "slot",
                "start": slot.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end": slot.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return JsonResponse(slot_list, safe=False)

def ReserveView(request):
    template = loader.get_template("myapp/reserve.html")
    return HttpResponse(template.render())

from django.db.models import Q
def SearchSubjects(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query", "")
        subjects = Subject.objects.filter(
            Q(name__icontains=query) | Q(subject_number__icontains=query)
        )
        subject_list = [{"id": subj.id, "name": subj.name, "subject_number": subj.subject_number} for subj in subjects]
        return JsonResponse(subject_list, safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
# def ReserveSlotView(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         slot_id = data.get("slot_id")
#         subject_id = data.get("subject_id")
        
#         slot = get_object_or_404(AvailableSlot, id=slot_id)
#         subject = get_object_or_404(Subject, id=subject_id)
        
#         # ログイン中のユーザーを取得
#         learner = request.user
        
#         # 予約を作成
#         Schedule.objects.create(
#             teacher=slot.teacher,
#             learner=learner,
#             subject=subject,
#             start_time=slot.start_time,
#             end_time=slot.end_time
#         )

#         # 対応するAvailableSlotを削除
#         slot.delete()
        
#         return JsonResponse({"status": "success"})
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=400)

def ReserveSlotView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        slot_id = data.get("slot_id")
        subject_id = data.get("subject_id")
        
        slot = get_object_or_404(AvailableSlot, id=slot_id)
        subject = get_object_or_404(Subject, id=subject_id)
        
        # ログイン中のユーザーを取得
        learner = request.user
        
        # ポイントの確認
        if learner.user_point <= 0:
            return JsonResponse({"error": "Not enough points"}, status=400)
        
        # 予約を作成
        Schedule.objects.create(
            teacher=slot.teacher,
            learner=learner,
            subject=subject,
            start_time=slot.start_time,
            end_time=slot.end_time
        )

        # ポイントの加減
        slot.teacher.user_point += 1
        learner.user_point -= 1
        slot.teacher.save()
        learner.save()

        # 対応するAvailableSlotを削除
        slot.delete()
        
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

def GetSchedulesView(request):
    if request.method == "POST":  # POSTに変更
        user = request.user

        # JSONの解析
        datas = json.loads(request.body)

        # UNIXタイムスタンプを文字列形式の日時に変換
        formatted_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas["start_time"] / 1000))
        formatted_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas["end_time"] / 1000))

        # ログイン中のユーザーが関与するスケジュールのみをフィルタリング
        schedules = Schedule.objects.filter(
            (Q(teacher=user) | Q(learner=user)),
            start_time__lt=formatted_end_time,
            end_time__gt=formatted_start_time
        )

        schedule_list = []
        for schedule in schedules:
            start_time_str = schedule.start_time.strftime("%Y-%m-%d %H:%M:%S")
            end_time_str = schedule.end_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Start time: {start_time_str}, End time: {end_time_str}")  # デバッグ用
            schedule_list.append(
                {
                    "id": schedule.id,
                    "title": f"{schedule.teacher.username} teaches {schedule.learner.username}",
                    "start": start_time_str,
                    "end": end_time_str,
                }
            )

        return JsonResponse(schedule_list, safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)