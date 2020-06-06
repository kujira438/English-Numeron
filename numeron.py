# -*- coding: utf-8 -*-
import csv
import copy
import sys
import numpy as np

class Numeron:
    def __init__(self, wl):
        self.word_length = wl
        self.candidates = self.preprocess()

    def preprocess(self):
        words = []
        candidates = []
        with open('./dictionary/'+str(self.word_length)+'char_words.csv', 'r') as f:
            contents = csv.reader(f)
            for row in contents:
                for col in row:
                    words.append(col)
        for word in words:
            if(len(set(word)) == len(word)):
                candidates.append(word)
        return candidates

    def refine(self,candidates, word, eat, bite):
        delete_list = []
        for i,candidate in enumerate(candidates):
            if(len(set(candidate+word)) != len(candidate)+len(word)-(eat+bite)):
                delete_list.append(i)
                continue
            accordance = 0
            for j in range(len(word)):
                if(word[j] == candidate[j]):
                    accordance += 1
            if(accordance != eat):
                delete_list.append(i)


        for element in delete_list[::-1]:
            candidates.pop(element)
        return candidates

    def respond(self,word, target):
        eat_bite = len(word)+len(target)-len(set(word+target))
        accordance = 0
        for i in range(len(word)):
            if(word[i] == target[i]):
                accordance += 1
        eat = accordance
        bite = eat_bite - eat
        return eat, bite

    def explore(self,candidates):
        expectation = np.zeros(len(candidates))
        for i, candidate in enumerate(candidates):
            tmp_sum = 0
            for target in candidates:
                e, b = self.respond(candidate, target)
                temporary_candidates = copy.deepcopy(candidates)
                remainder = self.refine(temporary_candidates, candidate, e, b)
                tmp_sum += len(remainder)
            expectation[i] = tmp_sum/len(candidates)
            sys.stdout.write("\rPlanning a strategy... {}/{}".format(i+1,len(candidates)))
            sys.stdout.flush()
            #print(candidate,expectation[i])
        print()
        return expectation

    def suggest(self, candidates, num = 5):
        expectation = self.explore(candidates)
        idx = np.argsort(expectation)
        ranking = np.sort(expectation)
        num = min(num, len(candidates))
        print('*** Effective attack words TOP '+str(num)+' ***')
        for i in range(num):
            print(candidates[idx[i]],ranking[i])
        print('************************************')
        return

def main():
    print('input length of words in the range of 3-10...(ex 4)')
    digit = int(input())
    nume = Numeron(digit)

    while(len(nume.candidates)>1):
        print('input '+str(nume.word_length)+' characters...(ex some)')
        input_word = input()
        while(len(input_word) != nume.word_length):
            input_word = input()
        print('input eat and bite...(ex 1 0)')
        eat, bite = list(map(int, input().split()))

        nume.candidates = nume.refine(nume.candidates, input_word, eat, bite)
        print(nume.candidates)
        nume.suggest(nume.candidates)

if __name__ == '__main__':
    main()
