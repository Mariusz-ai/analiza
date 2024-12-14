import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

# Ustawienie szerokości strony (musi być na początku)
st.set_page_config(layout="wide")

# Zmienia kontekst rozmiaru i stylu czcionek, aby były czytelne podczas prezentacji lub rozmowy
sns.set_theme(style="ticks", context="talk")

plt.style.use("dark_background")

# Tytuł
st.markdown("<h1 style='text-align: center;'>Analiza ankiety od zera do AI</h1>", unsafe_allow_html=True)

# Załadowanie danych z pliku CSV
df = pd.read_csv('35__welcome_survey_cleaned.csv', sep=';')

# Listę przedziałów wiekowych w kolejności
ordered_ages = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", ">=65"]
ordered_years_of_experience = ["0-2", "3-5", "6-10", "11-15", ">=16"]

# Zamień kolumny na kategorie z określoną kolejnością
df["age"] = pd.Categorical(df["age"], categories=ordered_ages, ordered=True)
df["years_of_experience"] = pd.Categorical(df["years_of_experience"], categories=ordered_years_of_experience, ordered=True)



# ======SIDEBAR======

with st.sidebar:
    wykształcenie = st.multiselect('Wybierz wykształcenie', sorted(df["edu_level"].dropna().unique()))
    
    # Używamy kolumny 'age' dla filtrowania przedziałów wiekowych
    age = st.multiselect(
        'Wybierz kategorię wiekową',
        ordered_ages  # Używamy listy ordered_ages bezpośrednio
    )

    # Używamy kolumny 'years_of_experience' dla filtrowania po doświadczeniu zawodowym
    years_of_experience = st.multiselect(
        'Wybierz kategorię doświadczenie zawodowe',
        ordered_years_of_experience  # Używamy listy ordered_years_of_experience bezpośrednio
    )

    gender = st.radio(
        "Wybierz płeć",
        ["Wszyscy", "Mężczyźni", "Kobiety"],
    )

    sweet_or_salty = st.radio(
        "Wybierz preferencje smakowe",
        ["słodkie i słone", "słodkie", "słone", ],
    )

# Filtracja danych na podstawie wyborów w sidebarze
if wykształcenie:
    df = df[df["edu_level"].isin(wykształcenie)]

if age:
    df = df[df["age"].isin(age)]  # Filtracja po wybranych kategoriach wiekowych

if years_of_experience:
    df = df[df["years_of_experience"].isin(years_of_experience)]  # Filtracja po doświadczeniu zawodowym

if gender == "Mężczyźni":
    df = df[df["gender"] == 0.0]
elif gender == "Kobiety":
    df = df[df["gender"] == 1.0]

if sweet_or_salty == "słodkie":
    df = df[df["sweet_or_salty"] == "sweet"]
elif sweet_or_salty == "słone":
    df = df[df["sweet_or_salty"] == "salty"]

# ======LINKI======

# Nowe linki do obrazków
images = {
    "dog": "https://i.postimg.cc/PxrVknTV/dog.png",
    "cat": "https://i.postimg.cc/L6690ncj/cat.png",
    "dog_and_cat": "https://i.postimg.cc/GttfvwfT/dog-cat.png",
    "others": "https://i.postimg.cc/WbJWVncV/others.png",
    "empty": "https://i.postimg.cc/MHnsv0cy/empty.png",
    "female": "https://i.postimg.cc/59LRhJcg/female.png",
    "male": "https://i.postimg.cc/wTkbBkjs/male.png",
    "total": "https://i.postimg.cc/rpDhQXCS/total.png",
    "salty": "https://i.postimg.cc/SNkJBHN8/salty.png",
    "sweet": "https://i.postimg.cc/KYkz72JX/sweet.png"
}

# ======LICZNIKI======

# Użycie 3 kolumn do wyświetlania wyników
col1, col2, col3 = st.columns(3)

# Funkcja pomocnicza do wyświetlania wyników i obrazków
def display_counts_and_images(counts_html, images_html):
    st.markdown(counts_html, unsafe_allow_html=True)
    st.markdown(images_html, unsafe_allow_html=True)

