import pandas as pd
import matplotlib.pyplot as plt
import spacy
from spacy.matcher import PhraseMatcher
from collections import Counter
from collections import defaultdict
import gc

gc.enable()
nlp = spacy.load('en_core_web_sm')

# Enter File paths:
# DATA_PATH = '<path for your resume/job description file>'
DATA_PATH = 'Skill-Extractor\JD.xlsx'
# SKILL_FILE_PATH = '<path for the skill-set file>'
SKILL_FILE_PATH = 'Skill-Extractor\Skill-set.xlsx'
keyword_ = pd.read_excel(SKILL_FILE_PATH)
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')


def create_profile(text, company_name):
    # Get the matches from the text
    doc = nlp(text)
    matches = matcher(doc)

    # Create a dataframe to return
    d = []
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the Skill, eg: 'Machine Learning'
        span = doc[start: end]  # get the Sub-skill, eg: 'Regression'
        d.append((rule_id, span.text))
    data = []
    for each, count in Counter(d).items():
        data.append([company_name, *each, count])
    dataf = pd.DataFrame(data, columns=['Company/Candidate Name', 'Skill', 'Sub-skill', 'Count'])
    data = pd.DataFrame(data, columns=['Company/Candidate Name', 'Skill', 'Sub-skill', 'Count'])
    return dataf, data


# Bar graph plot:
def plot_JD(final_database):
    final_database2 = final_database['Sub-skill'].groupby(
        [final_database['Company/Candidate Name'], final_database['Skill']]).count().unstack()
    final_database2.reset_index(inplace=True)
    final_database2.fillna(0, inplace=True)
    new_data = final_database2.iloc[:, 1:]
    new_data.index = final_database2['Company/Candidate Name']

    # Execute the below line if you want to see the JD profile in a csv format
    new_data.to_csv('skillset.csv')

    plt.rcParams.update({'font.size': 8})
    ax = new_data.plot.barh(title="JD/Resume keywords by category", legend=True, figsize=(25, 7), stacked=True)
    labels = []
    for j in new_data.columns:
        for i in new_data.index:
            label = str(j) + ": " + str(new_data.loc[i][j])
            labels.append(label)
    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
    plt.savefig('plot.png')
    plt.show()

def main(inputText):
    
    # Initializing PhraseMatcher

    for each in keyword_.columns:
        matcher.add(each, None, *[nlp(text) for text in keyword_[each].dropna(axis=0)])
    final_database = pd.DataFrame()
    l = [['1', inputText]]
    df = pd.DataFrame(l, columns=['Company','JD'])
    final_output = pd.DataFrame()
    for each in range(len(df)):
        JD = df.loc[each, 'JD']
        Company_name = df.loc[each, 'Company']
        data, needed = create_profile(JD, Company_name)
        final_output = final_output.append(needed)
        final_database = final_database.append(data)
        each += 1
        print('####################', each, '####################')

    # Saving the database
    
    # groupingData = pd.DataFrame(final_output, columns=[ 1, 2])
    # groupingData.groupby(1)
    # out = final_output['Sub-skill'].groupby( [final_database['Skill'], final_database['Company/Candidate Name']])
    out = final_output[['Skill', 'Sub-skill']].values.tolist()
    d = defaultdict(list)
    
    for key, val in out:
        d[key].append(val)
    return d

    # final_database.to_csv('data.csv')
    # final_output.to_csv('output.csv')

    # plot_JD(final_database)