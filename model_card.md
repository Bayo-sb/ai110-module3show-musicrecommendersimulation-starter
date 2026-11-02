# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender looks at four things about each song: its mood, its genre, its energy and its tempo. The user tells it their favorite mood and genre, how energetic they want the music to be, and the tempo they like. Every song in the catalog is given a score out of 100, and the best-scoring songs are recommended.

A song earns points like this:

- **Mood (up to 40 points).** An exact match with the user's mood earns 40 points. If the moods are different but both are in the group "chill", "relaxed" and "focused", the song earns 20 points. Any other mood earns 0.
- **Genre (up to 20 points).** An exact match earns 20 points, and anything else earns 0.
- **Energy (up to 30 points).** The closer the song's energy is to the user's target, the more points it earns. A perfect match earns all 30 points, and the points shrink steadily as the gap grows.
- **Tempo (up to 10 points).** The closer the song's tempo is to the user's target, the more points it earns. A perfect match earns all 10 points, and the points shrink steadily to zero when the difference reaches 40 beats per minute.

The points are added up, the songs are ranked from the highest total to the lowest, and the top `k` songs are returned. If two songs have the same total, the one that comes first alphabetically by title is listed first. Each recommendation also comes with the reasons behind its score, such as "mood matches chill (+40)".

The weights (40, 20, 30 and 10) and the "chill, relaxed, focused" mood group are assumptions I picked by hand. I chose them because mood seemed to say more about how a song sounds than genre does in this small catalog, but I did not test them on real listeners. This version also does not learn from listening history. It only uses what the user says they want, and it never changes its scores based on what anyone plays, likes or skips.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
