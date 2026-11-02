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

I always use four things from each song: its **mood**, its **genre**, its **energy** (0 to 1) and its **tempo** in beats per minute.

I also added five optional attributes: **popularity** (0 to 100), **release decade** (like 1990 or 2020), **detailed mood tags**, **instrumentalness** (0 to 1) and **lyrical themes**. I only use them when the user asks for them. The other columns in `songs.csv` (title, artist, valence, danceability, acousticness) get loaded, but I don't use them for scoring.
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

### Optional advanced preferences

A user can also give me any of these. Each one switches on only when it's supplied. An empty tag list switches it off too.

| Preference | Weight | How I match it (0 to 1) |
|---|---|---|
| `target_popularity` | 5 | 1 minus the gap in popularity divided by 100 |
| `target_release_decade` | 5 | 1 for the same decade, otherwise 0 |
| `preferred_mood_tags` | 10 | The fraction of the tags the user asked for that the song has |
| `target_instrumentalness` | 5 | 1 minus the gap in instrumentalness |
| `preferred_lyrical_themes` | 5 | The fraction of the themes the user asked for that the song has |

The score I described above counts as a match too: I divide it by 100 and give it a weight of 70. Then:

`final score = 100 × (sum of weight × match) ÷ (sum of the weights that are switched on)`

If the user gives no advanced preferences, I skip all of this and the score stays exactly the same as before. If they give all five, the weights add up to 100. Each reason in the output says which parts were switched on.

For example, with my Chill Lofi profile plus advanced preferences (popularity 50, decade 2020, tags calm and focused, instrumentalness 0.9, theme study), Midnight Coding scores 97.50 and moves ahead of Library Rain, which scores 94.33. Without the advanced preferences, Library Rain was first (99.25 to 97.15). Library Rain only has one of the two mood tags I asked for.

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

Output of `python -m src.main`. It runs nine profiles and prints a table for each: the six profiles without advanced preferences, then three advanced profiles. The first six give exactly the same scores and rankings as before I added the advanced attributes.

```text
Loading songs from data/songs.csv...
Loaded songs: 10
```

```text
######################################################################
PROFILE: High-Energy Pop
######################################################################
What it tests: Baseline: preferences that line up with a song in the catalog.
Preferences: genre=pop, mood=happy, energy=0.85, tempo=125 BPM

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Sunrise City         | 97.35     | - mood matches happy (+40)                             |
|      |                      |           | - genre matches pop (+20)                              |
|      |                      |           | - energy 0.82 vs target 0.85 (+29.10)                  |
|      |                      |           | - tempo 118 BPM vs target 125 (+8.25)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Rooftop Lights       | 77.05     | - mood matches happy (+40)                             |
|      |                      |           | - genre indie pop does not match pop (+0)              |
|      |                      |           | - energy 0.76 vs target 0.85 (+27.30)                  |
|      |                      |           | - tempo 124 BPM vs target 125 (+9.75)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Gym Hero             | 55.85     | - mood intense does not match happy (+0)               |
|      |                      |           | - genre matches pop (+20)                              |
|      |                      |           | - energy 0.93 vs target 0.85 (+27.60)                  |
|      |                      |           | - tempo 132 BPM vs target 125 (+8.25)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Night Drive Loop     | 33.25     | - mood moody does not match happy (+0)                 |
|      |                      |           | - genre synthwave does not match pop (+0)              |
|      |                      |           | - energy 0.75 vs target 0.85 (+27.00)                  |
|      |                      |           | - tempo 110 BPM vs target 125 (+6.25)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Storm Runner         | 31.45     | - mood intense does not match happy (+0)               |
|      |                      |           | - genre rock does not match pop (+0)                   |
|      |                      |           | - energy 0.91 vs target 0.85 (+28.20)                  |
|      |                      |           | - tempo 152 BPM vs target 125 (+3.25)                  |
+------+----------------------+-----------+--------------------------------------------------------+
```

