import glob
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import requests
import json
import urllib.parse
import urllib.request

base_url = '<API URL>'
prediction_key = '<Key>'

poke_root_dir = 'pokemon/'
# 検証対象のポケモン名一覧
pokemonnames = ['ピカチュウ','ゼニガメ','ヒトカゲ','フシギダネ','カビゴン']

for pokename in pokemonnames:
    testfiles = glob.glob(poke_root_dir + pokename + '/test/*')
    data_count = len(testfiles)
    true_count = 0
    
    for testfile in testfiles:
        headers = {
            'Content-Type': 'application/json',    
            'Prediction-Key': prediction_key
        }
        
        params = {}
        predicts = {}
        data = open(testfile, 'rb').read()
        response = requests.post(base_url, headers=headers, params=params, data=data)
        results = json.loads(response.text)
        
        try:
            # 予測結果のタグの数だけループ　…③
            for prediction in results['predictions']:
                # 予測したポケモンとその確率を紐づけて格納　…④
                predicts[prediction['tagName']] = prediction['probability']
            # 一番確率の高いポケモンを予測結果として選択　…⑤
            prediction_result = max(predicts, key=predicts.get)
        
            # 予測結果が合っていれば正解数を増やす
            if pokename == prediction_result:
                true_count += 1

        #画像サイズ > 6MB だとCustom Vision の制限にひっかりエラーが出るまで握り潰し
        except KeyError:
            data_count -= 1
            continue
    
    # 正解率の算出
    accuracy = (true_count / data_count) * 100
    print('ポケモン名:' + pokename)
    print('正解率:' + str(accuracy) + '%')