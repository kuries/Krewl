import json

def levenshtein_dist(word1, word2):

    word1, word2 = ' ' + word1, ' ' + word2
    total = [[0]*len(word1) for i in range(len(word2))]
    for i in range(len(word2)):
        total[i][0] = i
    for j in range(len(word1)):
        total[0][j] = j


    for i in range(1, len(word2)):
        for j in range(1, len(word1)):
            if word2[i] == word1[j]:
                total[i][j] = total[i-1][j-1]
            else:
                final = min([ total[i-1][j-1], total[i-1][j], total[i][j-1] ])
                total[i][j] = final + 1
    return total[-1][-1]

def word_check(word):
    fe = open("./storage/covid_data.json", mode='r')
    data_json = json.load(fe)['states']
    fe.close()
    store = []
    val = len(word)
    for i in data_json.keys():
        temp = len(word)
        if len(i) < len(word):
            temp_word = word[: ((len(word)-len(i))*-1) or len(word)]
            temp = levenshtein_dist(temp_word, i)
        else:
            temp_i = i[: ((len(i) - len(word)) * -1) or len(i)]
            temp = levenshtein_dist(word, temp_i)
        if val > temp:
            store = [i]
            val = temp
        elif val == temp:
            store.append(i)
    return (store, val)

if __name__ == "__main__":
    word = input("Enter: ")
    print(word_check(word))
    print(levenshtein_dist('madya', 'madhy'))