```text
######################################################################
PROFILE: Chill Lofi
######################################################################
What it tests: Baseline: low-energy taste, and whether the similar-mood partial credit
  (chill/relaxed/focused) shows up.
Preferences: genre=lofi, mood=chill, energy=0.35, tempo=75 BPM

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Library Rain         | 99.25     | - mood matches chill (+40)                             |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.35 vs target 0.35 (+30.00)                  |
|      |                      |           | - tempo 72 BPM vs target 75 (+9.25)                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Midnight Coding      | 97.15     | - mood matches chill (+40)                             |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.42 vs target 0.35 (+27.90)                  |
|      |                      |           | - tempo 78 BPM vs target 75 (+9.25)                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Focus Flow           | 77.25     | - mood focused is similar to chill (+20)               |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.4 vs target 0.35 (+28.50)                   |
|      |                      |           | - tempo 80 BPM vs target 75 (+8.75)                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Spacewalk Thoughts   | 74.15     | - mood matches chill (+40)                             |
|      |                      |           | - genre ambient does not match lofi (+0)               |
|      |                      |           | - energy 0.28 vs target 0.35 (+27.90)                  |
|      |                      |           | - tempo 60 BPM vs target 75 (+6.25)                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Coffee Shop Stories  | 55.65     | - mood relaxed is similar to chill (+20)               |
|      |                      |           | - genre jazz does not match lofi (+0)                  |
|      |                      |           | - energy 0.37 vs target 0.35 (+29.40)                  |
|      |                      |           | - tempo 90 BPM vs target 75 (+6.25)                    |
+------+----------------------+-----------+--------------------------------------------------------+
```

```text
######################################################################
PROFILE: Deep Intense Rock
######################################################################
What it tests: Baseline: extreme targets (energy 0.95, 150 BPM) at the edge of the catalog's range.
Preferences: genre=rock, mood=intense, energy=0.95, tempo=150 BPM

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Storm Runner         | 98.30     | - mood matches intense (+40)                           |
|      |                      |           | - genre matches rock (+20)                             |
|      |                      |           | - energy 0.91 vs target 0.95 (+28.80)                  |
|      |                      |           | - tempo 152 BPM vs target 150 (+9.50)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Gym Hero             | 74.90     | - mood matches intense (+40)                           |
|      |                      |           | - genre pop does not match rock (+0)                   |
|      |                      |           | - energy 0.93 vs target 0.95 (+29.40)                  |
|      |                      |           | - tempo 132 BPM vs target 150 (+5.50)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Sunrise City         | 28.10     | - mood happy does not match intense (+0)               |
|      |                      |           | - genre pop does not match rock (+0)                   |
|      |                      |           | - energy 0.82 vs target 0.95 (+26.10)                  |
|      |                      |           | - tempo 118 BPM vs target 150 (+2.00)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Rooftop Lights       | 27.80     | - mood happy does not match intense (+0)               |
|      |                      |           | - genre indie pop does not match rock (+0)             |
|      |                      |           | - energy 0.76 vs target 0.95 (+24.30)                  |
|      |                      |           | - tempo 124 BPM vs target 150 (+3.50)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Night Drive Loop     | 24.00     | - mood moody does not match intense (+0)               |
|      |                      |           | - genre synthwave does not match rock (+0)             |
|      |                      |           | - energy 0.75 vs target 0.95 (+24.00)                  |
|      |                      |           | - tempo 110 BPM vs target 150 (+0.00)                  |
+------+----------------------+-----------+--------------------------------------------------------+
```

