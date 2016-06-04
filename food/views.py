from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .forms import FoodForm
from .models import Food, FoodCategory

from actions.utils import create_action
from comments.models import Comment
from comments.forms import FoodCommentForm
from utils import make_paginator
from utils.decorators import ajax_required, tab
from updown.views import AddRatingFromModel

import redis


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

categorys = FoodCategory.objects.all()


@login_required
def food_create(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user
            food.save()
            return HttpResponseRedirect(reverse('food:detail', kwargs={'food_id': food.id}))
    else:
        form = FoodForm()
    return render(request, 'food/create.tpl', {
            'form': form,
            'categorys': categorys
        })


def food_latest(request):
    foods = Food.objects.all()
    return render(request, 'food/list.tpl', {
            'foods': foods,
            'categorys': categorys
        })


def food_detail(request, food_id):
    user = request.user
    food = get_object_or_404(Food, pk=food_id)
    comments = make_paginator(request, food.comments.all())
    if request.method == 'POST':
        comment_form = FoodCommentForm(request.POST)
        if user.is_authenticated():
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = user
                comment.food = food
                comment.save()
                messages.success(request, '评论成功')
            else:
                messages.error(request, '评论失败')
        else:
            messages.error(request, '请登录后评论')
    else:
        comment_form = FoodCommentForm()
    food_tags_ids = food.tags.values_list('id')
    similar_foods = Food.objects.filter(tags__in=food.tags.all()).exclude(id=food_tags_ids)
    similar_foods = similar_foods.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    total_views = r.incr('food:{}:views'.format(food.id))
    # r.zincrby('food_ranking', food.id, 1)
    return render(request, 'food/detail.tpl', {
            'food': food,
            'comments': comments,
            'comment_form': comment_form,
            'similar_foods': similar_foods,
            'total_views': total_views,
            'is_wta': user.foods_wta.filter(pk=food.id).exists(),
            'is_ate': user.foods_ate.filter(pk=food.id).exists(),
        })

def food_category(request, category):
    foods = make_paginator(request, Food.objects.filter(category__name=category))
    return render(request, 'food/list.tpl', {
            'foods': foods,
            'categorys': categorys,
            'section': category
        })

def food_tag(request, tag):
    foods = make_paginator(request, Food.objects.filter(tags__name=tag))
    return render(request, 'food/list.tpl', {
            'foods': foods,
            'categorys': categorys
        })

@tab('explore', sub_tab='new')
def explore(request):
    foods = make_paginator(request, Food.objects.all())
    return render(request, 'food/explore.tpl', {
                   'foods': foods
                })

@tab('explore', sub_tab='hot')
def hot(request):
    food_ranking = r.zrange('food_ranking', 0, -1, desc=True)[:10]
    food_ranking_ids = [int(id) for id in food_ranking]

    most_viewed = list(Food.objects.filter(id__in=food_ranking_ids))
    most_viewed.sort(key=lambda x: food_ranking_ids.index(x.id))

    return render(request, 'food/explore.tpl', {
                   'foods': most_viewed
                })

@ajax_required
@require_POST
@login_required
def food_rate(request):
    food_id = request.POST.get('id')
    action = request.POST.get('action')
    view = AddRatingFromModel()
    resp = view(request,
        app_label='food',
        model='Food',
        field_name='rating',
        object_id=int(food_id),
        score=1 if action=='like' else -1
    )
    return JsonResponse({'status': resp.status_code==200}, status=resp.status_code)

@ajax_required
@require_POST
@login_required
def food_wta(request):
    food_id = request.POST.get('id')
    action = request.POST.get('action')
    if food_id and action:
        food = Food.objects.get(pk=food_id)
        if action == 'wta':
            food.users_wta.add(request.user)
        else:
            food.users_wta.remove(request.user)
        return JsonResponse({'status': True})
    return JsonResponse({'status': False}, status=400)

@ajax_required
@require_POST
@login_required
def food_ate(request):
    food_id = request.POST.get('id')
    action = request.POST.get('action')
    if food_id and action:
        food = Food.objects.get(pk=food_id)
        if action == 'ate':
            food.users_ate.add(request.user)
        else:
            food.users_ate.remove(request.user)
        return JsonResponse({'status': True})
    return JsonResponse({'status': False}, status=400)
