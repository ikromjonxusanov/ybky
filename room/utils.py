import datetime

from django.db.models import Q
from rest_framework.serializers import ModelSerializer

from room.exceptions import HttpGone
from room.models import Book


def availabilities(request, obj):
    date = request.query_params.get('date', datetime.date.today())
    
    data = []

    if not isinstance(date, datetime.date):
        date = datetime.datetime.strptime(date, '%d-%m-%Y')

    start = datetime.datetime.combine(date, datetime.time(hour=0, minute=0))
    end = datetime.datetime.combine(date, datetime.time(hour=23, minute=59, second=59))

    date_q = Q(start__date=date, end__date=date)

    books = Book.objects.filter(date_q, room=obj).values('start', 'end')

    if not books:
        data.append({
            'start': start,
            'end': end
        })
        return data

    last_book = books.last()

    if books[0]['start'] != start:
        data.append({
            'start': start,
            'end': books[0]['start']
        })
    for i in range(len(books) - 1):
        if books[i]['end'] == books[i + 1]['start']:
            continue
        data.append({
            'start': books[i]['end'],
            'end': books[i + 1]['start']
        })

    if last_book and last_book['end'].hour != 23 and last_book['end'].minute != 59:
        data.append({
            'start': last_book['end'],
            'end': end
        })
    
    return data


class BookValidation:
    def validate(self, attrs):
        now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        room_id = self.context.get('view').kwargs.get('pk')

        start = attrs.get('start')
        end = attrs.get('end')

        availability = {
            'start': start.replace(hour=0, minute=0, second=0, microsecond=0),
            'end': start.replace(hour=23, minute=59, second=59, microsecond=0)
        }

        if now > start or now > end or end < start:
            raise HttpGone
        if not (availability['start'] <= start <= availability['end'] and
                availability['start'] <= end <= availability['end']):
            raise HttpGone
        if Book.objects.filter(
            Q(start__lte=start, end__gt=start) |
            Q(start__range=[start, end - datetime.timedelta(minutes=1)]),
            room_id=room_id,
        ).exists():
            raise HttpGone

        return attrs
