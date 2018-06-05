import pandas as pd
import numpy as np
import bson
from pymongo import MongoClient
import datetime

#just one commit jesus

client = MongoClient('mongodb://hyptastic001:the3men@ds229448.mlab.com:29448/projectx')
#mongodb://<dbuser>:<dbpassword>@ds229448.mlab.com:29448/projectx

#Read subjects file
subjects = []
#with open('./functions/matching/subjects.txt') as f:
with open('./subjects.txt') as f:
    for line in f:
        line = line.strip('\n')
        if not (line.startswith('//') or len(line) is 0):
            subjects.append(line)

#Read subcategories file
subcategories = []
# with open('./functions/matching/subcategories.txt') as f:
with open('./subcategories.txt') as f:
    for line in f:
        line = line.strip('\n')
        if not (line.startswith('//') or len(line) is 0):
            subcategories.append(line)

#Read classes to teach file
classes_to_teach = []
# with open('./functions/matching/classes_to_teach.txt') as f:
with open('./classes_to_teach.txt') as f:
    for line in f:
        line = line.strip('\n')
        if not (line.startswith('//') or len(line) is 0):
            classes_to_teach.append(line)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
db = client.projectx
jobs_collection = db.jobs

data = jobs_collection.find({'status': 0})
dict_list_raw_jobs = []
for document in data:
    dict_list_raw_jobs.append(document)

if(len(dict_list_raw_jobs) == 0):
    exit()



jobs_location_list = [
    list([val['locationLat'],val['locationLong']])
    for val in dict_list_raw_jobs
]
jobs_location_matrix = pd.DataFrame(jobs_location_list).as_matrix()

job_ids_list = [
    bson.objectid.ObjectId(val['_id'])
    for val in dict_list_raw_jobs
]

dict_list_jobs = []
#subject_keys = ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'Economics', 'Gender Preference', 'Salary']
subjects_list = [
    list(val['subjects'])
    for val in dict_list_raw_jobs
]

subcategory = [
    val['subcategory']
    for val in dict_list_raw_jobs
]

class_to_teach = [
    val['class']
    for val in dict_list_raw_jobs
]
subject_keys = subjects[:]
subcategory_keys = subcategories[:]
class_to_teach_keys = classes_to_teach[:]

for i in range(len(dict_list_raw_jobs)):
    dict_list_jobs.append(dict.fromkeys(subject_keys + subcategory_keys + class_to_teach_keys, 0))

for i in range(len(dict_list_raw_jobs)):
    dict_list_jobs[i]['Salary']=dict_list_raw_jobs[i]['salary']
    dict_list_jobs[i]['Gender Preference'] = dict_list_raw_jobs[i]['tutorGenderPreference']
    #dict_list_jobs[i]['Subcategory'] = dict_list_raw_jobs[i]['subcategory']
    #dict_list_jobs[i]['Class to teach'] = dict_list_raw_jobs[i]['class']
    dict_list_jobs[i][subcategory[i]]=1
    if not class_to_teach[i]=='':
        dict_list_jobs[i][class_to_teach[i]]=1

    for chunk in subjects_list[i]:
        if chunk in dict_list_jobs[i]:
            dict_list_jobs[i][chunk]=1

df = pd.DataFrame(dict_list_jobs)
jobs = df.as_matrix()
jobs[jobs=='m'] = 0
jobs[jobs=='f'] = 2
jobs[jobs=='any'] = 1

##############################################################################

tutors_collection = db.users
data = tutors_collection.find({"tutorUpdateFlag":"true"})
dict_list_raw_tutors = []

for document in data:
    dict_list_raw_tutors.append(document)

if(len(dict_list_raw_tutors) == 0):
    exit()

subjects_list = [
    list(val['preferredSubjects'])
    for val in dict_list_raw_tutors
]

subcategory = [
    list(val['preferredSubcategory'])
    for val in dict_list_raw_tutors
]

class_to_teach = [
    list(val['preferredClassToTeach'])
    for val in dict_list_raw_tutors
]

tutors_location_list = [
    list([val['locationLat'],val['locationLong']])
    for val in dict_list_raw_tutors
]
tutors_location_matrix = pd.DataFrame(tutors_location_list).as_matrix()

tutors_location_radius = [
    list([val['radius']])
    for val in dict_list_raw_tutors
]
tutors_location_radius = pd.DataFrame(tutors_location_radius)
r = np.array(tutors_location_radius)


tutor_ids_list = [
    bson.objectid.ObjectId(val['_id'])
    for val in dict_list_raw_tutors
]

