from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Word(models.Model):
    document = models.ManyToManyField(Document, through='Tf')
    word = models.CharField(max_length=255)

    def __str__(self):
        return self.word


class Tf(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    count = models.FloatField(default=0)

    def __str__(self):
        return str(self.word)+' в файле '+str(self.document)
