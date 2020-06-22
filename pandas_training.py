import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#tutorial: https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html

#create a series by passing a list of values, using a default integer index
s = pd.Series([1, 3, 5, np.nan, 6, 8])

#use dates to index a data frame that has been created with a numpy array
dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns = list('ABCD'))

#creating a data frame by passing a dict of objects
#seems like if you give it a scalar, it knows to repeat that over and over
df2 = pd.DataFrame({'A': 1.,
                    'B': pd.Timestamp('20130102'),
                    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D': np.array([3] * 4, dtype='int32'),
                    'E': pd.Categorical(["test", "train", "test", "train"]),
                    'F': 'foo'})

#to view the top and bottom rows:
df.head()
df.tail()

#to view the index:
df.index

#to view the columns:
df.columns

#to see quick statistics:
df.describe()

#to transpose:
df.T

#sorting...
#by axis:
df.sort_index(axis=1, ascending=False)
df.sort_values(by='B')

#selecting...
#use column name to select
df['A']

#a selection of certain rows
df[0:3]
df['20130102':'20130104']

#you can get all information that corresponds to a particular label
df.loc[dates[0]]

#or all data in some columns:
df.loc[:, ['A', 'B']]

#combining the above, notice that both endpoints are included:
df.loc['20130102':'20130104', ['A', 'B']]

#using a column's values to select data
df[df['A']>0]

#copying/adding
df3 = df.copy()
df3['E'] = ['one', 'one', 'two', 'three', 'four', 'three']
df3
df3[df3['E'].isin(['two', 'four'])]

#IMDB example: https://medium.com/datactw/imdb-dataset-visualization-data-analytics-using-pandas-97b5c6f03c6d

imdb_1000_data_url = r'imdb_1000.csv'
movies = pd.read_csv(imdb_1000_data_url)
#the head:
movies.head()
#the shape and data type:
movies.shape
movies.dtypes

#plotting and analytics
#movies.duration.plot(kind='hist')
#movies[['content_rating', 'title']].groupby('content_rating').count().plot(kind='bar', title='Content Rating')
#plt.xlabel('Content Rating')
#plt.ylabel('Title Count')
#plt.show()

print('Avg. star rating for movies 2 hours or longer: ', movies[movies['duration'] >= 120]['star_rating'].mean(),
      '\nAvg. star rating for movies shorter than 2 hours: ', movies[movies['duration'] < 120]['star_rating'].mean())

# calculate the average duration for each genre
movies[['duration','genre']].groupby('genre').mean()

# calculate the average star rating for each genre, but only include genres with at least 10 movies
genres = movies['genre'].value_counts()[movies['genre'].value_counts() > 10].index
print('the mean rating of genres with 10 or more movies are\n', movies[movies['genre'].isin(genres)].groupby('genre')['star_rating'].mean())