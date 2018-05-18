
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[24]:


jeopardy = pd.read_csv("jeopardy.csv")


# In[25]:


jeopardy.head(5)


# In[6]:


jeopardy.columns


# In[26]:


jeopardy.columns = ['Show Number', 'Air Date', 'Round', 'Category', 'Value','Question', 'Answer']


# In[27]:


jeopardy.dtypes


# In[28]:


jeopardy['Air Date'] = pd.to_datetime(jeopardy['Air Date'])


# In[29]:


import re

def normalize_text(text):
    text = text.lower()
    text = re.sub("[^A-Za-z0-9\s]", "", text)
    return text

def normalize_values(text):
    text = re.sub("[^A-Za-z0-9\s]", "", text)
    try:
        text = int(text)
    except Exception:
        text = 0
    return text


# In[32]:


jeopardy['clean_question'] = jeopardy['Question'].apply(normalize_text)
jeopardy['clean_answer'] = jeopardy['Answer'].apply(normalize_text)
jeopardy['clean_value'] = jeopardy['Value'].apply(normalize_values)


# In[33]:


jeopardy.head(20)


# In[37]:


def count_matches(row):
    split_answer = row["clean_answer"].split(" ")
    split_question = row["clean_question"].split(" ")
    if "the" in split_answer:
        split_answer.remove("the")
    if len(split_answer) == 0:
        return 0
    match_count = 0
    for item in split_answer:
        if item in split_question:
            match_count += 1
    return match_count / len(split_answer)

jeopardy["answer_in_question"] = jeopardy.apply(count_matches, axis=1)    


# In[38]:


jeopardy['answer_in_question'].mean()


# The meaning of this is that the answer only appears in the question 6% of the time, which really is quite low. You would still have to work hard on studying relevant topics, although this knowledge could prove useful if you hear a question and have no idea what the answer is

# In[40]:


question_overlap = []
terms_used = set()
for i,row in jeopardy.iterrows():
    split_question = row['clean_question'].split(" ")
    split_question = [q for q in split_question if len(q) > 5]
    match_count = 0
    for item in split_question:
        if item in terms_used:
            match_count += 1
    for item in split_question:
            terms_used.add(item)
    if len(split_question) > 0:
        match_count /= len(split_question)
    question_overlap.append(match_count)
    
jeopardy['question_overlap'] = question_overlap
jeopardy['question_overlap'].mean()
    


# From this it appears that terms do get recycled a lot, but we are only looking at reuse of single words and would have to interrogate the contents of terms_used a bit before knowing how useful this might be. But it is probably enough to say that looking at old questions should probably be a part of your studying technique

# In[41]:


def value_counts(row):
    value = 0
    if row['clean_value'] > 800:
        value = 1
    return value

jeopardy['high_value'] = jeopardy.apply(value_counts, axis = 1)


# In[42]:


def count_use(word):
    low_count = 0
    high_count = 0
    for i, row in jeopardy.iterrows():
        split_question = row['clean_question'].split(" ")
        if word in split_question:
            if row['high_value'] == 1:
                high_count += 1
            else:
                low_count += 1
    return high_count, low_count

observed_expected = []
comparison_terms = list(terms_used)[:5]
for word in comparison_terms:
    observed_expected.append(count_use(word))
        
observed_expected


# In[43]:


high_value_count = sum(jeopardy['high_value'])
low_value_count = jeopardy.shape[0] - high_value_count
high_value_count


# In[45]:


high_value_count


# In[ ]:


from scipy.stats import chisquare

chi_squared = []
for obs in observed_expected:
    total = high_value_count + low_value_count
    total_prop = total / jeopardy.shape[0]
    high_val_rows = total_prop * high_value_count
    low_val_rows = total_prop * low_value_count
    chi_sq, pval = 

