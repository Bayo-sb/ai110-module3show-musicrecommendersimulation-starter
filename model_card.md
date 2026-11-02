# 🎧 Model Card: RecomViber

## 1. Model Name

**RecomViber**

It is a small music recommender I built for a class project. It runs in the terminal.

---

## 2. Goal / Task

RecomViber recommends songs.

You tell it four things:

- your favorite genre
- your favorite mood
- how much energy you want
- the tempo you like

It scores every song in the catalog against those four things. Then it shows the best matches and the reasons behind each score.

I run it with `python -m src.main`. It tries six sample listeners and prints the top five songs for each one.

---

## 3. Data Used

**Size.** The catalog has 10 songs. I checked the count in `data/songs.csv`.
**Columns.** Each song has fifteen columns. The first ten are `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability` and `acousticness`. I added five more: `popularity` (0 to 100), `release_decade`, `detailed_mood_tags`, `instrumentalness` (0 to 1) and `lyrical_themes`. The two tag columns hold tags separated by semicolons.

**What I use for scoring.** Four columns every time: `genre`, `mood`, `energy` and `tempo_bpm`. The five new columns count only when the user asks for them (see section 4).

**What I use for other things.** `title` breaks ties and is shown in the results. `artist` is shown in the results.

**What I don't use.** `valence`, `danceability`, `acousticness` and `id`.

**What the catalog covers.**

- **Genres:** 7. Lofi has 3 songs and pop has 2. Ambient, indie pop, jazz, rock and synthwave have 1 each.
- **Moods:** 6. Chill has 3 songs. Happy and intense have 2 each. Focused, moody and relaxed have 1 each.
- **Energy:** the songs fall into two groups. Five songs sit between 0.28 and 0.42. Five sit between 0.75 and 0.93. No song sits between 0.45 and 0.74.
- **Tempo:** from 60 to 152 BPM.
- **Artists:** Neon Echo and LoRoom each have two songs.

**What's missing.** The catalog has no classical, no country and no hip hop. It has no sad or melancholy songs. It has no mid-energy songs. Ten songs is also very small. A top-five list is half the catalog.

---

## 4. Algorithm Summary

Every song gets a score out of 100. The songs with the highest scores are recommended.

I use the original weights and tested a second set temporarily.

### My original weights (my main design)

A song earns points like this:

- **Mood: up to 40.** An exact match earns 40. A different mood in the group "chill, relaxed, focused" earns 20. Anything else earns 0.
- **Genre: up to 20.** An exact match earns 20. Anything else earns 0.
- **Energy: up to 30.** The closer the song's energy is to the target, the more points it earns. An exact match earns all 30. Points drop in a straight line as the gap grows.
- **Tempo: up to 10.** The closer the tempo is to the target, the more points it earns. Points drop in a straight line as the gap grows. They reach zero at 40 BPM away and stay at zero after that.

I add the points up. I rank the songs from highest to lowest. If two songs tie, the one that comes first alphabetically by title goes first. I return the top few and say why each one scored the way it did. Capital letters and extra spaces don't matter when I compare text.

I gave mood more weight than genre. In my catalog, mood says more about how a song sounds. Five of my seven genres have only one song.

### Optional advanced preferences

A user can also ask for any of five extra things. Each one switches on only when it is supplied, and an empty tag list switches it off.

- **Popularity (weight 5):** 1 minus the gap in popularity divided by 100.
- **Release decade (weight 5):** 1 for the same decade, otherwise 0.
- **Detailed mood tags (weight 10):** the fraction of the tags the user asked for that the song has.
- **Instrumentalness (weight 5):** 1 minus the gap in instrumentalness.
- **Lyrical themes (weight 5):** the fraction of the themes the user asked for that the song has.

The score from above counts too. I divide it by 100 and give it a weight of 70. Then the final score is `100 × (sum of weight × match) ÷ (sum of the weights that are switched on)`.

With no advanced preferences, the original score is returned untouched. I checked this for all six of my original profiles. The scores, the order and the reasons were identical to the code before this change.

### My experimental weights (temporary)

I wanted to see how much my weights matter. So I changed them for one experiment:

- Genre dropped from 20 to 10.
- Energy went up from 30 to 60.
- Mood and tempo stayed the same.

