from django.db import models

# Create your models here.

class Match(models.Model):
    RESULT_CHOICES = (
        ('W', '勝ち'),
        ('D', '引き分け'),
        ('L', '負け'),
    )

    date = models.DateField(verbose_name="試合日")
    opponent = models.CharField(max_length=100, verbose_name="対戦相手")
    tournament = models.CharField(max_length=200, verbose_name="大会名")
    japan_score = models.IntegerField(verbose_name="日本得点")
    opponent_score = models.IntegerField(verbose_name="相手得点")
    result = models.CharField(max_length=1, choices=RESULT_CHOICES, verbose_name="勝敗")
    venue = models.CharField(max_length=200, verbose_name="開催地")
    manager = models.CharField(max_length=100, verbose_name="監督", blank=True, null=True)
    scorers = models.TextField(verbose_name="得点者", blank=True, null=True, help_text="カンマや改行区切りで入力してください")
    notes = models.TextField(verbose_name="メモ/詳細", blank=True, null=True)
    def __str__(self):
        return f"{self.date} vs {self.opponent} ({self.japan_score}-{self.opponent_score})"
    class Meta:
        verbose_name = "戦績"
        verbose_name_plural = "戦績一覧"
        ordering = ['-date']  # 新しい日付順にソート