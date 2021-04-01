import cv2


def image_to_picture(img):
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # Cannyアルゴリズムで輪郭抽出
    edge = cv2.Canny(gray, 100, 200)

    #輪郭画像をRGBへ
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    # 差分を返す
    return cv2.subtract(img, edge)


# コマンドラインからのテスト用
if __name__ == '__main__':
    # 入力
    img = cv2.imread("input.jpg")
    # 画像を絵のようにする
    anime = image_to_picture(img)
    #　出力
    cv2.imwrite('output.jpg', anime)
