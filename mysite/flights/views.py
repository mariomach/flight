from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Flights, Airport, Passenger

# Create your views here.
def Index(request):
    context = {
        "flights": Flights.objects.all()
    }
    return render(request, "flights/index.html", context) 
    #it is already assume the file is 1 directory lower

def flight(request, flight_id):
    try:
        flight = Flights.objects.get(pk=flight_id)
    except Flights.DoesNotExist:
        raise Http404("Flight does not exist")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(), #passengers is the nickname
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flights.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "flights/error.html", {"message":"no selection"})
    except Passenger.DoesNotExit:
        return render(request, "flights/error.html", {"Message": "no passenger"})
    except Flights.DoesNotExist:
        return render(request, "flights/error.html", {"Message": "no Flight"})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))