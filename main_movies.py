from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.empireonline.com/movies/features/best-movies-2/")
eo_web_page = response.text

movies_filename = "movies.txt"

soup = BeautifulSoup(eo_web_page, "html.parser")

movie_items_soup = soup.find_all(name="div", class_="article-title-description__text")

movie_items_dict = {}
movie_items_list = []

movie_rank = 0
for article_title_description in movie_items_soup:
    for movie_title in article_title_description.find_all(name="h3", class_="title"):
        movie_text = movie_title.getText()
        try:
            movie_rank_x = int(movie_text[:movie_text.find(")")])
            if movie_rank != 0:
                # Capture Spirited Away Movie incorrectly labelled as 15 rather than 80
                if movie_rank_x == movie_rank - 1:
                    movie_rank = movie_rank_x
                else:
                    movie_rank -= 1
            else:
                movie_rank = movie_rank_x
        except ValueError:
            movie_rank -= 1
            movie_text = f"{movie_rank}) {movie_text}"
        finally:
            movie_items_dict[movie_rank] = movie_text

total_items = len(movie_items_dict)
for item in range(1, total_items+1):
    if item in movie_items_dict:
        movie_items_list.append(movie_items_dict[item])
    else:
        print(item)
        raise Exception(f"Missing entry on movie list: Movie Rank = {item}")

movie_items_dict = None     # Clear Dictionary from memory

print(f"Exporting list of {len(movie_items_list)} movies to {movies_filename}")

# Write movie list to file
with open(movies_filename, "w", encoding="utf8") as movie_file:
    movies_string = ""
    for movie_title in movie_items_list:
        movies_string += f"{movie_title}\n"
    movie_file.write(movies_string)