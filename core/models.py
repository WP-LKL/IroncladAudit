from django.db import models

def hundredYears():
    now = timezone.now()

    return DateTimeTZRange(now, now + timedelta(days=36000))

class Contract(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, blank=True)

    active = DateTimeRangeField(blank=True, default=hundredYears)
    slug = AutoSlugField(_('slug'), max_length=512, populate_from=('name',))

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Contract, self).save(*args, **kwargs)

    class Meta:
        db_table = 'contract'


class Provider(models.Model):
    name = models.CharField(max_length=255)
    identity = models.CharField(max_length=255, blank=True)
    
    website = models.CharField(max_length=255, blank=True)
    github = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    discord = models.CharField(max_length=255, blank=True)
    telegram = models.CharField(max_length=255, blank=True)

    active = DateTimeRangeField(blank=True, default=hundredYears)
    slug = AutoSlugField(_('slug'), max_length=512, populate_from=('name',))

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Provider, self).save(*args, **kwargs)

    class Meta:
        db_table = 'provider'


class Token(models.Model):
    name = models.CharField(max_length=255)
    supply = models.DecimalField(max_digits=64, decimal_places=32)
    price = models.DecimalField(max_digits=64, decimal_places=32)
    
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    slug = AutoSlugField(_('slug'), max_length=512, populate_from=('name',))

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Token, self).save(*args, **kwargs)

    class Meta:
        db_table = 'token'


class Balance(models.Model):
    balance = models.DecimalField(max_digits=64, decimal_places=32)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)

    class Meta:
        db_table = 'balance'


class Chain(models.Model):
    name = models.CharField(max_length=255)
    chainname = models.IntegerField()
    chainid = models.IntegerField()
    description = models.TextField(max_length=2000, blank=True)

    class Meta:
        db_table = 'chain'


class Address(models.Model):
    address = models.CharField(max_length=255)
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)

    class Meta:
        db_table = 'address'


class AddressBalance(models.Model): #Through table
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)

    class Meta:
        db_table = 'addressbalance'
        constraints = [
            models.UniqueConstraint(
                fields=('address', 'balance'),
                name='uniqueaddressbalance'
            )
        ]