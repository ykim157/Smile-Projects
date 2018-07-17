# Smile Projects
Small projects in SMILE
## List of Projects
### 1. Creating quality questions from an article
#### Instruction
1. Install dependencies with the following commands
'''
pip install -r requirements.txt
'''
2. Create a file named 'credentials.json' with your Watson NLU credentials
EX)
'''
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "your username hash",
  "password": "your password hash"
}
'''
#### Levels 1 & 2
1. Summarize article
2. Extract key phrases(words)
3. Create questions
#### Level 3 (Comparison)
1. Same process as lower level
2. Get comparable phrases(words) from Google based on frequency of mutual appearance
3. Create questions
##### Level 4 (Why)
1. Same process as lower level
2. Create hypothetical
##### Level 5 (What if)
1. Same process as lower level
2. Create hypothetical statements (how?)
3. Create questions by reversing the statements.
### 2. Creating characteristic statements based on users' questions.
1. Collect questions each user created
2. Retrieve nested statements in their questions.
3. Create collection of statements
