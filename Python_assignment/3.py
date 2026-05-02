# Write a Python program to count the occurrences of each word in a given sentence.

sentence = input("enter any sentence: ")
words = sentence.lower().split()
wc = {}
for word in words:
    if word in wc:
        wc[word] += 1
    else:
        wc[word] = 1
print("word count in the sentence is:")
for word, count in wc.items():
    print(f"{word}: {count}")
