from django.shortcuts import render, redirect
from .models import Report
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from collections import Counter
from .models import Report
import json
import random
import string


def landing(request):
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
        priority = request.POST.get('priority', 'low')

        # Generate a reference number for this report (e.g. JHB00042)
        # In production, use a sequential counter or UUID-based scheme.
        ref_number = "JHB" + ''.join(random.choices(string.digits, k=5))

        Report.objects.create(
            issue_type=issue_type,
            description=description,
            latitude=latitude,
            longitude=longitude,
            reference_number=ref_number,
        )

        # Pass reference number to track page so user sees their own report
        return redirect(f'/track/?language={language}&ref={ref_number}')

    return render(request, 'core/report.html', {'language': language})


def track(request):
    """
    Track page now supports:
    1. ?ref=JHBxxxxx  — pre-fills the lookup from a redirect after report submission
    2. POST or GET lookup from the reference input field on the page
    3. Returns report data as JSON for the front-end lookup widget
    """
    language = request.GET.get('language', 'en')

    # Pre-fill reference number if redirected from report submission
    prefill_ref = request.GET.get('ref', '')

    return render(request, 'core/track.html', {
        'language': language,
        'prefill_ref': prefill_ref,
    })


def track_lookup_api(request):
    """
    JSON API endpoint: /track/lookup/?ref=JHBxxxxx
    The track page's JS calls this to look up a report by reference number.
    Returns JSON so the page can update without a full reload.
    """
    ref = request.GET.get('ref', '').strip().upper()

    if not ref:
        return JsonResponse({'found': False, 'error': 'No reference number provided'})

    try:
        report = Report.objects.get(reference_number=ref)
        return JsonResponse({
            'found': True,
            'ref': report.reference_number,
            'category': report.issue_type,
            'description': report.description,
            'location': f"{report.latitude}, {report.longitude}",
            'date': report.created_at.strftime('%d %B %Y'),
            'status': report.status,
        })
    except Report.DoesNotExist:
        return JsonResponse({'found': False})


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
    language = request.GET.get('language', request.POST.get('language', 'en'))

    if request.method == "POST":
        language = request.POST.get("language", "en")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        user = authenticate(request, username=phone, password=password)

        if user:
            login(request, user)
        else:
            user = User.objects.create_user(username=phone, password=password)
            login(request, user)

        return redirect(f'/home/?language={language}')

    return render(request, 'core/login.html', {'language': language})