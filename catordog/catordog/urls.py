
from django.urls import path
from prediction.views import predict
#from prediction.views import predict これではエラーが出たので、
#その後に、from catordog.prediction.views import predictで　この部分のエラーはなくなったが、うまくrunserverが実行できなかった。ChatGPTで調べて
# -> その後環境変数でset PYTHONPATH=C:XXXXX\\\appvenv\catordogと設定し、上記の通り、prediction.viewsにしたら波線エラーが出ているようにみえるが、実行が成功した。
urlpatterns = [
    path('', predict, name='predict'),
]

