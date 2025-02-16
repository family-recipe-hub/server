from django.shortcuts import render,get_object_or_404
from .serializers import UserFamilyListSerializer,CreateFamilyGroupSerializer,JoinFamilyGroup,UpdateFamilySerializer,FamilyCollectionSerializer,GroupCollectionSerializer,GroupCollection1Serializer
from .serializers import UpdateGroupSerializer,CollectionSerializer,PublicCollectionsSerializer,MemberShipSerializer
from .serializers import FamilyMembersSerializer,FamilyGroupDetailSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status,generics
from .models import FamilyGroup,Membership,GroupCollection,Recipe,Collection
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from .permissions import IsOwner
# Create your views here.

                          #familygroups endpoints
#================================================================================
# lists the user's family group names that he is an admin in it
class FamilyGroupView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        user_data = UserFamilyListSerializer(user)
        return Response(user_data.data,status=status.HTTP_200_OK)
    
# create a family group
class CreateFamilyGroup(generics.CreateAPIView):
    queryset = FamilyGroup.objects.all()
    serializer_class = CreateFamilyGroupSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        return serializer.save(admin=self.request.user)


# show the details of the family group including the admin of each group collection and the recipes inside each collection
class FamilyDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        family_group = FamilyGroup.objects.filter(id=id,admin=request.user)
        details = FamilyGroupDetailSerializer(family_group)
        return Response(details.data,status=status.HTTP_200_OK)
    
class JoinGrouView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id):
        group_data = get_object_or_404(FamilyGroup,id=id)
        
        group_code = group_data.code
        serializer = JoinFamilyGroup(data= request.data)
        serializer.is_valid(raise_exception=True)
        if group_code==serializer.validated_data['code']:
            # give it the object
            Membership.objects.create(user = self.request.user,family_group=group_data)
            return Response({"you have joined this family group":self.request.user.username},status=status.HTTP_200_OK)
        return Response({"error":"incorrect code"},status=status.HTTP_403_FORBIDDEN)
    
class joined_groupsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        groups = Membership.objects.filter(user=request.user,many=True)
        serializer = MemberShipSerializer(groups)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UpdateFamilyGroup(UpdateAPIView):
    def put(self,request,id):
        obj = get_object_or_404(FamilyGroup,id=id)
        if self.request.user == obj.admin:
            serializer = UpdateFamilySerializer(obj,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'the family group is updated successfullly'},status=status.HTTP_200_OK)
        
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id):
        obj = get_object_or_404(FamilyGroup,id=id)
        if self.request.user == obj.admin:
            serializer = UpdateFamilySerializer(obj,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'the family group is updated successfullly'},status=status.HTTP_200_OK)
       
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class DeleteFamilyGroup(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        obj = get_object_or_404(FamilyGroup,id=id,admin=request.user)
        obj.delete()
        return Response({'message':"the group has been deleted successfully"},status=status.HTTP_200_OK)
        
class FamilyMembers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        obj = get_object_or_404(FamilyGroup,id=id)
        serializer = FamilyMembersSerializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    

# class JoinedGroupsCollectionView(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request,id):
#         collection = get_object_or_404(FamilyGroup,id=id)
#         serializer = FamilyCollectionSerializer(collection)
#         return Response(serializer.data,status=status.HTTP_200_OK)

# members can add collections in the family group
class AddGroupCollection(generics.CreateAPIView):
    permission_classes= [IsAuthenticated]
    queryset = GroupCollection.objects.all()
    serializer_class = GroupCollectionSerializer
    def create(self,request,*args,**kwargs):
        family_group_id = self.kwargs.get('family_group_id')

        try:
            family_group = FamilyGroup.objects.get(id=family_group_id)
        except FamilyGroup.DoesNotExist:
            return Response({"error": "Family group not found."}, status=status.HTTP_404_NOT_FOUND)
       
        if Membership.objects.filter(user = request.user,family=family_group).exists():
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(family_group=family_group,owner=request.user)  
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'you are not member in that family group'},status=status.HTTP_403_FORBIDDEN)
    

