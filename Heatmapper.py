import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#import the results as a dataframe
df_remotemodel = pd.read_excel('RemoteModel_v4_Solved.xlsx', sheet_name = "Remote Base")

df_SOC = pd.DataFrame()

df_SOC['Day'] = pd.to_datetime(df_remotemodel['DateTime']).dt.date
df_SOC['Hour'] = pd.to_datetime(df_remotemodel['DateTime']).dt.time

df_SOC['BB SOC (%)'] = 100*df_remotemodel['BB SOC (%)'].round(4)

df_heatmap1 = df_SOC.pivot("Hour", "Day", "BB SOC (%)")

ax = sns.heatmap(df_heatmap1, cmap="Blues_r") #rocket for standard
ax.invert_yaxis()
title = 'BB SOC (%)'
plt.title(title,fontsize=16)
plt.show()


#sns.heatmap(df_SOC, yticklabels = "Hour", xticklabels = "Day")  

#plt.figure(figsize = [20, 50])
#title = 'BB SOC (%)'
#plt.title(title,fontsize=24)
#
#ax = sns.heatmap(df_SOC, annot = True, fmt='f', linewidths = .5,
#                 cmap = plt.cm.get_cmap('RdYlGn', 7))
#ax.figure.axes[-1].yaxis.label.set_size(20)


