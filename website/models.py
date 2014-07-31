from django.db import models

"""
Models from Scilab Database created using inspectdb
Use it with the "scilab" database eg:using("scilab") 
These models are used only for django orm reference.
"""
class TextbookCompanionPreference(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    proposal_id = models.IntegerField()
    pref_number = models.IntegerField()
    book = models.CharField(max_length=100L)
    author = models.CharField(max_length=100L)
    isbn = models.CharField(max_length=25L)
    publisher = models.CharField(max_length=50L)
    edition = models.CharField(max_length=2L)
    year = models.IntegerField()
    category = models.IntegerField()
    approval_status = models.IntegerField()
    cloud_pref_err_status = models.IntegerField()
    class Meta:
        db_table = 'textbook_companion_preference'

class TextbookCompanionProposal(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    uid = models.IntegerField()
    approver_uid = models.IntegerField()
    full_name = models.CharField(max_length=50L)
    mobile = models.CharField(max_length=15L)
    gender = models.CharField(max_length=10L)
    how_project = models.CharField(max_length=50L)
    course = models.CharField(max_length=50L)
    branch = models.CharField(max_length=50L)
    university = models.CharField(max_length=100L)
    faculty = models.CharField(max_length=100L)
    reviewer = models.CharField(max_length=100L)
    completion_date = models.IntegerField()
    creation_date = models.IntegerField()
    approval_date = models.IntegerField()
    proposal_status = models.IntegerField()
    message = models.TextField()
    scilab_version = models.CharField(max_length=20L)
    operating_system = models.CharField(max_length=20L)
    teacher_email = models.CharField(max_length=20L)
    class Meta:
        db_table = 'textbook_companion_proposal'

class TextbookCompanionChapter(models.Model):
    id = models.IntegerField(primary_key=True)
    preference_id = models.IntegerField()
    number = models.IntegerField()
    name = models.CharField(max_length=255L)
    cloud_chapter_err_status = models.CharField(max_length=255L)
    class Meta:
        db_table = 'textbook_companion_chapter'

class TextbookCompanionExample(models.Model):
    id = models.IntegerField(primary_key=True)
    chapter_id = models.IntegerField()
    approver_uid = models.IntegerField()
    number = models.CharField(max_length=10L)
    caption = models.CharField(max_length=255L)
    approval_date = models.IntegerField()
    approval_status = models.IntegerField()
    timestamp = models.IntegerField()
    cloud_err_status = models.IntegerField()
    class Meta:
        db_table = 'textbook_companion_example'

class TextbookCompanionExampleFiles(models.Model):
    id = models.IntegerField(primary_key=True)
    example_id = models.IntegerField()
    filename = models.CharField(max_length=255L)
    filepath = models.CharField(max_length=500L)
    filemime = models.CharField(max_length=255L)
    filesize = models.IntegerField()
    filetype = models.CharField(max_length=1L)
    caption = models.CharField(max_length=100L)
    timestamp = models.IntegerField()
    class Meta:
        db_table = 'textbook_companion_example_files'

class TextbookCompanionExampleDependency(models.Model):
    id = models.IntegerField(primary_key=True)
    example_id = models.IntegerField()
    dependency_id = models.IntegerField()
    approval_status = models.IntegerField()
    timestamp = models.IntegerField()
    class Meta:
        db_table = 'textbook_companion_example_dependency'

class TextbookCompanionDependencyFiles(models.Model):
    id = models.IntegerField(primary_key=True)
    preference_id = models.IntegerField()
    filename = models.CharField(max_length=255L)
    filepath = models.CharField(max_length=500L)
    filemime = models.CharField(max_length=255L)
    filesize = models.IntegerField()
    caption = models.CharField(max_length=100L)
    description = models.TextField()
    timestamp = models.IntegerField()
    class Meta:
        db_table = 'textbook_companion_dependency_files'