```text
######################################################################
PROFILE: Adversarial: Energetic but Sad
######################################################################
What it tests: Conflicting preferences: very high energy and fast tempo with a 'sad' mood. No song
  is sad, so mood can never score, and the ranking is decided by genre, energy and tempo alone.
Preferences: genre=pop, mood=sad, energy=0.95, tempo=160 BPM

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Gym Hero             | 52.40     | - mood intense does not match sad (+0)                 |
|      |                      |           | - genre matches pop (+20)                              |
|      |                      |           | - energy 0.93 vs target 0.95 (+29.40)                  |
|      |                      |           | - tempo 132 BPM vs target 160 (+3.00)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Sunrise City         | 46.10     | - mood happy does not match sad (+0)                   |
|      |                      |           | - genre matches pop (+20)                              |
|      |                      |           | - energy 0.82 vs target 0.95 (+26.10)                  |
|      |                      |           | - tempo 118 BPM vs target 160 (+0.00)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Storm Runner         | 36.80     | - mood intense does not match sad (+0)                 |
|      |                      |           | - genre rock does not match pop (+0)                   |
|      |                      |           | - energy 0.91 vs target 0.95 (+28.80)                  |
|      |                      |           | - tempo 152 BPM vs target 160 (+8.00)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Rooftop Lights       | 25.30     | - mood happy does not match sad (+0)                   |
|      |                      |           | - genre indie pop does not match pop (+0)              |
|      |                      |           | - energy 0.76 vs target 0.95 (+24.30)                  |
|      |                      |           | - tempo 124 BPM vs target 160 (+1.00)                  |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Night Drive Loop     | 24.00     | - mood moody does not match sad (+0)                   |
|      |                      |           | - genre synthwave does not match pop (+0)              |
|      |                      |           | - energy 0.75 vs target 0.95 (+24.00)                  |
|      |                      |           | - tempo 110 BPM vs target 160 (+0.00)                  |
+------+----------------------+-----------+--------------------------------------------------------+
```

```text
######################################################################
PROFILE: Adversarial: Genre and Mood Not in CSV
######################################################################
What it tests: Missing categories: 'classical' and 'melancholy' appear in no song, so only energy
  and tempo can differentiate. Shows how the recommender degrades when categorical signals are dead.
Preferences: genre=classical, mood=melancholy, energy=0.3, tempo=60 BPM

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Spacewalk Thoughts   | 39.40     | - mood chill does not match melancholy (+0)            |
|      |                      |           | - genre ambient does not match classical (+0)          |
|      |                      |           | - energy 0.28 vs target 0.3 (+29.40)                   |
|      |                      |           | - tempo 60 BPM vs target 60 (+10.00)                   |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Library Rain         | 35.50     | - mood chill does not match melancholy (+0)            |
|      |                      |           | - genre lofi does not match classical (+0)             |
|      |                      |           | - energy 0.35 vs target 0.3 (+28.50)                   |
|      |                      |           | - tempo 72 BPM vs target 60 (+7.00)                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Focus Flow           | 32.00     | - mood focused does not match melancholy (+0)          |
|      |                      |           | - genre lofi does not match classical (+0)             |
|      |                      |           | - energy 0.4 vs target 0.3 (+27.00)                    |
|      |                      |           | - tempo 80 BPM vs target 60 (+5.00)                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Midnight Coding      | 31.90     | - mood chill does not match melancholy (+0)            |
|      |                      |           | - genre lofi does not match classical (+0)             |
|      |                      |           | - energy 0.42 vs target 0.3 (+26.40)                   |
|      |                      |           | - tempo 78 BPM vs target 60 (+5.50)                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Coffee Shop Stories  | 30.40     | - mood relaxed does not match melancholy (+0)          |
|      |                      |           | - genre jazz does not match classical (+0)             |
|      |                      |           | - energy 0.37 vs target 0.3 (+27.90)                   |
|      |                      |           | - tempo 90 BPM vs target 60 (+2.50)                    |
+------+----------------------+-----------+--------------------------------------------------------+
```

