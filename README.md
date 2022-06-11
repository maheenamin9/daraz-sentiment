# Sentiment analysis of product reviews posted on daraz website using neural networks


## 1. **Data Scraping** <br>
Data scraping refers to the extraction of data from a website. Firstly, scrapping of the reviews from the category named "Men’s Fashion" from Daraz website is carried out. Scraping is done using python’s library named beautifulsoup. The total collected reviews are 5k after scraping.

## 2. **Data Labeling** <br>
In the next step, reviews are labeled as 1(positive) and 0(negative) according to nature of review.

## 3. **Data Preprocessing/ Cleaning** <br>
Data cleaning and transformation are methods used to remove outliers and standardize the data so that they take a form that can be easily used to create a model. Following preprocessing techniques are carried out:
   * Make reviews lower case
   * Remove punctuation
   * Remove emojis
   * Delete stop words
   * Perform lemmatization using Spacy
   * Convert our data into bag of word using CountVectorizer
   * Remove duplications in reviews
   
## 4. **Visualization of data statistics** <br>
After preprocessing, 4644 reviews were left. 3411 reviews are labeled as 1(postive) while 1233 reviews are labeled as 0(negative). These statistics are shown in [pie chart](https://github.com/maheenamin9/daraz-sentiment/blob/master/images/pie_chart.png) and [bar graph](https://github.com/maheenamin9/daraz-sentiment/blob/master/images/bar_graph.png).

## 5. **Data transformation**
The cleaned dataset is converted into bag of words. Finally, data is splited into 80% training and 20% testing sets for model’s training and testing purposes.

## 6. **Model’s Overview**
The model implemeted is neural networks. Neural network is a network or circuit of neurons.
   * It has 3 dense layers. First layer contains 100 neurons, second contains 10 neurons and last third layer contains 1 neuron.
   * Output layer has sigmoid activation function.
   * Adam optimizer with 0.001 learning rate is used.
   * Model is trained for 10 epochs.

The architecture of neural network is shown in [figure](https://github.com/maheenamin9/daraz-sentiment/blob/master/images/model's%20summary.png).

## 7. **Evaluation**
The accuracy of neural networks on test/unseen data is 95%.
