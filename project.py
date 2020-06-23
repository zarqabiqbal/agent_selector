#main function which checks the selection mode and use other function according to it
def give_available_agent_list(agent_data,choice, issue_list):
    available_agent_list = []
    if choice is "all_available":
        available_agent_list = all_available_mode(agent_data, issue_list)
    elif choice is "least_busy":
        available_agent_list= least_busy_mode(agent_data,issue_list)
    elif choice is "random":
        available_agent_list = random_mode(agent_data,issue_list)
    return available_agent_list


#function for selecting all agent available for issue
def all_available_mode(agent_data, issue_list):
    agents_list = []
    for issue in issue_list:
        available_agent = []
        for agent in agent_data:
            issues = issue.split("/")
            if check_agent_suitaility_for_role(agent[2].split("/"), issues) and agent[0]:
                available_agent.append(agent[3])
        agents_list.append(available_agent)
    return agents_list


#function for least busy agent selection
def least_busy_mode(agent_data,issue_list):
        agents_list=[]
        for issue in issue_list:
            available_agent=[]
            for agent in agent_data:
                issues = issue.split("/")
                if check_agent_suitaility_for_role(agent[2].split("/"), issues) and agent[0]:
                    available_agent.append(agent)
            agents_list.append([check_longest_availability(available_agent)])
        return agents_list


#function for random agent selection
def random_mode(agent_data,issue_list):
    from random import randint
    agents_list = []
    for issue in issue_list:
        available_agent = []
        for agent in agent_data:
            issues = issue.split("/")
            if check_agent_suitaility_for_role(agent[2].split("/"), issues) and agent[0]:
                available_agent.append(agent[3])
        agents_list.append([available_agent[randint(0,len(available_agent)-1)]])
    return agents_list

#extract issue list from csv
def give_issue_list(filePath):
    import pandas as pd
    issue_list_data = pd.read_csv(filePath, sep=",")
    return issue_list_data["issue_list"].tolist()

#extract agent_data from csv
def give_agent_details(filePath):
    import pandas as pd
    agent_data = pd.read_csv(filePath, sep=",")
    return agent_data.values.tolist()

#function for check agent is suitable for issue or not
def check_agent_suitaility_for_role(agent_role, issues):
    agent_suitable = False
    for issue in issues:
        if issue in agent_role:
            agent_suitable = True
            break
    return agent_suitable

#function for checking agent longest availability
def check_longest_availability(agent_data):
    from datetime import datetime
    availability_time=[]
    for data in agent_data:
        current_time=datetime.now()
        agent_available_time=datetime.strptime(data[1],"%H:%M:%S")
        availability_time.append((current_time-agent_available_time).seconds)
    return agent_data[availability_time.index(max(availability_time))][3]

#extract data from csv
agent_data=give_agent_details("./agent_data.csv")
issues_list=give_issue_list("./issue_list.csv")

#use function for agent selection with diffrent mode and print it
print(give_available_agent_list(agent_data,"all_available",issues_list ))
print(give_available_agent_list(agent_data,"least_busy", issues_list))
print(give_available_agent_list(agent_data,"random", issues_list))
