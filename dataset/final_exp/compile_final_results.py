import os


def get_acc(file):
    value = ""
    f = open(file, 'r')
    f.readline()
    readings = f.readlines()
    for reading in readings:
        reading.rstrip()
        value = str(reading.split(",")).split("_")[1].replace("\\n']", "")
    f.close()
    # print(values)
    return value


def compile_per_dataset(file_list):
    # filename is constructed from : programs/github/course_repos/FP-690N/dataset/experiments/history_gru_3.csv
    f = open("results.csv", 'w')
    lines_to_write = []
    for process in file_list:
        base_filename = str(str(process[0]).split("/")[-1].split("_")[2]).split(".")[0]
        print(base_filename)
        gru_acc = 3
        lstm_acc = 3
        simple_acc = 3
        for file in process:
            if 'gru' in file:
                gru_acc = get_acc(file)
            if 'lstm' in file:
                lstm_acc = 3
                lstm_acc = get_acc(file)
            if 'simple' in file:
                simple_acc = 3
                simple_acc = get_acc(file)

        lines_to_write = str(base_filename) + "," + str(simple_acc) + "," + str(gru_acc) + "," + str(lstm_acc)
        print(lines_to_write)
        f.write(lines_to_write)
        f.write("\n")


def compile():
    file_list = os.listdir(os.getcwd())
    files_to_process = []
    for i in range(3, 21):
        count = 0
        dataset_i = []
        for file in file_list:
            if (count == 3):
                break
            if file.endswith("_" + str(i) + ".csv"):
                if file.startswith("test"):
                    count += 1
                    dataset_i.append(os.getcwd() + "/" + file)
        files_to_process.append(dataset_i)

    compile_per_dataset(files_to_process)


if __name__ == '__main__':
    compile()