```text
######################################################################
PROFILE: Adversarial: Chill but Frantic
######################################################################
What it tests: Conflict between categories and numbers: lofi/chill taste paired with maximum energy
  and tempo. Checks whether the 40+20 category points override the numeric targets.
Preferences: genre=lofi, mood=chill, energy=1.0, tempo=180 BPM

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Midnight Coding      | 72.60     | - mood matches chill (+40)                             |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.42 vs target 1.0 (+12.60)                   |
|      |                      |           | - tempo 78 BPM vs target 180 (+0.00)                   |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Library Rain         | 70.50     | - mood matches chill (+40)                             |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.35 vs target 1.0 (+10.50)                   |
|      |                      |           | - tempo 72 BPM vs target 180 (+0.00)                   |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Focus Flow           | 52.00     | - mood focused is similar to chill (+20)               |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.4 vs target 1.0 (+12.00)                    |
|      |                      |           | - tempo 80 BPM vs target 180 (+0.00)                   |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Spacewalk Thoughts   | 48.40     | - mood matches chill (+40)                             |
|      |                      |           | - genre ambient does not match lofi (+0)               |
|      |                      |           | - energy 0.28 vs target 1.0 (+8.40)                    |
|      |                      |           | - tempo 60 BPM vs target 180 (+0.00)                   |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Coffee Shop Stories  | 31.10     | - mood relaxed is similar to chill (+20)               |
|      |                      |           | - genre jazz does not match lofi (+0)                  |
|      |                      |           | - energy 0.37 vs target 1.0 (+11.10)                   |
|      |                      |           | - tempo 90 BPM vs target 180 (+0.00)                   |
+------+----------------------+-----------+--------------------------------------------------------+
```

```text
######################################################################
PROFILE: Advanced: Study Session
######################################################################
What it tests: Same core taste as Chill Lofi, plus all five advanced preferences. Checks whether
  tags, themes and instrumentalness can reorder songs the core score nearly ties.
Preferences: genre=lofi, mood=chill, energy=0.35, tempo=75 BPM
Advanced preferences: target_popularity=50, target_release_decade=2020, preferred_mood_tags=['calm',
  'focused'], target_instrumentalness=0.9, preferred_lyrical_themes=['study']

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Midnight Coding      | 97.50     | - mood matches chill (+40)                             |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.42 vs target 0.35 (+27.90)                  |
|      |                      |           | - tempo 78 BPM vs target 75 (+9.25)                    |
|      |                      |           | - core score 97.15/100 counts for weight 70            |
|      |                      |           | - popularity 58 vs target 50: match 0.92 x weight 5    |
|      |                      |           | - release decade 2020 vs target 2020: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 2 of 2 wanted found (calm, focused): match |
|      |                      |           |   1.00 x weight 10                                     |
|      |                      |           | - instrumentalness 0.88 vs target 0.9: match 0.98 x    |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 1 of 1 wanted found (study): match    |
|      |                      |           |   1.00 x weight 5                                      |
|      |                      |           | - final = 100 x 97.50 / 100 = 97.50                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Library Rain         | 94.33     | - mood matches chill (+40)                             |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.35 vs target 0.35 (+30.00)                  |
|      |                      |           | - tempo 72 BPM vs target 75 (+9.25)                    |
|      |                      |           | - core score 99.25/100 counts for weight 70            |
|      |                      |           | - popularity 49 vs target 50: match 0.99 x weight 5    |
|      |                      |           | - release decade 2020 vs target 2020: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 1 of 2 wanted found (calm): match 0.50 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - instrumentalness 0.92 vs target 0.9: match 0.98 x    |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 1 of 1 wanted found (study): match    |
|      |                      |           |   1.00 x weight 5                                      |
|      |                      |           | - final = 100 x 94.33 / 100 = 94.33                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Focus Flow           | 83.97     | - mood focused is similar to chill (+20)               |
|      |                      |           | - genre matches lofi (+20)                             |
|      |                      |           | - energy 0.4 vs target 0.35 (+28.50)                   |
|      |                      |           | - tempo 80 BPM vs target 75 (+8.75)                    |
|      |                      |           | - core score 77.25/100 counts for weight 70            |
|      |                      |           | - popularity 52 vs target 50: match 0.98 x weight 5    |
|      |                      |           | - release decade 2020 vs target 2020: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 2 of 2 wanted found (calm, focused): match |
|      |                      |           |   1.00 x weight 10                                     |
|      |                      |           | - instrumentalness 0.9 vs target 0.9: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 1 of 1 wanted found (study): match    |
|      |                      |           |   1.00 x weight 5                                      |
|      |                      |           | - final = 100 x 83.97 / 100 = 83.97                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Spacewalk Thoughts   | 65.86     | - mood matches chill (+40)                             |
|      |                      |           | - genre ambient does not match lofi (+0)               |
|      |                      |           | - energy 0.28 vs target 0.35 (+27.90)                  |
|      |                      |           | - tempo 60 BPM vs target 75 (+6.25)                    |
|      |                      |           | - core score 74.15/100 counts for weight 70            |
|      |                      |           | - popularity 34 vs target 50: match 0.84 x weight 5    |
|      |                      |           | - release decade 2000 vs target 2020: match 0.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 1 of 2 wanted found (calm): match 0.50 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - instrumentalness 0.95 vs target 0.9: match 0.95 x    |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 65.86 / 100 = 65.86                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Coffee Shop Stories  | 46.26     | - mood relaxed is similar to chill (+20)               |
|      |                      |           | - genre jazz does not match lofi (+0)                  |
|      |                      |           | - energy 0.37 vs target 0.35 (+29.40)                  |
|      |                      |           | - tempo 90 BPM vs target 75 (+6.25)                    |
|      |                      |           | - core score 55.65/100 counts for weight 70            |
|      |                      |           | - popularity 41 vs target 50: match 0.91 x weight 5    |
|      |                      |           | - release decade 1990 vs target 2020: match 0.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 0 of 2 wanted found (none): match 0.00 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - instrumentalness 0.45 vs target 0.9: match 0.55 x    |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 46.25 / 100 = 46.26                    |
+------+----------------------+-----------+--------------------------------------------------------+
```

