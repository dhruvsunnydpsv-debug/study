
Everything is contained in one file – easy to host on GitHub Pages, Netlify, or any static server.

---

## 🔧 Technical Details

- **Frontend:** Vanilla HTML5, CSS3 (with CSS variables, grid, flexbox), JavaScript (ES6).
- **Fonts:** Google Fonts (Inter, Noto Serif, Noto Sans Devanagari).
- **Database:** [Supabase](https://supabase.com/) – a PostgreSQL‑based backend. The app uses the public anon key to read from the `question_bank` table.
- **CBSE Blueprints:** Hardcoded JavaScript objects for each subject, defining section structure, marks, and instructions.

### Database Schema (expected by the app)

The app queries a table named `question_bank` with at least these columns:

| Column          | Type   | Description                                |
|-----------------|--------|--------------------------------------------|
| `id`            | int    | Primary key                                |
| `subject`       | text   | Subject name (e.g. "Maths", "Science")     |
| `difficulty`    | text   | "Easy", "Medium", "Hard"                   |
| `question_text` | text   | The full question (may contain `[Image: URL]` or `[Figure: URL]`) |
| `image_url`     | text   | Optional direct image URL                   |
| `answer`        | text   | Suggested answer (for the answer key)       |

The app also supports composite subject names like `Maths_9` if you want to separate by grade.

---

## 🧪 Customization

- **Change the question bank:**  
  Replace the Supabase URL and anon key in the `db` variable with your own project credentials.  
  Make sure your `question_bank` table matches the expected schema.

- **Modify blueprints:**  
  Edit the `BLUEPRINTS` object inside the `<script>` tag to adjust section counts, marks, or instructions.

- **Add more subjects:**  
  Add a new entry to `BLUEPRINTS` and a corresponding button in the subject grid.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).  
Feel free to use, modify, and distribute it as you like.

---

## 🙏 Acknowledgements

- [Supabase](https://supabase.com/) for the generous free tier and easy‑to‑use database.
- Google Fonts for the beautiful typefaces.
- The CBSE board for providing clear exam patterns (blueprints used are based on public documents).

---

## 📬 Contact

For questions or suggestions, please open an issue on GitHub or reach out directly.
