import pandas as pd
import plotly.express as px


df = pd.read_csv('send.csv')
print(df.columns)


fig = px.scatter(df.query('sending_total==0'), x="sending_count", y="sending_partners",
             size="sending_partners")
fig.show()
