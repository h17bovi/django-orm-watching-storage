from django.shortcuts import get_object_or_404, render

from datacenter.models import Passcard, Visit


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = [
        {
            "entered_at": visit.entered_at,
            "duration": visit.get_duration,
            "is_strange": visit.is_strange,
        }
        for visit in visits
    ]
    context = {"passcard": passcard, "this_passcard_visits": this_passcard_visits}
    return render(request, "passcard_info.html", context)
