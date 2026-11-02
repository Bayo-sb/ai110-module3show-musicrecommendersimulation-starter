# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Extend RecomViber with five new song attributes (popularity, release decade, detailed mood tags, instrumentalness, lyrical themes). The attributes needed new CSV columns, loader conversions, optional user preferences and an extra scoring layer that only switches on when a preference is supplied.

**Prompts used:**

Extend RecomViber with five new song attributes. Ensure that you first inspect the current CSV, loader, profiles, and scoring functions.

Add these columns to `data/songs.csv`: popularity (integer 0 to 100), release_decade (integer such as 1990 or 2020), detailed_mood_tags (semicolon-separated tags), instrumentalness (float 0 to 1) and lyrical_themes (semicolon-separated tags).

Preserve existing songs and columns. Because these are fictional songs, clearly document the new values as synthetic demonstration data, not verified musical facts. Provide varied values suitable for testing.

Update the loader to convert numerical fields to their correct types and parse tag fields into normalized lists.

Add optional user preferences for all five attributes. Update `src/recommender.py` using this scoring design:

- Existing recommendation score: weight 70.
- Popularity match: weight 5.
- Release-decade match: weight 5.
- Detailed-mood match: weight 10.
- Instrumentalness match: weight 5.
- Lyrical-theme match: weight 5.

Express each component as a match between 0 and 1: existing score divided by 100; popularity `1 - abs(song_popularity - target_popularity) / 100`; decade 1 for an exact match, otherwise 0; instrumentalness `1 - abs(song_value - target_value)`; mood tags and lyrical themes as the fraction of the user's requested tags present in the song.

Calculate the final score as `100 * weighted_match_total / active_weight_total`. Only activate an advanced component when its preference is supplied. Empty tag preferences should be inactive. Profiles without advanced preferences must retain their original scores and rankings.

Preserve existing scoring modes and alphabetical tie-breaking. Explain each active component in the recommendation reasons.

Verify that existing profiles retain their results without advanced preferences, new preferences can change rankings, scores remain between 0 and 100, exact matches earn 100, and missing preferences and empty tag lists do not cause errors. Run `python -m src.main` with both existing and advanced profiles.

In `ai_interactions.md`, record this prompt, summarize the generated changes, and list the checks actually performed. Add a clearly labelled "Manual verification — pending" checklist for me to complete. Do not claim I performed checks myself. Update relevant documentation and sample output to reflect the final behavior. Show the changes and actual verification results. Do not commit yet.

**What did the agent generate or change?**

- `data/songs.csv`: appended five columns to all 10 songs. The first ten columns were not changed. The values are varied for testing (decades 1990 to 2020, popularity 34 to 90, instrumentalness 0.02 to 0.95).
- `src/recommender.py`:
  - `load_songs` converts `popularity` and `release_decade` to integers and `instrumentalness` to a float. It splits `detailed_mood_tags` and `lyrical_themes` into lowercase, trimmed lists. A missing column or value becomes `None` or an empty list.
  - The old `score_song` became `_core_score`, with its logic unchanged.
  - A new `score_song` wraps it. It switches on each advanced component only when its preference is supplied, and returns the original score and reasons untouched when none are.
  - New constants `CORE_WEIGHT` (70) and `ADVANCED_WEIGHTS`, and helpers `_split_tags` and `_tag_match`.
  - `recommend_songs` was not changed, so ranking and alphabetical tie-breaking are the same.
- `src/main.py`: three new profiles ("Advanced: Study Session", "Advanced: Chart-Topping Workout", "Advanced: Retro Night Drive") and a line that prints the advanced preferences above each table.
- `README.md`: an "Optional advanced preferences" section and a regenerated sample output with all nine profiles.
- `model_card.md`: the data section (fifteen columns) and the algorithm section (advanced preferences).
- Preference keys: `target_popularity`, `target_release_decade`, `preferred_mood_tags`, `target_instrumentalness`, `preferred_lyrical_themes`.
- Left alone: the `Song` and `UserProfile` classes and the `Recommender` class (still a placeholder). The advanced preferences work through the dictionary profiles that `main.py` uses.

**What did you verify or fix manually?**

 I reviewed the results and confirm the followings

1. **Loader types.** Song 1 loads with `popularity` and `release_decade` as integers, `instrumentalness` as a float, and both tag fields as lists. A multi-word tag like "city life" stays whole.
2. **Existing profiles unchanged.** For all six original profiles, the titles, order, scores and reasons were identical to the code from before the change. Claude compared them exactly against a saved copy of the old file.
3. **Rankings can change.**
   - "Study Session" swapped the top two: Midnight Coding 97.50 moved ahead of Library Rain 94.33.
   - "Retro Night Drive" brought Midnight Coding into the top five in place of Gym Hero.
   - "Chart-Topping Workout" kept the same order and only the scores changed, so not every advanced profile reorders anything.


---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
