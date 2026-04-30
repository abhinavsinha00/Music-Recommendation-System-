import streamlit as st
import pickle

df = pickle.load(open("song_df.pkl","rb"))
similarity= pickle.load(open("similarity.pkl","rb"))

st.title("🎵 Bollywood Music Recommender")

song_list = df['song_name'].str.strip().tolist()
user_input = st.selectbox("Search a song:", sorted(song_list))

def recommend(song):
    song = song.strip().lower()

    try:
        index = df[df['song_name'].str.strip().str.lower() == song].index[0]
    except Exception as e:
        st.error(f"Error: {e}")  # ← sirf yeh line badlo
        return []
    distance = similarity[index]
    song_list = sorted(list(enumerate(distance)),
                        reverse = True,key = lambda x:x[1])[1:6]
    rec = []

    for i, score in song_list:
        rec.append({
            "song":df.iloc[i]["song_name"],
            "artist" :df.iloc[i]["artist"],
            "thumbnail": df.iloc[i]["thumbnail"] if "thumbnail" in df.columns else None
        })
    return rec    



if st.button("Recommend"):
    try:
        
        idx = df[df["song_name"].str.lower()== user_input.lower()].index[0]
        st.subheader("you search for:")
        col1,col2 = st.columns([1,3])

        with col1:
            if "thumbnail" in df.columns:
                st.image(df.iloc[idx]["thumbnail"],width=120)
        with col2:
            st.write("**song:**",df.iloc[idx]['song_name'])
            st.write("**artist:**",df.iloc[idx]['artist'])
    except Exception:
        st.error("Song not found.")
        st.stop()

    st.subheader("Recommend song ")
    result = recommend(user_input)

    for item in result:
        col1,col2= st.columns([1,3])
        with col1:
            if item["thumbnail"]:
                st.image(item["thumbnail"],width=120)
        with col2:
            st.write("**" + item["song"] + "**")
            st.write(item["artist"])        

