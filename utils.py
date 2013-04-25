from django.core import serializers

def serialize_page(page, fields=[]):
    serialized_page = dict(num_pages=page.paginator.num_pages, number=page.number)
    serialized_page['object_list'] = serializers.serialize("python", page.object_list)
    return serialized_page
