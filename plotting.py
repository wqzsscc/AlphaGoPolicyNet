# python libraries
import numpy as np
import tensorflow as tf
import pickle
import pandas as pd
import matplotlib.pyplot as plt

#my scripts
import go_parser as gp
import DNN_go_tensorflow as dnn_go
import visualization as vz


COLUMNS = [chr(ord('a') + i) for i in range(19)]
ROWS = [chr(ord('a') + i) for i in range(19)]

def main():
    dropout_or_not()


def dropout_or_not():
    go_data = gp.parse_games(num_games=300, first_n_moves=10, onehot=True)
    x = [0.0, .2, 0.5, 0.8]
    train_accu = []
    test_accu = []
    time = []
    for rate in [0.0, .2, 0.5, 0.8]:
        train_accuracy, test_accuracy, training_time = dnn_go.basic_3layer_NN(
            go_data, hidden_layer_num=2000, drop_out_rate=rate)
        train_accu.append(train_accuracy)
        test_accu.append(test_accuracy)
        time.append(training_time)
    with open("generated_data/dropout_or_not.pkl", "w") as f:
        f.write(pickle.dumps([x, train_accu, test_accu, time]))

    with open("generated_data/dropout_or_not.pkl", "r") as f:
        print pickle.loads(f.read())


def plot_accuracy_scaling_with_training_example():
    # accu = {"train": [], "test": [], "epoch_time": []}
    # for n in [1000, 3000, 5000, 10000, 30000, 50000, 'All']:
    #     go_data = gp.parse_games(num_games=n, first_n_moves=10, onehot=True)
    #     train_accuracy, test_accuracy, epoch_time = dnn_go.basic_3layer_NN(go_data, hidden_layer_num=2000)
    #     accu["train"].append(train_accuracy)
    #     accu["test"].append(test_accuracy)
    #     accu["epoch_time"].append(epoch_time)
    #     print n
    #     print train_accuracy
    #     print test_accuracy
    #     print epoch_time, "seconds"
    # print accu
    with open("generated_data/first_10/sample_size_accuracy_2.pkl", "r") as f:
        accu2 = pickle.loads(f.read())
        f.close()

    with open("generated_data/first_10/sample_size_accuracy.pkl", "r") as f:
        accu1 = pickle.loads(f.read())
        f.close()
    x = accu1['x'] + [10000, 30000, 50000]
    test = accu1['test'] + accu2['test']
    train = accu1['train'] + accu2['train']
    epoch_time = accu1['epoch_time'] + accu2['epoch_time']

    plt.figure(1)
    plt.plot(x, test)
    plt.plot(x, train, "r")
    plt.xlabel("number of games as training data")
    plt.ylabel("prediction accuracy")
    plt.title("accurayc scaling with more training data")
    plt.legend(["test accuracy", "train accuracy"], loc="best")
    plt.figure(2)
    plt.plot(x, epoch_time)
    plt.xlabel("number of games as training data")
    plt.ylabel("epoch time in seconds")
    plt.title("epoch time increasing with more training data")
    plt.show()




    plt.show()


def plot_hidden_node_and_accuracy():
    accu = {"train": [], "test": []}
    go_data = gp.parse_games(num_games=10000, first_n_moves=10, onehot=True)
    for hidden_nodes in range(100, 1100, 100) + range(1500, 6500, 500):
        train_accuracy, test_accuracy = dnn_go.basic_3layer_NN(go_data, hidden_layer_num=hidden_nodes)
        accu["train"].append(train_accuracy)
        accu["test"].append(test_accuracy)
        print hidden_nodes
        print train_accuracy
        print test_accuracy
    print accu
    with open("generated_data/first_10/hidden_nodes_accuracy.pkl", "w") as f:
        f.write(pickle.dumps(accu))

    with open("generated_data/first_10/hidden_nodes_accuracy.pkl", "r") as f:
        accuracies = pickle.loads(f.read())
        f.close()

    x = range(100, 1100, 100) + range(1500, 6500, 500)

    plt.plot(x, accuracies["train"], "r")
    plt.plot(x, accuracies["test"], "g")
    legend=["train accuracy", "test accuracy"]
    plt.xlabel("number hidden nodes")
    plt.ylabel("accuracy")
    plt.title("prediction accuracy with different number of hidden nodes")
    plt.legend(legend, loc="best")
    plt.show()


def get_prediction_example():
    prob, board, move = gp.basic_3layer_NN(
        num_games=1000, first_n=10, epoch=20, move_only=True)
    print board
    print move
    print prob

    with open("generated_data/first_10/probability_10_step", "w") as f:
        f.write(pickle.dumps([prob, board, move]))
        f.close()




def draw_board_probabilities_10_step():
    with open("/Users/Molly/Desktop/CMPS218 Deep Learning/AlphaGoPolicyNet/generated_data/probability_10_step", "r") as f:
        prob, board, move = pickle.loads(f.read())
        f.close()
    board = (board * 2).astype(int)

    vz.draw_board(board, move, prob)



def plot_accuracy_decay_over_moves():
    # test_accu = {1000: [], 5000: [], 20000: []}
    # for n in [1000, 5000, 20000]:
    #     for move in range(1, 21):
    #         go_data = gp.parse_games(num_games=n, first_n_moves=move, onehot=True)
    #         dummy1, test_accuracy, dummy2 = dnn_go.basic_3layer_NN(
    #             go_data, verbose=False, hidden_layer_num=2000)
    #         test_accu[n].append(test_accuracy)
    #         print "num games = %d, moves = %d, accuracy=%f" %(n, move, test_accuracy)
    # with open("generated_data/accuracy_decay", "w") as f:
    #     f.write(pickle.dumps(test_accu))

    with open("generated_data/accuracy_decay", "r") as f:
        result = pickle.loads(f.read())
        f.close()
    legend = []
    for num_game, accuracies in result.iteritems():
        plt.plot(range(1, 21), accuracies)
        legend.append(str(num_game) + " training games")

    plt.xlabel("number of moves")
    plt.ylabel("prediction accuracy")
    plt.title("decreasing prediction accuracy with increasing board complexity")
    plt.legend(legend, loc="bestdfd")
    plt.show()


def draw_board_probabilities():
    with open("probabilitiy_of_open_game", "r") as f:
        probs = pickle.loads(f.read())
        f.close()

    open_moves =gp.map_1d_to_2d(get_open_move())
    vz.draw_openning_board([], probs['All'])

def get_open_move():
    go_data = gp.parse_games(num_games=100, first_n_moves=1)
    open_moves = go_data.train.labels
    for i in [60, 72, 288, 300]:
        print i, len(open_moves[open_moves == i])
    return open_moves

if __name__ == '__main__':
    main()