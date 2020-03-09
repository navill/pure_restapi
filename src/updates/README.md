## Model

- Update

  - serialize(\<type>, \<instance>, \<fields>): 매개 변수를 이용한 데이터 직렬화

  - UpdateQuerySet: 모델 객체 직렬화하기 위한 serialize() 메소드

    - django.core.serailizers.serialize: django에서 제공하는 객체 직렬화 메소드

    ```python
    class UpdateQuerySet(models.QuerySet):
        def serialize(self):
            # QuerySet.values(<fields>)
            list_values = list(self.values('id', 'user', 'text', 'image'))
            return json.dumps(list_values)
    
    
    class UpdateManager(models.Manager):
        def get_queryset(self):
            return UpdateQuerySet(self.model, using=self._db)
    
    
    class Update(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        text = models.TextField(blank=True, null=True)
        image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
        updated = models.DateTimeField(auto_now=True)
        timestamp = models.DateTimeField(auto_now=True)
    
        objects = UpdateManager()
    
        def __str__(self):
            return self.text
    
    		# 객체에 대한 json.dumps
        def serialize(self):
            try:
                image = self.image.url
            except:
                image = ''
            data = {
                'id': self.id,
                'text': self.text,
                'user': self.user.id,
                'image': image,
            }
    
            data = json.dumps(data)
            return data
    ```