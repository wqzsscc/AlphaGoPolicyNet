import tensorflow as tf
import copy
import go_parser
from datetime import datetime

def main():
    t1 = datetime.now()
    basic_3layer_NN()
    t2 = datetime.now()
    print "time spent: ", t2-t1


def conv(num_games=100, epoch=50, batch_size=500,
         learning_rate=3e-4, drop_out_rate=0.2,
         conv_patch_size=6, conv_features=10):
    go_data = go_parser.parse_games(num_games=num_games, onehot=True)
    sess = tf.InteractiveSession()

    x = tf.placeholder(tf.float32, shape=[None, 361])
    y_ = tf.placeholder(tf.float32, shape=[None, 361])

    W_conv1 = weight_variable([conv_patch_size, conv_patch_size, 1, conv_features])
    b_conv1 = bias_variable([10])
    x_board = tf.reshape(x, [-1, 19, 19, 1])

    h_conv1 = tf.nn.relu(conv2d(x_board, W_conv1) + b_conv1)

    W_fc1 = weight_variable([19 * 19 * 10, 361])
    b_fc1 = bias_variable([361])

    h_pool2_flat = tf.reshape(h_conv1, [-1, 19*19*10])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    W_fc2 = weight_variable([361, 361])
    b_fc2 = bias_variable([361])

    y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess.run(tf.initialize_all_variables())

    best_accuracy = 0
    previous_epoch = 0
    while go_data.train.epochs_completed < epoch:
        batch = go_data.train.next_batch(batch_size)
        if go_data.train.epochs_completed > previous_epoch:
            previous_epoch = go_data.train.epochs_completed
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob:1.0})
            val_accuracy = accuracy.eval(feed_dict={
                x: go_data.validation.features, y_: go_data.validation.labels, keep_prob:1.0})
            print("epoch %d: training accuracy %g, validation accuracy %g" %(
                previous_epoch, train_accuracy, val_accuracy))
            if val_accuracy > best_accuracy:
                print "best accuracy"
                best_accuracy = copy.deepcopy(val_accuracy)

        train_step.run(feed_dict={
            x: batch[0], y_: batch[1], keep_prob:(1-drop_out_rate)})
    test_accuracy = accuracy.eval(feed_dict={
        x: go_data.test.features, y_: go_data.test.labels, keep_prob:1})
    print "test accuracy %f" % test_accuracy


def basic_3layer_NN(num_games='All',
                    epoch=50, batch_size=500,
                    learning_rate=1.0,
                    hidden_layer_num=361,
                    drop_out_rate=0.2):
    go_data = go_parser.parse_games(num_games=num_games, first_n_moves=2, onehot=True)
    x = tf.placeholder(tf.float32, [None, 361])

    W1 = weight_variable([361, hidden_layer_num])
    b1 = bias_variable([hidden_layer_num])
    y1 = tf.nn.relu(tf.matmul(x, W1) + b1)

    keep_prob = tf.placeholder(tf.float32)
    y_drop = tf.nn.dropout(y1, keep_prob)

    W2 = weight_variable([hidden_layer_num, 361])
    b2 = bias_variable([361])

    y = tf.nn.softmax(tf.matmul(y_drop, W2) + b2)


    y_ = tf.placeholder(tf.float32, [None, 361])

    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    sess = tf.InteractiveSession()
    sess.run(tf.initialize_all_variables())

    best_accuracy = 0
    previous_epoch = 0
    while go_data.train.epochs_completed < epoch:
        batch = go_data.train.next_batch(batch_size)
        if go_data.train.epochs_completed > previous_epoch:
            previous_epoch = go_data.train.epochs_completed
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob:1.0})
            val_accuracy = accuracy.eval(feed_dict={
                x: go_data.validation.features, y_: go_data.validation.labels, keep_prob:1.0})
            print("epoch %d: training accuracy %g, validation accuracy %g" %(
                previous_epoch, train_accuracy, val_accuracy))
            if val_accuracy > best_accuracy:
                print "best accuracy"
                best_accuracy = copy.deepcopy(val_accuracy)

        train_step.run(feed_dict={
            x: batch[0], y_: batch[1], keep_prob:(1-drop_out_rate)})
    test_accuracy = accuracy.eval(feed_dict={
        x: go_data.test.features, y_: go_data.test.labels, keep_prob:1})
    print "test accuracy %f" % test_accuracy



def basic_softmax_NN():
    go_data = go_parser.parse_games(num_games=100, onehot=True)

    x = tf.placeholder(tf.float32, [None, 361])
    W = tf.Variable(tf.zeros([361, 361]))
    b = tf.Variable(tf.zeros([361]))
    y = tf.nn.softmax(tf.matmul(x, W) + b)
    y_ = tf.placeholder(tf.float32, [None, 361])

    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    sess = tf.InteractiveSession()
    sess.run(tf.initialize_all_variables())

    best_accuracy = 0
    previous_epoch = 0

    while go_data.train.epochs_completed < 50:
        batch = go_data.train.next_batch(500)
        if go_data.train.epochs_completed > previous_epoch:
            previous_epoch = go_data.train.epochs_completed
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1]})
            val_accuracy = accuracy.eval(feed_dict={
                x: go_data.validation.features, y_: go_data.validation.labels})
            print("epoch %d: training accuracy %g, validation accuracy %g" %(
                previous_epoch, train_accuracy, val_accuracy))
            if val_accuracy > best_accuracy:
                print "best accuracy"
                best_accuracy = copy.deepcopy(val_accuracy)

        train_step.run(feed_dict={x: batch[0], y_: batch[1]})
    test_accuracy = accuracy.eval(feed_dict={
        x: go_data.test.features, y_: go_data.test.labels})
    print "test accuracy %f" %test_accuracy

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


if __name__ == '__main__':
    main()