# Uzupełnianie brakujących wartości (NaN) o 'Brak'
df['fav_place'] = df['fav_place'].fillna('Brak')
df['sweet_or_salty'] = df['sweet_or_salty'].fillna('Brak')
df['industry'] = df['industry'].fillna('Brak')
# Zastępowanie wartości, które mogą powodować problemy przy liczeniu (np. dodatkowe spacje)
df['fav_animals'] = df['fav_animals'].replace({'Brak ulubionych': 'Brak'})

# Usunięcie wierszy, gdzie sweet_or_salty to 'Brak' (jeśli nie są one zamierzone jako kategorie)
df['sweet_or_salty'] = df['sweet_or_salty'].fillna('Brak')

# Ulubione zwierzęta (z poprawkami)
with col1:
    # Liczenie wystąpień każdego ulubionego zwierzęcia
    fav_animals_count = df['fav_animals'].value_counts()

    counts_html = f"""
    <div style='width: 375px; height: 35px; text-align: center; display: flex; justify-content: space-around; align-items: center;'>
        <span style='font-weight: bold; font-size: 35px;'>{fav_animals_count.get('Psy', 0)}</span>
        <span style='font-weight: bold; font-size: 35px;'>{fav_animals_count.get('Koty', 0)}</span>
        <span style='font-weight: bold; font-size: 35px;'>{fav_animals_count.get('Koty i Psy', 0)}</span>
        <span style='font-weight: bold; font-size: 35px;'>{fav_animals_count.get('Inne', 0)}</span>
        <span style='font-weight: bold; font-size: 35px;'>{fav_animals_count.get('Brak', 0)}</span>
    </div>
    """

    # Obrazki
    images_html = f"""
    <div style='width: 100%; display: flex; justify-content: start;'>
        <img src='{images["dog"]}' width='75'>
        <img src='{images["cat"]}' width='75'>
        <img src='{images["dog_and_cat"]}' width='75'>
        <img src='{images["others"]}' width='75'>
        <img src='{images["empty"]}' width='75'>
    </div>
    """
    display_counts_and_images(counts_html, images_html)

# Płeć
with col2:
    
    # Zastąpienie 0 i 1 w kolumnie 'gender' na 'Mężczyzna' i 'Kobieta'
    df['gender'] = df['gender'].replace({0: "Mężczyźni", 1: "Kobiety"})  # Upewnienie się, że 0 i 1 są zamieniane
    df['gender'] = df['gender'].fillna('Unknown')  # Uzupełnienie brakujących wartości o 'Unknown'
    
    gender_count = df['gender'].value_counts()

    counts_html = f"""
    <div style='width: 100%; height: 35px; text-align: center; display: flex; justify-content: center; align-items: center;'>
        <span style='font-weight: bold; font-size: 35px; margin-right: 30px'>{gender_count.get('Mężczyźni', 0)}</span>
        <span style='font-weight: bold; font-size: 35px; margin-right: 30px'>{gender_count.get('Kobiety', 0)}</span>
        <span style='font-weight: bold; font-size: 35px;'>{gender_count.get('Mężczyżni', 0) + gender_count.get('Kobiety', 0)}</span>
    </div>
    """

    # Obrazki
    images_html = f"""
    <div style='width: 100%; display: flex; justify-content: center;'>
        <img src='{images["male"]}' width='75'>
        <img src='{images["female"]}' width='75'>
        <img src='{images["total"]}' width='75'>
    </div>
    """
    display_counts_and_images(counts_html, images_html)

# Słodkie/Słone
with col3:
    sweet_or_salty_count = df['sweet_or_salty'].value_counts()

    counts_html = f"""
    <div style='width: 100%; height: 35px; text-align: center; display: flex; justify-content: right; align-items: center;'>
        <span style='font-weight: bold; font-size: 35px; margin-right: 30px'>{sweet_or_salty_count.get('sweet', 0)}</span>
        <span style='font-weight: bold; font-size: 35px; margin-right: 20px'>{sweet_or_salty_count.get('salty', 0)}</span>
    </div>
    """

    # Obrazki
    images_html = f"""
    <div style='width: 100%; display: flex; justify-content: flex-end;'>
        <img src='{images["sweet"]}' width='75'>
        <img src='{images["salty"]}' width='75'>
    </div>
    """
    display_counts_and_images(counts_html, images_html)
    
