import json

# Example input data
data = {
    "name": "Rahul Rajasekharan Menon",
    "headline": "Machine Learning Intern at Notion Press | B.Tech CSE Student at Jain (Deemed-to-be University) | Frontend Developer",
    "location": "Bengaluru, Karnataka, India",
    "connections": "130",
    "about": ("I am a third year student pursuing B.Tech in Computer Science and Engineering at Jain (Deemed-to-be University) Kanakapura Campus, Bengaluru and looking forward to "
              "having new experiences, meeting new people, and learning new things. I want to make the world a much more peaceful, smoother, and technologically more advanced through "
              "the practical implementation of my learning and using my skills. I am having a big dream to learn many coding languages, Artificial Intelligence, Data Science, full stack "
              "development, etc., and I started to follow my dream by choosing Computer Science in 11th and 12th (CBSE). The language they taught us was Python. I also got an opportunity "
              "to learn the basics of Structured Query Language (SQL) as it was a part of the 12th standard curriculum. I also learned Java and C languages as a part of my college curriculum. "
              "I have also successfully completed a Web Development course in collaboration with IIT Roorkee through which I have a good amount of knowledge regarding HTML, CSS, and JavaScript. "
              "I also got an opportunity to do a project regarding Web Development and I have completed it successfully. Along with my engineering classes, I am doing a course named 'CEE - IIT "
              "Madras - Advanced Certification in Data Science and AI'. It is a seven-month course. And I am not going to stop with this course, I will be learning more and more concepts related "
              "to Computer Science."),
    "skills": ["Generative AI", "Machine Learning", "Develop GenAI Apps with Gemini and Streamlit", "Prompt Design in Vertex AI", 
               "Large Language Models (LLM)", "Web Scraping", "Beautiful Soup", "Selenium", "Git and GitHub", 
               "Natural Language Processing (NLP)", "Deep Learning", "Reinforcement Learning", "Linear Regression", 
               "Machine Learning", "Kaggle", "Microsoft SQL Server", "MariaDB", "Web Development", "MySQLi", "PHP", 
               "Embedded JavaScript (EJS)", "Express.js", "Node.js", "JavaScript"]
}

# Concatenate fields into a single string
question = (f"Name: {data['name']}, Headline: {data['headline']}, Location: {data['location']}, Connections: {data['connections']}, "
            f"About: {data['about']}, Skills: {', '.join(data['skills'])}")

# Create the JSON structure
output = {
    "question": question
}

# Convert to JSON
output_json = json.dumps(output, indent=4)

# Print or save the JSON
print(output_json)
