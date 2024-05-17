from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('finaldatatoprocess.csv')

@app.route('/')
def index():
    return render_template('templates.html', total_listings=len(df), average_price=df['Price'].mean(),
                           average_ratings=df['Scores'].mean(), average_review_count=df['Num of Ratings'].mean(),
                           total_questions=df['Answered Qs'].sum(), top_products=get_top_products('Scores'),
                           average_review=df['Num of Ratings'].mean(),
                           total_questions_asked=df['Answered Qs'].sum())


def get_top_products(criteria):
    return df.sort_values(by=criteria, ascending=False).head(5)

if __name__ == '__main__':
    app.run(debug=True)
