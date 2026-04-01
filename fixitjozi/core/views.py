from django.shortcuts import render, redirect
from .models import Report
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from collections import Counter
from .models import Report
import json


def landing(request):
    # Landing just renders the language picker — form POSTs/GETs to /login/
    return render(request, 'core/landing.html')


def home(request):
    language = request.GET.get('language', 'en')
    return render(request, 'core/home.html', {'language': language})


def report(request):
    language = request.GET.get('language', 'en')
    if request.method == "POST":
        issue_type = request.POST.get('category')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        Report.objects.create(
            issue_type=issue_type,
            description=description,
            latitude=latitude,
            longitude=longitude
        )
        return redirect(f'/track/?language={language}')

    return render(request, 'core/report.html', {'language': language})


def track(request):
    language = request.GET.get('language', 'en')
    reports = Report.objects.all()

    data = [
        {
            "lat": r.latitude,
            "lng": r.longitude,
            "type": r.issue_type,
            "desc": r.description
        }
        for r in reports
    ]

    return render(request, 'core/track.html', {
        'reports_json': json.dumps(data),
        'language': language,
    })


def community(request):
    language = request.GET.get('language', 'en')
    return render(request, 'core/community.html', {'language': language})


def dashboard(request):
    reports = Report.objects.all()
    total_reports = reports.count()

    issue_types = [r.issue_type for r in reports]
    type_counts = Counter(issue_types)

    labels = list(type_counts.keys())
    data = list(type_counts.values())

    return render(request, 'core/dashboard.html', {
        'total_reports': total_reports,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })


def login_view(request):
    # GET: receives ?language= from landing page
    language = request.GET.get('language', request.POST.get('language', 'en'))

    if request.method == "POST":
        language = request.POST.get("language", "en")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        user = authenticate(request, username=phone, password=password)

        if user:
            login(request, user)
        else:
            # Auto-create account if user doesn't exist
            user = User.objects.create_user(username=phone, password=password)
            login(request, user)

        return redirect(f'/home/?language={language}')

    return render(request, 'core/login.html', {'language': language})