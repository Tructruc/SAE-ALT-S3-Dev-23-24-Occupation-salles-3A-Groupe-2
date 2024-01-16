import pytz, time

from dateutil import parser

def data_id_to_data_objet(objet, date_from, date_to):
    """
    Objet : objet Sensor
    """
    data_ids = objet.all_data.values_list('id', flat=True)
    all_data_qs = objet.objects.filter(id__in=data_ids)

def data_date_sort(objet, date_from, date_to):
    """
    Objet : objet Data

    date_from exemple : 2024-01-10T17:18:42.771040 01:00
    fromat : %Y-%m-%dT%H:%M:%S.%f %z
    """
    
    utc = pytz.UTC

    objet_time = objet.time.replace(tzinfo=utc)

    if date_from:
        # Split on the space to delete the +01:00
        date_from = date_from.split(' ')[0]
        date_from = parser.parse(date_from) if isinstance(date_from, str) else date_from
        date_from = date_from.replace(tzinfo=utc) if date_from.tzinfo is None else date_from

    if date_to:
        # Split on the space to delete the +01:00
        date_to = date_to.split(' ')[0]
        date_to = parser.parse(date_to) if isinstance(date_to, str) else date_to
        date_to = date_to.replace(tzinfo=utc) if date_to.tzinfo is None else date_to

    print("objet_time : ")
    print(objet_time)
    print("date_from : ")
    print(date_from)
    print("date_to : ")
    print(date_to)

    if date_from is not None and objet_time < date_from:
        print("On garde pas")
        return False
    
    if date_to is not None and objet_time > date_to:
        print("On garde pas")
        return False
    
    print("On garde")
    return True