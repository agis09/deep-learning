#######

import numpy as np
import tensorflow as tf
from sklearn.utils import shuffle  # データをランダムにシャッフル
# 実験設定
M = 2   # 入力データの次元
K = 3   # クラス数
n = 100  # クラスごとのデータ数
N = n * K  # 全データ数
# サンプルデータ群
X1 = np.random.randn(n, M) + np.array([0, 10])
X2 = np.random.randn(n, M) + np.array([5, 5])
X3 = np.random.randn(n, M) + np.array([10, 0])
Y1 = np.array([[1, 0, 0]for i in range(n)])
Y2 = np.array([[0, 1, 0]for i in range(n)])
Y3 = np.array([[0, 0, 1]for i in range(n)])

X = np.concatenate((X1, X2, X3), axis=0)
Y = np.concatenate((Y1, Y2, Y3), axis=0)

"""
モデル定義(rogistic:sigmoid->multiclass:softmax)
"""

W = tf.Variable(tf.zeros([M, K]))
b = tf.Variable(tf.zeros([K]))

x = tf.placeholder(tf.float32, shape=[None, M])
t = tf.placeholder(tf.float32, shape=[None, K])
y = tf.nn.softmax(tf.matmul(x, W) + b)

# ミニバッチごとの平均値
cross_entropy = tf.reduce_mean(-tf.reduce_sum(t * tf.log(y),
                                              reduction_indices=[1]))   # 行列のどの方向に向かって和をとるか
# 確率的勾配降下法で最小化
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy)

# 分類が正しいかどうか
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(t, 1))

"""
モデル学習
"""
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

batch_size = 50  # ミニバッチサイズ
n_batches = N // batch_size

for epoch in range(20):
    X_, Y_ = shuffle(X, Y)

    for i in range(n_batches):
        start = i * batch_size
        end = start * batch_size

        sess.run(train_step, feed_dict={
            x: X_[start:end],
            t: Y_[start:end]
        })

# ランダムに選んだ１０個のデータを確認
X_, Y_ = shuffle(X, Y)

classified = correct_prediction.eval(session=sess, feed_dict={
    x: X_[0:10],
    t: Y_[0:10]
})
prob = y.eval(session=sess, feed_dict={
    x: X_[0:10]
})

print('classified')
print(classified)
print()
print('output probability')
print(prob)
