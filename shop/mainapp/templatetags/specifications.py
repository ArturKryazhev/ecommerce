from django import template
from django.utils.safestring import mark_safe
from mainapp.models import SmartPhone
register =template.Library()
TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """


PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Частота процессора': 'processor_freq',
        'Оперативная память': 'ram',
        'Видеокарта': 'video',
        'Время работы аккумулятора': 'time_without_charge'
    },
    'smartphone':{
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разрешение экрана': 'resolution',
        'Заряд аккумулятора': 'accum_volume',
        'Оперативная память': 'ram',
        'Наличие слота sd карты': 'sd',
        'Максимальный объем SD карты': 'sd_volume_max',
        'Камера (МП)': 'main_camp_mp',
        'Фронтальная камера (МП)': 'frontal_cam_mp'
        
    }

}
def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items(): #берем value
        table_content+=TABLE_CONTENT.format(name=name,value=getattr(product,value)) #конкатенация #getattr - взяли продукт и попросили дать значение value
        
    return table_content
@register.filter #фильтр из html {{product|product_spec}}
def product_spec(product):
    model_name = product.__class__._meta.model_name #узнаем имя
    if isinstance(product, SmartPhone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объем SD карты')
        else:
            PRODUCT_SPEC['smartphone']['Максимальный объем SD карты'] = 'sd_volume_max' #почему то кидает эту строку последней
    return mark_safe(TABLE_HEAD+get_product_spec(product,model_name)+TABLE_TAIL)