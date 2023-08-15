from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import SearchHistory, NewsArticle
from .serializers import SearchHistorySerializer, NewsArticleSerializer

NEWS_API_KEY = '93651d9d640a402c8b497d05ae11594c'

def index(request):
    return render(request, 'index.html')


class NewsSearchView(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword')
        if keyword:
            url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}'
            response = requests.get(url)
            data = response.json()

            search_history = SearchHistory(user=request.user, keyword=keyword)
            search_history.save()

            articles = data.get('articles', [])
            news_articles = []
            for article in articles:
                news_article = NewsArticle(
                    title=article['title'],
                    description=article['description'],
                    url=article['url'],
                    date_published=article['publishedAt'],
                    search_history=search_history
                )
                news_articles.append(news_article)
            
            NewsArticle.objects.bulk_create(news_articles)

            return Response(data)
        return Response({'error': 'Keyword parameter is required.'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_search_history(request):
    search_history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
    serializer = SearchHistorySerializer(search_history, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_search_results(request, search_history_id):
    news_articles = NewsArticle.objects.filter(search_history__user=request.user, search_history_id=search_history_id).order_by('-date_published')
    serializer = NewsArticleSerializer(news_articles, many=True)
    return Response(serializer.data)
