import os
import glob
import random
import shutil
from icrawler.builtin import GoogleImageCrawler

#画像を保存するルートディレクトリ
root_dir = 'pokemon/'
#ポケモン画像検索キーワードリスト
pokemonnames = ['ピカチュウ','ゼニガメ','ヒトカゲ','フシギダネ','カビゴン']

#収集画像データ数
data_count = 100

for pokemonname in pokemonnames:
    crawler = GoogleImageCrawler(storage={'root_dir':root_dir + pokemonname + '/train'})
    
    filters = dict(
        size = 'large',
        type = 'photo'
    )
    
    #クローリングの実行
    crawler.crawl(
        keyword=pokemonname,
        filters=filters,
        max_num=data_count
    )
    
    #前回実行時のtestディレクトリが存在する場合、ファイルをすべて削除する
    
    if os.path.isdir(root_dir + pokemonname + '/test'):
        shutil.rmtree(root_dir + pokemonname + '/test')
    os.makedirs(root_dir + pokemonname + '/test')
    
    #ダウンロードファイルのリストを取得
    filelist = glob.glob(root_dir + pokemonname + '/train/*')
    #ダウンロード数の2割をtestデータとして抽出
    test_ratio = 0.2
    testfiles = random.sample(filelist, int(len(filelist) * test_ratio))
    
    for testfile in testfiles:
        shutil.move(testfile, root_dir + pokemonname + '/test/')