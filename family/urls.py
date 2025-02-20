from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'collection',views.UserCollection,basename='user_collections')
router.register(r'public_collections',views.PublicCollectionListView,basename='public_collections')
urlpatterns = [
    path('family_groups/',views.FamilyGroupView.as_view(),name='my_family_groups'),
    path('create_family_group/',views.CreateFamilyGroup.as_view(),name='create_family_group'),
    path('family_group/<int:id>/',views.FamilyDetailsView.as_view(),name='famiy_group_details'),
    path('join_group/<int:id>/',views.JoinGroupView.as_view(),name="join_family_group"),
    path('joinedgroups/',views.joined_groupsView.as_view(),name='joined_groups'),
    path('updategroup/<int:id>/',views.UpdateFamilyGroup.as_view(),name='update_family_group'), # update the name or the description of the family group or code
    path('deletegroup/<int:id>/',views.DeleteFamilyGroup.as_view(),name='delete_family_group'),
    path('family_group/members/<int:id>/',views.FamilyMembers.as_view(),name='family_group_members'),
    path('family_group/create_groupcollection/<int:family_group_id>/',views.AddGroupCollection.as_view(),name='add_groupCollections'), # members can add group collections in the family group
    path('family_group/update_collection/<int:id>/',views.UpdateGroupCollection.as_view(),name='update_group_collection'),
    path('family_group/delete_collection/<int:id>/',views.DestroyGroupCollection.as_view(),name='delete_group_collection'),
    path('family/<int:family_id>/group/<int:group_collection_id>/',views.AddRecipeGroupCollection.as_view(),name = 'add recipes to the group collection'),
    path('family/<int:family_id>/group/<int:group_collection_id>/',views.AddRecipeGroupCollection.as_view(),name = 'remove recipes from the group collection'),
    path('collections/<int:collection_id>/recipe/<uuid:recipe_id>/',views.AddRecipeCollection.as_view(),name='add recipes to the collection'),
    path('collections/<int:collection_id>/recipe/<uuid:recipe_id>/',views.AddRecipeCollection.as_view(),name='remove recipes from the collection'),
    path('',include(router.urls)),

]
