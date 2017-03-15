import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data


def trial1():
    # node1 = tf.constant(3.0, tf.float32)
    # node2 = tf.constant(4.0)  # also tf.float32 implicitly
    # print(node1, "\n", node2)
    #
    sess = tf.Session()
    # # print(sess.run([node1, node2]))
    #
    # add = tf.add(node1, node2)
    # print(add, sess.run(add))

    # a = tf.placeholder(tf.float32)
    # b = tf.placeholder(tf.float32)
    # adder = a + b
    # print(sess.run(adder, {a:[1,2.0], b:[2.0,3]}))
    W = tf.Variable([.3], tf.float32)
    b = tf.Variable([-.3], tf.float32)
    x = tf.placeholder(tf.float32)
    linear_model = W * x + b

    y = tf.placeholder(tf.float32)
    square_delta = tf.square(linear_model - y)
    loss = tf.reduce_sum(square_delta)
    init = tf.initialize_all_variables()
    sess.run(init)
    # fixW = tf.assign(W, [-1.])
    # fixb = tf.assign(b, [1.])
    # sess.run([fixW, fixb])

    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = optimizer.minimize(loss)
    sess.run(init)  # reset values to incorrect defaults.
    for i in range(1000):
        sess.run(train, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]})
        if (i % 100 == 0):
            print(sess.run([W, b]))


            # print(sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))
            # print(W)
            # print(b)
            # print(x)
            # print(linear_model)
            # print(sess.run(linear_model, {x: [1, 2, 3, 4]}))


def mnist_for_beginners():
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    x = tf.placeholder(tf.float32, [None, 784])

    # W = tf.Variable(tf.float32, [784,10])
    # b = tf.Variable(tf.float32, [10])

    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

    y = tf.nn.softmax(tf.matmul(x, W) + b)
    # y = tf.nn.softmax((x * W) + b)
    # y_exp = tf.nn.softmax(tf.matmul(W, x) + b)
    y_ = tf.placeholder(tf.float32, [None, 10])
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

    train = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.Session()

    init = tf.initialize_all_variables()
    sess.run(init)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    for i in range(1000):
        x_s, y_s = mnist.train.next_batch(100)
        sess.run(train, feed_dict={x: x_s, y_: y_s})
        # if (i % 100 == 0):
        #     print(sess.run(cross_entropy))

    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))


if __name__ == '__main__':
    # trial1()
    mnist_for_beginners()
    # deep_mnist()