The points now add up to 120, so I rescale the total with `raw × 100 ÷ 120`. A perfect match still scores 100.

**The code uses my original weights.** I ran the experiment temporarily and then took it back out. It is not in the code now. The experiment used genre 10, energy up to 60 and a total of 120 points.

### What I picked by hand

I picked all the weights by hand. I also picked the group "chill, relaxed, focused" by hand. I did not tune any of it on real listeners.

RecomViber does not learn from listening history. It only uses what the user types in.

---

## 5. Observed Behavior / Biases

These are patterns I saw in my results.

**The catalog has two energy groups.**

- Under my original weights, all six top-five lists came from one group. Under the experimental weights, five of six did.
- The three high-energy profiles (Pop, Rock and Sad) all got the same five songs. Only the order changed. The catalog has five songs with energy of 0.75 or higher.
- The five songs in the group "chill, relaxed, focused" are the same five low-energy songs. For these listeners, the mood credit and the energy score both push toward the same songs.

**Exact matching depends on labels.** "Indie pop" does not match "pop". Rooftop Lights gets no genre points for a pop fan, even if it sounds similar.

**Some listeners get more help from mood.**

- A chill, relaxed or focused listener can earn mood points on 5 of 10 songs.
- A happy or intense listener can earn them on 2 of 10.
- A moody listener can earn them on 1 of 10.
- Nobody can earn mood points for "sad" or "melancholy".

**Missing categories.** "Classical" and "melancholy" match no song. Those profiles receive no genre or mood match points, so recommendations depend entirely on energy and tempo. The "classical, melancholy" profile still got a top score of 39.40 under my original weights and 57.33 under the experimental ones. Nothing matched its categories, but the scores did not look like zero.

**Categories can beat numbers.** Under my original weights, a song with the right category can beat a song with closer numbers. In "Chill but Frantic" the target energy is 1.0. Coffee Shop Stories (energy 0.37, relaxed) scored 31.10. Storm Runner (energy 0.91) scored 30.30. Storm Runner was much closer on the numbers. Coffee Shop Stories won because its mood counted as similar to chill.

**Numbers can beat categories too.** Under the experimental weights, the same profile put Storm Runner (48.00) ahead of Coffee Shop Stories. Storm Runner even came in ahead of the chill song Spacewalk Thoughts (47.33). Which result is "right" depends on what the user meant.

**Why Gym Hero shows up for a happy pop listener.** Its mood is intense, so it earns 0 mood points. It still earns points for the rest. Under my original weights for High-Energy Pop, it got 20 for genre, 27.60 for energy and 8.25 for tempo. That is 55.85, which is third. Only three songs are labelled pop or happy, so it fills third place.

**Tempo.** The tempo score drops steadily to a floor of zero. At a 180 BPM target, Midnight Coding (78 BPM) and Gym Hero (132 BPM) get 0 tempo points. Storm Runner (152 BPM) gets 3.
**Scores are preference points, not probabilities.** A score of 72.60 is not a 72.6% chance that someone will like the song. It only shows how well the song fits what the user typed in, compared with the other songs.

**What looked fine.** For the three baseline profiles (Pop, Lofi and Rock), the songs on top were the ones I expected. That is my judgment. It is not a measure of accuracy.

---

## 6. Evaluation Process

I did not test with real listeners. I did not collect feedback. Everything below is what I ran on my 10 songs.

### The six profiles

| Profile | Preferences | What it tests |
|---|---|---|
| High-Energy Pop | pop, happy, energy 0.85, 125 BPM | A normal listener whose taste matches songs in the catalog |
| Chill Lofi | lofi, chill, energy 0.35, 75 BPM | A calm listener, and whether similar-mood credit shows up |
| Deep Intense Rock | rock, intense, energy 0.95, 150 BPM | Extreme targets at the edge of the catalog |
| Energetic but Sad | pop, sad, energy 0.95, 160 BPM | A mood that no song has |
| Genre and Mood Not in CSV | classical, melancholy, energy 0.30, 60 BPM | Missing genre and mood together |
| Chill but Frantic | lofi, chill, energy 1.0, 180 BPM | Categories that fight with the numbers |

