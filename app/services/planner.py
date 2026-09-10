from datetime import date,timedelta
from app.services.memory import memory,course_scope


def allocate_plan(exam_date,topics,scores,daily_minutes,today=None):
    today=today or date.today()
    exam=date.fromisoformat(exam_date) if isinstance(exam_date,str) else exam_date
    days=(exam-today).days-1
    if days<1:raise ValueError('Choose an exam at least two days away; the day before the exam is kept free.')
    if days>365:raise ValueError('Choose an exam within the next year.')
    topics=list({t.strip().casefold():t.strip() for t in topics if t.strip()}.values())
    lookup={k.casefold():v for k,v in scores.items()}
    scores={topic:lookup[topic.casefold()] for topic in topics if topic.casefold() in lookup}
    if not topics:raise ValueError('Provide topics or add a syllabus first.')
    slots=max(1,daily_minutes//30)
    weights={t:1+(100-float(scores.get(t,50)))/25 for t in topics}
    allocations={t:0 for t in topics}
    schedule=[]
    # Cover every topic once, weakest first, then weighted fair allocation.
    initial=sorted(topics,key=lambda t:float(scores.get(t,50)))
    for day in range(days):
        sessions=[]
        for slot in range(slots):
            topic=initial.pop(0) if initial else max(topics,key=lambda t:weights[t]/(allocations[t]+1))
            allocations[topic]+=1
            sessions.append({'topic':topic,'minutes':daily_minutes//slots+(1 if slot<daily_minutes%slots else 0),
                             'activity':'Learn and practice' if allocations[topic]==1 else 'Recall, practice and review mistakes',
                             'score':scores.get(topic)})
        schedule.append({'date':(today+timedelta(days=day)).isoformat(),'sessions':sessions})
    return {'exam_date':exam.isoformat(),'free_day':(exam-timedelta(days=1)).isoformat(),'schedule':schedule,
            'uncovered_topics':initial,'allocations':allocations,'daily_minutes':daily_minutes,
            'warning':'Not enough time to cover every topic. Increase daily minutes or narrow the syllabus.' if initial else None}


def save_plan(req):
    scope=course_scope(req.subject,req.level,req.board)
    profile=memory.profile(req.student_id,scope)
    topics=req.topics
    if not topics:
        from app.services.syllabus import syllabus_topics
        topics=syllabus_topics(req.subject,req.level,req.board)
    result=allocate_plan(req.exam_date,topics,profile['scores'],req.daily_minutes)
    profile['exam_date']=str(req.exam_date)
    memory.put(req.student_id,'profile',profile,scope,True)
    memory.put(req.student_id,'plan_spec',{'exam_date':str(req.exam_date),'topics':topics,'daily_minutes':req.daily_minutes},scope,True)
    return result


def current_plan(student_id,scope):
    specs=memory.read(student_id,'plan_spec',scope)
    if not specs:return None
    try:return allocate_plan(**specs[-1],scores=memory.profile(student_id,scope)['scores'])
    except ValueError as exc:return {'expired':True,'message':str(exc)}
