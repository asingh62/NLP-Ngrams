'''
*************************************NGRAMS*************************************************#
............................................................................................#

Date : 10th October, 2020
This program is developed by Team 9 of AIT 590-001 section. 
The team comprises of 3 members : Prateek Chitpur, Amrita Jose and Asmita Singh.

The following code will learn an N-gram language model from an arbitrary number of plain text files and generate a given number of sentences based on that N-gram model.
It will work for any value of N, and output m sentences.

Before learning the N-gram model, we did the following steps:
1. Reading the input files.
2. Merging the files into one file.
3. Converting all text to lowercase.
4. Tokenizing the text into sentences.
5. Tokenizing the sentence tokens into words.

Once the n-gram model is built, below steps are performed
6. Building n-grams model on the tokenized words
7. Computing count of occurences of generated Ngrams
8. Building sentences from occurences of generated Ngrams

Instructions to run :

1: Use command line to run the python code.
2: Provide the python code file name, n, m, and text files as the arguments.
3: The program will generate sentences based on arguments passed(ngrams, no.of sentences).

Sample command:

time python ngram.py 1 10 pg2554.txt pg2600.txt pg1399.txt

time python ngram.py 2 10 pg2554.txt pg2600.txt pg1399.txt

time python ngram.py 3 10 pg2554.txt pg2600.txt pg1399.txt

time python ngram.py 4.10 pg2554.txt pg2600.txt pg1399.txt

References:
1. https://stackoverflow.com/questions/58848824/how-to-save-python-command-line-arguments-to-a-log-file
2. https://stackoverflow.com/questions/2513479/redirect-prints-to-log-file
3. https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
4. http://www.samansari.info/2016/01/generating-sentences-with-markov-chains.html
5. https://stackoverflow.com/questions/1150144/generating-random-sentences-from-custom-text-in-pythons-nltk
6. https://stackoverflow.com/questions/45489141/python-loop-through-multiple-text-files-extract-target-strings-and-append-the

'''

#Import libraries
import sys
import time
import re
import nltk
# nltk.download('punkt')
#import sets
import pip
#pip.main(["install","sets"])
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
from nltk.probability import FreqDist, MLEProbDist

#Log file open
old_stdout = sys.stdout
log_file = open("ngram-log.txt","w")
sys.stdout = log_file

#record the start time
starttime=time.time() 

# Initialize the system arguments
arg = sys.argv
ngrams = int(arg[1])
nsentences = int(arg[2])

#print description
print("Description : This program generates random sentences based on an Ngram model.")
print("Authors : Asmita Singh, Prateek Chitpur, and Amrita Jose")
print("Command line settings: ngram.py ",ngrams, nsentences)
print(" \n")

#validate if the length of the arguments is less than 4
if len(arg) < 4:
    print ("Insufficient parameters passed")
    sys.exit(0)
        
#declare an empty bytes variable
merged_data = b''

#loop through text files and merge the data
for files in range (3,len(arg)):
    
    #Opens the file as read-only in binary format and start reading from the file
    file = open(arg[files],"rb")
    
    #merge text file with the variable's value and assign new value to merged_data 
    merged_data += file.read()
    merged_data += b' '

#convert byte to string
merged_data = merged_data.decode(encoding='utf-8')

#convert from multiline to single line
merged_data = re.sub('\\r\\n',' ',merged_data.rstrip())

#replace multiple white spaces
merged_data = re.sub(' +', ' ',merged_data)

#convert to lowercase
merged_data = merged_data.lower()
merged_data = re.sub('[^a-zA-Z0-9 \n\.?!,]', '', merged_data)

#Text corpus is tokenized into sentences
sentence_tokens = sent_tokenize(text=merged_data)

word_tokens = []
wordtokenlist= []
#Sentence tokens obtained are tokenized into words
for sentences in sentence_tokens:
    word_tokens = word_tokenize(sentences)

#Check whether the length of the sentence is less than n, if so then discard the sentence
    if len(word_tokens) >= int(ngrams):
        for i in range(int(ngrams)-1):
            word_tokens.insert(0,"<start>")
        word_tokens.append("<end>")
        wordtokenlist.append(word_tokens)

    
#Check total number of tokens in the files is more than 1,000,000. 
wordtokenlength = 0
for token in wordtokenlist:
    wordtokenlength=wordtokenlength+len(token)
if(wordtokenlength<1000000):
    print("Word tokens are less than 1000000. Please pass text files with higher word limit.")
    sys.exit(2)

word_list = []
for single_list in wordtokenlist:
    for one_object in single_list:
        word_list.append(one_object)


# Building N-grams
ngram = ''
def gene_ngrams(word_list, ngrams):
    ngrams_list = []
    for num in range(0, len(word_list)-ngrams+1):
            ngram_pairs =()
            for i in range(num, num+ngrams):
                ngram_pairs += (word_list[i],)
            ngrams_list.append(ngram_pairs)
    return ngrams_list
final_ngrams_list = gene_ngrams(word_list, int(ngrams))

#Computing count of occurences of generated Ngrams
ngrams_frequency = Counter(final_ngrams_list)

#Building N sentences from occurences of generated Ngrams
def sentence_generator(gramFreq,numofsentences):
    i = 0
    for  i in range (numofsentences):
        sentenceGen = True
        sentencelist = ()
        generateSentence = ""
        for size in range (int(ngrams)-1):
            sentencelist += ('<start>',)   
        while sentenceGen == True:
            token_dict = {}
            for index, val in ngrams_frequency.items():
                index2 = index[:-1]
                if index2 == sentencelist:
                    token_dict.update({index[-1]: val})

            # generating frequency using the function
            frequencyDistribution = FreqDist(token_dict)

            # generating probability using the function
            probabilityDistribution = MLEProbDist(frequencyDistribution)

            # predicting the next word
            next_word = probabilityDistribution.generate()
            
            # words having ".,?,!"
            if (next_word =="." or next_word == "?" or next_word == "!"):
                sentenceGen = False
                generateSentence += next_word
                continue
            
            # words having , '
            elif (next_word == "," or next_word == "’"):
                generateSentence += next_word
                
            else:
                generateSentence += " %s"%next_word

            if len(sentencelist) != 0 :   
                my_list = list(sentencelist)
                my_list.pop(0)
                my_list.append(next_word)
                sentencelist = tuple(my_list)
        # Display sentences
        print ("\nSentence %s: %s"%(i+1,generateSentence))

sentence_generator(ngrams_frequency,int(nsentences))
print("\n")

#get filenames which are passed as arguments

f=""
for filenames in range(3,len(arg)):
    f += sys.argv[filenames] + " "

#record the end time
endtime = time.time()
executiontime = endtime-starttime

print("%s" % executiontime + " secs for executing python ngram.py " + "%s %s %s" % (ngrams, nsentences, f) + "\n")

sys.stdout = old_stdout
log_file.close()






