# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Most music apps learn from what people do: what they replay, like, finish or skip, and what people with similar habits enjoy. My recommender is much simpler. It only looks at what the user tells me they want right now, and it scores every song against that.

### What I look at in each song

I use four things from each song: its **mood**, its **genre**, its **energy** (0 to 1) and its **tempo** in beats per minute. The other columns in `songs.csv` (title, artist, valence, danceability, acousticness) get loaded, but I don't use them for scoring.

### What the user gives me

The user gives me a taste profile with their favorite genre, their favorite mood, the energy they're after and the tempo they like. I also pass in how many songs they want (`k`).

```python
taste_profile = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.35,
    "target_tempo_bpm": 75,
}
```

### How I score a song

Every song gets a score out of 100:

| What I check | Points | How it works |
|---|---|---|
| Mood | 40 | 40 if it's the same mood, 20 if it's a similar mood, 0 otherwise |
| Genre | 20 | 20 if it's the same genre, 0 otherwise |
| Energy | up to 30 | The closer the song's energy is to the target, the more points. An exact match gets all 30. |
| Tempo | up to 10 | The closer the tempo is to the target, the more points. It drops to 0 when it's 40 BPM or more away. |

I count similar moods as partial credit because "chill", "relaxed" and "focused" feel alike, and I didn't want a relaxed jazz song to count as a complete miss for someone who wants chill music.

I weigh mood more than genre because of what's in my data. Five of my seven genres belong to only one song, so a genre match mostly picks out that one song. Mood groups songs together and tells me more about how a song sounds. Every chill song has low energy, and both intense songs have very high energy. Genre still matters, just at half the weight.

### How I pick what to recommend

1. **Input:** I take the taste profile, the number of songs wanted and the songs from the CSV.
2. **Process:** I go through every song one at a time and give it a score, plus a short reason for the score.
3. **Output:** I sort the songs from highest score to lowest and return the top ones. If two songs tie, I put them in order by title so the results are always the same.

For example, with the profile above, Library Rain (lofi, chill) scores about 99. Coffee Shop Stories (jazz, relaxed) gets about 56, because a similar mood earns partial credit. Storm Runner (rock, intense) gets about 13.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` with the default profile (pop, happy, energy 0.8, tempo 120 BPM):

```text
Loading songs from data/songs.csv...
Loaded songs: 10

Top 5 recommendations for: genre=pop, mood=happy, energy=0.8, tempo=120 BPM
============================================================

1. Sunrise City by Neon Echo
   Score: 98.90 / 100
   Reasons:
     - mood matches happy (+40)
     - genre matches pop (+20)
     - energy 0.82 vs target 0.8 (+29.40)
     - tempo 118 BPM vs target 120 (+9.50)

2. Rooftop Lights by Indigo Parade
   Score: 77.80 / 100
   Reasons:
     - mood matches happy (+40)
     - genre indie pop does not match pop (+0)
     - energy 0.76 vs target 0.8 (+28.80)
     - tempo 124 BPM vs target 120 (+9.00)

3. Gym Hero by Max Pulse
   Score: 53.10 / 100
   Reasons:
     - mood intense does not match happy (+0)
     - genre matches pop (+20)
     - energy 0.93 vs target 0.8 (+26.10)
     - tempo 132 BPM vs target 120 (+7.00)

4. Night Drive Loop by Neon Echo
   Score: 36.00 / 100
   Reasons:
     - mood moody does not match happy (+0)
     - genre synthwave does not match pop (+0)
     - energy 0.75 vs target 0.8 (+28.50)
     - tempo 110 BPM vs target 120 (+7.50)

5. Storm Runner by Voltline
   Score: 28.70 / 100
   Reasons:
     - mood intense does not match happy (+0)
     - genre rock does not match pop (+0)
     - energy 0.91 vs target 0.8 (+26.70)
     - tempo 152 BPM vs target 120 (+2.00)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

My recommender is small and simple, and I expect this bias in it:

- **Labels count more than sound.** Genre and mood must match exactly, so a song labelled "indie pop" gets no genre credit for a pop fan even though it sounds similar. Mood alone is worth 40 of 100 points, so one label can outweigh a close fit on energy and tempo.



---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



