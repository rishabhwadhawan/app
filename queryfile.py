import sys
import re
from py2neo import  Node,Relationship,Graph

file = open('/home/master/data/test_query.txt','w')

authorvalue  = sys.argv[1]
papervalue = sys.argv[2]
journalvalue  = sys.argv[3]

ifauthornodetrue = sys.argv[4]
ifpapernodetrue = sys.argv[5]
ifjournalnodetrue = sys.argv[6]

firstnode = sys.argv[7]
secondnode = sys.argv[8]
thirdnode = sys.argv[9]

#RISHABH CODE STARTS HERE
journalyearvalue = re.search('\d\d\d\d',journalvalue);

if journalyearvalue is None:
    journalyear = '*'
    journalname = journalvalue

else:

    journalyear = journalyearvalue.group(0)
    journalvalue = re.sub('\d\d\d\d','',journalvalue);
    journal_list = journalvalue.split(',')

    if journal_list[0] is "":
        journalname = journal_list[1]
    else:
        journalname = journal_list[0]

journalvalues = [journalname,journalyear]

#RISHABH CODE ENDS HERE

#ifauthornodetrue = '0'
#ifpapernodetrue = '1'
#ifjournalnodetrue = '1'
if_list = [ifauthornodetrue,ifpapernodetrue,ifjournalnodetrue]
step_num = 0
for i in range(0,3):
    if(if_list[i] == '1'):    step_num+=1

#firstnode = "journal"
#secondnode = "paper"
#thirdnode = "author"
node_list = [firstnode,secondnode,thirdnode]

#authorvalue = "*"
#papervalue = "*"
#journalvalues = ["IEEE Trans. Knowl. Data Eng.","*"]
value_list = [authorvalue,papervalue,journalvalues]

flag = 1
for i in range(0,step_num):
    if(node_list[i] == "journal"):
        node_list[i] = "Journal"
        if(journalvalues[0] != "*" or journalvalues[1] != "*"):
            flag = 0
    else:
        if(node_list[i] == "author"):
            node_list[i] = "Author"
            if(authorvalue != "*"):
                flag = 0
        if(node_list[i] == "paper"):
            node_list[i] = "Article"
            if(papervalue != "*"):
                flag = 0

query_string = "match $ = "
#sprint (query_string)
for i in range(0,step_num):
    query_string = query_string+" ($"+str(i)+":"+node_list[i]+") - [] -> "
query_string = query_string[:len(query_string) - 8]
#print (query_string)
#print(flag)
if(flag == 0):

    query_string+=" where "
    for i in range(0,step_num):
        if(node_list[i] == "Journal"):
            if(journalvalues[0] != "*"):    query_string = query_string + "$" + str(i) + ".name = \"" + journalvalues[0] + "\" and "
            if(journalvalues[1] != "*"):    query_string = query_string + "$" + str(i) + ".year = \"" + journalvalues[1] + "\" and "
        if(node_list[i] == "Author" and authorvalue != "*"):
            query_string = query_string + "$" + str(i) + ".name = \"" + authorvalue + "\" and "
        if(node_list[i] == "Article"and papervalue != "*"):
            query_string = query_string + "$" + str(i) + ".title = \"" + papervalue + "\" and "
    query_string = query_string[:len(query_string) - 4]

query_string+=" return "
for i in range(0,step_num):
    query_string = query_string + "$" + str(i) + ".latitude, $" + str(i) + ".longitude, $" + str(i) + ", "
query_string = query_string[:len(query_string) - 2]
#print query_string
file.write(query_string)
file.write("   ")
file.write(firstnode)
file.write("   ")
file.write(secondnode)
file.write("   ")
file.write(thirdnode)
file.write("   ")
file.write(ifauthornodetrue)
file.write("   ")
file.write(ifpapernodetrue)
file.write("   ")
file.write(ifjournalnodetrue)
file.write("   ")
file.write(authorvalue)
file.write("   ")
file.write(papervalue)
file.write("   ")
file.write(journalyear)
file.write("   ")
file.write(journalname)
file.write("FLAG IS           ->    ")
file.write(str(flag))
graph = Graph()
results = graph.cypher.execute(query_string)

l = []

for record in results:
    ll = []

    for row in record:

        print row








