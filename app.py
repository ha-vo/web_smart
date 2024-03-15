import pickle
import streamlit as st

rating_with_book = pickle.load(open("rating_with_book.pkl","rb"))
matrix_similar = pickle.load(open("matrix_similar.pkl","rb"))
embed = pickle.load(open("embeding.pkl","rb"))

st.title("The Book Recommendation System")
def recommend(name):
    try:
        i = rating_with_book[rating_with_book['title'].str.contains(name, case=False, na=False)].iloc[0]['id']
    except:
        try:
            i = rating_with_book[rating_with_book['author'].str.contains(name, case=False, na=False)].iloc[0]['id']
        except:
            try:
                i = rating_with_book[rating_with_book['publisher'].str.contains(name, case=False, na=False)].iloc[0]['id']
            except:
                i = -1
    if i != -1:
        distance = sorted(list(enumerate(matrix_similar[i])), reverse=True ,key=lambda embed:embed[1])
        recommend = []
        url_links = []
        for j in range(6):
            recommend.append(rating_with_book[rating_with_book['id'] == distance[j][0]]['title'].values[0])
            url_links.append(rating_with_book[rating_with_book['id'] == distance[j][0]]['img_url'].values[0])
        return url_links, recommend
    else:
        return ["Your key doesn't match with our dataset"],[]
    
titles = []
url_links = []
for i in range(6):
    titles.append(rating_with_book['title'][i])
    url_links.append(rating_with_book['img_url'][i])
search_query = st.text_input("Input the name, author, publisher of the book")
if search_query:
    links_temp, titles_temp = recommend(search_query)
    if len(titles_temp) > 0:
        filtered_links, filtered_titles = links_temp, titles_temp
    else:
        st.error(links_temp[0])
        filtered_links, filtered_titles = [],[]
    print()
else:
    filtered_links, filtered_titles = url_links, titles

if len(filtered_links) == 6:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(filtered_titles[0])
        st.image(filtered_links[0])

    with col2:
        st.text(filtered_titles[1])
        st.image(filtered_links[1])
    with col3:
        st.text(filtered_titles[2])
        st.image(filtered_links[2])   

    col4, col5, col6 = st.columns(3) 
    with col4:
        st.text(filtered_titles[3])
        st.image(filtered_links[3])

    with col5:
        st.text(filtered_titles[4])
        st.image(filtered_links[4])
    with col6:
        st.text(filtered_titles[5])
        st.image(filtered_links[5])


