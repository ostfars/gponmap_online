from django import forms


class KMLLayerForm(forms.Form):
    layer1 = forms.BooleanField(required=False, label='Все опоры')
    layer2 = forms.BooleanField(required=False, label='ОСБ')
    layer3 = forms.BooleanField(required=False, label='ОСКМ')
    layer4 = forms.BooleanField(required=False, label='Муфты')
    layer5 = forms.BooleanField(required=False, label='Базовые станции')
    layer6 = forms.BooleanField(required=False, label='Покрытие')
    layer7 = forms.BooleanField(required=False, label='Линии проектные')
    layer8 = forms.BooleanField(required=False, label='Линии фактические')


class KMLUploadForm(forms.Form):
    kml_file = forms.FileField()
