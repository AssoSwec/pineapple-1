{% extends 'user/base.tpl' %}
{% load staticfiles %}
{% load humanize %}
{% block head %}
<link href="{% static 'css/user_share.css' %}" rel="stylesheet">
{% endblock head %}
{% block content %}
<div class="tab-container">
    <div class="share-container">
        <ul class="share-container-ul">
            {% for food in foods %}
            <li class="share-container-item clearfix">
                <span class="share-time">分享于 {{ food.created | naturaltime }}</span>
                <div class="item-index">
                    {{ forloop.counter }}
                </div>
                <div class="images-item" style="background-image: url('{{ MEDIA_URL }}{{ food.cover_image }}')"></div>
                <div class="item-main">
                    <h3 class="item-title"><a href="{{ food.get_absolute_url }}">{{ food.title }}</a></h3>
                    <p class="item-desc">
                        {{ food.description }}
                    </p>
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>
</div>
{% endblock content %}
{% block js %}
<script src="{% static 'js/user_share.js' %}"></script>
{% endblock js %}
