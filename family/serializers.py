from rest_framework import serializers
from .models import FamilyGroup,Membership,Collection,GroupCollection,Collection,Recipe
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'



# lists the user's family group names
class FamilyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyGroup
        fields = ['name','description']

class UserFamilyListSerializer(serializers.ModelSerializer):
    my_family_groups = FamilyGroupSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['my_family_groups']

#===================================================================
# create a family group
class CreateFamilyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyGroup
        fields = ['name','description','code']

#===================================================================

#serializer for the Group collection
class GroupCollection1Serializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    recipes = RecipeSerializer(many=True,read_only=True)
    class Meta:
        model = GroupCollection
        fields = ['owner','title','description','recipes']


# show the details of the family group including the admin of each group collection and the recipes inside each collection
class FamilyGroupDetailSerializer(serializers.ModelSerializer):
    group_collection = GroupCollection1Serializer(many=True,read_only=True)
    class Meta:
        model = FamilyGroup
        fields = '__all__'

#====================================================================

class MemberShipSerializer(serializers.ModelSerializer):
    family = FamilyGroupDetailSerializer(many=True,read_only=True)
    class Meta:
        model = Membership
        fields = ['family','joined_at']

class JoinFamilyGroup(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    

class UpdateFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyGroup
        fields = ['name','description','code']

#====================================================================
class Membership2Serializer(serializers.ModelSerializer):
    user=UserSerializer(many=True,read_only=True)
    class Meta:
        model = Membership
        fields = ['user']

class FamilyMembersSerializer(serializers.ModelSerializer):
    group_members = Membership2Serializer(many=True,read_only=True)
    class Meta:
        model = FamilyGroup
        fileds = ['group_members']

class GroupCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCollection
        fields = ['owner','title','description']

class FamilyCollectionSerializer(serializers.ModelSerializer):
    group_collections = GroupCollectionSerializer(many=True,read_only=True)
    class Meta:
        model = FamilyGroup
        fields = ['admin','group_collections']


#================================================

class UpdateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCollection
        fields = ['title','description']

class RecipesInGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyGroup
        fields = ['recipes']

# ===========================================#
                #collection serializers




class PublicCollectionsSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True,read_only=True)
    owner = UserSerializer(read_only=True)
    class Meta:
        model= Collection
        fields = '__all__'
#========================================================

class CollectionSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Automatically set owner
    recipes = serializers.SerializerMethodField()
    class Meta:
        model = Collection
        fields = ['id', 'owner', 'title', 'description', 'is_public', 'recipes']
        read_only_fields = ['owner']  

    def get_recipes(self, obj):
        """Return detailed recipe information instead of just IDs"""
        return [model_to_dict(recipe) for recipe in obj.recipes.all() ]

    def create(self, validated_data):
        recipes = validated_data.pop('recipes', [])
        collection = Collection.objects.create(owner=self.context['request'].user, **validated_data)
        collection.recipes.set(recipes)  
        return collection

    def update(self, instance, validated_data):
        
        recipes = validated_data.pop('recipes', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if recipes is not None:
            instance.recipes.set(recipes)  

        instance.save()
        return instance