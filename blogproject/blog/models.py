from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Category(models.Model):

    """
    Django    要求模型必须继承 models.Model 类
    Category  只需一个简单分类名 name 即可
    CharField  指定分类名 name 的数据类型，CharField是字符型
    max_length 参数指定最大长度

    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文

    # Textfield 字符型存储大段文本
    body = models.TextField()

    # 文章创建时间和最后一次更改时间
    # DateTimeField 存储时间数据类型
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要

    # CharField 为空报错（blank = True允许空值
    excerpt = models.CharField(max_length=200, blank=True)

    # 分类与标签

    # 一篇文章对应一个分类，一个分类对应多篇文章
    # 使用ForeignKey 一对多关系
    # 一篇文章对应多个标签，一个标签对应多篇文章
    # ManyToManyField 多对多关系
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 作者

    # User 是从 django.contrib.auth.model 导入的
    # django.contrib.auth：Django内置应用，处理网站用户注册、登陆等流程
    # User 是 Django 写好的用户模型
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})