# ======Wykresy kołowe======

# Użycie 2 kolumn do wyświetlania wyników
col1, col2 = st.columns(2)

# Wykres słoneczny dla Płeć, Zwierzęta, Miejsce
with col1:
    # Sprawdzenie, czy dane po filtrze nie są puste
    df_gender_animal_place = df[['gender', 'fav_animals', 'fav_place']].dropna()
    if not df_gender_animal_place.empty:
        fig_sunburst_gender_animal_place = px.sunburst(
            df_gender_animal_place,
            path=['gender', 'fav_animals', 'fav_place'],
            color='fav_animals',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        # Aktualizacja układu wykresu słonecznego
        fig_sunburst_gender_animal_place.update_layout(
            width=800,
            height=800,
            font=dict(size=16, family="Arial, sans-serif", color="black")
        )

        # Dodanie procentów obok etykiet
        fig_sunburst_gender_animal_place.update_traces(
            textinfo='label+percent parent',  # Wyświetla etykiety z procentami
            textfont=dict(size=14, family="Arial", color="black", weight='bold')
        )

        st.plotly_chart(fig_sunburst_gender_animal_place)
    else:
        st.write("Brak danych dla wykresu Płeć, Zwierzęta, Miejsce")

# Wykres słoneczny dla Słodkie/Słone, Edukacja, Branża
with col2:
    # Sprawdzenie, czy dane po filtrze nie są puste
    df_sweet_salty_edu_industry = df[['sweet_or_salty', 'edu_level', 'industry']].dropna()
    if not df_sweet_salty_edu_industry.empty:
        fig_sunburst_sweet_salty_edu_industry = px.sunburst(
            df_sweet_salty_edu_industry,
            path=['sweet_or_salty', 'edu_level', 'industry'],
            color='edu_level',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        # Aktualizacja układu wykresu słonecznego
        fig_sunburst_sweet_salty_edu_industry.update_layout(
            width=800,
            height=800,
            font=dict(size=16, family="Arial, sans-serif", color="black")
        )

        # Dodanie procentów obok etykiet
        fig_sunburst_sweet_salty_edu_industry.update_traces(
            textinfo='label+percent parent',  # Wyświetla etykiety z procentami
            textfont=dict(size=14, family="Arial", color="black", weight='bold')
        )

        st.plotly_chart(fig_sunburst_sweet_salty_edu_industry)
    else:
        st.write("Brak danych dla wykresu Słodkie/Słone, Edukacja, Branża")



# ======HITOGRAMY======

# Lista kolumn związanych z hobby, preferencjami w nauce i motywacją
hobby_columns = ['hobby_art', 'hobby_books', 'hobby_movies', 'hobby_other', 'hobby_sport', 'hobby_video_games']
learning_pref_columns = ['learning_pref_books', 'learning_pref_chatgpt', 'learning_pref_offline_courses', 
                         'learning_pref_online_courses', 'learning_pref_personal_projects', 'learning_pref_teaching', 
                         'learning_pref_teamwork', 'learning_pref_workshops']
motivation_columns = ['motivation_career', 'motivation_challenges', 'motivation_creativity_and_innovation', 
                      'motivation_money_and_job', 'motivation_personal_growth', 'motivation_remote']

# Wypełnienie brakujących wartości
for col in hobby_columns + learning_pref_columns + motivation_columns:
    df[col] = df[col].fillna(0)

# Łączenie wszystkich hobby w jedną kolumnę
df_hobbies = df[hobby_columns].apply(lambda x: x.index[x == 1].tolist(), axis=1)
df_hobbies = df_hobbies[df_hobbies.apply(len) > 0]  # Usuwanie wierszy, które nie mają żadnych wybranych hobby
df_hobbies = df_hobbies.explode().reset_index(drop=True)

# Łączenie wszystkich preferencji w nauce w jedną kolumnę
df_learning_pref = df[learning_pref_columns].apply(lambda x: x.index[x == 1].tolist(), axis=1)
df_learning_pref = df_learning_pref[df_learning_pref.apply(len) > 0]
df_learning_pref = df_learning_pref.explode().reset_index(drop=True)

# Łączenie wszystkich motywacji w jedną kolumnę
df_motivation = df[motivation_columns].apply(lambda x: x.index[x == 1].tolist(), axis=1)
df_motivation = df_motivation[df_motivation.apply(len) > 0]
df_motivation = df_motivation.explode().reset_index(drop=True)

# Tłumaczenie kategorii na polski
hobby_translation = {
    'hobby_art': 'Sztuka',
    'hobby_books': 'Książki',
    'hobby_movies': 'Filmy',
    'hobby_other': 'Inne',
    'hobby_sport': 'Sport',
    'hobby_video_games': 'Gry wideo'
}

learning_pref_translation = {
    'learning_pref_books': 'Książki',
    'learning_pref_chatgpt': 'ChatGPT',
    'learning_pref_offline_courses': 'Kursy offline',
    'learning_pref_online_courses': 'Kursy online',
    'learning_pref_personal_projects': 'Projekty osobiste',
    'learning_pref_teaching': 'Nauczanie',
    'learning_pref_teamwork': 'Praca zespołowa',
    'learning_pref_workshops': 'Warsztaty'
}

motivation_translation = {
    'motivation_career': 'Kariera',
    'motivation_challenges': 'Wyzwania',
    'motivation_creativity_and_innovation': 'Kreatywność i innowacja',
    'motivation_money_and_job': 'Pieniądze i praca',
    'motivation_personal_growth': 'Rozwój osobisty',
    'motivation_remote': 'Praca zdalna'
}

translations_sweet_and_salty = {
    "sweet": "Słodkie",
    "salty": "Słone",
    "brak": "Brak"
}



# Grupowanie po kategoriach wiekowych i doświadczeniu zawodowym
grouped = df.groupby(['age', 'years_of_experience']).size().reset_index(name='count')

# Tworzenie wykresów w układzie 2 wierszy i 3 kolumny
fig, axes = plt.subplots(2, 3, figsize=(18, 12))  # Układ 2 wiersze, 3 kolumny

# 1. Hobby Histogram
df_hobbies_df = pd.DataFrame(df_hobbies, columns=['Hobby'])
sns.countplot(data=df_hobbies_df, y='Hobby', palette='Set2', order=df_hobbies_df['Hobby'].value_counts().index, ax=axes[0, 0])
axes[0, 0].set_title('Hobby ankietowanych', fontsize=18, fontweight='bold')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('')
axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=0, fontsize=14, fontweight='bold')
axes[0, 0].set_yticklabels([hobby_translation.get(label, label) for label in df_hobbies_df['Hobby'].unique()], fontsize=14, fontweight='bold')

# 2. Preferencje nauki Histogram
df_learning_pref_df = pd.DataFrame(df_learning_pref, columns=['Learning Preference'])
sns.countplot(data=df_learning_pref_df, y='Learning Preference', palette='Set1', order=df_learning_pref_df['Learning Preference'].value_counts().index, ax=axes[0, 1])
axes[0, 1].set_title('Preferencje nauki ankietowanych', fontsize=18, fontweight='bold')
axes[0, 1].set_xlabel('')
axes[0, 1].set_ylabel('')
axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=0, fontsize=14, fontweight='bold')
axes[0, 1].set_yticklabels([learning_pref_translation.get(label, label) for label in df_learning_pref_df['Learning Preference'].unique()], fontsize=14, fontweight='bold')

