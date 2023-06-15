from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, filters
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Subscription, User

from .filters import NameFilter, RecipeFilter
from .pagination import CustumPagination
from .permissions import AuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeGetSerializer,
    RecipeShortSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer,
)
from .utils import download_shopping_cart


class CustomUserViewSet(UserViewSet):
    """Вьюсет User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Список на кого подписан пользователь"""
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True, url_path='subscribe',
        url_name='subscribe',
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        """Подписка на автора"""
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {'errors': 'На себя самого нельзя подписаться/отписаться'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription = Subscription.objects.filter(
            author=author, user=user)

        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    {'errors': 'Вы уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = Subscription.objects.create(author=author, user=user)
            serializer = SubscriptionSerializer(
                queryset, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not subscription.exists():
                return Response(
                    {'errors': 'Вы уже отписались'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_backends = (NameFilter,)
    search_fields = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):
    """Вюсет рецептов"""

    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = CustumPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('pk'))
        recipe_serializer = RecipeShortSerializer(recipe)
        favorites = Favorite.objects.filter(
            recipe_id=recipe.id,
            user_id=self.request.user.id,
        )

        if (self.request.method == 'POST') and not favorites.exists():
            Favorite(
                recipe_id=recipe.id,
                user_id=self.request.user.id,
            ).save()
            return Response(
                recipe_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        if (self.request.method == 'DELETE') and favorites.exists():
            favorites.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Не верный запрос'},
            status=status.HTTP_400_BAD_REQUEST,
            exception=True,
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.post_method(ShoppingCart, request.user, pk)
        return self.delete_method(ShoppingCart, request.user, pk)

    def post_method(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {'errors': 'Рецепт уже в списке'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_method(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if not obj.exists():
            return Response(
                {'errors': 'Рецепта нет в списке'},
                status=status.HTTP_400_BAD_REQUEST
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        return download_shopping_cart(self, request)
