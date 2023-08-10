from django.urls import path

from todos.views import TodoListCreateAPI, TodoUpdateAPIViews


urlpatterns = [
    path('list/', TodoListCreateAPI.as_view(), name='list-create'),
    path('list/<int:id>/',TodoUpdateAPIViews.as_view(), name='update' )

]