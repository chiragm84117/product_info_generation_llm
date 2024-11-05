import streamlit as st
import cv2
import numpy as np
import os
import pyimgur
from serpapi import GoogleSearch
from api_access_key import imgur_CLIENT_ID,lens_api_key
from call_llm_file import call_llm


def save_uploaded_file(uploaded_image):
    try:
        with open(os.path.join('uploads', uploaded_image.name), 'wb') as f:
            f.write(uploaded_image.getbuffer())
        return True
    except:
        return False



def generated_text_box(information_graph, count):
    text,name = call_llm(data = information_graph,count = count)
    # here the llm model will be called to generate the text from the data can from the google lens
    st.text_area(label="Generating", value=text, placeholder="This might take the moment.........", disabled=True,
                 height=200)
    st.write(f'The generated text have {len(text)} characters')
    return text,name


def upload(name):
    CLIENT_ID = imgur_CLIENT_ID
    folder_path = r'C:\code\inventory_product_desc\uploads'
    file_path = name
    PATH = os.path.join(folder_path, file_path)
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH)
    link = uploaded_image.link
    print(link)
    return link

links = []
def call_lens_api(link):
    params = {
        "engine": "google_lens",
        "hl":"en",
        "country" : "in",
        "url": link,
        "api_key": lens_api_key
    }
    search = GoogleSearch(params)
    results = search.get_json()
    # for checking if both are present in json or not
    # print(results)

    visual_matches_exist = 'visual_matches' in results
    text_results_exist = 'text_results' in results
    knowledge_exist = 'knowledge_graph' in results
    related_content_exist ='related_content' in results

    information_graph = []


    if related_content_exist:
        for item in results['related_content']:
            content = item['query']
            information_graph.append(content)

    if knowledge_exist:
        for item in results['knowledge_graph']:
            # Append title and subtitle if needed
            information_graph.append(item.get('title', ''))
            information_graph.append(item.get('subtitle', ''))



        for knowledge_entry in results.get("knowledge_graph", []):
            # Check if "shopping_results" key is available in the current entry
            if "shopping_results" in knowledge_entry:
                # Access shopping_results for the current entry
                shopping_results = knowledge_entry["shopping_results"]
                # Iterate through shopping results
                for shopping_result in shopping_results:
                    price = shopping_result.get("price", "")
                    information_graph.append('price of the product = ' + price)
                    snippet = shopping_result.get("snippet", "")
                    information_graph.append(snippet)

    if text_results_exist:
        text_result = ' '.join(item['text'] for item in results.get('text_results', []))
        information_graph.append(text_result)

    cnt = 0
    if visual_matches_exist:
        for item in results['visual_matches']:
            visual = item['title']
            information_graph.append(visual)
            if cnt < 6:
                image_link = item['thumbnail']
                links.append(image_link)
                cnt = cnt+1;



    print(links)
    return information_graph


def comparitor_price(prod_name):
    params = {
        "engine": "google_shopping",
        "q": prod_name,  # Use prod_name to dynamically set the product name
        "api_key": lens_api_key,
        "gl" : "in"
    }

    # Perform the search
    search = GoogleSearch(params)
    results = search.get_dict()

    # Check if "shopping_results" is in results to avoid errors
    shopping_results = results.get("shopping_results", [])

    # Prepare a list to store the price and source of each product
    product_details = []

    # Loop through the first 5 products and collect their price and source
    for product in shopping_results[:5]:
        price = product.get('price', 'Price not available')
        source = product.get('source', 'Source not available')
        product_details.append({"price": price, "source": source})

    return product_details


# Streamlit front end
def display_product_comparison(prod_name):
    st.title("Product Price Comparator")

    if st.button("Compare Prices"):
        # Fetch product details
        products = comparitor_price(prod_name)

        # Display results
        st.subheader("Top 5 Products")
        for i, product in enumerate(products, 1):
            st.write(f"**{i}. Source:** {product['source']}")
            st.write(f"**Price:** {product['price']}")
            st.write("---")


# print the title on the UI
st.set_page_config(page_title="inventory product", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; color: white'>INVENTORY DESCRIPTION GENERATOR</h1>", unsafe_allow_html=True)


# taking the image here
col3, col4, col5 = st.columns((0.25, 0.50, 0.25))
with col3:
    st.write("")
with col4:
    picture = st.camera_input("Take the product image")
with col5:
    st.write("")


# uploaded image processing
if picture is not None:
    # taking the imput of the image
    bytes_data = picture.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # saving the image to local
    save_uploaded_file(picture)

    # upload the image to ingur
    link = upload(picture.name)

    # call the google lens API
    information_graph = call_lens_api(link)


    # print the upload picture
    col1, col2 = st.columns((1, 4), gap="small")

    with col1:
        st.header('Product')
        st.write("Sending the information !!")
        st.image(picture, width=200)

    # output text box of generated text
    with col2:
        count = 1
        st.header("Description :")
        text1,name = generated_text_box(information_graph,count)
        count = count + 1
        next_decs1 = st.button(label="generate other")
        if next_decs1 == True:
            text2,name = generated_text_box(information_graph,count)
            count = count + 1

        columns_per_row=3
        for i in range(0, len(links), columns_per_row):
            cols = st.columns(columns_per_row)
            for j, image in enumerate(links[i:i + columns_per_row]):
                cols[j].image(image)


        # price fixing
        st.header("Price Fixation")
        purchase_price = st.number_input("Enter Purchase Price", min_value=0.0, format="%.2f")
        selling_price = st.number_input("Enter Selling Price", min_value=0.0, format="%.2f")

        # Calculate net profit
        if purchase_price and selling_price:
            net_profit = selling_price - purchase_price
            st.write(f"Net Profit: ₹{net_profit:.2f}")

        #compare the other website prices
        prod_name = name
        display_product_comparison(prod_name)





