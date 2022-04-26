"""inventory urls file."""

from django.test import TestCase

# Create your tests here.
from django.urls import path,include
#from inventory.views import inventory_views as views
import inventory.views as views
from inventory.decorators import permission_denied_view,admin_required

"""URL for all users"""
urlpatterns = [
    path('',views.home,name='home'),
    path('403/', permission_denied_view, name='permission_denied_view'),
    path('login',views.login,name='login'),
    path('logout',views.logout, name='logout'),
    path('login_option/<int:user_id>/', views.login_option, name='login_option'),
    path('home', views.dashboard, name='dashboard'),
    path('search_devices',views.search_devices, name='search_devices'),
    path('details/<int:device_id>', views.device_details, name='device_details'),
    path('getProjectData', views.projectData)

]
"""Urls for Admin and Super User"""
urlpatterns += [
    path('add_device/<int:id>',admin_required(views.add_device),name='add_device'),
    path('delete_device/<int:device_id>',admin_required(views.delete_device),name='delete_device'),
    path('modify_item', admin_required(views.modify_item), name='edit_device'),
    path('edit_item/<int:id>', admin_required(views.edit_item), name='edit_item'),
    path('accept/<int:allo_id>', views.accept, name='accept'),
    path('reject/<int:allo_id>', views.reject, name='reject'),
    path('ldap/', admin_required(views.ldap), name='ldaps'),
    path('disallow/', admin_required(views.disallow), name='disallow'),
    path('allow/', admin_required(views.allow), name='allow'),
    path('service', views.create_service, name='service'),
    path('create_reject_service_view/<int:allo_id>', views.create_reject_service_view, name='create_reject_service_view'),
    path('release/<int:allo_id>', views.release_service, name='release'),
    path('borrow/<int:allo_id>', views.borrow_service, name='borrow'),
    path('accept1/<int:allo_id>',views.accept_service,name='accept1'),
    path('reject1/<int:allo_id>',views.reject_service,name='reject1'),
    path('device_information/<int:allo_id>', views.device_information, name='device_information'),
    path('item_modification', admin_required(views.item_modification), name='item_modification'),
    path('advance_search', views.advance_search, name='advance_search'),
]
"""Urls for USER."""
urlpatterns += [
    path('information/<int:allo_id>', views.information, name='information'),
    path('transfer/<int:allo_id>', views.transfer, name='transfer'),
    path('free_Item/<int:allo_id>', views.free_item, name='free_item'),
    path('create_service/<str:allo_id>', views.create_service, name='create_service'),
    path('return_to_store/<int:allo_id>', views.return_to_store, name='return_to_store'),
    path('incorrect/<int:allo_id>', views.incorrect, name='incorrect'),
]
