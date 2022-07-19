from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from newsportal.filters import PostFilter
from newsportal.forms import NewsForm
from newsportal.models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class NewsListView(ListView):
    model=Post
    template_name = 'news_all.html'
    context_object_name = 'posts'
    ordering = ['-date_time_create']
    paginate_by = 5






class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_single.html'

class NewsSearchView(ListView):
    model =Post
    template_name = 'news_search.html'
    context_object_name = 'posts'
    ordering = ['-date_time_create']
    paginate_by = 5


    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
            context = super().get_context_data(**kwargs)
            context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
            return context



class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'





# дженерик для удаления товара
class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm
    permission_required =('newsportal.add_post', 'newsportal.change_post')

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_update.html'
    form_class = NewsForm
    permission_required =('newsportal.add_post', 'newsportal.change_post')

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')