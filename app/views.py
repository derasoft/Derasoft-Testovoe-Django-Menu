from django.shortcuts import render

def baserend(request):
	return render(request, "base.html") 
