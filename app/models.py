from django.db import models
maax = 120

class Menu(models.Model):
    name = models.CharField(max_length = maax)

class Node(models.Model):
    name = models.CharField(max_length = maax)
    parentElem = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True)
    url = models.CharField(max_length = maax)
    menu = models.ForeignKey(Menu, on_delete = models.CASCADE)


    