from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404

from ua_parser import user_agent_parser
from ipware import get_client_ip
import logging
from inflection import underscore
import json

from .models import Link, Visit
from .utils import is_bot, get_ray_id


def _save_data_from_request(request, link):
    try:
        user_agent = request.META["HTTP_USER_AGENT"]
        client_ip, _is_routable = get_client_ip(request)
        visit = Visit(
            link=link,
            user_agent=user_agent,
            ip=client_ip,
            is_bot=is_bot(user_agent),
            city=request.ipinfo.city,
            country=request.ipinfo.country,
            hostname=request.ipinfo.hostname,
            latitude=float(request.ipinfo.latitude),
            longitude=float(request.ipinfo.longitude),
        )
        visit.save()
        return visit
    except Exception as e:
        # something went wrong but we don't want to alert the visitor...
        logging.error(
            "Failed to save visit to {}. IP: {}, UA: {}".format(
                link, client_ip, user_agent
            )
        )
        logging.error(e)


def _save_visit_minimal(request, link):
    # Directly redirects visitor to the destination
    _save_data_from_request(request, link)
    return redirect(link.destination)


def _save_visit_extended(request, link):
    # Shows visitor an interstitial and uses Javascript to collect extra data
    visit = _save_data_from_request(request, link)
    request.session["visit_pk"] = visit.pk

    pretty_destination = link.destination.replace("https://", "").replace("http://", "")
    return render(
        request,
        "links/interstitial_blank.html",
        {
            "link": link,
            "pretty_destination": pretty_destination,
            "ray_id": get_ray_id(),
            "visit": visit,
        },
    )


def redirect_to_destination(request, short_id):
    link = get_object_or_404(Link, short_id=short_id)
    if link.collect_extended_data:
        return _save_visit_extended(request, link)
    else:
        return _save_visit_minimal(request, link)


def update_visit(request):
    # if request.method != "POST":
    #     raise Http404("Invalid method")

    data = json.loads(request.body)
    visit = get_object_or_404(Visit, pk=request.session["visit_pk"])
    fields = [
        "webdriver",
        "colorDepth",
        "pixelRatio",
        "hardwareConcurrency",
        "timezone",
        "sessionStorage",
        "localStorage",
        "indexedDb",
        "addBehavior",
        "openDatabase",
        "platform",
        "webglVendorAndRenderer",
        "touchSupport",
    ]
    for key in fields:
        model_field = underscore(key)
        setattr(visit, model_field, data[key])
    # Handle screen resolutions separately
    visit.screen_x = data.get("screenResolution", [0, 0])[0]
    visit.screen_y = data.get("screenResolution", [0, 0])[1]
    visit.available_screen_x = data.get("availableScreenResolution", [0, 0])[0]
    visit.available_screen_y = data.get("availableScreenResolution", [0, 0])[1]

    visit.save(update_fields=([underscore(f) for f in fields] + ['screen_x', 'screen_y', 'available_screen_x', 'available_screen_y']))
    return HttpResponse(status=204)  # HTTP No Content
