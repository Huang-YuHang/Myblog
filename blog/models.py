import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

# Create your models here.
class Category(models.Model): #继承models.Model类  ---> 分类
    name = models.CharField(max_length=100)   #CharField是字符型
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Tag(models.Model):  #--->标签
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField('标题',max_length=70) #标题
    body = models.TextField('正文') #正文
    create_time = models.DateTimeField('创建时间',default=timezone.now()) #创建时间
    modfied_time = models.DateTimeField('最后一次修改时间') #最后一次修改时间
    excerpt = models.CharField('文章摘要',max_length=200,blank=True) #文章摘要,CharField默认必须存入数据否则报错,但是blank=True可以允许空值
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE) #当某个分类标签被删除,models.CASCADE会将该分类下的文章全部删除
    tags = models.ManyToManyField(Tag,verbose_name='标题',blank=True)#ManyToManyField，表明这是多对多的关联关系。
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural= verbose_name
        ordering = ['-create_time']

    def save(self,*args,**kwargs):
        self.modfied_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body)[:54])
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
