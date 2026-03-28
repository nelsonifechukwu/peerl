"""
Study content: Priming texts, quizzes, challenge questions
All content is conceptual - no programming knowledge required
"""

CONTENT = {
    "lazy_eager_evaluation": {
        "title": "Lazy vs Eager Evaluation",
        "priming_text": """
**Lazy vs Eager Evaluation: When to load data all-at-once vs on-demand**

Imagine organizing a massive library with millions of books. You have two approaches:

**Eager Approach:** Catalog every single book upfront before opening to the public. This means:
- You do MORE WORK INITIALLY (cataloging everything)
- But FAST LOOKUPS later (everything's already organized)
- Requires LOTS OF STORAGE for the complete catalog

**Lazy Approach:** Only catalog books when visitors actually request them. This means:
- LESS WORK INITIALLY (only catalog what's needed)
- But SLOWER for each individual request (need to catalog on-the-fly)
- Requires LESS STORAGE (only catalog what's been requested)

**Real-World Example:**
A streaming service has 100,000 movies, but most users only watch 5-10 per month.
- **Eager:** Load information about all 100,000 movies when user opens app (slow start, but smooth browsing)
- **Lazy:** Load each movie's information only when user scrolls to it (fast start, but slight delay per movie)

**Key Tradeoff:** Eager uses more resources upfront for faster access later. Lazy saves resources upfront but pays the cost each time something is accessed.
        """,
        "challenge_question": """
**Challenge Question:**

A research team is analyzing climate data from 50,000 weather stations over 100 years (5 million total data points). Their typical analysis only looks at data from 10 specific stations in a given time period (about 100 data points at a time).

Should they use **eager evaluation** (load all 5 million points at once) or **lazy evaluation** (load data points only as they're needed for each analysis)?

**Consider:**
- How much memory is available?
- How often will different parts of the data be accessed?
- Is startup time or per-request speed more important?

Discuss as a group: What would you recommend and why?
        """,
        "quiz": [
            {
                "id": 1,
                "question": "Which approach uses MORE MEMORY initially?",
                "options": {
                    "A": "Eager evaluation",
                    "B": "Lazy evaluation",
                    "C": "Both use the same memory",
                    "D": "It depends on the access pattern"
                },
                "correct": "A",
                "explanation": "Eager evaluation loads everything upfront, using more memory initially."
            },
            {
                "id": 2,
                "question": "When is lazy evaluation most beneficial?",
                "options": {
                    "A": "When you need all data immediately",
                    "B": "When you only need a small portion of available data",
                    "C": "When memory is unlimited",
                    "D": "When data never changes"
                },
                "correct": "B",
                "explanation": "Lazy evaluation shines when you only need a fraction of available data, avoiding unnecessary work."
            },
            {
                "id": 3,
                "question": "A video platform loads the entire video file before playback starts. This is an example of:",
                "options": {
                    "A": "Lazy evaluation - loading as needed",
                    "B": "Eager evaluation - loading everything upfront",
                    "C": "Neither - this is caching",
                    "D": "Both approaches combined"
                },
                "correct": "B",
                "explanation": "Loading the entire file before playback is eager evaluation."
            },
            {
                "id": 4,
                "question": "Which statement is TRUE about eager evaluation?",
                "options": {
                    "A": "Always faster than lazy in every scenario",
                    "B": "Uses less memory than lazy evaluation",
                    "C": "Has slower startup but faster subsequent access",
                    "D": "Never useful in modern systems"
                },
                "correct": "C",
                "explanation": "Eager pays cost upfront (slower startup) for faster access later."
            },
            {
                "id": 5,
                "question": "For the climate data scenario (50,000 stations, analyzing only 10 at a time), which approach is better?",
                "options": {
                    "A": "Eager - load all 5 million data points",
                    "B": "Lazy - load only the needed data points",
                    "C": "Both are equally good",
                    "D": "Neither would work for this amount of data"
                },
                "correct": "B",
                "explanation": "Since only 100 out of 5 million points are needed per analysis, lazy evaluation avoids loading 4,999,900 unnecessary points."
            },
            {
                "id": 6,
                "question": "What is the PRIMARY tradeoff between lazy and eager evaluation?",
                "options": {
                    "A": "Security vs speed",
                    "B": "Initial resource use vs ongoing access cost",
                    "C": "Accuracy vs approximation",
                    "D": "Simplicity vs complexity"
                },
                "correct": "B",
                "explanation": "The core tradeoff is paying costs upfront (eager) versus paying per-access (lazy)."
            }
        ]
    },
    "shared_independent_parallelism": {
        "title": "Shared-Memory vs Independent Parallelism",
        "priming_text": """
**Shared-Memory vs Independent Parallelism: When tasks should communicate vs run separately**

Imagine a restaurant kitchen during dinner rush. You need to prepare 100 meals quickly. How should your team work?

**Shared-Memory Parallelism (Shared Workspace):**
- All chefs work in ONE KITCHEN, sharing the same ingredients, tools, and workspace
- They can SEE what others are doing and COORDINATE in real-time
- If one chef updates the recipe, everyone immediately knows
- **Risk:** Chefs might bump into each other or fight over the same knife
- **Benefit:** Easy coordination when tasks need to interact

**Independent Parallelism (Separate Kitchens):**
- Each chef works in their OWN SEPARATE KITCHEN with their own supplies
- They CAN'T see or interfere with each other
- If one chef finds a better technique, others don't automatically know
- **Benefit:** No conflicts - each chef works at full speed without interruptions
- **Risk:** Hard to coordinate if tasks need to share results

**Real-World Example:**
A company needs to process 1,000 customer orders:

- **Shared-Memory:** All workers access the SAME customer database. When one updates a customer's address, everyone sees it immediately. But workers might conflict when trying to update the same record at the same time.

- **Independent:** Each worker gets their OWN COPY of 100 customers. No conflicts since everyone works on different data. But if customer info changes, copies might be out of sync.

**Key Tradeoff:** Shared-memory makes coordination easy but creates conflicts. Independent parallelism avoids conflicts but makes sharing results harder.
        """,
        "challenge_question": """
**Challenge Question:**

A news website needs to analyze 10,000 articles to find trending topics. They have two approaches:

**Approach A (Shared-Memory):**
- 10 analysts share ONE MASTER LIST of trending words
- Each analyst reads articles and updates the shared list
- Everyone can see the current trending topics in real-time
- When one person adds "climate change" to the list, all others immediately see it

**Approach B (Independent):**
- Each of the 10 analysts gets 1,000 articles and their OWN separate trending word list
- They work completely independently with no coordination
- At the end, all 10 lists are combined

Discuss as a group:
- Which approach finishes faster? Why?
- Which approach is easier to implement?
- What problems might each approach encounter?
- Which would YOU recommend for this scenario?
        """,
        "quiz": [
            {
                "id": 1,
                "question": "In shared-memory parallelism, what is the main ADVANTAGE?",
                "options": {
                    "A": "No conflicts between tasks",
                    "B": "Tasks can easily communicate and coordinate",
                    "C": "Always faster than independent parallelism",
                    "D": "Requires less total memory"
                },
                "correct": "B",
                "explanation": "Shared-memory makes it easy for tasks to see each other's work and coordinate."
            },
            {
                "id": 2,
                "question": "In independent parallelism, what is the main ADVANTAGE?",
                "options": {
                    "A": "Easier to share data between tasks",
                    "B": "No risk of conflicts since each task is isolated",
                    "C": "Uses less total memory",
                    "D": "Always faster execution"
                },
                "correct": "B",
                "explanation": "Independent tasks can't interfere with each other, eliminating conflicts."
            },
            {
                "id": 3,
                "question": "For the news article scenario (10 analysts, 10,000 articles), what is a problem with Approach A (shared-memory)?",
                "options": {
                    "A": "Analysts can't see each other's findings",
                    "B": "Analysts might conflict when updating the shared trending word list",
                    "C": "It requires more total memory",
                    "D": "It's impossible to combine results"
                },
                "correct": "B",
                "explanation": "With shared access, multiple analysts might try to update the same word's count simultaneously, creating conflicts."
            },
            {
                "id": 4,
                "question": "For the news article scenario, what is a problem with Approach B (independent)?",
                "options": {
                    "A": "Analysts will conflict when accessing articles",
                    "B": "Requires combining 10 separate lists at the end",
                    "C": "Uses less memory so results are less accurate",
                    "D": "Analysts can see each other's work in real-time"
                },
                "correct": "B",
                "explanation": "Independent parallelism requires an extra step to merge all the separate results."
            },
            {
                "id": 5,
                "question": "When would shared-memory parallelism be MOST appropriate?",
                "options": {
                    "A": "When tasks need to frequently share and update common data",
                    "B": "When tasks are completely independent",
                    "C": "When you want to avoid all coordination",
                    "D": "When memory is extremely limited"
                },
                "correct": "A",
                "explanation": "Shared-memory shines when tasks need to coordinate and share data frequently."
            },
            {
                "id": 6,
                "question": "What is the PRIMARY tradeoff between these two approaches?",
                "options": {
                    "A": "Speed vs accuracy",
                    "B": "Easy coordination vs avoiding conflicts",
                    "C": "Memory usage vs CPU usage",
                    "D": "Simplicity vs complexity"
                },
                "correct": "B",
                "explanation": "Shared-memory makes coordination easy but creates potential conflicts. Independent avoids conflicts but makes coordination harder."
            }
        ]
    }
}
