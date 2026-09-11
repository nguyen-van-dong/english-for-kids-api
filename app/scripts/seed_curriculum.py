import os
import sys

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import SessionLocal
from app.models.curriculum import Category, VocabularyWord, AlphabetLesson
from app.models.games import QuizQuestion, SpellingWord, SpeakingChallenge
from app.models.gamification import AchievementBadge, AvatarCharacter, StickerItem
from app.models.cms import HomeBanner, DailyQuest, AppSetting, ContentVersion

def seed():
    db = SessionLocal()
    print("🌱 Seeding English for Kids Database...")

    try:
        # =========================================================================
        # 1. CATEGORIES
        # =========================================================================
        categories_data = [
            {"id": "animals", "title": "Animals & Pets", "description": "Explore the amazing animal kingdom!", "icon": "paw", "color": "#FF9671", "light_color": "#FFF0EB", "order_index": 1},
            {"id": "fruits", "title": "Fruits & Food", "description": "Yummy fruits, vegetables, and snacks!", "icon": "nutrition", "color": "#6BCB77", "light_color": "#EBFBEE", "order_index": 2},
            {"id": "colors", "title": "Colors & Shapes", "description": "Rainbow colors and cool geometric shapes!", "icon": "color-palette", "color": "#845EC2", "light_color": "#F3ECF8", "order_index": 3},
            {"id": "numbers", "title": "Numbers (1 - 20)", "description": "Learn to count easily and have fun!", "icon": "calculator", "color": "#4D96FF", "light_color": "#E8F1FF", "order_index": 4},
            {"id": "school", "title": "School & House", "description": "Items around your classroom and home!", "icon": "school", "color": "#00C9A7", "light_color": "#E6FAF6", "order_index": 5},
            {"id": "body", "title": "Body & Feelings", "description": "Parts of the human body and emotions!", "icon": "happy", "color": "#FF6F91", "light_color": "#FFEBF1", "order_index": 6},
        ]
        for c in categories_data:
            if not db.query(Category).filter(Category.id == c["id"]).first():
                db.add(Category(**c))
        db.commit()
        print(f"✅ Categories seeded ({len(categories_data)})")

        # =========================================================================
        # 2. VOCABULARY WORDS
        # =========================================================================
        words_data = [
            # Animals
            {"id": "anim_1", "category_id": "animals", "word": "Lion", "phonetic": "/ˈlaɪ.ən/", "emoji": "🦁", "example_sentence": "The lion roars loudly in the savanna.", "fun_fact": "Lions live in family groups called prides!", "difficulty_level": "easy", "order_index": 1},
            {"id": "anim_2", "category_id": "animals", "word": "Elephant", "phonetic": "/ˈel.ə.fənt/", "emoji": "🐘", "example_sentence": "An elephant can spray water with its trunk.", "fun_fact": "Elephants are the largest land animals on Earth!", "difficulty_level": "medium", "order_index": 2},
            {"id": "anim_3", "category_id": "animals", "word": "Monkey", "phonetic": "/ˈmʌŋ.ki/", "emoji": "🐵", "example_sentence": "The cheerful monkey loves yellow bananas.", "fun_fact": "Monkeys use their tails for balance when jumping.", "difficulty_level": "easy", "order_index": 3},
            {"id": "anim_4", "category_id": "animals", "word": "Dolphin", "phonetic": "/ˈdɒl.fɪn/", "emoji": "🐬", "example_sentence": "Friendly dolphins leap out of the ocean waves.", "fun_fact": "Dolphins are super smart and communicate using clicks!", "difficulty_level": "hard", "order_index": 4},
            {"id": "anim_5", "category_id": "animals", "word": "Giraffe", "phonetic": "/dʒɪˈrɑːf/", "emoji": "🦒", "example_sentence": "The giraffe reaches the highest green leaves.", "fun_fact": "A giraffe neck can be over 6 feet long!", "difficulty_level": "medium", "order_index": 5},
            {"id": "anim_6", "category_id": "animals", "word": "Puppy", "phonetic": "/ˈpʌp.i/", "emoji": "🐶", "example_sentence": "The cute puppy loves playing fetch with a ball.", "fun_fact": "Puppies love to take cozy naps after playing.", "difficulty_level": "easy", "order_index": 6},
            {"id": "anim_7", "category_id": "animals", "word": "Kitten", "phonetic": "/ˈkɪt.ən/", "emoji": "🐱", "example_sentence": "The soft kitten purrs when you pet it.", "fun_fact": "Kittens have very sharp hearing!", "difficulty_level": "easy", "order_index": 7},
            {"id": "anim_8", "category_id": "animals", "word": "Penguin", "phonetic": "/ˈpeŋ.ɡwɪn/", "emoji": "🐧", "example_sentence": "Penguins waddle cutely across the snowy ice.", "fun_fact": "Penguins cannot fly in the air, but they fly underwater!", "difficulty_level": "medium", "order_index": 8},

            # Fruits
            {"id": "fruit_1", "category_id": "fruits", "word": "Apple", "phonetic": "/ˈæp.əl/", "emoji": "🍎", "example_sentence": "The crunchy red apple is sweet and juicy.", "fun_fact": "Apples float in water because 25% of their volume is air!", "difficulty_level": "easy", "order_index": 1},
            {"id": "fruit_2", "category_id": "fruits", "word": "Banana", "phonetic": "/bəˈnɑː.nə/", "emoji": "🍌", "example_sentence": "Peel the bright yellow banana before eating.", "fun_fact": "Bananas are rich in potassium and give you lots of energy.", "difficulty_level": "easy", "order_index": 2},
            {"id": "fruit_3", "category_id": "fruits", "word": "Strawberry", "phonetic": "/ˈstrɔː.bər.i/", "emoji": "🍓", "example_sentence": "Fresh sweet strawberries make tasty smoothies.", "fun_fact": "Strawberries are the only fruit with seeds on the outside!", "difficulty_level": "medium", "order_index": 3},
            {"id": "fruit_4", "category_id": "fruits", "word": "Watermelon", "phonetic": "/ˈwɔː.təˌmel.ən/", "emoji": "🍉", "example_sentence": "Cold watermelon is the best snack on a hot sunny day.", "fun_fact": "Watermelon is over 90% fresh water!", "difficulty_level": "medium", "order_index": 4},
            {"id": "fruit_5", "category_id": "fruits", "word": "Pizza", "phonetic": "/ˈpiːt.sə/", "emoji": "🍕", "example_sentence": "We shared a hot cheese pizza for dinner.", "fun_fact": "Pizza was invented hundreds of years ago in Italy!", "difficulty_level": "easy", "order_index": 5},
            {"id": "fruit_6", "category_id": "fruits", "word": "Ice Cream", "phonetic": "/ˈaɪs ˌkriːm/", "emoji": "🍦", "example_sentence": "I love strawberry ice cream on a waffle cone.", "fun_fact": "Vanilla is the most popular ice cream flavor in the world.", "difficulty_level": "easy", "order_index": 6},

            # Colors
            {"id": "col_1", "category_id": "colors", "word": "Red", "phonetic": "/red/", "emoji": "🔴", "example_sentence": "The fire truck is painted bright red.", "fun_fact": "Red is the color of ripe strawberries and rubies!", "difficulty_level": "easy", "order_index": 1},
            {"id": "col_2", "category_id": "colors", "word": "Blue", "phonetic": "/bluː/", "emoji": "🔵", "example_sentence": "The clear sky and deep ocean are blue.", "fun_fact": "Blue is one of the three primary colors!", "difficulty_level": "easy", "order_index": 2},
            {"id": "col_3", "category_id": "colors", "word": "Yellow", "phonetic": "/ˈjel.əʊ/", "emoji": "🟡", "example_sentence": "Sunflowers and the morning sun are yellow.", "fun_fact": "Yellow is the brightest color human eyes can see!", "difficulty_level": "easy", "order_index": 3},
            {"id": "col_4", "category_id": "colors", "word": "Green", "phonetic": "/ɡriːn/", "emoji": "🟢", "example_sentence": "The garden grass and tree leaves are green.", "fun_fact": "Mixing blue and yellow makes the color green!", "difficulty_level": "easy", "order_index": 4},
            {"id": "col_5", "category_id": "colors", "word": "Star", "phonetic": "/stɑːr/", "emoji": "⭐", "example_sentence": "Look at the glowing golden star at night.", "fun_fact": "A five-pointed star is a classic symbol of success!", "difficulty_level": "easy", "order_index": 5},
            {"id": "col_6", "category_id": "colors", "word": "Heart", "phonetic": "/hɑːt/", "emoji": "💖", "example_sentence": "Draw a pretty pink heart for someone you love.", "fun_fact": "The heart shape represents kindness and friendship!", "difficulty_level": "easy", "order_index": 6},

            # Numbers
            {"id": "num_1", "category_id": "numbers", "word": "One", "phonetic": "/wʌn/", "emoji": "1️⃣", "example_sentence": "I have one nose and one mouth.", "fun_fact": "The number 1 is where we start counting!", "difficulty_level": "easy", "order_index": 1},
            {"id": "num_2", "category_id": "numbers", "word": "Two", "phonetic": "/tuː/", "emoji": "2️⃣", "example_sentence": "I have two eyes to see the world.", "fun_fact": "Two of something is called a pair!", "difficulty_level": "easy", "order_index": 2},
            {"id": "num_3", "category_id": "numbers", "word": "Three", "phonetic": "/θriː/", "emoji": "3️⃣", "example_sentence": "A triangle has three straight sides.", "fun_fact": "Three is a magic number in many fairy tales!", "difficulty_level": "easy", "order_index": 3},
            {"id": "num_4", "category_id": "numbers", "word": "Four", "phonetic": "/fɔːr/", "emoji": "4️⃣", "example_sentence": "A cute puppy has four paws.", "fun_fact": "Four seasons make up one whole year: Spring, Summer, Autumn, Winter!", "difficulty_level": "easy", "order_index": 4},
            {"id": "num_5", "category_id": "numbers", "word": "Five", "phonetic": "/faɪv/", "emoji": "5️⃣", "example_sentence": "Give me a high five with five fingers!", "fun_fact": "We have five fingers on each hand!", "difficulty_level": "easy", "order_index": 5},
            {"id": "num_10", "category_id": "numbers", "word": "Ten", "phonetic": "/ten/", "emoji": "🔟", "example_sentence": "Count all ten toes on your feet!", "fun_fact": "Ten is the base of our decimal counting system!", "difficulty_level": "easy", "order_index": 6},

            # School
            {"id": "sch_1", "category_id": "school", "word": "Book", "phonetic": "/bʊk/", "emoji": "📚", "example_sentence": "Open your storybook and read magical tales.", "fun_fact": "Reading books grows your imagination and vocabulary!", "difficulty_level": "easy", "order_index": 1},
            {"id": "sch_2", "category_id": "school", "word": "Pencil", "phonetic": "/ˈpen.səl/", "emoji": "✏️", "example_sentence": "Use the pencil to draw a happy picture.", "fun_fact": "A single pencil can draw a line up to 35 miles long!", "difficulty_level": "easy", "order_index": 2},
            {"id": "sch_3", "category_id": "school", "word": "Backpack", "phonetic": "/ˈbæk.pæk/", "emoji": "🎒", "example_sentence": "Put your lunchbox and books into your backpack.", "fun_fact": "Wearing a backpack on both shoulders protects your back!", "difficulty_level": "easy", "order_index": 3},
            {"id": "sch_4", "category_id": "school", "word": "Clock", "phonetic": "/klɒk/", "emoji": "⏰", "example_sentence": "The clock tells us when it is playtime.", "fun_fact": "Clocks have been keeping time for thousands of years!", "difficulty_level": "easy", "order_index": 4},

            # Body
            {"id": "body_1", "category_id": "body", "word": "Smile", "phonetic": "/smaɪl/", "emoji": "😊", "example_sentence": "A warm smile makes everyone happy.", "fun_fact": "Smiling uses 17 different facial muscles!", "difficulty_level": "easy", "order_index": 1},
            {"id": "body_2", "category_id": "body", "word": "Eyes", "phonetic": "/aɪz/", "emoji": "👀", "example_sentence": "We look at colorful pictures with our eyes.", "fun_fact": "Your eyes can distinguish millions of different colors!", "difficulty_level": "easy", "order_index": 2},
            {"id": "body_3", "category_id": "body", "word": "Hands", "phonetic": "/hændz/", "emoji": "🙌", "example_sentence": "Clap your hands together along with the music!", "fun_fact": "Human hands are amazingly dexterous tools.", "difficulty_level": "easy", "order_index": 3},
        ]
        for w in words_data:
            if not db.query(VocabularyWord).filter(VocabularyWord.id == w["id"]).first():
                db.add(VocabularyWord(**w))
        db.commit()
        print(f"✅ Vocabulary words seeded ({len(words_data)})")

        # =========================================================================
        # 3. ALPHABET PHONICS
        # =========================================================================
        alphabet_data = [
            {"id": "a", "letter": "A", "lowercase": "a", "word": "Apple", "phonics": "/æ/", "emoji": "🍎", "example_sentence": "An apple a day keeps the doctor away!", "color": "#FF6B6B", "order_index": 1},
            {"id": "b", "letter": "B", "lowercase": "b", "word": "Bear", "phonics": "/b/", "emoji": "🐻", "example_sentence": "The brown bear loves sweet honey.", "color": "#4D96FF", "order_index": 2},
            {"id": "c", "letter": "C", "lowercase": "c", "word": "Cat", "phonics": "/k/", "emoji": "🐱", "example_sentence": "The cute cat says meow meow.", "color": "#6BCB77", "order_index": 3},
            {"id": "d", "letter": "D", "lowercase": "d", "word": "Dog", "phonics": "/d/", "emoji": "🐶", "example_sentence": "The friendly dog wags its tail.", "color": "#FFD93D", "order_index": 4},
            {"id": "e", "letter": "E", "lowercase": "e", "word": "Elephant", "phonics": "/e/", "emoji": "🐘", "example_sentence": "The elephant has a very long trunk.", "color": "#845EC2", "order_index": 5},
            {"id": "f", "letter": "F", "lowercase": "f", "word": "Fish", "phonics": "/f/", "emoji": "🐠", "example_sentence": "Little fish swim happily in the water.", "color": "#00C9A7", "order_index": 6},
            {"id": "g", "letter": "G", "lowercase": "g", "word": "Giraffe", "phonics": "/dʒ/", "emoji": "🦒", "example_sentence": "The tall giraffe eats green leaves.", "color": "#FF9671", "order_index": 7},
            {"id": "h", "letter": "H", "lowercase": "h", "word": "House", "phonics": "/h/", "emoji": "🏠", "example_sentence": "We live together in a warm house.", "color": "#FF6F91", "order_index": 8},
            {"id": "i", "letter": "I", "lowercase": "i", "word": "Ice Cream", "phonics": "/aɪ/", "emoji": "🍦", "example_sentence": "Sweet ice cream is cold and yummy.", "color": "#4D96FF", "order_index": 9},
            {"id": "j", "letter": "J", "lowercase": "j", "word": "Juice", "phonics": "/dʒ/", "emoji": "🧃", "example_sentence": "Drinking fresh orange juice is healthy.", "color": "#FFD93D", "order_index": 10},
            {"id": "k", "letter": "K", "lowercase": "k", "word": "Kite", "phonics": "/k/", "emoji": "🪁", "example_sentence": "The colorful kite flies high in the sky.", "color": "#6BCB77", "order_index": 11},
            {"id": "l", "letter": "L", "lowercase": "l", "word": "Lion", "phonics": "/l/", "emoji": "🦁", "example_sentence": "The mighty lion is the king of the jungle.", "color": "#FF9671", "order_index": 12},
            {"id": "m", "letter": "M", "lowercase": "m", "word": "Monkey", "phonics": "/m/", "emoji": "🐵", "example_sentence": "Playful monkeys swing on tree branches.", "color": "#845EC2", "order_index": 13},
            {"id": "n", "letter": "N", "lowercase": "n", "word": "Nest", "phonics": "/n/", "emoji": "🪺", "example_sentence": "Baby birds rest safely in their nest.", "color": "#00C9A7", "order_index": 14},
            {"id": "o", "letter": "O", "lowercase": "o", "word": "Owl", "phonics": "/aʊ/", "emoji": "🦉", "example_sentence": "The wise owl stays awake all night.", "color": "#FF6B6B", "order_index": 15},
            {"id": "p", "letter": "P", "lowercase": "p", "word": "Panda", "phonics": "/p/", "emoji": "🐼", "example_sentence": "The fluffy panda loves green bamboo.", "color": "#4D96FF", "order_index": 16},
            {"id": "q", "letter": "Q", "lowercase": "q", "word": "Queen", "phonics": "/kw/", "emoji": "👑", "example_sentence": "The kind queen wears a shiny golden crown.", "color": "#FFD93D", "order_index": 17},
            {"id": "r", "letter": "R", "lowercase": "r", "word": "Rabbit", "phonics": "/r/", "emoji": "🐰", "example_sentence": "The quick rabbit hops through the grass.", "color": "#FF6F91", "order_index": 18},
            {"id": "s", "letter": "S", "lowercase": "s", "word": "Sun", "phonics": "/s/", "emoji": "☀️", "example_sentence": "The bright sun shines warmly in the sky.", "color": "#FFD93D", "order_index": 19},
            {"id": "t", "letter": "T", "lowercase": "t", "word": "Tiger", "phonics": "/t/", "emoji": "🐯", "example_sentence": "The energetic tiger has beautiful stripes.", "color": "#FF9671", "order_index": 20},
            {"id": "u", "letter": "U", "lowercase": "u", "word": "Umbrella", "phonics": "/ʌ/", "emoji": "☂️", "example_sentence": "Open the umbrella when it starts to rain.", "color": "#845EC2", "order_index": 21},
            {"id": "v", "letter": "V", "lowercase": "v", "word": "Violin", "phonics": "/v/", "emoji": "🎻", "example_sentence": "The violin makes lovely musical sounds.", "color": "#00C9A7", "order_index": 22},
            {"id": "w", "letter": "W", "lowercase": "w", "word": "Whale", "phonics": "/w/", "emoji": "🐋", "example_sentence": "The giant whale swims gracefully in the ocean.", "color": "#4D96FF", "order_index": 23},
            {"id": "x", "letter": "X", "lowercase": "x", "word": "Xylophone", "phonics": "/z/", "emoji": "🎼", "example_sentence": "Tap the colorful xylophone bars to play music.", "color": "#FF6B6B", "order_index": 24},
            {"id": "y", "letter": "Y", "lowercase": "y", "word": "Yo-yo", "phonics": "/j/", "emoji": "🪀", "example_sentence": "The spinning yo-yo goes up and down.", "color": "#FF9671", "order_index": 25},
            {"id": "z", "letter": "Z", "lowercase": "z", "word": "Zebra", "phonics": "/z/", "emoji": "🦓", "example_sentence": "The friendly zebra has black and white stripes.", "color": "#6BCB77", "order_index": 26},
        ]
        for a in alphabet_data:
            if not db.query(AlphabetLesson).filter(AlphabetLesson.id == a["id"]).first():
                db.add(AlphabetLesson(**a))
        db.commit()
        print(f"✅ Alphabet Lessons seeded ({len(alphabet_data)})")

        # =========================================================================
        # 4. QUIZ QUESTIONS
        # =========================================================================
        quiz_data = [
            {
                "id": "q_e1", "level": "easy", "question_type": "picture-word", "question": "What animal is this?", "target_word": "Lion", "prompt_emoji": "🦁",
                "options": [{"id": "o1", "text": "Lion", "emoji": "🦁", "isCorrect": True}, {"id": "o2", "text": "Puppy", "emoji": "🐶", "isCorrect": False}, {"id": "o3", "text": "Monkey", "emoji": "🐵", "isCorrect": False}, {"id": "o4", "text": "Penguin", "emoji": "🐧", "isCorrect": False}],
                "explanation": "🦁 This is a Lion, the king of the jungle!", "reward_stars": 1, "order_index": 1
            },
            {
                "id": "q_e2", "level": "easy", "question_type": "picture-word", "question": "Which word matches this juicy fruit?", "target_word": "Apple", "prompt_emoji": "🍎",
                "options": [{"id": "o1", "text": "Banana", "emoji": "🍌", "isCorrect": False}, {"id": "o2", "text": "Apple", "emoji": "🍎", "isCorrect": True}, {"id": "o3", "text": "Strawberry", "emoji": "🍓", "isCorrect": False}, {"id": "o4", "text": "Pizza", "emoji": "🍕", "isCorrect": False}],
                "explanation": "🍎 Apple is crunchy, sweet, and red!", "reward_stars": 1, "order_index": 2
            },
            {
                "id": "q_e3", "level": "easy", "question_type": "picture-word", "question": "What is this cheerful shape?", "target_word": "Star", "prompt_emoji": "⭐",
                "options": [{"id": "o1", "text": "Circle", "emoji": "🔴", "isCorrect": False}, {"id": "o2", "text": "Heart", "emoji": "💖", "isCorrect": False}, {"id": "o3", "text": "Star", "emoji": "⭐", "isCorrect": True}, {"id": "o4", "text": "Square", "emoji": "🟨", "isCorrect": False}],
                "explanation": "⭐ Twinkle twinkle little star in the sky!", "reward_stars": 1, "order_index": 3
            },
            {
                "id": "q_e4", "level": "easy", "question_type": "picture-word", "question": "Which pet loves playing with a ball?", "target_word": "Puppy", "prompt_emoji": "🐶",
                "options": [{"id": "o1", "text": "Puppy", "emoji": "🐶", "isCorrect": True}, {"id": "o2", "text": "Kitten", "emoji": "🐱", "isCorrect": False}, {"id": "o3", "text": "Dolphin", "emoji": "🐬", "isCorrect": False}, {"id": "o4", "text": "Bear", "emoji": "🐻", "isCorrect": False}],
                "explanation": "🐶 A puppy is a friendly, loyal little dog!", "reward_stars": 1, "order_index": 4
            },
            {
                "id": "q_m1", "level": "medium", "question_type": "listen-choose", "question": "Listen carefully! Which animal did you hear?", "target_word": "Elephant", "prompt_audio": "Elephant",
                "options": [{"id": "o1", "text": "Giraffe", "emoji": "🦒", "isCorrect": False}, {"id": "o2", "text": "Puppy", "emoji": "🐶", "isCorrect": False}, {"id": "o3", "text": "Elephant", "emoji": "🐘", "isCorrect": True}, {"id": "o4", "text": "Dolphin", "emoji": "🐬", "isCorrect": False}],
                "explanation": "🐘 Elephants have big floppy ears and long trunks!", "reward_stars": 2, "order_index": 5
            },
            {
                "id": "q_m2", "level": "medium", "question_type": "listen-choose", "question": "Listen to the sound and choose the fruit!", "target_word": "Banana", "prompt_audio": "Banana",
                "options": [{"id": "o1", "text": "Watermelon", "emoji": "🍉", "isCorrect": False}, {"id": "o2", "text": "Banana", "emoji": "🍌", "isCorrect": True}, {"id": "o3", "text": "Ice Cream", "emoji": "🍦", "isCorrect": False}, {"id": "o4", "text": "Strawberry", "emoji": "🍓", "isCorrect": False}],
                "explanation": "🍌 Bananas are yellow and delicious!", "reward_stars": 2, "order_index": 6
            },
            {
                "id": "q_h1", "level": "hard", "question_type": "listen-choose", "question": "Listen to the ocean animal and pick it!", "target_word": "Dolphin", "prompt_audio": "Dolphin",
                "options": [{"id": "o1", "text": "Penguin", "emoji": "🐧", "isCorrect": False}, {"id": "o2", "text": "Dolphin", "emoji": "🐬", "isCorrect": True}, {"id": "o3", "text": "Elephant", "emoji": "🐘", "isCorrect": False}, {"id": "o4", "text": "Giraffe", "emoji": "🦒", "isCorrect": False}],
                "explanation": "🐬 Dolphins are super smart marine mammals!", "reward_stars": 3, "order_index": 7
            },
            {
                "id": "q_h2", "level": "hard", "question_type": "picture-word", "question": "Which animal has the longest neck in the world?", "target_word": "Giraffe", "prompt_emoji": "🦒",
                "options": [{"id": "o1", "text": "Lion", "emoji": "🦁", "isCorrect": False}, {"id": "o2", "text": "Monkey", "emoji": "🐵", "isCorrect": False}, {"id": "o3", "text": "Giraffe", "emoji": "🦒", "isCorrect": True}, {"id": "o4", "text": "Puppy", "emoji": "🐶", "isCorrect": False}],
                "explanation": "🦒 A giraffe can reach leaves at the very top of trees!", "reward_stars": 3, "order_index": 8
            },
        ]
        for q in quiz_data:
            if not db.query(QuizQuestion).filter(QuizQuestion.id == q["id"]).first():
                db.add(QuizQuestion(**q))
        db.commit()
        print(f"✅ Quiz Questions seeded ({len(quiz_data)})")

        # =========================================================================
        # 5. SPELLING WORDS
        # =========================================================================
        spelling_data = [
            {"id": "sp_e1", "level": "easy", "word": "CAT", "emoji": "🐱", "hint": "A soft furry pet that loves milk", "reward_stars": 1, "order_index": 1},
            {"id": "sp_e2", "level": "easy", "word": "DOG", "emoji": "🐶", "hint": "Man's best friend that barks", "reward_stars": 1, "order_index": 2},
            {"id": "sp_e3", "level": "easy", "word": "SUN", "emoji": "☀️", "hint": "Shines brightly in the daytime sky", "reward_stars": 1, "order_index": 3},
            {"id": "sp_e4", "level": "easy", "word": "RED", "emoji": "🔴", "hint": "The color of apples and hearts", "reward_stars": 1, "order_index": 4},
            {"id": "sp_m1", "level": "medium", "word": "BEAR", "emoji": "🐻", "hint": "Loves sweet honey in the forest", "reward_stars": 2, "order_index": 5},
            {"id": "sp_m2", "level": "medium", "word": "LION", "emoji": "🦁", "hint": "The brave king of the savanna", "reward_stars": 2, "order_index": 6},
            {"id": "sp_m3", "level": "medium", "word": "BOOK", "emoji": "📚", "hint": "Filled with exciting stories to read", "reward_stars": 2, "order_index": 7},
            {"id": "sp_m4", "level": "medium", "word": "APPLE", "emoji": "🍎", "hint": "A sweet and crunchy red fruit", "reward_stars": 2, "order_index": 8},
            {"id": "sp_h1", "level": "hard", "word": "MONKEY", "emoji": "🐵", "hint": "Loves swinging on vines and eating bananas", "reward_stars": 3, "order_index": 9},
            {"id": "sp_h2", "level": "hard", "word": "PENCIL", "emoji": "✏️", "hint": "Used for writing and drawing cute pictures", "reward_stars": 3, "order_index": 10},
            {"id": "sp_h3", "level": "hard", "word": "BANANA", "emoji": "🍌", "hint": "A long yellow fruit rich in energy", "reward_stars": 3, "order_index": 11},
            {"id": "sp_h4", "level": "hard", "word": "PENGUIN", "emoji": "🐧", "hint": "A cute bird that swims in icy oceans", "reward_stars": 3, "order_index": 12},
        ]
        for sp in spelling_data:
            if not db.query(SpellingWord).filter(SpellingWord.id == sp["id"]).first():
                db.add(SpellingWord(**sp))
        db.commit()
        print(f"✅ Spelling Words seeded ({len(spelling_data)})")

        # =========================================================================
        # 6. SPEAKING CHALLENGES
        # =========================================================================
        speaking_data = [
            {"id": "spk_e1", "level": "easy", "text": "Apple", "phonetic": "/ˈæp.əl/", "emoji": "🍎", "fun_fact": "Quả táo giòn ngọt", "pass_threshold_percent": 70, "reward_stars": 2, "order_index": 1},
            {"id": "spk_e2", "level": "easy", "text": "Lion", "phonetic": "/ˈlaɪ.ən/", "emoji": "🦁", "fun_fact": "Sư tử dũng mãnh", "pass_threshold_percent": 70, "reward_stars": 2, "order_index": 2},
            {"id": "spk_e3", "level": "easy", "text": "Puppy", "phonetic": "/ˈpʌp.i/", "emoji": "🐶", "fun_fact": "Cún con tinh nghịch", "pass_threshold_percent": 70, "reward_stars": 2, "order_index": 3},
            {"id": "spk_e4", "level": "easy", "text": "Sun", "phonetic": "/sʌn/", "emoji": "☀️", "fun_fact": "Mặt trời ấm áp", "pass_threshold_percent": 70, "reward_stars": 2, "order_index": 4},
            {"id": "spk_m1", "level": "medium", "text": "Red apple", "phonetic": "/red ˈæp.əl/", "emoji": "🍎", "fun_fact": "Quả táo màu đỏ tươi", "pass_threshold_percent": 75, "reward_stars": 3, "order_index": 5},
            {"id": "spk_m2", "level": "medium", "text": "Cute puppy", "phonetic": "/kjuːt ˈpʌp.i/", "emoji": "🐶", "fun_fact": "Chú cún dễ thương", "pass_threshold_percent": 75, "reward_stars": 3, "order_index": 6},
            {"id": "spk_m3", "level": "medium", "text": "Big elephant", "phonetic": "/bɪɡ ˈel.ə.fənt/", "emoji": "🐘", "fun_fact": "Chú voi to lớn", "pass_threshold_percent": 75, "reward_stars": 3, "order_index": 7},
            {"id": "spk_m4", "level": "medium", "text": "Happy smile", "phonetic": "/ˈhæp.i smaɪl/", "emoji": "😊", "fun_fact": "Nụ cười rạng rỡ", "pass_threshold_percent": 75, "reward_stars": 3, "order_index": 8},
            {"id": "spk_h1", "level": "hard", "text": "I love bananas", "phonetic": "/aɪ lʌv bəˈnɑː.nəz/", "emoji": "🍌", "fun_fact": "Tôi rất thích ăn chuối", "pass_threshold_percent": 80, "reward_stars": 4, "order_index": 9},
            {"id": "spk_h2", "level": "hard", "text": "The lion is strong", "phonetic": "/ðə ˈlaɪ.ən ɪz strɒŋ/", "emoji": "🦁", "fun_fact": "Sư tử rất khỏe", "pass_threshold_percent": 80, "reward_stars": 4, "order_index": 10},
            {"id": "spk_h3", "level": "hard", "text": "Look at the rainbow", "phonetic": "/lʊk æt ðə ˈreɪn.bəʊ/", "emoji": "🌈", "fun_fact": "Hãy ngắm cầu vồng kìa", "pass_threshold_percent": 80, "reward_stars": 4, "order_index": 11},
        ]
        for spk in speaking_data:
            if not db.query(SpeakingChallenge).filter(SpeakingChallenge.id == spk["id"]).first():
                db.add(SpeakingChallenge(**spk))
        db.commit()
        print(f"✅ Speaking Challenges seeded ({len(speaking_data)})")

        # =========================================================================
        # 7. GAMIFICATION (Badges, Avatars, Stickers)
        # =========================================================================
        badges_data = [
            {"id": "badge_welcome", "title": "First Steps", "description": "Joined English for Kids!", "badge_icon": "🌱", "condition_type": "FIRST_LOGIN", "condition_value": 1, "reward_stars": 5, "order_index": 1},
            {"id": "badge_streak_3", "title": "3 Days Explorer", "description": "Learned English 3 days in a row!", "badge_icon": "🔥", "condition_type": "STREAK_DAYS", "condition_value": 3, "reward_stars": 10, "order_index": 2},
            {"id": "badge_streak_7", "title": "7 Days Master", "description": "Maintained a 7-day study streak!", "badge_icon": "⚡", "condition_type": "STREAK_DAYS", "condition_value": 7, "reward_stars": 20, "order_index": 3},
            {"id": "badge_vocab_10", "title": "Word Collector", "description": "Mastered 10 new vocabulary words!", "badge_icon": "📚", "condition_type": "WORDS_MASTERED", "condition_value": 10, "reward_stars": 15, "order_index": 4},
            {"id": "badge_speaking_star", "title": "Speech Prodigy", "description": "Scored over 90% in AI speaking!", "badge_icon": "🎤", "condition_type": "SPEECH_SCORE", "condition_value": 90, "reward_stars": 15, "order_index": 5},
            {"id": "badge_quiz_champion", "title": "Quiz Master", "description": "Achieved a perfect score in Quiz mode!", "badge_icon": "🏆", "condition_type": "QUIZ_PERFECT", "condition_value": 100, "reward_stars": 25, "order_index": 6},
        ]
        for b in badges_data:
            if not db.query(AchievementBadge).filter(AchievementBadge.id == b["id"]).first():
                db.add(AchievementBadge(**b))

        avatars_data = [
            {"id": "av_lion", "name": "Brave Lion", "emoji": "🦁", "unlock_type": "free", "price_stars": 0, "required_level": 1, "order_index": 1},
            {"id": "av_bear", "name": "Cozy Bear", "emoji": "🐻", "unlock_type": "free", "price_stars": 0, "required_level": 1, "order_index": 2},
            {"id": "av_panda", "name": "Gentle Panda", "emoji": "🐼", "unlock_type": "free", "price_stars": 0, "required_level": 1, "order_index": 3},
            {"id": "av_unicorn", "name": "Magic Unicorn", "emoji": "🦄", "unlock_type": "stars", "price_stars": 20, "required_level": 2, "order_index": 4},
            {"id": "av_dragon", "name": "Fire Dragon", "emoji": "🐲", "unlock_type": "stars", "price_stars": 50, "required_level": 3, "order_index": 5},
            {"id": "av_superstar", "name": "Super Explorer", "emoji": "🦸", "unlock_type": "stars", "price_stars": 80, "required_level": 5, "order_index": 6},
        ]
        for av in avatars_data:
            if not db.query(AvatarCharacter).filter(AvatarCharacter.id == av["id"]).first():
                db.add(AvatarCharacter(**av))

        stickers_data = [
            {"id": "stk_gold_star", "name": "Super Star", "emoji": "⭐", "category_name": "Trophies", "price_stars": 5, "order_index": 1},
            {"id": "stk_rocket", "name": "Space Rocket", "emoji": "🚀", "category_name": "Space", "price_stars": 10, "order_index": 2},
            {"id": "stk_rainbow", "name": "Rainbow Ribbon", "emoji": "🌈", "category_name": "Nature", "price_stars": 10, "order_index": 3},
            {"id": "stk_crown", "name": "Golden Crown", "emoji": "👑", "category_name": "Royalty", "price_stars": 15, "order_index": 4},
            {"id": "stk_balloon", "name": "Party Balloon", "emoji": "🎈", "category_name": "Celebration", "price_stars": 5, "order_index": 5},
            {"id": "stk_medal", "name": "Winner Medal", "emoji": "🥇", "category_name": "Trophies", "price_stars": 20, "order_index": 6},
        ]
        for stk in stickers_data:
            if not db.query(StickerItem).filter(StickerItem.id == stk["id"]).first():
                db.add(StickerItem(**stk))

        db.commit()
        print("✅ Gamification items seeded")

        # =========================================================================
        # 8. CMS (Banners, Daily Quests, App Settings, Content Versions)
        # =========================================================================
        banners_data = [
            {"id": "banner_animals", "title": "Explore Animal Safari 🦁", "subtitle": "Listen to roaring lions and cute puppies!", "image_url": "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?w=600", "action_type": "NAVIGATE_CATEGORY", "action_payload": "animals", "background_color": "#FF9671", "display_order": 1},
            {"id": "banner_speaking", "title": "Speak English with AI 🎙️", "subtitle": "Practice pronunciation and earn shiny stars!", "image_url": "https://images.unsplash.com/photo-1516627145497-ae6968895b74?w=600", "action_type": "NAVIGATE_GAME", "action_payload": "speaking", "background_color": "#4D96FF", "display_order": 2},
        ]
        for bn in banners_data:
            if not db.query(HomeBanner).filter(HomeBanner.id == bn["id"]).first():
                db.add(HomeBanner(**bn))

        quests_data = [
            {"id": "quest_words_3", "title": "Practice 3 Words", "description": "Explore and tap any 3 vocabulary cards", "emoji": "📖", "target_type": "WORDS_PRACTICED", "target_count": 3, "reward_stars": 3, "order_index": 1},
            {"id": "quest_speak_2", "title": "Record 2 Pronunciations", "description": "Score at least 70% in AI speaking challenge", "emoji": "🎙️", "target_type": "SPEECH_RECORDED", "target_count": 2, "reward_stars": 5, "order_index": 2},
            {"id": "quest_quiz_1", "title": "Play 1 Quiz Game", "description": "Answer quiz questions and test your memory", "emoji": "🎯", "target_type": "QUIZ_PLAYED", "target_count": 1, "reward_stars": 4, "order_index": 3},
        ]
        for qst in quests_data:
            if not db.query(DailyQuest).filter(DailyQuest.id == qst["id"]).first():
                db.add(DailyQuest(**qst))

        settings_data = [
            {"config_key": "DEFAULT_TTS_VOICE", "config_value": "en-US-JennyNeural", "data_type": "string", "description": "Microsoft Neural voice for TTS", "is_public": True},
            {"config_key": "DAILY_RECOMMENDED_STUDY_MINUTES", "config_value": "15", "data_type": "number", "description": "Target daily study time for kids", "is_public": True},
            {"config_key": "SPEECH_PASSING_ACCURACY", "config_value": "70", "data_type": "number", "description": "Minimum speech score threshold to pass", "is_public": True},
            {"config_key": "ENABLE_PARENTAL_GATE_PIN", "config_value": "true", "data_type": "boolean", "description": "Require math gate or PIN for parents settings", "is_public": True},
            {"config_key": "APP_ANNOUNCEMENT", "config_value": "Welcome to English for Kids 🎈! Have fun learning today!", "data_type": "string", "description": "Global banner announcement", "is_public": True},
        ]
        for s in settings_data:
            if not db.query(AppSetting).filter(AppSetting.config_key == s["config_key"]).first():
                db.add(AppSetting(**s))

        modules = ["curriculum", "games", "gamification", "cms"]
        for m in modules:
            if not db.query(ContentVersion).filter(ContentVersion.id == m).first():
                db.add(ContentVersion(id=m, version_number=1))

        db.commit()
        print("✅ CMS Banners, Quests, App Settings, and Content Versions seeded successfully!")

        print("\n🎉 ALL DATABASE SEEDING COMPLETED SUCCESSFULLY!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error during database seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
