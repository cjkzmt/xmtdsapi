
while True:
    list=fetch_new_tasks(12)
    if len(list)==0: break
    for i in list:
        worker(i)
