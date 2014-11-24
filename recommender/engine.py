# -*- coding: utf-8 -*-
from constants import DEFAULT_RECOMMENDER

from recommender.rec import Dacu, HitsRec, get_acepted_problems
from recommender.database import ProblemsDatabase
from recommender.metrics import Metrics

def create_default_recommender():
    print 'load problems database'
    database = ProblemsDatabase()
    print 'calc metrics'
    metrics = Metrics(database.get_problems_by_user())
    print 'save metrics'
    database.save_metrics(metrics)


def rec(spojId, recName='DACU',topk=5):
    database = ProblemsDatabase(True)
    metricsDict = database.get_metrics()
    user = database.find_user(spojId)

    if spojId in metricsDict["problems"]:
        pass
    elif user is not None:
        metrics = Metrics()
        metrics.__dict__.update(metricsDict)
        recommendedProblems = []
        userProblems = database.get_problems_of_user_from_db(spojId)
        
        if recName == 'DACU':
            rec = Dacu(metrics, get_acepted_problems(userProblems))
            recProblems = rec.rec(spojId, topk)
        elif recName == 'HITS':
            rec = HitsRec(metrics, get_acepted_problems(userProblems))
            recProblems = rec.rec(spojId, topk)
            
        cnt = 0
        for (problem, score) in recProblems:
            if cnt >= topk:
                break
            
            theProblem = database.find_problem(problem)
            title = problem
            url = 'http://br.spoj.com/problems/' + problem
            snippet = ''
            if theProblem is not None:
            	title = theProblem['title']
            	url = theProblem['url']
            	snippet = theProblem['snippet']
            	snippet = str(snippet)[0 : min(len(snippet), 200)]
            recommendedProblems.append({'spojId':problem, 'url':url, 'title':title, 'snippet':snippet})
    
            cnt += 1
        
        return recommendedProblems

if __name__ == "__main__":
    create_default_recommender()
    #print rec("ederfmartins", 10)
