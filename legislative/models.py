from django.db import models

class Members(models.Model):
    name = models.CharField(max_length=512, null=False)
    state = models.CharField(max_length=128, null=True, blank=True)
    district = models.CharField(max_length=128, null=True, blank=True)
    party = models.CharField(max_length=128, null=True, blank=True)
    employer = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=512, blank=True, null=True)
    phone_number = models.CharField(max_length=512, blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    image_name = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class Committees(models.Model):
    name = models.CharField(max_length=512, null=False)
    link = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name
    

class SubCommittees(models.Model):
    name = models.CharField(max_length=512, null=False)
    link = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    title = models.CharField(max_length = 512, null = False)

    def __str__(self):
        return self.title


class Hierarchy(models.Model):
    hierarchy = models.CharField(max_length=512, null=False)

    def __str__(self):
        return self.hierarchy


class Data(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE, null=True, blank=True)
    committee = models.ForeignKey(Committees, on_delete=models.CASCADE, null=True, blank=True)
    subcommittee = models.ForeignKey(SubCommittees, on_delete=models.CASCADE, null=True, blank=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True, blank=True)
    hierarchy = models.ForeignKey(Hierarchy, on_delete=models.CASCADE, null=True, blank=True)


# class Data(models.Model):
#     member = models.ForeignKey(Members, on_delete=models.CASCADE, null=True, blank=True)
#     committee = models.ManyToManyField(Committees, blank=True)
#     subcommittee = models.ManyToManyField(SubCommittees, blank=True)
#     title = models.ManyToManyField(Title, blank=True)
#     hierarchy = models.ManyToManyField(Hierarchy, blank=True)


class LegislativeCSVFiles(models.Model):
    file_name = models.CharField(max_length=255, null=True)

    