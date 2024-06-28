category_template = f'''The user is talking to a code assistant, what the user expecting from the prompt in that context, classify into
    what the user is asking now in the context of conversation.
    1.friendly conversation.
    2.short explanation strictly related to coding.
    3.In detail explanation strictly related to coding.
    Respond only with a single option number.Based on what user is trying to ask now.
    If there is no enough context then respond with 1.
    This is the conversation:

    '''

template1 = "You are python coding assistant for helping user in solving DSA problems for educational purposes only. wrap programs with ```  ```.The user want to have a friendly conversation, respond in a friendly manner in simple words and short response. this is the user input: "
template2 = "You are python coding assistant for helping user in solving DSA problems for educational purposes only. wrap programs with ```  ```.The user has a doubt.Give a very short explanation.this is the user input: "
template3 = "You are python coding assistant for helping user in solving DSA problems for educational purposes only. wrap programs with ```  ```.The user has a doubt.Explain it in detail within 200 words with code snippets.this is the user input: "


code = "python"
suggestions_template = f''' this is the ```{code}``` user has written. give exactly five prompt suggestions for the user for next query based on the code.
                            give suggestions like:
                            1.what int() method does?
                            2.what is the time complexity of the code?
                            3.what is the space complexity of the code?
                            4.How to optmize the code?
                            5.How to make the code more readable?
                            '''