dict_list_tutors = []
#subject_keys = ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'Economics', 'Gender Preference', 'Salary']
subject_keys = subjects[:]

for i in range(len(dict_list_raw_tutors)):
    dict_list_tutors.append(dict.fromkeys(subject_keys + subcategory_keys + class_to_teach_keys, 0))

for i in range(len(dict_list_raw_tutors)):
    dict_list_tutors[i]['Salary'] = dict_list_raw_tutors[i]['minPreferredSalary']
    dict_list_tutors[i]['Gender Preference'] = dict_list_raw_tutors[i]['gender']

    for chunk in subcategory[i]:
        if chunk in dict_list_tutors[i]:
            dict_list_tutors[i][chunk]=1

    for chunk in class_to_teach[i]:
        if chunk in dict_list_tutors[i]:
            dict_list_tutors[i][chunk]=1

    for chunk in subjects_list[i]:
        if chunk in dict_list_tutors[i]:
            dict_list_tutors[i][chunk]=1

df = pd.DataFrame(dict_list_tutors)
tutor_matrix = df.as_matrix()
tutors = np.transpose(tutor_matrix)
tutors[tutors=='m'] = 1
tutors[tutors=='f'] = 0

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#location input from mongo

## input from csv is akin to input from mongo query
## csv rows ---> collection documents
df_j_l = pd.DataFrame(jobs_location_list)
df_t_l = pd.DataFrame(tutors_location_list)
df_j_l = df_j_l.rename(index=str, columns={0: "latitude", 1: "longitude"})
df_t_l = df_t_l.rename(index=str, columns={0: "latitude", 1: "longitude"})


R = 6371.0
def haversine_np(lon1, lat1, lon2, lat2):

    #Calculate the great circle distance between two points
    #on the earth (specified in decimal degrees)

    #All args must be of equal length.
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = R * c
    return km

#df_jobs = df_jobs.iloc[0:3]
#radius_metres = df_tutors.iloc[:,2:3]
km2 = [haversine_np(df_j_l['longitude'],df_j_l['latitude'],
                    df_t_l['longitude'][i],df_t_l['latitude'][i]) for i in range(df_t_l.shape[0])]
km2 = np.array(km2)
km2 = np.transpose(km2)
distances = km2.copy()
r = r.reshape(1,r.shape[0])/1000
distances[(distances-r)<=0]=1
distances[distances!=1]=0


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#preferences matching using cosine similarities

g = np.dot(jobs,tutors)
norm_jobs = np.apply_along_axis(np.linalg.norm, 1, jobs)
norm_tutors = np.apply_along_axis(np.linalg.norm, 0, tutors)
norm_matrix = norm_jobs.reshape(jobs.shape[0],1)*norm_tutors.reshape(1,tutors.shape[1])
cosine_similarities = g / norm_matrix
haha = np.apply_along_axis(np.median, 1, cosine_similarities)
haha = haha.reshape(haha.shape[0],1)
takes=cosine_similarities>=haha

cosine_similarities[takes] = 1
cosine_similarities[~takes] = 0
matches = distances*cosine_similarities
matches = pd.DataFrame(matches)

#prepare matches DataFrame and export it to Mongo collection
#for i in range(len(job_ids_list)):
#    matches.rename(columns={i : i+1}, inplace=True)
#prepare list of match dicts with keys 'tutorid' 'jobId'
#populate each row of list that each dict with ids from the job_ids_list
#and the tutor_ids_list

dict_list_matches = []

states = np.where(matches==1)
matches_dict_keys = ['tutorId',  'jobId', 'previousStatus', 'currentStatus', 'dateOfStatusChange']
for i in range(len(states[0])):
    dict_list_matches.append(dict.fromkeys(matches_dict_keys, 0))
    dict_list_matches[i]['tutorId'] = tutor_ids_list[states[1][i]]
    dict_list_matches[i]['jobId'] = job_ids_list[states[0][i]]
    dict_list_matches[i]['dateOfStatusChange'] = datetime.datetime.now()
    dict_list_matches[i]['notified'] = 0
    #print(dict_list_matches[i])
matches_frame = pd.DataFrame(dict_list_matches)
matches_collection = db.matches
for i in range(len(dict_list_matches)):
    if(matches_collection.find_one({"$and": [{'tutorId': dict_list_matches[i]['tutorId']},
                                          {'jobId': dict_list_matches[i]['jobId']}]}) is None):
        matches_collection.insert(dict_list_matches[i])
    #matches_collection.replace_one
#matches_collection.insert(dict_list_matches)