```text
######################################################################
PROFILE: Advanced: Chart-Topping Workout
######################################################################
What it tests: Pop and intense taste with a very popular, recent, vocal track in mind. Checks that
  popularity and decade can lift a song.
Preferences: genre=pop, mood=intense, energy=0.9, tempo=130 BPM
Advanced preferences: target_popularity=90, target_release_decade=2020,
  preferred_mood_tags=['energetic', 'motivating'], target_instrumentalness=0.05,
  preferred_lyrical_themes=['workout']

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Gym Hero             | 98.92     | - mood matches intense (+40)                           |
|      |                      |           | - genre matches pop (+20)                              |
|      |                      |           | - energy 0.93 vs target 0.9 (+29.10)                   |
|      |                      |           | - tempo 132 BPM vs target 130 (+9.50)                  |
|      |                      |           | - core score 98.60/100 counts for weight 70            |
|      |                      |           | - popularity 90 vs target 90: match 1.00 x weight 5    |
|      |                      |           | - release decade 2020 vs target 2020: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 2 of 2 wanted found (energetic,            |
|      |                      |           |   motivating): match 1.00 x weight 10                  |
|      |                      |           | - instrumentalness 0.03 vs target 0.05: match 0.98 x   |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 1 of 1 wanted found (workout): match  |
|      |                      |           |   1.00 x weight 5                                      |
|      |                      |           | - final = 100 x 98.92 / 100 = 98.92                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Storm Runner         | 60.99     | - mood matches intense (+40)                           |
|      |                      |           | - genre rock does not match pop (+0)                   |
|      |                      |           | - energy 0.91 vs target 0.9 (+29.70)                   |
|      |                      |           | - tempo 152 BPM vs target 130 (+4.50)                  |
|      |                      |           | - core score 74.20/100 counts for weight 70            |
|      |                      |           | - popularity 71 vs target 90: match 0.81 x weight 5    |
|      |                      |           | - release decade 2010 vs target 2020: match 0.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 0 of 2 wanted found (none): match 0.00 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - instrumentalness 0.05 vs target 0.05: match 1.00 x   |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 60.99 / 100 = 60.99                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Sunrise City         | 57.67     | - mood happy does not match intense (+0)               |
|      |                      |           | - genre matches pop (+20)                              |
|      |                      |           | - energy 0.82 vs target 0.9 (+27.60)                   |
|      |                      |           | - tempo 118 BPM vs target 130 (+7.00)                  |
|      |                      |           | - core score 54.60/100 counts for weight 70            |
|      |                      |           | - popularity 82 vs target 90: match 0.92 x weight 5    |
|      |                      |           | - release decade 2020 vs target 2020: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 1 of 2 wanted found (energetic): match     |
|      |                      |           |   0.50 x weight 10                                     |
|      |                      |           | - instrumentalness 0.02 vs target 0.05: match 0.97 x   |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 57.67 / 100 = 57.67                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Rooftop Lights       | 32.51     | - mood happy does not match intense (+0)               |
|      |                      |           | - genre indie pop does not match pop (+0)              |
|      |                      |           | - energy 0.76 vs target 0.9 (+25.80)                   |
|      |                      |           | - tempo 124 BPM vs target 130 (+8.50)                  |
|      |                      |           | - core score 34.30/100 counts for weight 70            |
|      |                      |           | - popularity 67 vs target 90: match 0.77 x weight 5    |
|      |                      |           | - release decade 2010 vs target 2020: match 0.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 0 of 2 wanted found (none): match 0.00 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - instrumentalness 0.12 vs target 0.05: match 0.93 x   |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 32.51 / 100 = 32.51                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Night Drive Loop     | 26.75     | - mood moody does not match intense (+0)               |
|      |                      |           | - genre synthwave does not match pop (+0)              |
|      |                      |           | - energy 0.75 vs target 0.9 (+25.50)                   |
|      |                      |           | - tempo 110 BPM vs target 130 (+5.00)                  |
|      |                      |           | - core score 30.50/100 counts for weight 70            |
|      |                      |           | - popularity 63 vs target 90: match 0.73 x weight 5    |
|      |                      |           | - release decade 2010 vs target 2020: match 0.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 0 of 2 wanted found (none): match 0.00 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - instrumentalness 0.7 vs target 0.05: match 0.35 x    |
|      |                      |           |   weight 5                                             |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 26.75 / 100 = 26.75                    |
+------+----------------------+-----------+--------------------------------------------------------+
```

