from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
# from django.utils.safestring import mark_safe
from .models import *
# from PIL import Image
# class NotebookAdminForm(ModelForm): #загрузка изображений, запрет загрузки меньше минимального размера
    
#     def __init__(self,*args,**kwargs): #функция вывода на админке минимального разрешения
#         super().__init__(*args,**kwargs)
#         self.fields['image'].help_text = mark_safe('<span style="color:red; font-size:14px;">При загрузке изображения с разрешением больше  {}x{} оно будет обрезано</span>'.format(
#             *Product.MAX_RESOLUTION
#             ))
    
    # def clean_image(self): #исключение возможности загрузки зображения меньше заданного значения
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     min_height, min_width = Product.MIN_RESOLUTION
    #     max_height, max_width = Product.MAX_RESOLUTION
    #     if image.size > Product.MAX_IMAGE_SIZE:
    #         raise ValidationError('Размер изображение не должен превышать 3мб!')
    #     if img.height < min_height or img.width < min_width:
    #         raise ValidationError('Разрешение изображения меньше минимального!')
    #     if img.height > max_height or img.width > max_width:
    #         raise ValidationError('Разрешение изображения выше максимального!')
    #     return image

class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: gray;'
            })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max']= None
        return self.cleaned_data

class NotebookAdmin(admin.ModelAdmin):
    # form = NotebookAdminForm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'Category':
            return ModelChoiceField(Category.objects.filter(slug ='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'admin.html'
    form = SmartphoneAdminForm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'Category':
            return ModelChoiceField(Category.objects.filter(slug ='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(SmartPhone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)


# Register your models here.