# 3. Motywacja Histogram
df_motivation_df = pd.DataFrame(df_motivation, columns=['Motivation'])
sns.countplot(data=df_motivation_df, y='Motivation', palette='Set3', order=df_motivation_df['Motivation'].value_counts().index, ax=axes[0, 2])
axes[0, 2].set_title('Co motywuje ankietowanych', fontsize=18, fontweight='bold')
axes[0, 2].set_xlabel('')
axes[0, 2].set_ylabel('')
axes[0, 2].set_xticklabels(axes[0, 2].get_xticklabels(), rotation=0, fontsize=14, fontweight='bold')
axes[0, 2].set_yticklabels([motivation_translation.get(label, label) for label in df_motivation_df['Motivation'].unique()], fontsize=14, fontweight='bold')

# 4. Histogram dla grupy wiekowej (horyzontalny)
sns.countplot(data=df, y='age', palette='Blues', ax=axes[1, 0])
axes[1, 0].set_title('Rozkład wiekowy ankietowanych', fontsize=18, fontweight='bold')
axes[1, 0].set_xlabel('')
axes[1, 0].set_ylabel('')
axes[1, 0].tick_params(axis='y', rotation=0)
axes[1, 0].set_xticklabels([int(tick) for tick in axes[1, 0].get_xticks()], fontsize=14, fontweight='bold')
axes[1, 0].set_yticklabels(axes[1, 0].get_yticklabels(), fontsize=14, fontweight='bold')