```text
######################################################################
PROFILE: Advanced: Retro Night Drive
######################################################################
What it tests: Only some advanced preferences (no popularity, no instrumentalness target). Checks
  that unused components stay switched off.
Preferences: genre=synthwave, mood=moody, energy=0.75, tempo=110 BPM
Advanced preferences: target_release_decade=2010, preferred_mood_tags=['nocturnal', 'brooding'],
  preferred_lyrical_themes=['night']

Top 5 recommendations:
+------+----------------------+-----------+--------------------------------------------------------+
| Rank | Song                 | Score/100 | Reasons                                                |
+------+----------------------+-----------+--------------------------------------------------------+
| 1    | Night Drive Loop     | 100.00    | - mood matches moody (+40)                             |
|      |                      |           | - genre matches synthwave (+20)                        |
|      |                      |           | - energy 0.75 vs target 0.75 (+30.00)                  |
|      |                      |           | - tempo 110 BPM vs target 110 (+10.00)                 |
|      |                      |           | - core score 100.00/100 counts for weight 70           |
|      |                      |           | - release decade 2010 vs target 2010: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 2 of 2 wanted found (nocturnal, brooding): |
|      |                      |           |   match 1.00 x weight 10                               |
|      |                      |           | - lyrical themes 1 of 1 wanted found (night): match    |
|      |                      |           |   1.00 x weight 5                                      |
|      |                      |           | - final = 100 x 90.00 / 90 = 100.00                    |
+------+----------------------+-----------+--------------------------------------------------------+
| 2    | Rooftop Lights       | 33.71     | - mood happy does not match moody (+0)                 |
|      |                      |           | - genre indie pop does not match synthwave (+0)        |
|      |                      |           | - energy 0.76 vs target 0.75 (+29.70)                  |
|      |                      |           | - tempo 124 BPM vs target 110 (+6.50)                  |
|      |                      |           | - core score 36.20/100 counts for weight 70            |
|      |                      |           | - release decade 2010 vs target 2010: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 0 of 2 wanted found (none): match 0.00 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 30.34 / 90 = 33.71                     |
+------+----------------------+-----------+--------------------------------------------------------+
| 3    | Sunrise City         | 27.92     | - mood happy does not match moody (+0)                 |
|      |                      |           | - genre pop does not match synthwave (+0)              |
|      |                      |           | - energy 0.82 vs target 0.75 (+27.90)                  |
|      |                      |           | - tempo 118 BPM vs target 110 (+8.00)                  |
|      |                      |           | - core score 35.90/100 counts for weight 70            |
|      |                      |           | - release decade 2020 vs target 2010: match 0.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 0 of 2 wanted found (none): match 0.00 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 25.13 / 90 = 27.92                     |
+------+----------------------+-----------+--------------------------------------------------------+
| 4    | Storm Runner         | 25.16     | - mood intense does not match moody (+0)               |
|      |                      |           | - genre rock does not match synthwave (+0)             |
|      |                      |           | - energy 0.91 vs target 0.75 (+25.20)                  |
|      |                      |           | - tempo 152 BPM vs target 110 (+0.00)                  |
|      |                      |           | - core score 25.20/100 counts for weight 70            |
|      |                      |           | - release decade 2010 vs target 2010: match 1.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 0 of 2 wanted found (none): match 0.00 x   |
|      |                      |           |   weight 10                                            |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 22.64 / 90 = 25.16                     |
+------+----------------------+-----------+--------------------------------------------------------+
| 5    | Midnight Coding      | 22.74     | - mood chill does not match moody (+0)                 |
|      |                      |           | - genre lofi does not match synthwave (+0)             |
|      |                      |           | - energy 0.42 vs target 0.75 (+20.10)                  |
|      |                      |           | - tempo 78 BPM vs target 110 (+2.00)                   |
|      |                      |           | - core score 22.10/100 counts for weight 70            |
|      |                      |           | - release decade 2020 vs target 2010: match 0.00 x     |
|      |                      |           |   weight 5                                             |
|      |                      |           | - mood tags 1 of 2 wanted found (nocturnal): match     |
|      |                      |           |   0.50 x weight 10                                     |
|      |                      |           | - lyrical themes 0 of 1 wanted found (none): match     |
|      |                      |           |   0.00 x weight 5                                      |
|      |                      |           | - final = 100 x 20.47 / 90 = 22.74                     |
+------+----------------------+-----------+--------------------------------------------------------+
```

