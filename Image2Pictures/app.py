from flask import Flask, render_template, request, redirect, url_for
import picture_images
import numpy as np
import time
import cv2
import os


app = Flask(__name__)

@app.route('/')
def hello():
    html = render_template('index.html', message = 'Hello_World')
    return html

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        if not request.files['file'].filename == u'':

            #ディレクトリの作成
            desktop_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Pictures"
            path = desktop_path+"\\Image2Picture"
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)

            #時間の取得
            now = time.ctime()
            cnvtime = time.strptime(now)

            # アップロードされたファイルを保存
            f = request.files['file']
            img_path = os.path.join(path, time.strftime("%Y_%m_%d_%H_%M", cnvtime) + "_input.png")
            f.save(img_path)

            # 入力
            img = cv2.imread(img_path)

            # picture_images.pyへアップロードされた画像を渡す
            anime = picture_images.image_to_picture(img)

            check = np.any(anime)

            #　出力
            cv2.imwrite(time.strftime("%Y_%m_%d_%H_%M", cnvtime) + "_output.png", anime)


        return render_template('index.html',check=check)
    else:
        # エラーなどでリダイレクトしたい場合
        return redirect(url_for('index'))



if __name__ == "__main__":
    app.run()