# 5. Histogram dla doświadczenia zawodowego (horyzontalny)
sns.countplot(data=df, y='years_of_experience', palette='viridis', ax=axes[1, 1])
axes[1, 1].set_title('Doświadczenie zawodowe', fontsize=18, fontweight='bold')
axes[1, 1].set_xlabel('')
axes[1, 1].set_ylabel('')
axes[1, 1].tick_params(axis='y', rotation=0)
axes[1, 1].set_xticklabels([int(tick) for tick in axes[1, 1].get_xticks()], fontsize=14, fontweight='bold')
axes[1, 1].set_yticklabels(axes[1, 1].get_yticklabels(), fontsize=14, fontweight='bold')

# 6. Histogram dla sweet_or_salty względem płci
sns.countplot(data=df, y='sweet_or_salty', hue='gender', palette='Set2', ax=axes[1, 2])
axes[1, 2].set_title('Preferencje słodkie vs. słone względem płci', fontsize=18, fontweight='bold')
axes[1, 2].set_xlabel('')
axes[1, 2].set_ylabel('')
axes[1, 2].tick_params(axis='y', rotation=0)

# Tłumaczenie etykiet osi X dla sweet_or_salty
axes[1, 2].set_yticklabels(
    [translations_sweet_and_salty.get(tick.get_text(), tick.get_text()) for tick in axes[1, 2].get_yticklabels()],
    fontsize=14, fontweight='bold'
)
axes[1, 2].set_xticklabels([int(tick) for tick in axes[1, 2].get_yticks()], fontsize=14, fontweight='bold')

# Dynamiczna aktualizacja legendy na podstawie filtra płci
if gender == "Mężczyzna":
    handles, labels = axes[1, 2].get_legend_handles_labels()
    axes[1, 2].legend(handles, ['Mężczyźni'], title='Płeć', fontsize=12, title_fontsize=14, loc='upper right')
elif gender == "Kobiety":
    handles, labels = axes[1, 2].get_legend_handles_labels()
    axes[1, 2].legend(handles, ['Kobiety    '], title='Płeć', fontsize=12, title_fontsize=14, loc='upper right')
else:
    handles, labels = axes[1, 2].get_legend_handles_labels()
    axes[1, 2].legend(handles, ['Kobiety', 'Mężczyźni', 'Brak'], title='Płeć', fontsize=12, title_fontsize=14, loc='upper right')

# Zwiększenie odstępu między wykresami
plt.subplots_adjust(hspace=0.3, wspace=0.1)  # Większy odstęp w pionie i poziomie

# Dostosowanie układu i marginesów
fig.tight_layout(pad=1.2)  # Zwiększa marginesy między wykresami

# Wyświetlanie wykresów w aplikacji Streamlit
st.pyplot(fig)

# Tworzenie osobnego wykresu dla branży
fig_industry, ax_industry = plt.subplots(figsize=(18, 5))
sns.countplot(data=df, x='industry', palette='coolwarm', ax=ax_industry)
ax_industry.set_title('Branże ankietowanych', fontsize=16)
ax_industry.set_xlabel('')
ax_industry.set_ylabel('')
ax_industry.tick_params(axis='x', rotation=90)
ax_industry.set_xticklabels(ax_industry.get_xticklabels(), fontsize=12, fontweight='bold')
ax_industry.set_yticklabels([int(tick) for tick in ax_industry.get_yticks()], fontsize=12, fontweight='bold')

# Wyświetlanie wykresu branży w aplikacji Streamlit
st.pyplot(fig_industry)