---

## Experiments You Tried

**Reweighting experiment.** I wanted to see how much my weights matter, so I ran one temporary experiment and then took it back out of the code. I cut genre from 20 to 10 points and doubled energy to up to 60 points. Mood (40, or 20 for a similar mood) and tempo (up to 10) stayed the same. The points then added up to 120, so I rescaled every score with `raw × 100 ÷ 120`. An exact match still scored 100, and every score stayed between 16.50 and 99.38. The profiles, the songs, the mood group and the tie-breaking stayed the same.

What changed in the top five:

- **High-Energy Pop and Deep Intense Rock:** the same five songs in the same order. Only the scores moved.
- **Chill Lofi:** Spacewalk Thoughts moved up from 4th to 3rd. Focus Flow dropped to 4th.
- **Energetic but Sad:** Storm Runner moved up from 3rd to 2nd. Sunrise City dropped to 3rd.
- **Genre and Mood Not in CSV:** Coffee Shop Stories moved up from 5th to 4th. Midnight Coding dropped to 5th. They tied at 48.58, and the title order decided it.
- **Chill but Frantic:** the top two stayed the same, but their scores fell. Storm Runner and Gym Hero came into the top five. Focus Flow and Coffee Shop Stories dropped out.

| Rank | Chill but Frantic, my original weights | Chill but Frantic, experiment |
|---|---|---|
| 1 | Midnight Coding, 72.60 | Midnight Coding, 62.67 |
| 2 | Library Rain, 70.50 | Library Rain, 59.17 |
| 3 | Focus Flow, 52.00 | Storm Runner, 48.00 |
| 4 | Spacewalk Thoughts, 48.40 | Spacewalk Thoughts, 47.33 |
| 5 | Coffee Shop Stories, 31.10 | Gym Hero, 46.50 |

