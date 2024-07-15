import pandas as pd

# Create a sample login database
data = {'Username': ['user1', 'user2'], 'Password': ['pass1', 'pass2']}
df = pd.DataFrame(data)
df.to_excel('login_database.xlsx', index=False)
