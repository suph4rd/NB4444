# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models





class B4Amortizatia(models.Model):
    date_amortizatia = models.DateTimeField()
    ostatoc_amortizatia = models.FloatField()
    sum_amortizatia = models.FloatField()
    describe_amortizatia = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'b4_amortizatia'


class B4Eda(models.Model):
    date_eda = models.DateTimeField()
    ostatoc_eda = models.FloatField()
    sum_eda = models.FloatField()
    describe_eda = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'b4_eda'


class B4Minfin(models.Model):
    date_minfin = models.DateTimeField()
    ostatoc_minfin = models.FloatField()
    sum_minfin = models.FloatField()
    describe_minfin = models.CharField(max_length=255)
    type_table = models.CharField(max_length=255, blank=True, null=True)
    id_insert = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'b4_minfin'


class B4Nds(models.Model):
    date_nds = models.DateTimeField()
    ostatoc_nds = models.FloatField()
    sum_nds = models.FloatField()
    describe_nds = models.CharField(max_length=255)
    type_table = models.CharField(max_length=255, blank=True, null=True)
    id_insert = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'b4_nds'


class B4Nlg(models.Model):
    date_nlg = models.DateTimeField()
    text_nlg = models.TextField()
    image_nlg = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'b4_nlg'


class B4Prochee(models.Model):
    date_prochee = models.DateTimeField()
    ostatoc_prochee = models.FloatField()
    sum_prochee = models.FloatField()
    describe_prochee = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'b4_prochee'


class B4Razvlechenia(models.Model):
    date_razvlechenia = models.DateTimeField()
    ostatoc_razvlechenia = models.FloatField()
    sum_razvlechenia = models.FloatField()
    describe_razvlechenia = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'b4_razvlechenia'


class B4StandartVichet(models.Model):
    hata = models.FloatField()
    proezd = models.FloatField()
    mobila = models.FloatField()
    eda = models.FloatField()
    itogo = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'b4_standart_vichet'


class B4Transport(models.Model):
    date_transport = models.DateTimeField()
    ostatoc_transport = models.FloatField()
    sum_transport = models.FloatField()
    describe_transport = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'b4_transport'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