### Top five under my original weights

| Profile | Top five (score) |
|---|---|
| High-Energy Pop | Sunrise City 97.35, Rooftop Lights 77.05, Gym Hero 55.85, Night Drive Loop 33.25, Storm Runner 31.45 |
| Chill Lofi | Library Rain 99.25, Midnight Coding 97.15, Focus Flow 77.25, Spacewalk Thoughts 74.15, Coffee Shop Stories 55.65 |
| Deep Intense Rock | Storm Runner 98.30, Gym Hero 74.90, Sunrise City 28.10, Rooftop Lights 27.80, Night Drive Loop 24.00 |
| Energetic but Sad | Gym Hero 52.40, Sunrise City 46.10, Storm Runner 36.80, Rooftop Lights 25.30, Night Drive Loop 24.00 |
| Genre and Mood Not in CSV | Spacewalk Thoughts 39.40, Library Rain 35.50, Focus Flow 32.00, Midnight Coding 31.90, Coffee Shop Stories 30.40 |
| Chill but Frantic | Midnight Coding 72.60, Library Rain 70.50, Focus Flow 52.00, Spacewalk Thoughts 48.40, Coffee Shop Stories 31.10 |

### The sensitivity experiment

I reran all six profiles with my experimental weights. I kept the profiles, the data, the mood group and the tie-breaking the same.

- An exact match scored 100. Across all six profiles and all 10 songs, scores stayed between 16.50 and 99.38.
- **High-Energy Pop and Deep Intense Rock:** same five songs, same order.
- **Chill Lofi:** Spacewalk Thoughts moved up from 4th to 3rd. Focus Flow dropped to 4th.
- **Energetic but Sad:** Storm Runner moved up from 3rd to 2nd. Sunrise City dropped to 3rd.
- **Genre and Mood Not in CSV:** Coffee Shop Stories moved up from 5th to 4th. Midnight Coding dropped to 5th. They now tie at 48.58, and the title order decides it.
- **Chill but Frantic:** the top two stayed the same, but their scores fell. Storm Runner (48.00) and Gym Hero (46.50) came in. Focus Flow and Coffee Shop Stories dropped out.

| Rank | Chill but Frantic, original weights | Chill but Frantic, experimental weights |
|---|---|---|
| 1 | Midnight Coding, 72.60 | Midnight Coding, 62.67 |
| 2 | Library Rain, 70.50 | Library Rain, 59.17 |
| 3 | Focus Flow, 52.00 | Storm Runner, 48.00 |
| 4 | Spacewalk Thoughts, 48.40 | Spacewalk Thoughts, 47.33 |
| 5 | Coffee Shop Stories, 31.10 | Gym Hero, 46.50 |

For most profiles, the new weights only shuffled neighbors. The results were different, not clearly better. I have no listener feedback to say which version is better.

### Comparing every pair of profiles

I compared all 15 pairs of profiles under my original weights. "Shared" means how many of the five songs appear in both lists.

