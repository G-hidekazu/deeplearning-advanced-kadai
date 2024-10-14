from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    #質問「forms」モジュールの「Form」クラスを継承し」　とは？
  