with open('test/headers/full100_150k.txt') as f:
  for h in f:
    print(h[:160])
