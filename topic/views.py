from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import FoodTopic

from actions.utils import create_action
from utils import make_paginator
from utils.decorators import ajax_required

# 专题列表
def topic_list(request):
    topics = make_paginator(request, topic.objects.all())
    if request.is_ajax():
        return render(request, 'topic/list_ajax.tpl',
                      {'topics': topics})
    return render(request, 'topic/list.tpl', {
            'topics': topics
        })

# 专题详情
def topic_detail(request, topic_id):
    topic = FoodTopic.objects.get(pk=topic_id)
    foods = make_paginator(request, topic.foods.all())
    return render(request, 'topic/detail.tpl', {
            'foods': foods
        })

# 收藏
@login_required
@require_POST
@ajax_required
def topic_collect(request):
    topic_id = request.POST.get('id') 
    action = request.POST.get('action')
    if topic_id and action:
        topic = FoodTopic.objects.get(pk=topic_id)
        if action == 'collect':
            topic.users_collect.add(request.user)
            create_action(request.user, '收藏了', topic)
        elif action == 'uncollect':
            topic.users_collect.remove(request.user)
        else:
            return JsonResponse({'status': False})
        return JsonResponse({'status': True})
    return JsonResponse({'status': False}, status=400)
