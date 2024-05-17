import re
import tkinter as tk
from chatbot_gui import ChatbotGUI
import pandas as pd

df = pd.read_csv('finaldatatoprocess.csv', index_col='product_id')

df['Scores'].fillna(0, inplace=True)

def filter_products(keyword):
    return df[df['Title'].str.contains(keyword, case=False) == False]

def find_best_phones_under_price(max_price):
    relevant_products = df[df['Price'] <= max_price].sort_values(by='Scores', ascending=False).head(5)
    return relevant_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings', 'Answered Qs']]

def find_best_phone_most_answered():
    return df[df['Answered Qs'] == df['Answered Qs'].max()]

def find_best_phones_greatest_responses():
    return df[df['Num of Ratings'] == df['Num of Ratings'].max()]

def find_phones_by_rating(min_rating):
    return df[df['Scores'] >= min_rating].sort_values(by='Scores', ascending=False)

def find_phones_by_brand(brand):
    return df[df['Brand'].str.lower() == brand.lower()]

def find_phone_with_most_responses():
    return df[df['Num of Ratings'] == df['Num of Ratings'].max()]

def exclude_phones_from_brand(brand):
    return df[df['Brand'].str.lower() != brand.lower()]

def find_highest_rated_phones():
    return df[df['Scores'] == df['Scores'].max()]

def find_best_phones():
    return df.sort_values(by='Scores', ascending=False).head(5)

def handle_greeting(query):
    greetings = ['hi', 'hello', "what's up"]
    if any(greeting in query.lower() for greeting in greetings):
        return "Hi! I hope you are doing well."
    else:
        return None

def handle_query(query):
    greeting_response = handle_greeting(query)
    if greeting_response:
        return greeting_response

    if re.search(r'(best phones under|\bphones under\b|\bphones below\b|\bbest\b).*\$(\d+)', query, re.IGNORECASE):
        max_price_match = re.search(r'\b(\d+)', query)
        print("Extracted max_price:", max_price_match.group(1) if max_price_match else None)
        if max_price_match:
            max_price = int(max_price_match.group(1))
            relevant_products = find_best_phones_under_price(max_price)
            return f"Phones below ${max_price}:\n{relevant_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)}"
    elif re.search(r'phones (above|over) \$(\d+)', query, re.IGNORECASE):
        min_price_match = re.search(r'\b(\d+)', query)
        print("Extracted min_price:", min_price_match.group(1) if min_price_match else None)
        if min_price_match:
            min_price = int(min_price_match.group(1))
            above_price_products = df[df['Price'] > min_price]
            return f"Phones above ${min_price}:\n{above_price_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)}"
    elif re.search(r'phones (between|from) \$(\d+) and \$(\d+)', query, re.IGNORECASE):
        price_match = re.search(r'\b(\d+)\b.*\b(\d+)\b', query)
        print("Extracted prices:", price_match.groups() if price_match else None)
        if price_match:
            min_price, max_price = map(int, price_match.groups())
            between_price_products = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)]
            return f"Phones between ${min_price} and ${max_price}:\n{between_price_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)}"

    elif 'most answered' in query.lower():
        most_answered_product = find_best_phone_most_answered()
        return most_answered_product[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif 'greatest responses' in query.lower():
        greatest_responses_products = find_best_phones_greatest_responses()
        return greatest_responses_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif re.search(r'rating(s)? (above|over) (\d+(\.\d+)?)', query, re.IGNORECASE):
        min_rating = float(re.search(r'rating(s)? (above|over) (\d+(\.\d+)?)', query, re.IGNORECASE).group(3))
        rating_based_products = find_phones_by_rating(min_rating)
        return rating_based_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif re.search(r'phones from (\w+)', query, re.IGNORECASE):
        brand = re.search(r'phones from (\w+)', query, re.IGNORECASE).group(1)
        brand_specific_products = find_phones_by_brand(brand)
        return brand_specific_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif 'greatest number of responses' in query.lower():
        greatest_responses_product = find_phone_with_most_responses()
        return greatest_responses_product[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif re.search(r'phones not from (\w+)', query, re.IGNORECASE):
        brand_to_exclude = re.search(r'phones not from (\w+)', query, re.IGNORECASE).group(1)
        phones_not_from_brand = exclude_phones_from_brand(brand_to_exclude)
        return phones_not_from_brand[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif 'highest rated phones' in query.lower():
        highest_rated_phones = find_highest_rated_phones()
        return highest_rated_phones[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif re.search(r'top 5 phones of (\w+)', query, re.IGNORECASE):
        top_brand_match = re.search(r'top 5 phones of (\w+)', query, re.IGNORECASE)
        if top_brand_match:
            brand_name = top_brand_match.group(1)
            top_brand_products = find_phones_by_brand(brand_name).head(5)
            return f"Top 5 phones of {brand_name}:\n{top_brand_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)}"
    elif re.search(r'\b(\w+)\b', query, re.IGNORECASE):
        search_word = re.search(r'\b(\w+)\b', query, re.IGNORECASE).group(1)
        matching_products = df[
            df.apply(lambda row: any(search_word.lower() in str(cell).lower() for cell in row), axis=1)]
        return matching_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif 'best phones' in query.lower():
        best_phones = find_best_phones()
        return best_phones[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif re.search(r'\bnot include\b (\w+)', query, re.IGNORECASE):
        keyword = re.search(r'\bnot include\b (\w+)', query, re.IGNORECASE)
        if keyword:
            keyword = keyword.group(1)
            filtered_products = filter_products(keyword)
            return filtered_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    elif re.search(r'phones under \$([\d,]+).*brand (\w+).*rating (above|over) (\d+(\.\d+)?)', query, re.IGNORECASE):
        match = re.search(r'phones under \$([\d,]+).*brand (\w+).*rating (above|over) (\d+(\.\d+)?)', query,
                          re.IGNORECASE)
        if match:
            max_price = int(match.group(1).replace(',', ''))
            brand_name = match.group(2)
            min_rating = float(match.group(4))

            filtered_products = df[(df['Price'] <= max_price) & (df['Brand'].str.lower() == brand_name.lower()) & (
                        df['Scores'] > min_rating)]
            return f"Phones under ${max_price}, brand {brand_name}, rating above {min_rating}:\n{filtered_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)}"
    elif re.search(r'\b(\w+)\b', query, re.IGNORECASE):
        search_word = re.search(r'\b(\w+)\b', query, re.IGNORECASE).group(1)
        matching_products = df[
            df.apply(lambda row: any(search_word.lower() in str(cell).lower() for cell in row), axis=1)]
        return matching_products[['Title', 'Brand', 'Price', 'Scores', 'Num of Ratings']].to_string(index=False)
    else:
        return "I'm sorry, I couldn't understand your query."


if __name__ == "__main__":
    root = tk.Tk()

    chatbot_gui = ChatbotGUI(root, handle_query)

    root.mainloop()
