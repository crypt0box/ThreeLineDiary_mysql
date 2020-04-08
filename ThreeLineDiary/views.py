from django.db.models import Q
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from .models import Post
from .forms import LoginForm, UserCreateForm, PostCreateForm


User = get_user_model()


class IndexView(generic.ListView):
    model = Post

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at') # 昇順の場合-を付けない
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'ThreeLineDiary/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'ThreeLineDiary/home.html'


class UserCreate(generic.CreateView):
    """ユーザー登録"""
    template_name = 'ThreeLineDiary/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        return redirect('ThreeLineDiary:user_create_complete')


class UserCreateComplete(generic.TemplateView):
    """ユーザー本登録"""
    template_name = 'ThreeLineDiary/user_create_complete.html'


class OnlyYouMixin(UserPassesTestMixin):
    """本人か、スーパーユーザーだけユーザーページアクセスを許可する"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.ListView):
    """ユーザーの詳細ページ"""
    model = Post
    template_name = 'ThreeLineDiary/user_detail.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = Post.objects.all()
        return context


class PostCreate(generic.CreateView):
    """日記投稿"""
    template_name = 'ThreeLineDiary/post_create.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        user_pk = self.kwargs['user_pk']    # urlに含まれているプライマリキーの取得
        post = form.save(commit=False)   # commit=False: データを保存する一歩手前のモデルインスタンスを返す
        post.user = get_object_or_404(User, pk=user_pk)
        post.save()  # ここでDBに保存
        return redirect('ThreeLineDiary:user_detail', pk=user_pk)


class IconUpdate(generic.UpdateView):
    """サムネイル投稿"""
    model = User
    fields = ('image',)
    template_name = 'ThreeLineDiary/icon_update.html'

    def get_success_url(self):
        return reverse('ThreeLineDiary:user_detail', kwargs={'pk': self.object.pk})


class About(generic.TemplateView):
    """ユーザー本登録"""
    template_name = 'ThreeLineDiary/about.html'