class UpdateGroupCollection(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = GroupCollection.objects.all()
    serializer_class = UpdateGroupSerializer
    lookup_field = "id"

    def update(self,request,*args,**kwargs):
        instance = self.get_object()
        if instance.owner == request.user:
            return super().update(request,*args,**kwargs)
        return Response({"error":"not allowed"},status=status.HTTP_403_FORBIDDEN)
    
class DestroyGroupCollection(generics.DestroyAPIView):
    queryset = GroupCollection.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def delete(self,request,*args,**kwargs):
        instance = self.get_object()
        if request.user == instance.owner:
            self.perform_destroy(instance)
            return Response({"message":"the object is GroupCollection is deleted succussfully"},status=status.HTTP_200_OK)
        return Response({"error":"not allowed"},status=status.HTTP_403_FORBIDDEN)


class AddRecipeGroupCollection(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,family_id,group_collection_id):
        family_group = get_object_or_404(FamilyGroup,id=family_id)
        recipe_id = request.data.get('recipe_id')
      
        if not recipe_id :
            return Response({"error":"recipe_id must be provided"},status=status.HTTP_400_BAD_REQUEST)
        
        recipe = get_object_or_404(Recipe,id=recipe_id)
        
        group_collection = get_object_or_404(GroupCollection,family_group=family_group,id=group_collection_id,owner = request.user)
        
        if not group_collection.recipes.filter(id=recipe_id).exists():
            group_collection.recipes.add(recipe)
            return Response({"message":"the recipe is added to the family group successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"error": "This recipe is already in the group collection"}, status=status.HTTP_400_BAD_REQUEST)
        
class RemoveRecipeGroupCollection(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,family_id,group_collection_id):
        family_group = get_object_or_404(FamilyGroup,id=family_id)

        recipe_id = request.data.get('recipe_id')
      
        if not recipe_id:
            return Response({"error":"recipe_id must be provided"},status=status.HTTP_400_BAD_REQUEST)
        
        recipe = get_object_or_404(Recipe,id=recipe_id)
        
        group_collection = get_object_or_404(GroupCollection,family_group=family_group,id=group_collection_id,owner = request.user)
        if group_collection.recipes.filter(id=recipe_id).exists():
            group_collection.recipes.remove(recipe)
            return Response({"message":"the recipe is removed from the family group successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"error": "This recipe is not in the group collection"}, status=status.HTTP_400_BAD_REQUEST)
    

######################################################################33

                             #collections endpoint
#===============================================================================#

class AddRecipeCollection(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,collection_id,recipe_id):
        collection = get_object_or_404(Collection,owner=request.user,id=collection_id)
        recipe = get_object_or_404(Recipe,id=recipe_id)
        if collection.recipes.filter(id=recipe_id).exists():
            return Response({"error": "This recipe is already in the collection"}, status=status.HTTP_400_BAD_REQUEST)
        collection.recipes.add(recipe)
        return Response({"message":"the recipe is added to your collection successfully"},status=status.HTTP_200_OK)
     
class RemoveRecipeCollection(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,collection_id,recipe_id):
        collection = get_object_or_404(Collection,owner=request.user,id=collection_id)
        recipe = get_object_or_404(Recipe,id=recipe_id)
        if not collection.recipes.filter(id=recipe_id).exists():
            return Response({"error": "This recipe is not in your collection"}, status=status.HTTP_400_BAD_REQUEST)
        collection.recipes.remove(recipe)
        return Response({"message":"the recipe is removed from your collection successfully"},status=status.HTTP_200_OK)
     

###########################################################################3

# create,update,delete and get the user's collections
class UserCollection(ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwner]
    serializer_class = CollectionSerializer

    def get_queryset(self):
        # el7aga elly hayshofha
        return Collection.objects.filter(owner=self.request.user)
    
# retrieve all the user's collections and a specific collection according to the id
class PublicCollectionListView(ReadOnlyModelViewSet):
    serializer_class = PublicCollectionsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Collection.objects.filter(is_public=True)
    