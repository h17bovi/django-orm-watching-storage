from django.shortcuts import render

from datacenter.models import Visit


def storage_information_view(request):
    visitors = Visit.objects.filter(leaved_at=None)

    non_closed_visits = [
        {
            "who_entered": visitor.passcard.owner_name,
            "entered_at": visitor.entered_at,
            "duration": Visit.format_duration(visitor.get_duration),
            "is_strange": visitor.is_strange,
        }
        for visitor in visitors
    ]

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, "storage_information.html", context)
