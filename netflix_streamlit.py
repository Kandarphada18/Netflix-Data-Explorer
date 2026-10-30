import streamlit as st  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(
    page_title="Netflix Data Explorer",
    page_icon="🎬",
    layout="wide"
)


st.markdown("""
    <style>
    #netflix-logo {
        position: fixed;
        top: 50px;
        right: 24px;
        z-index: 999;
        font-size: 42px;
        font-weight: 900;
        color: red;
        letter-spacing: 3px;
        font-family: Arial Black, sans-serif;
    }
    </style>
    <div id="netflix-logo">NETFLIX DATA EXPLORER</div>
""", unsafe_allow_html=True)

# Load data from CSV
df=pd.read_csv("netflix_titles.csv")
print("\n===== Loaded Dataset =====")
print(df)
#hnadle missing values
print("\nMisssing Valus Summary::")
print(df.isnull().sum())
df['director'].fillna('Unknown',inplace=True)
df['cast'].fillna('Unknown',inplace=True)
#filling missing values with mode for categorical columns
categorical_cols=['director','cast','country','date_added','rating','duration','listed_in','description']
for col in categorical_cols:
  df[col].fillna(df[col].mode()[0],inplace=True)
print("\n===== Dataset after handling missing values =====")
print(df)   
#convert dataframe columns to numpy arrays
title=df["title"].to_numpy()
release_year=df["release_year"].to_numpy()
print("\n=====Numpy-Based-Analysis=====")
#descriptive statistics using numpy
st.subheader("Numpy-Based Analysis")
c1,c2,c3,c4=st.columns(4)
c1.metric(f"Total Title",f"{np.size(title):,}")
c2.metric(f"Year Range",f"{np.min(release_year)}-{np.max(release_year)}")
c3.metric(f"Average  Year",f"{np.mean(release_year):.2f}")
c4.metric(f"Std Deviation",f"{np.std(release_year):.2f}")
st.divider()
# Show table — replaces ttk.Treeview



# These replace your print("1. ...") / input() menu

show_histogram    = st.sidebar.button("📊 Release Year Histogram")   # option 1
show_bar          = st.sidebar.button("🎬 Movies vs TV Shows")        # option 2
show_country      = st.sidebar.button("🌍 Top 10 Countries")          # option 3
show_pie          = st.sidebar.button("🥧 Rating Distribution")       # option 4
show_exit_anim    = st.sidebar.button("👋 Animated Goodbye")          # option 5
st.sidebar.divider()


st.sidebar.title("Filter Table")



genres    = ["All", "Dramas", "Comedies", "Documentaries",
             "Action & Adventure", "Thrillers", "Children & Family",
             "Horror Movies", "Stand-Up Comedy", "Romantic Movies"]
years     = ["All"] + [str(y) for y in sorted(
                df["release_year"].dropna().astype(int).unique(), reverse=True)]
genre_sel = st.sidebar.selectbox("Genre", genres)       # replaces ttk.Combobox
year_sel  = st.sidebar.selectbox("Year",  years)        # replaces ttk.Combobox
type_sel  = st.sidebar.selectbox("Type",  ["All", "Movie", "TV Show"])
def reset_ax(ax, fig):
    """Same reset_ax logic — fig.clf() + fresh subplot."""
    fig.clf()
    ax = fig.add_subplot(111)
    ax.set_facecolor("#1f1f1f")
    fig.patch.set_facecolor("#141414")
    for s in ax.spines.values():
        s.set_edgecolor("#333333")
    ax.tick_params(colors="white", labelsize=8)
    return ax





def plot_release_year_histogram(release_year):
    fig=plt.figure(figsize=(10,4))
    ax = fig.add_subplot(111)
    ax=reset_ax(ax,fig)
    ax.hist(release_year,bins=30,color='skyblue',edgecolor='black')
    ax.set_title('Distribution of Release Year', color='white', fontsize=12)
    ax.set_xlabel('Release Year', color='#aaaaaa', fontsize=9)
    ax.set_ylabel('Number of Titles', color='#aaaaaa', fontsize=9)
    fig.tight_layout()
    st.pyplot(fig)            


