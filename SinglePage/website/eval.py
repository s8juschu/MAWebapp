import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

submissions = pd.read_csv('exports/submission_score.csv')
questionnaires = pd.read_csv('exports/questionnaires.csv')
times = pd.read_csv('exports/time.csv')

# ---------------- SUBMISSIONS
# get list of all submission_ids
session_col = submissions['session'].tolist()
ctrl_cond = submissions.loc[submissions['framing'] == 0, ['session']]['session'].tolist()
print(ctrl_cond)
pos_cond = submissions.loc[submissions['framing'] == 1, ['session']]['session'].tolist()
print(pos_cond)
neg_cond = submissions.loc[submissions['framing'] == 2, ['session']]['session'].tolist()
print(neg_cond)

age = submissions.groupby(["age"]).size()
print(age)
framing = submissions.groupby(["framing"]).size()
print(framing)
gender = submissions.groupby(["gender"]).size()
print(gender)
deception = submissions.groupby(["suspect_deception"]).size()
print(deception)
text_deception = submissions['text_deception'].tolist()
print(text_deception)

score = submissions.set_index("session", inplace=True)
score = submissions.loc[:, ('taskscore__score_pre', 'taskscore__score_main')]
score['Total'] = score.sum(axis=1)
score.loc['mean', :] = score.mean()

# score.plot(kind='bar')
#
# plt.show()

score.reset_index().to_csv('exports/export_score.csv', index=False, header=True)

# score.plot(kind='bar')

# ---------------- TIME
# times['start_time'] = pd.to_datetime(times['start_time'], unit='s')
# times['page_nr_idx'] = 'page_nr' + times.page_nr.astype(str)
# times = times.pivot(index='session', columns='page_nr_idx', values='start_time')
# times = times.reindex(sorted(times.columns, key=lambda x: int(x[7:])), axis=1)

# times.reset_index().to_csv('export_time.csv', index=False, header=True)

times['page_nr_idx'] = 'page_nr' + times.page_nr.astype(str)
times = times.pivot(index='session', columns='page_nr_idx', values='start_time')
times = times.reindex(sorted(times.columns, key=lambda x: int(x[7:])), axis=1)

for i in range(1, 14):
    # times.loc[(times['page_nr_idx'] == i), 'page_nr_idx'] = (8 - times['answer'])
    times['page_nr'+str(i)] = (times['page_nr'+str(i+1)] - times['page_nr'+str(i)])/60

times['total'] = times['page_nr1']+times['page_nr2']+times['page_nr3']+times['page_nr4']+times['page_nr5']+times['page_nr6']+times['page_nr7']+\
                 times['page_nr8']+times['page_nr9']+times['page_nr10']+times['page_nr11']+times['page_nr12']+times['page_nr13']
# times['total'] = (times['page_nr'+str(14)] - times['page_nr1'])/60

del times['page_nr14']

times.loc['mean', :] = times.mean()

times.reset_index().to_csv('exports/export_time.csv', index=False, header=True)

# ---------------- QUESTIONNAIRES

# ------ IMI
revert_nr = [2, 9, 11, 14, 19, 21]

interest_nr = [1, 5, 8, 10, 14, 17, 20]
competence_nr = [4, 7, 12, 16, 22]
choice_nr = [3, 11, 15, 19, 21]
tension_nr = [2, 6, 9, 13, 18]

# Revert the needed
for rev in revert_nr:
    questionnaires.loc[(questionnaires['item'] == rev) & (questionnaires['type'] == "IMI"), 'answer'] = (
            8 - questionnaires['answer'])

# -- PRE
pre = questionnaires.loc[(questionnaires['name'] == "pre") & (questionnaires['type'] == "IMI")]

pre_interest = pre.loc[(pre['item'].isin(interest_nr))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_interest'})
pre_competence = pre.loc[(pre['item'].isin(competence_nr))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_competence'})
pre_choice = pre.loc[(pre['item'].isin(choice_nr))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_choice'})
pre_tension = pre.loc[(pre['item'].isin(tension_nr))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_tension'})

result_imi_pre = pd.concat([pre_interest, pre_competence, pre_choice, pre_tension], axis=1)
result_imi_pre.loc['mean', :] = result_imi_pre.mean()

result_imi_pre.reset_index().to_csv('exports/export_imi_pre.csv', index=False, header=True)

# -- MAIN
main = questionnaires.loc[(questionnaires['name'] == "main") & (questionnaires['type'] == "IMI")]

main_interest = main.loc[(main['item'].isin(interest_nr))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_interest'})
main_competence = main.loc[(main['item'].isin(competence_nr))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_competence'})
main_choice = main.loc[(main['item'].isin(choice_nr))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_choice'})
main_tension = main.loc[(main['item'].isin(tension_nr))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_tension'})

result_imi_main = pd.concat([main_interest, main_competence, main_choice, main_tension], axis=1)
result_imi_main.loc['mean', :] = result_imi_main.mean()

result_imi_main.reset_index().to_csv('exports/export_imi_main.csv', index=False, header=True)

# ------ PANAS

pos_items = [1, 3, 4, 6, 10, 11, 13, 15, 17, 18]
neg_items = [2, 5, 7, 8, 9, 12, 14, 16, 19, 20]

# -- PRE
pre_panas = questionnaires.loc[(questionnaires['name'] == "pre") & (questionnaires['type'] == "PANAS")]

pre_panas_pos = pre_panas.loc[(pre_panas['item'].isin(pos_items))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_positive'})
pre_panas_neg = pre_panas.loc[(pre_panas['item'].isin(neg_items))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_negative'})

result_panas_pre = pd.concat([pre_panas_pos, pre_panas_neg], axis=1)
result_panas_pre.loc['mean', :] = result_panas_pre.mean()

result_panas_pre.reset_index().to_csv('exports/export_panas_pre.csv', index=False, header=True)

# -- MAIN
main_panas = questionnaires.loc[(questionnaires['name'] == "main") & (questionnaires['type'] == "PANAS")]

main_panas_pos = main_panas.loc[(main_panas['item'].isin(pos_items))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_positive'})
main_panas_neg = main_panas.loc[(main_panas['item'].isin(neg_items))].groupby('session').agg({'answer': 'mean'}).rename(
    columns={'answer': 'Average_negative'})

result_panas_main = pd.concat([main_panas_pos, main_panas_neg], axis=1)
result_panas_main.loc['mean', :] = result_panas_main.mean()

result_panas_main.reset_index().to_csv('exports/export_panas_main.csv', index=False, header=True)
