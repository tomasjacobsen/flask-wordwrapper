from flask import Flask, request
import random
import textwrap
from itertools import zip_longest

app = Flask(__name__)

def generate_random_number():
    return random.randint(2,9)

def wordwrapper(string_of_words, column_number):

    #Simple method:
    #print("\n".join(textwrap.wrap(string_of_words, width=column_number)))

    #Add hyphen to broken words:
    n = column_number
    lines = string_of_words.split()

    list_of_words = []

    for s in lines:
        word_list_map = list(map(''.join, zip_longest(*[iter(s)]*n, fillvalue='')))
        
        #check if the word is broken by checking lenght of list, then apply hyphen to every item except the last in list
        if len(word_list_map) > 1:
            for index, brokenword in enumerate(word_list_map[:-1]):
                word_list_map[index] = brokenword + '-'

        #Add the single word to the list_of_words
        for word in word_list_map:
            list_of_words.append(word)

    #print('\n'.join(list_of_words))
    

    string_converted = '\n'.join(list_of_words)
    return {'string-converted': string_converted}



@app.route('/', methods=['POST'])
def json_view():

    req_data = request.get_json()

    if not req_data:
        message = "No valid JSON object found in POST request"
        app.logger.info(message)
        return {'Error': True, 'Message': message}

    if 'string-of-words' in req_data:
        string_of_words = req_data.get('string-of-words')

        if not string_of_words:
            message = "The key 'string-of-words' has no value. Unable to run function."
            app.logger.info(message)
            return {'Error': True, 'Message': message}
    else:
        message = "The key 'string-of-words' is not present in the POST request. Unable to run function."
        app.logger.info(message)
        return {'Error': True, 'Message': message}    
        
    if 'column-number' in req_data:
        column_number = req_data.get('column-number')
        
        if not column_number:
            message = "The key 'column-number' has no value, genrating a random number"
            app.logger.info(message)
            column_number = generate_random_number()
        elif not isinstance(column_number, int):
            column_number = int(column_number)
    else:
        message = "The key 'column-number' is not present in the POST request, genrating a random number"
        app.logger.info(message)
        column_number = generate_random_number()

    return wordwrapper(string_of_words,column_number)

if __name__ == '__main__':
    app.run(debug=True, port=5000)