def show_Bar_chart():
    fig = plt.figure(figsize=(10, 4))
    ax  = fig.add_subplot(111)
    ax  = reset_ax(ax, fig)
    Type_counts = df["type"].value_counts()
    ax.bar(Type_counts.index, Type_counts.values,
           color='Lightgreen', edgecolor='lightyellow')
    ax.set_title("Movies vs TV Shows", color='white', fontsize=12)
    ax.set_xlabel("Type", color='#aaaaaa', fontsize=9)
    ax.set_ylabel("Count", color='#aaaaaa', fontsize=9)
    fig.tight_layout()
    st.pyplot(fig)  


def show_county_bar():
    fig = plt.figure(figsize=(10, 4))
    ax  = fig.add_subplot(111)
    ax  = reset_ax(ax, fig)
    # Your original logic — unchanged
    top_countries = df["country"].value_counts().head(10)
    ax.bar(top_countries.index, top_countries.values,
           color='orange', edgecolor='red')
    ax.set_title("Top 10 Countries by Number of Titles",
                 color='white', fontsize=12)
    ax.set_xlabel("Country", color='#aaaaaa', fontsize=9)
    ax.set_ylabel("Count",   color='#aaaaaa', fontsize=9)
    ax.tick_params(axis='x', rotation=30)
    ax.invert_xaxis()                       # your original line
    fig.tight_layout()
    st.pyplot(fig)  

def show_pie_chart():
    fig = plt.figure(figsize=(7, 7))
    ax  = fig.add_subplot(111)
    ax  = reset_ax(ax, fig)
    # Your original logic — unchanged
    rating_counts = df["rating"].value_counts()
    ax.pie(rating_counts.values,
           labels=rating_counts.index,
           autopct='%1.1f%%',
           startangle=140,
           labeldistance=1.1,
           pctdistance=0.8)
    ax.set_title("Distribution of Ratings",
                 fontsize=14, fontweight='bold', color='white')
    fig.tight_layout()
    st.pyplot(fig)     


def animated_exit():
    # Your original print messages kept
    st.success("Thanks for using Netflix Data Visualizer ❤️")
    st.info("Keep Coding, keep Learning!")
    st.balloons()      

if not any([show_histogram, show_bar, show_country, show_pie, show_exit_anim]):
    st.subheader("Release Year Distribution")
    plot_release_year_histogram(release_year)
 
if show_histogram:
    st.subheader("Release Year Distribution")
    plot_release_year_histogram(release_year)
 
if show_bar:
    st.subheader("Movies vs TV Shows")
    show_Bar_chart()
 
if show_country:
    st.subheader("Top 10 Countries")
    show_county_bar()
 
if show_pie:
    st.subheader("Rating Distribution")
    show_pie_chart()
 
if show_exit_anim:
    animated_exit()
 
st.divider()
 
st.subheader("Browse Titles")
# Apply filters — same logic as your filter_table() function
filtered = df.copy()
if genre_sel != "All":
    filtered = filtered[filtered["listed_in"].str.contains(genre_sel, na=False)]
if year_sel != "All":
    filtered = filtered[filtered["release_year"] == int(year_sel)]
if type_sel != "All":
    filtered = filtered[filtered["type"] == type_sel]
 
st.caption(f"{len(filtered):,} results")
 
# Show table — replaces ttk.Treeview
st.dataframe(
    filtered[["title", "type", "release_year", "rating", "listed_in", "country"]]
    .rename(columns={
        "title":        "Title",
        "type":         "Type",
        "release_year": "Year",
        "rating":       "Rating",
        "listed_in":    "Genre",
        "country":      "Country"
    })
    .head(300),
    use_container_width=True,
    hide_index=True
)
