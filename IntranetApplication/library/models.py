from __future__ import unicode_literals
from django.db import models
from randr.models import Associate

class PhysicalObject(models.Model):
    title 				= models.CharField(max_length=200)
    desc                = models.TextField(blank = True, null = True)
    storate_location 	= models.CharField(max_length=200, blank = True, null = True)

    def __unicode__(self):
    	return self.title

class Book(PhysicalObject):
    author              = models.CharField(max_length=200, blank = True, null = True)
    cover_image         = models.ImageField(blank = True, null = True, upload_to='uploads/%Y/%m/%d/')

class InternetDongle(PhysicalObject):
    device_id           = models.CharField(max_length=200, blank = True, null = True)
    imei                = models.CharField(max_length=200, blank = True, null = True)

 
class TransactionRecord(models.Model):
    obj             = models.ManyToManyField(PhysicalObject)
    trans_type      = models.BooleanField() # 1, means objected added to library, 0 means object removed from library
    trans_date      = models.DateTimeField(auto_now_add = True)
    transuser       = models.ForeignKey(Associate, blank = True, null = True, related_name='transuser')
    librarian       = models.ForeignKey(Associate, related_name='librarian')

    def __unicode__(self):
        return str(self.trans_date)
