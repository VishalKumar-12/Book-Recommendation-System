from flask import Flask, render_template,request
import pickle
import numpy as np
popular_df = pickle.load(open('popular.pk1', 'rb'))
pt = pickle.load(open('pt.pk1','rb'))
books= pickle.load(open('books.pk1','rb'))
similarity_scores =pickle.load(open('similarity_scores.pk1','rb'))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_ratings'].values)
    )

# Define the route for the recommendation page
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    def recommend(book_name):  # here book name se index fetch kran
        index = np.where(pt.index == user_input)[0][0]  # here finding index of books
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]
        # here finding simailar items books
        data = []
        for i in similar_items:
            item = []
            # print(pt.index[i[0]])
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
        return data
    data= recommend(user_input)
    return render_template('recommend.html',data=data)
# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
