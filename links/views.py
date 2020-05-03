from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from ua_parser import user_agent_parser
from ipware import get_client_ip
import logging

from .models import Link, Visit
from .utils import is_bot


def redirect_to_destination(request, short_id):
    link = get_object_or_404(Link, short_id=short_id)

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
    except Exception as e:
        # something went wrong but we don't want to alert the visitor...
        logging.error(
            "Failed to save visit to {}. IP: {}, UA: {}".format(
                link, client_ip, user_agent
            )
        )
        logging.error(e)

    return redirect(link.destination)
