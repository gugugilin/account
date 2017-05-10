from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Detail(models.Model):
    author = models.ForeignKey(User)
    item = models.TextField()
    cost = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['date']
        permissions = (
            ("Can_account", "Can into account.html"),  # 只有一個權限時，千萬不要忘了逗號！
        )
        def __unicode__(self):
            return self.author

    def __str__(self):
        return self.item

    


class Account(models.Model):
    author = models.ForeignKey(User)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.balance

