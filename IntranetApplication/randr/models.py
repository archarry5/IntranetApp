from __future__ import unicode_literals
from django.db import models

class MODOBJ_STATUS(object):
	Active = 'A'
	Hidden = 'H'
	Deleted = 'D'

	OBJECT_STATUS_CHOICES = (
		(Active, 'Normal'),
		(Hidden, 'Hidden'),
		(Deleted, 'Deleted'),
	)

class Associate(models.Model):
    employee_id = models.IntegerField(primary_key=True, default=000)
    username = models.CharField(max_length=50, default = '')
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    is_manager = models.BooleanField()
    manager = models.ForeignKey('self', 
        null = True, 
        blank=True, 
        related_name = 'reportingmgr',
        limit_choices_to={'is_manager': True})

    def __unicode__(self):
    	return self.name

class Recognition(models.Model):
    associate = models.ForeignKey(Associate, related_name = 'associate')
    recognition_by = models.ForeignKey(Associate, max_length = 10, blank=True, related_name = 'recog_associate')
    status = models.CharField(max_length = 1, 
    			choices=MODOBJ_STATUS.OBJECT_STATUS_CHOICES, 
    			default = 'N')
    annotation_title = models.CharField(max_length=200)
    annotation_desc = models.TextField(max_length=200)
    #recognition_by = models.ForeignKey(Associate, related_name = 'recognizedby', null = True, blank = True)

    def __unicode__(self):
    	return "{} > {}".format(self.associate.name, self.annotation_title)
