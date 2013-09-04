from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50,blank=False)
    username = models.CharField(max_length=50,unique=True,blank=False)
    password = models.CharField(max_length=30,blank=False)
    tag_set = models.TextField(null=True,blank=True)
    tag_set_improved = models.TextField(null=True,blank=True)

    class Meta:
        db_table = "User"


class Booth(models.Model):
    title = models.CharField(max_length=50,blank=False)
    description = models.TextField(null=True,blank=True)
    logo = models.CharField(max_length=50,null=True,blank=True)
    tag_set = models.TextField(null=True,blank=True)

    class Meta:
        db_table = "Booth"


class UserToBooth(models.Model):
    user = models.ForeignKey(User)
    booth = models.ForeignKey(Booth)

    class Meta:
        db_table = "UserToBooth"


class UserSimilarities(models.Model):
    userFrom = models.ForeignKey(User, related_name='userSimilarities_userFrom')
    userTo = models.ForeignKey(User, related_name='userSimilarities_userTo')
    similarity = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = "UserSimilarities"


class BoothSimilarities(models.Model):
    userFrom = models.ForeignKey(User)
    boothTo = models.ForeignKey(Booth)
    similarity = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = "BoothSimilarities"