| Profiles compared | What changed | Why |
|---|---|---|
| High-Energy Pop vs Chill Lofi | 0 shared. #1 is Sunrise City vs Library Rain. | One wants energy 0.85 and the other wants 0.35. The catalog's songs are all 0.75 or higher, or 0.42 or lower. The mood and genre points land on different songs too. |
| High-Energy Pop vs Deep Intense Rock | Same five songs, none in the same place. Storm Runner goes from #5 (31.45) to #1 (98.30). | Both want high energy. The catalog has five songs with energy of 0.75 or higher, so both lists hold all five. Rock's category points go to Storm Runner (60) and Gym Hero (40). Pop's go to Sunrise City (60) and Rooftop Lights (40). |
| High-Energy Pop vs Energetic but Sad | Same five songs, none in the same place. Gym Hero goes from #3 to #1 (52.40). Sunrise City drops from #1 (97.35) to #2 (46.10). | No song is "sad", so Sunrise City loses its 40 mood points. Gym Hero and Sunrise City both still get 20 genre points for pop. Gym Hero's energy (0.93) is closer to 0.95. |
| High-Energy Pop vs Genre and Mood Not in CSV | 0 shared. #1 is Sunrise City vs Spacewalk Thoughts. | They sit in opposite energy groups. The second one gets no category points at all. |
| High-Energy Pop vs Chill but Frantic | 0 shared. #1 is Sunrise City vs Midnight Coding. | Frantic wants lofi and chill, so those songs get 60 category points. That keeps low-energy songs on top even though they are far from its energy target of 1.0. |
| Chill Lofi vs Deep Intense Rock | 0 shared. #1 is Library Rain vs Storm Runner. | Opposite energy groups. The category points go to lofi/chill songs for one and rock/intense songs for the other. |
| Chill Lofi vs Energetic but Sad | 0 shared. #1 is Library Rain vs Gym Hero. | Energy 0.35 vs 0.95. For Energetic but Sad, only genre can earn category points; energy and tempo still contribute. |
| Chill Lofi vs Genre and Mood Not in CSV | Same five songs. Two stay in place (Focus Flow #3, Coffee Shop Stories #5). Spacewalk Thoughts goes from #4 to #1 (39.40). Midnight Coding goes from #2 to #4. | Both want low energy. Chill Lofi has categories that separate the songs. The other one has none, so energy and tempo decide. Spacewalk Thoughts (energy 0.28, exactly 60 BPM) earns 29.40 for energy and the full 10 for tempo. |
| Chill Lofi vs Chill but Frantic | Same five songs. Three stay in place. Only Library Rain and Midnight Coding swap #1 and #2. | Their category points are identical. Frantic's energy target of 1.0 gives Midnight Coding (0.42) 12.60 energy points and Library Rain (0.35) 10.50, so Midnight Coding comes out ahead (72.60 vs 70.50). |
| Deep Intense Rock vs Energetic but Sad | Same five songs. Two stay in place (Rooftop Lights #4, Night Drive Loop #5). Storm Runner drops from #1 to #3. | Rock gives Storm Runner 60 category points and Gym Hero 40. "Sad" gives no mood points. The pop genre match gives Gym Hero and Sunrise City 20 points each, which lifts them above Storm Runner (36.80). |
| Deep Intense Rock vs Genre and Mood Not in CSV | 0 shared. #1 is Storm Runner vs Spacewalk Thoughts. | High energy and 150 BPM vs low energy and 60 BPM. Rock has category matches. The other one has none. |
| Deep Intense Rock vs Chill but Frantic | 0 shared. #1 is Storm Runner vs Midnight Coding. | Rock's list is all high-energy songs. Frantic's lofi/chill category points keep low-energy songs on top. |
| Energetic but Sad vs Genre and Mood Not in CSV | 0 shared. #1 is Gym Hero vs Spacewalk Thoughts. | Neither profile gets mood points. "Pop" still matches two songs for Energetic but Sad. "Classical" matches none. So the second list comes from energy and tempo only. |
| Energetic but Sad vs Chill but Frantic | 0 shared. #1 is Gym Hero vs Midnight Coding. | One list is all high-energy songs and the other is all low-energy songs. Frantic's lofi/chill category points decide its list. |
| Genre and Mood Not in CSV vs Chill but Frantic | Same five songs. Three stay in place (Library Rain #2, Focus Flow #3, Coffee Shop Stories #5). Spacewalk Thoughts goes from #1 to #4. Midnight Coding goes from #4 to #1. | Frantic gives Midnight Coding and Library Rain 60 category points even with poor energy. The other profile gives no song any. |

---

## 7. Intended Use and Non-Intended Use

**Intended use.** RecomViber shows how a simple recommender can turn preferences into scores and a ranked list. It is good for learning, for testing ideas and for seeing how weights change results.

**Not intended for:**

- Reliably predicting what someone will enjoy without listener testing.
- Making decisions about artists, since it only holds a few made-up songs.



---

## 8. Ideas for Improvement

1. **Expand the catalog.** Add more songs for each genre and mood, and add songs between 0.45 and 0.74 energy. Right now two energy groups limit the variety. I could also try optional diversity controls. But forcing energetic songs into a calm playlist could weaken its fit.
2.  **Explain preferences it can't match well.** If someone asks for a mood or genre that no song has, RecomViber should say so. It could also warn when preferences fight each other, like chill music at maximum energy. That would make the results easier to understand.
