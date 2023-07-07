from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# Two lists of sentences
questions1 = ['Передо мной сейчас красная кошка?', 'Погода сейчас ясная?', 'Какая погода?', 'Сколько месяцев в году?',
              'Лето длится три месяца?', 'Сколько длится лето?', 'Где красная кошка?']

embeddings1 = model.encode(questions1)

my_question = "GTA"  # input('Задай вопрос:')

embeddings2 = model.encode(my_question)

cosine_scores = util.cos_sim(embeddings1, [model.encode(my_question)])

print(cosine_scores)
qq = 0
sentence_combinations = []
for i in range(0, len(cosine_scores)):
    sentence_combinations.append([i, cosine_scores[i]])

sorted_combinations = sorted(sentence_combinations, key=lambda x: x[1], reverse=True)

for el in sorted_combinations:
    print(questions1[el[0]])

if sorted_combinations[0][1] <= 0.5:
    print("\n\n\nСейчас мы свяжем вас с оператором!")
else:
    print('\n', questions1[sorted_combinations[0][0]])