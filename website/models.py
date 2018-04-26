from django.db import models


"""
Models from Scilab Database created using inspectdb
Use it with the "scilab" database eg:using("scilab")
These models are used only for django orm reference.
"""


# class TextbookCompanionPreference(models.Model):
#     id = models.IntegerField(unique=True, primary_key=True)
#     proposal_id = models.IntegerField()
#     pref_number = models.IntegerField()
#     book = models.CharField(max_length=100)
#     author = models.CharField(max_length=100)
#     isbn = models.CharField(max_length=25)
#     publisher = models.CharField(max_length=50)
#     edition = models.CharField(max_length=2)
#     year = models.IntegerField()
#     category = models.IntegerField()
#     approval_status = models.IntegerField()
#     cloud_pref_err_status = models.IntegerField()

#     class Meta:
#         db_table = 'textbook_companion_preference'


class TextbookCompanionCategoryList(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    category_name = models.CharField(max_length=100)
    category_id = models.IntegerField()
    maincategory = models.CharField(max_length=255)

    class Meta:
        db_table = 'list_of_category'


class ScilabCloudComment(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    type = models.IntegerField()
    comment = models.TextField()
    email = models.CharField(max_length=100)
    category = models.IntegerField()
    books = models.IntegerField()
    chapter = models.IntegerField()
    example = models.IntegerField()
    reply = models.TextField()
    reply_status = models.IntegerField(default='0')
    user = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'scilab_cloud_comment'


class TextbookCompanionSubCategoryList(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    subcategory_id = models.IntegerField()
    subcategory = models.CharField(max_length=255)
    maincategory_id = models.IntegerField()

    class Meta:
        db_table = 'list_of_subcategory'


class TextbookCompanionProposal(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    uid = models.IntegerField()
    approver_uid = models.IntegerField()
    full_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    how_project = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    university = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    reviewer = models.CharField(max_length=100)
    completion_date = models.IntegerField()
    creation_date = models.IntegerField()
    approval_date = models.IntegerField()
    proposal_status = models.IntegerField()
    message = models.TextField()
    scilab_version = models.CharField(max_length=20)
    operating_system = models.CharField(max_length=20)
    teacher_email = models.CharField(max_length=20)

    class Meta:
        db_table = 'textbook_companion_proposal'


class TextbookCompanionPreference(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    proposal = models.ForeignKey(
        TextbookCompanionProposal, on_delete=models.CASCADE)
    pref_number = models.IntegerField()
    book = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=25)
    publisher = models.CharField(max_length=50)
    edition = models.CharField(max_length=2)
    year = models.IntegerField()
    category = models.IntegerField()
    approval_status = models.IntegerField()
    cloud_pref_err_status = models.IntegerField()

    class Meta:
        db_table = 'textbook_companion_preference'


class TextbookCompanionChapter(models.Model):
    id = models.IntegerField(primary_key=True)
    preference = models.ForeignKey(
        TextbookCompanionPreference, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    cloud_chapter_err_status = models.CharField(max_length=255)

    class Meta:
        db_table = 'textbook_companion_chapter'


class TextbookCompanionExample(models.Model):
    id = models.IntegerField(primary_key=True)
    chapter = models.ForeignKey(
        TextbookCompanionChapter, on_delete=models.CASCADE)
    approver_uid = models.IntegerField()
    number = models.CharField(max_length=10)
    caption = models.CharField(max_length=255)
    approval_date = models.IntegerField()
    approval_status = models.IntegerField()
    timestamp = models.IntegerField()
    cloud_err_status = models.IntegerField()

    class Meta:
        db_table = 'textbook_companion_example'


class TextbookCompanionExampleFiles(models.Model):
    id = models.IntegerField(primary_key=True)
    example = models.ForeignKey(
        TextbookCompanionExample, on_delete=models.CASCADE)
    # =======
    # example_id = models.IntegerField()
    # >>>>>>> upstream/devel
    filename = models.CharField(max_length=255)
    filepath = models.CharField(max_length=500)
    filemime = models.CharField(max_length=255)
    filesize = models.IntegerField()
    filetype = models.CharField(max_length=1)
    caption = models.CharField(max_length=100)
    timestamp = models.IntegerField()

    class Meta:
        db_table = 'textbook_companion_example_files'


class TextbookCompanionRevision(models.Model):
    example_file = models.ForeignKey(
        TextbookCompanionExampleFiles, on_delete=models.CASCADE)
    # sha checksum of commit in github
    commit_sha = models.CharField(max_length=100)
    committer_name = models.CharField(max_length=100)
    committer_email = models.EmailField()
    commit_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    push_status = models.BooleanField(default=0)

    class Meta:
        db_table = 'textbook_companion_revision'


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
    filename = models.CharField(max_length=255)
    filepath = models.CharField(max_length=500)
    filemime = models.CharField(max_length=255)
    filesize = models.IntegerField()
    caption = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.IntegerField()

    class Meta:
        db_table = 'textbook_companion_dependency_files'


class TextbookCompanionExampleViews(models.Model):
    id = models.IntegerField(primary_key=True)
    chapter_id = models.IntegerField(default=0)
    example_id = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'textbook_companion_example_views'


class TextbookCompanionPreferenceHits(models.Model):
    id = models.IntegerField(primary_key=True)
    pref_id = models.IntegerField(default=0)
    hitcount = models.IntegerField(default=0)
    last_search = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'textbook_companion_preference_hits'
