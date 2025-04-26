import tiktoken

enocder =  tiktoken.encoding_for_model("gpt-4o")

# vocab size
print(enocder.n_vocab)

text = "The people sat on the floor"
text1 = "India is the best."
tokens = enocder.encode(text)
tokens1 = enocder.encode(text1)

print(tokens)
print(tokens1)

encodedText = [976, 1665, 10139, 402, 290, 8350]
decode = enocder.decode(encodedText)

print(decode)

