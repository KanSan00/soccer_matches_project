import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from matches.models import Match
class Command(BaseCommand):
    help = 'CSVファイルから戦績データをインポートします'
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSVファイルのパス')
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            created_count = 0
            
            for row in reader:
                # 日付のフォーマット変換 (例: "2026-06-01" または "2026/06/01")
                date_str = row['date'].replace('/', '-')
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                # 日本の得点と相手の得点から勝敗を自動判定（CSVにresultが無い場合の補助）
                j_score = int(row['japan_score'])
                o_score = int(row['opponent_score'])
                if j_score > o_score:
                    res = 'W'
                elif j_score < o_score:
                    res = 'L'
                else:
                    res = 'D'
                Match.objects.update_or_create(
                    date=date_obj,
                    opponent=row['opponent'],
                    defaults={
                        'tournament': row.get('tournament', '親善試合'),
                        'japan_score': j_score,
                        'opponent_score': o_score,
                        'result': row.get('result', res),
                        'venue': row.get('venue', ''),
                        'manager': row.get('manager', ''),
                        'scorers': row.get('scorers', ''),
                        'notes': row.get('notes', ''),
                    }
                )
                created_count += 1
                
        self.stdout.write(self.style.SUCCESS(f'{created_count} 件の戦績データをインポートしました。'))