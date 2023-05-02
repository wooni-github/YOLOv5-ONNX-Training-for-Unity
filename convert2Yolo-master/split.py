# -*-coding:utf-8-*-

import os
import random
import shutil
import argparse

parser = argparse.ArgumentParser(description='label Converting example.')
parser.add_argument('--img_path', type=str, help='directory of image folder')
parser.add_argument('--img_type', type=str, help='type of image')
parser.add_argument('--split_int', type=int, default=3, help='split every *k* th images as validation image')
parser.add_argument('--random', type=bool, default=False, help='shuffle images')
args = parser.parse_args()

def main(config):
    # Specify the directory to search
    directory = config['img_path']

    # Specify the file extension to search for
    file_extension = config['img_type']

    file_list = []

    for filename in os.listdir(directory):
        if filename.endswith(file_extension):
            file_list.append(os.path.join(directory, filename))

    k = config['split_int']
    if config['random']:
        random.shuffle(file_list)

    valid_sublist = []
    train_sublist = []

    for i, filename in enumerate(os.listdir(directory)):
        if filename.endswith(file_extension):
            if i % k == 0:
                valid_sublist.append(os.path.join(directory, filename))
            else:
                train_sublist.append(os.path.join(directory, filename))

    # create folders
    train_directory = directory + '/train/'
    valid_directory = directory + '/valid/'
    if not os.path.exists(train_directory):
        os.makedirs(train_directory)
    if not os.path.exists(valid_directory):
        os.makedirs(valid_directory)

    # movel files to subfolders
    print('Moving files...')
    for file_path in valid_sublist:
        file_name = os.path.basename(file_path)
        shutil.move(file_path, os.path.join(valid_directory, file_name))
        file_path = file_path.replace(file_extension, 'txt')
        file_name = os.path.basename(file_path)
        shutil.move(file_path, os.path.join(valid_directory, file_name))

    for file_path in train_sublist:
        file_name = os.path.basename(file_path)
        shutil.move(file_path, os.path.join(train_directory, file_name))
        file_path = file_path.replace(file_extension, 'txt')
        file_name = os.path.basename(file_path)
        shutil.move(file_path, os.path.join(train_directory, file_name))

    # Open the class.names file in read mode
    with open(directory + '/class.names', 'r') as f:
        class_names = f.read().splitlines()

    # Create a new string with each value in my_list surrounded by single quotes and separated by commas
    save_class_names = ', '.join(f"'{value}'" for value in class_names)

    # Open a new .yaml file in write mode
    with open(directory + '/dataset.yaml', 'w') as f:
        f.write('train: ../' + train_directory + '\n')
        f.write('val: ../' + valid_directory + '\n\n')

        f.write('# number of classes\n')
        f.write('nc: '+str(len(class_names)) + '\n\n')
        f.write('# class names\n')
        f.write('names: [' + save_class_names + ']\n')

    print('Data preparation complete!')

if __name__ == '__main__':

    config = {
        "img_path": args.img_path,
        "img_type": args.img_type,
        "split_int": args.split_int,
        "random":args.random
    }

    main(config)
