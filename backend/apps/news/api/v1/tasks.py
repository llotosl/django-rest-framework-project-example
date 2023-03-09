from django.core.mail import send_mail

from config.celery import app
from apps.news.models import News

from django.conf import settings


@app.task()
def send_news_to_email(news_id: int, email: str):
    news = News.objects.filter(
        id=news_id
    ).first()
    
    if news is None:
        return

    message = news.subtitle + '\n\n' if news.subtitle else '' + news.text

    send_mail(
        subject=news.title,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