For most profiles, the new weights only shuffled neighbors. The results were different, not clearly better. I have no listener feedback to say which version is better. The sample output above uses my original weights.

**Tempo.** For a 180 BPM target, Midnight Coding (78 BPM) and Gym Hero (132 BPM) get zero tempo points. Storm Runner, at 152 BPM, gets 10 × (1 − 28/40) = 3 points. The tempo score drops in a straight line and stays at zero once the gap reaches 40 BPM.

**What happened with tempo and valence.** Tempo was already part of my score (up to 10 points), so I tested what it does by taking it out and changing nothing else. All six profiles kept the same five songs. Four of them kept the same order. Two moved a little:

- **High-Energy Pop:** Night Drive Loop and Storm Runner swapped 4th and 5th place. With tempo, Night Drive Loop led 33.25 to 31.45. Without it, Storm Runner led 28.20 to 27.00.
- **Genre and Mood Not in CSV:** Coffee Shop Stories moved up from 5th to 3rd. Focus Flow and Midnight Coding each dropped one place.

So tempo mostly breaks close calls. It never changed who made the top five. In Chill but Frantic it changed nothing at all, because no low-energy song is within 40 BPM of 180, so none of them earned tempo points. I did not add valence. None of my profiles has a valence target, so I have nothing to compare yet.

**How the system behaved for different types of users.**

- **Normal tastes (High-Energy Pop, Chill Lofi, Deep Intense Rock):** the songs I expected came out on top. The best scores were 97.35, 99.25 and 98.30.
- **A mood no song has (Energetic but Sad):** nothing could earn mood points, so the pop genre points and the energy decided the order. The best score was only 52.40.
- **A genre and mood the catalog lacks (Genre and Mood Not in CSV):** no song earned any category points, so energy and tempo decided. The best score was 39.40.
- **Conflicting tastes (Chill but Frantic):** the lofi and chill songs stayed on top even though their energy was far from 1.0. The best score was 72.60. A relaxed jazz song (31.10) even beat Storm Runner (30.30), whose energy was much closer, because its mood counted as similar to chill.
- **Every list stayed inside one energy group.** The catalog has no songs between 0.45 and 0.74 energy. Pop, Rock and Sad all got the same five songs and only the order changed.

---

## Limitations and Risks

My recommender is small and simple, and I expect this bias in it:

- **Labels count more than sound.** Genre and mood must match exactly, so a song labelled "indie pop" gets no genre credit for a pop fan even though it sounds similar. Mood alone is worth 40 of 100 points, so one label can outweigh a close fit on energy and tempo.

My recommendations depend on a small catalog that lacks medium-energy songs and several genres and moods. This limits the choices available to some listeners, even when the scoring works correctly. Adding popularity could favor mainstream songs, while detailed mood tags and lyrical themes could reflect my own interpretation rather than the listener’s. I would need listener feedback to check whether the added features improve recommendations.



---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

My biggest learning moment was realizing that a working algorithm does not always give the recommendations I expect. In RecomViber, Midnight Coding ranked first for a profile asking for chill lofi with very high energy and tempo. The calculation was correct, but my weights gave genre and mood more influence. This helped me understand how my design choices shape the results.

AI helped me write the loading and scoring functions, format the terminal output, and create profiles for testing. It also helped me explain unexpected rankings. However, I still needed to double-check its calculations and claims. Some explanations had incorrect arithmetic or conclusions that the results did not support.

I was surprised that a few simple rules could produce recommendations that felt reasonable. Changing the profile changed the results in understandable ways, even though the system was not learning from listening history. At the same time, testing unusual profiles showed how limited those rules could be.

If I continued this project, I would first add more songs, especially medium-energy songs and missing genres and moods. I would also collect listener feedback to test the weights instead of relying only on my judgment. Finally, I would make the output clearer when the catalog cannot closely match someone’s preferences.



