#!/usr/bin/env python3

## inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4

import json

class Node:
    def __init__(self, label=None, fullWord=False):
        self.label = label
        self.fullWord = fullWord
        self.children = dict()
    
    def addChild(self, key, fullWord=False):
        if not isinstance(key, Node):
            self.children[key] = Node(key, fullWord)
        else:
            self.children[key.label] = key
    
    def __getitem__(self, key):
        return self.children[key]

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word):
        current_node = self.head
        word_finished = True
        
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break
        
        # For ever new letter, create a new child node
        if not word_finished:
            while i < len(word):
                current_node.addChild(word[i])
                current_node = current_node.children[word[i]]
                i += 1

        current_node.fullWord = True
    
    def has_word(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError('Trie.has_word requires a not-Null string')
        
        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break
        
        # Still need to check if we just reached a word like 't'
        # that isn't actually a full word in our dictionary
        if exists:
            if current_node.fullWord == False:
                exists = False
        
        return exists

def getSuffixes():
    """ get the suffixes from tibetan-spellchecker """
    suffixesData = json.load(open('tibetan-spellchecker/syllables/suffixes.json'))
    print(suffixesData)
    return suffixesData

def addSyllablesFromFile(fileName, syllablesList):
    """ get all the syllables from a file """
    with open(fileName) as f:
        syllablesList += [line.strip() for line in open(fileName)]

def getSyllables():
    """ get all the syllables from tibetan-spellchecker as a list """
    fileDir = 'tibetan-spellchecker/syllables/'
    fileList = ['root.txt', 'wasurs.txt', 'rare.txt', 'exceptions.txt', 'proper-names.txt']
    syllablesList = []
    for fileName in fileList:
        addSyllablesFromFile(fileDir+fileName, syllablesList)
    return syllablesList

def addBasePlusSuffixesToTrie(syllableBase, suffixesList, trie):
    """ Add all the suffix combinations for one syllable """
    for suffix in suffixesList:
        trie.add(syllableBase+suffix)

def addSyllablesToTrie(syllablesList, suffixesData, trie):
    """ Add all the combinations of syllables + suffixes to the trie """
    for syl in syllablesList:
        # if syl ends with /A, /NB or /C, add all the corresponding suffix possiblities
        slashIdx = syl.find('/')
        if slashIdx != -1:
            addBasePlusSuffixesToTrie(syl[:slashIdx], suffixesData[syl[slashIdx+1:]], trie)
        else:
            trie.add(syl)

def getTrie():
    suffixesData = getSuffixes()
    syllablesList = getSyllables()
    trie = Trie()
    addSyllablesToTrie(syllablesList, suffixesData, trie)
    return trie

if __name__ == '__main__':
    """ Example use """
    trie = getTrie()
    words = 'མདྲོམ་བདྭག་བདྲའ་དཀ་ཁནད་པའིས་དཀའ་དཀའི་དཀར་བ་བོ་བར་བོར་བ༷'
    for word in words.split('་'):
        print("'%s' correct: %r" %(word, trie.has_word(word)))
