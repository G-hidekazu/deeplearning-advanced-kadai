from django.shortcuts import render
from .forms import ImageUploadForm
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
#このvgg16の２つが前と異なる部分
from io import BytesIO
import os
import pandas as pd

def predict(request):
    if request.method == 'GET':
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            img_file = BytesIO(img_file.read())
            img = load_img(img_file, target_size=(224, 224)) #ここでモデルに合わせてサイズ変更
            img_array = img_to_array(img)
            img_array = img_array.reshape((1, 224, 224, 3)) #ここで配列を4次元に変更
            img_array = preprocess_input(img_array)  #VGG16に対する前処理
            model_path = os.path.join(settings.BASE_DIR, 'prediction', 'models', 'vgg16.h5')
            model = load_model(model_path)
            result = model.predict(img_array)
            prediction_top5 = decode_predictions(result)[0]
            df_Prediction_Top5 = pd.DataFrame(prediction_top5,columns=['ClassID', 'Label', 'Probability']) 
            df_Prediction_Top5["Probability"] = df_Prediction_Top5["Probability"]*100
            dict_prediction_top5 = df_Prediction_Top5.to_dict(orient='records')
            #format_prediction_top5 = [prediction_top5[0][1]]
            #df_Prediction_Top5 = pd.DataFrame(prediction_top5[0],columns=['Class ID', 'Label', 'Probability']) 
            #return render(request, 'home.html', {'form': form, 'prediction': format_prediction_top5})
            #途中で「print(df_Prediction_Top5.columns)」とかをやりたいときは通常どうすればいいのか？
            img_data = request.POST.get('img_data')

            return render(request, 'home.html', {'form': form, 'prediction': dict_prediction_top5,'img_data': img_data})
        else:
            form = ImageUploadForm()
            return render(request, 'home.html', {'form': form})
