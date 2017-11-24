# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

def main(path):
    lists = []
    with open(path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line not in lists:
                lists.append(line)

    print len(lists)

    with open(path, 'w') as file:
        file.write('\n'.join(lists))

if __name__ == '__main__':
    main('resource/stop_words.txt')
