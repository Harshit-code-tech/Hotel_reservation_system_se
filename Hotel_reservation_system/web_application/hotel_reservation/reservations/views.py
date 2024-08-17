from django.shortcuts import render
from .models import Hotel

def search_hotels(request):
    location = request.GET.get('location')
    hotels = Hotel.objects.filter(location=location)
    return render(request, 'hotels/search_results.html', {'hotels': hotels})
