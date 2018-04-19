from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


# 先获取被评论文章
def post_comment(request, post_pk):
    # Django提供的get_object_or_404函数，
    # 当文章（Post）存在，获取，否则404
    post = get_object_or_404(Post, pk=post_pk)

    # HTTP有get和post两种请求，一般用户表单提交数据用post
    if request.method == 'POST':  # 用户提交的数据存在request.POST，这是一个类字典
        form = CommentForm(request.POST)  # 利用这些数据构造了CommentForm的实例，生成Django表单

        # 调用form.is_valid()，Django自动检查表单数据是否符合格式要求
        if form.is_valid():
            comment = form.save(commit=False)  # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库
            comment.post = post  # 评论和被评论文章关联
            comment.save()  # 最终将评论数据保存进数据库，调用模型实例的 save 方法

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)