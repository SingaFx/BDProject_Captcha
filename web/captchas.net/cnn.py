#coding=utf-8  
from PIL import Image
import numpy as np
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import random



class cnn():
    def __init__(self):
        self.IMAGE_HEIGHT = 80
        self.IMAGE_WIDTH = 240
        self.MAX_CAPTCHA = 6
        self.CHAR_SET_LEN = 26
        self.X = tf.placeholder(tf.float32, [None, self.IMAGE_HEIGHT*self.IMAGE_WIDTH])
        self.Y = tf.placeholder(tf.float32, [None, self.MAX_CAPTCHA*self.CHAR_SET_LEN])
        self.keep_prob = tf.placeholder(tf.float32)
        self.all_image = None

    def get_all_images(self):
        self.all_image = os.listdir('./img999/')

    def get_name_and_image(self):
        try:
            random_file = random.randint(0, len(self.all_image) - 1)
            base = os.path.basename('./img999/' + self.all_image[random_file])
            name = os.path.splitext(base)[0]
            name = name[:6]
            image = Image.open('./img999/' + self.all_image[random_file])
            image = np.array(image)
            return name, image
        except:
            print(random_file)
            return '', None


    def name2vec(self, name):
        vector = np.zeros(self.MAX_CAPTCHA*self.CHAR_SET_LEN)
        for i, c in enumerate(name):
            idx = i * 26 + ord(c) - 97
            vector[idx] = 1
        return vector


    def vec2name(self, vec):
        name = []
        for i in vec:
            a = chr(i + 97)
            name.append(a)
        return "".join(name)


    # 生成一个训练batch
    def get_next_batch(self, batch_size=64):
        batch_x = np.zeros([batch_size, self.IMAGE_HEIGHT*self.IMAGE_WIDTH])
        batch_y = np.zeros([batch_size, self.MAX_CAPTCHA*self.CHAR_SET_LEN])

        for i in range(batch_size):
            name, image = self.get_name_and_image()
            batch_x[i, :] = 1*(image.flatten())
            batch_y[i, :] = self.name2vec(name)
        return batch_x, batch_y

    ####################################################

    # 定义CNN
    def crack_captcha_cnn(self, w_alpha=0.01, b_alpha=0.1):
        x = tf.reshape(self.X, shape=[-1, self.IMAGE_HEIGHT, self.IMAGE_WIDTH, 1])
        # 3 conv layer
        w_c1 = tf.Variable(w_alpha * tf.random_normal([5, 5, 1, 32]))
        b_c1 = tf.Variable(b_alpha * tf.random_normal([32]))
        conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
        conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv1 = tf.nn.dropout(conv1, self.keep_prob)

        w_c2 = tf.Variable(w_alpha * tf.random_normal([5, 5, 32, 64]))
        b_c2 = tf.Variable(b_alpha * tf.random_normal([64]))
        conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
        conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv2 = tf.nn.dropout(conv2, self.keep_prob)

        w_c3 = tf.Variable(w_alpha * tf.random_normal([5, 5, 64, 64]))
        b_c3 = tf.Variable(b_alpha * tf.random_normal([64]))
        conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
        conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv3 = tf.nn.dropout(conv3, self.keep_prob)

        # Fully connected layer
        w_d = tf.Variable(w_alpha * tf.random_normal([10 * 30 * 64, 1024]))
        b_d = tf.Variable(b_alpha * tf.random_normal([1024]))
        dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])
        dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
        dense = tf.nn.dropout(dense, self.keep_prob)

        w_out = tf.Variable(w_alpha * tf.random_normal([1024, self.MAX_CAPTCHA * self.CHAR_SET_LEN]))
        b_out = tf.Variable(b_alpha * tf.random_normal([self.MAX_CAPTCHA * self.CHAR_SET_LEN]))
        out = tf.add(tf.matmul(dense, w_out), b_out)
        return out


    # 训练
    def train_crack_captcha_cnn(self):
        output = self.crack_captcha_cnn()
        loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=self.Y))
        optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

        predict = tf.reshape(output, [-1, self.MAX_CAPTCHA, self.CHAR_SET_LEN])
        max_idx_p = tf.argmax(predict, 2)
        max_idx_l = tf.argmax(tf.reshape(self.Y, [-1, self.MAX_CAPTCHA, self.CHAR_SET_LEN]), 2)
        correct_pred = tf.equal(max_idx_p, max_idx_l)
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            step = 0
            while True:
                batch_x, batch_y = self.get_next_batch(64)
                _, loss_ = sess.run([optimizer, loss], feed_dict={self.X: batch_x, self.Y: batch_y, self.keep_prob: 0.5})
                print(step, loss_)

                # 每100 step计算一次准确率
                if step % 100 == 0:
                    batch_x_test, batch_y_test = self.get_next_batch(100)
                    acc = sess.run(accuracy, feed_dict={self.X: batch_x_test, self.Y: batch_y_test, self.keep_prob: 1.})
                    print(step, acc)
                    # 如果准确率大于50%,保存模型,完成训练
                    if acc > 0.99:
                        saver.save(sess, "./crack_capcha.model", global_step=step)
                        break

                step += 1


    #训练完成后#掉train_crack_captcha_cnn()，取消下面的注释，开始预测，注意更改预测集目录
    def crack_captcha(self):
        output = self.crack_captcha_cnn()
        correctTimes = 0
        saver = tf.train.Saver()
        with tf.Session() as sess:
            saver.restore(sess, tf.train.latest_checkpoint('.'))
            n = 1
            while n <= len(self.all_image):
                text, image = self.get_name_and_image()
                image = 1 * (image.flatten())
                predict = tf.argmax(tf.reshape(output, [-1, self.MAX_CAPTCHA, self.CHAR_SET_LEN]), 2)
                text_list = sess.run(predict, feed_dict={self.X: [image], self.keep_prob: 1})
                vec = text_list[0].tolist()
                predict_text = self.vec2name(vec)
                print("Correct: {}  Predict: {}".format(text, predict_text))
                if text == predict_text:
                    correctTimes += 1
                n += 1

        print(str(correctTimes) + '/' + str(len(self.all_image)))


if __name__ == '__main__':
    CNN = cnn()
    CNN.get_all_images()
    # CNN.train_crack_captcha_cnn()
    CNN.crack_captcha()
