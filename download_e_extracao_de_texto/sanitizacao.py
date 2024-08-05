import pickle
import pandas as pd

def load_pickle(path):
  with open(path, 'rb') as handle:
    data = pickle.load(handle)
  return data

def save_data_to_pickle(data, path):
  with open (path, 'wb') as file:
    pickle.dump(data, file)
    
data = load_pickle('../pickles/data.pkl')
df = pd.DataFrame(data)
df['sanitized_text'] = [text.replace('\n', ' ') for text in df['text']]
df['sanitized_text'] = [' '.join(text.lower().split()) for text in df['sanitized_text']]
df.head()
df.to_pickle('../pickles/data_sanitized.pkl')

print(df['sanitized_text'][1])