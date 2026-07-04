from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Match
class MatchListView(ListView):
    model = Match
    template_name = 'matches/match_list.html'
    context_object_name = 'matches'
    paginate_by = 10  # 1ページに10件表示
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')          # キーワード検索
        result = self.request.GET.get('result')    # 勝敗フィルター
        year = self.request.GET.get('year')        # 年フィルター
        if query:
            queryset = queryset.filter(
                Q(opponent__icontains=query) |
                Q(tournament__icontains=query) |
                Q(manager__icontains=query) |
                Q(scorers__icontains=query)
            )
        if result:
            queryset = queryset.filter(result=result)
        if year:
            queryset = queryset.filter(date__year=year)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 検索条件をテンプレートに引き継ぐための処理
        context['q'] = self.request.GET.get('q', '')
        context['result'] = self.request.GET.get('result', '')
        context['year'] = self.request.GET.get('year', '')
        
        # 絞り込み用の年リスト（データベースに登録されている年の一覧を取得）
        context['years'] = Match.objects.dates('date', 'year', order='DESC')
        return context
class MatchDetailView(DetailView):
    model = Match
    template_name = 'matches/match_detail.html'
    context_object_name = 'match'
