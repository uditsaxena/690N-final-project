import os

import matplotlib.pyplot as plt

fig_num = 1


def read_file(read_index, file):
    values = []
    f = open(file, 'r')
    f.readline()
    readings = f.readlines()
    for reading in readings:
        # print(reading)
        reading.rstrip()
        values.append(reading.split(",")[read_index])

    f.close()
    # print(values)
    return values


def plot_per_dataset(file_list):
    global fig_num
    # filename is constructed from : programs/github/course_repos/FP-690N/dataset/experiments/history_gru_3.csv
    print(file_list)
    base_filename = str(str(file_list[0]).split("/")[-1].split("_")[5]).split(".")[0]
    print(base_filename)
    x = [i for i in range(1, 101)]
    for i in range(1, 3):
        plt.figure(fig_num)
        plt.xlabel("Epochs")
        if (i == 1):
            plt.ylabel("Accuracy")
            filename = base_filename + "_accuracy"
        else:
            plt.ylabel("Loss")
            filename = base_filename + "_loss"
        for file in file_list:
            y = read_file(i, file)
            label = str(file.split("_")[4]).upper()
            # print(file, label)
            # print(len(x), len(y))
            # print("x: ", x)
            # print("y: ", y)
            plt.plot(x, y, '-', label=label)
            # read_file(1)
            # read_file(2)
        plt.legend(loc=0)
        plt.savefig(filename + ".png")
        fig_num += 1


def plot(subdir):
    file_list = os.listdir(os.getcwd()+"/"+subdir)
    files_to_process = []
    for i in range(1, 21):
        count = 0
        dataset_i = []
        for file in file_list:
            # if (count == 3):
            #     break
            if file.endswith("_" + str(i) + ".csv"):
                if file.startswith("__basic_history"):
                    count += 1
                    dataset_i.append(os.getcwd() + "/" + subdir + "/" + file)
        files_to_process.append(dataset_i)

    for process in files_to_process:
        plot_per_dataset(process)


if __name__ == '__main__':
    # plot("rnn")
    # plot("memn2n/_Pret")
    plot("memn2n/_Basic")
