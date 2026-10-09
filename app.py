import streamlit as st
import json
import os

# Задай здесь свой секретный пароль админа
ADMIN_PASSWORD = "israiloff14"

DB_FILE = "articles.json"

# Загрузка статей из файла
def load_articles():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохранение статей в файл
def save_articles(articles):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="База Знаний", page_icon="📚", layout="wide")

st.title("📚 Моя База Знаний и Статей")
st.caption("Коллекция полезных материалов, заметок и ссылок")

# --- БОКОВАЯ ПАНЕЛЬ (SIDEBAR) ---
with st.sidebar:
    st.header("🔑 Авторизация")
    
    # Поле ввода пароля
    password = st.text_input("Введите пароль админа", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("Вы вошли как админ!")
        st.markdown("---")
        st.header("➕ Добавить статью")
        
        title = st.text_input("Название статьи")
        category = st.text_input("Категория (например: Python, Math, English)")
        content = st.text_area("Текст статьи или ссылка", height=150)
        
        if st.button("Сохранить"):
            if title and content:
                articles = load_articles()
                new_article = {
                    "title": title,
                    "category": category if category else "Общее",
                    "content": content
                }
                articles.append(new_article)
                save_articles(articles)
                st.success(f"Статья '{title}' успешно добавлена!")
                st.rerun()
            else:
                st.error("Заполните название и текст статьи!")
    else:
        if password:
            st.error("Неверный пароль")
        st.info("Режим гостя: доступен только просмотр и поиск материалов.")

# --- ОСНОВНАЯ ЧАСТЬ (ДЛЯ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ) ---
articles = load_articles()

# Поиск
search_query = st.text_input("🔍 Поиск по названию или категории", "")

filtered_articles = [
    a for a in articles 
    if search_query.lower() in a.get("title", "").lower() or search_query.lower() in a.get("category", "").lower()
]

st.subheader(f"Все статьи ({len(filtered_articles)})")

if not filtered_articles:
    st.write("Статей пока нет.")

for idx, article in enumerate(filtered_articles):
    with st.expander(f"📌 [{article.get('category', 'Общее')}] {article.get('title')}"):
        st.write(article.get("content"))
        
        # Кнопка удаления доступна ТОЛЬКО если введён правильный пароль
        if password == ADMIN_PASSWORD:
            if st.button("Удалить статью", key=f"del_{idx}"):
                articles.remove(article)
                save_articles(articles)
                st.warning("Статья удалена!")
                st.rerun()
