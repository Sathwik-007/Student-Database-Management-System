from tkinter import *
from tkinter import ttk, messagebox
import json, os

textFont='Conoslas'

class displayQueries():

    allQueriesProcessed = False

    def checkQueries(self,root,*args):
        try:
            filehandler = open('queries.json','r')
            if os.path.getsize('queries.json') == 0:
                with open('queries.json','w') as file:
                    json.dump({"requests":[]},file,indent=4)
            filehandler.close()
        except FileNotFoundError:
            with open('queries.json','w') as file:
                json.dump({"requests":[]},file,indent=4)
            displayQueries.checkQueries = True

        with open('queries.json','r') as file:
            x = json.load(file)
            l = x['requests']
        if len(l) == 0:
            displayQueries.allQueriesProcessed = True
            self.disableButtons(*args)
            messagebox.showinfo(parent=root,title='No queries left',message='No queries left to be processed')
        else:
            displayQueries.allQueriesProcessed = False
            for i in args:
                i['state'] = NORMAL
        del x,l

    def retrieveQueries(self,root,b1,b2,b3,b4):
        self.checkQueries(root,b1,b2,b3,b4)
        if not displayQueries.allQueriesProcessed:
            b1['state'] = NORMAL
            b2['state'] = NORMAL
            b3['state'] = NORMAL
            b4['state'] = NORMAL
            d = dict()
            with open('queries.json','r') as file:
                x = json.load(file)
                d = x['requests']
            rollNumbers = []
            queryData = []
            for i in d:
                rollno = list(i.keys())
                rollNumbers.append(*rollno)
                data = list(i.values())
                queryData.append(list(data[0][0].values()))
            # print('Query data',queryData)
            for j in queryData:
                del j[len(j)-1] # removes profile_pic location
            for k in range(len(queryData)):
                queryData[k].insert(0,rollNumbers[k]) # inserts roll no
            # print('User requested queries:',queryData)
            del rollNumbers, d
            return queryData

    def disableButtons(self,*args):
        for i in args:
            i['state'] = DISABLED

    def denyAll(self,root,treeview,b1,b2,b3,b4):
        for row in treeview.get_children():
            treeview.delete(row)
        self.disableButtons(b1,b2,b3,b4)
        with open('queries.json','w') as file:
            json.dump({'requests':[]},file,indent=4)
        messagebox.showinfo(title='Denied requests',parent=root,message='All queries have been rejected.')

    def denySelected(self,treeview,b1,b2,b3,b4):
        deleteQuery = []
        for row in treeview.selection():
            deleteQuery.append(list(treeview.item(row)['values']))
            treeview.delete(row)
        with open('queries.json','r') as file:
            x = json.load(file)
            requests = x['requests']
            with open('queries.json','w') as filehandler:
                for query in deleteQuery:
                    for i in requests:
                        if query[0] in i.keys():
                            requests.remove(i)
                json.dump({"requests":requests},filehandler,indent=4)

        if len(treeview.get_children()) == 0:
            self.disableButtons(b1,b2,b3,b4)

    def approveAll(self,root,treeview,b1,b2,b3,b4):

        if len(treeview.get_children()) == 0:
            self.disableButtons(b1,b2,b3,b4)
        else:
            requests = dict()
            with open('queries.json','r') as file:
                x = json.load(file)
                requests = x['requests']

            queryList = []
            usrs = []
            for i in requests:
                x = list(i.keys())
                usrs.append(*x) 
                if x[0] in i.keys():
                    data = list(i.values())
                    queryList.append(list(data[0][0].items()))

            for i in range(len(queryList)):
                queryList[i].insert(0,('Roll no',usrs[i]))

            del usrs

            users = []
            with open('users.json','r') as file:
                a = json.load(file)
                users = a['users']
        
            safeUsers = []

            for usr in users:
                safe = True
                dontAppend = False
                for query in queryList:
                    for rollnoTuple in query:
                        if usr['Roll no'] != rollnoTuple[1]:
                            safe = True
                            dontAppend = False
                        else:
                            safe = False
                            dontAppend = True
                        break
                    if dontAppend:
                        break
                if safe:
                    safeUsers.append(usr)
            
            for i in queryList:
                with open('users.json','r') as file:
                    x = json.load(file)
                    d = x['users']
                    for k in d:
                        if k['Roll no'] == i[0][1]:
                            i.insert(3,('Password',k['Password']))
                            break
            
            try:
                f = open('users.json','r')
                if os.path.getsize('users1.json') == 0:
                    with open('users.json','w') as fhand:
                        d = {'users':[]}
                        json.dump(d,fhand,indent=4)
                f.close()
            except FileNotFoundError:
                with open('users.json','w') as file:
                    d = {'users':[]}
                    json.dump(d,file,indent=4)


            with open('users.json','r') as file:
                readFile = json.load(file)
                usersList = readFile['users']
                
                with open('users.json','w') as fhand:
                    # appending new details into users.json
                    for qry in queryList:
                        tempDict = {}
                        for item in qry:
                            tempDict[item[0]] = item[1]
                        
                        usersList.append(tempDict)
                    # appending remaining users into users.json

                    for usr in safeUsers:
                        usersList.append(usr)
                        
                    json.dump(readFile,fhand,indent=4)
            
            with open('queries.json','w') as file:
                reqs = {'requests':[]}
                json.dump(reqs,file,indent=4)

            del safeUsers, users
            messagebox.showinfo(parent=root,title='Processed all queries',message='All queries have been processed')
            self.disableButtons(b1,b2,b3,b4)
            
            for row in treeview.get_children():
                treeview.delete(row)

    def approveSelected(self,root,treeview,b1,b2,b3,b4):

        queries = []
        if len(treeview.get_children()) == 0:
            self.disableButtons(b1,b2,b3,b4)
        else:   
            for i in treeview.selection():
                # print("Selected requests:",i)
                rollno = treeview.item(i)['values']
                queries.append(list(rollno))
        
            del rollno
            for row in treeview.selection():
                treeview.delete(row)
        
            with open('users.json','r') as file:
                x = json.load(file)
                d = x['users']
            with open('queries.json','r') as file:
                y = json.load(file)
                e = y['requests']

                if len(e) == 0:
                    messagebox.showinfo(parent=root,title='Processed all queries',message='There are currently no queries left to be processed.')
                    self.disableButtons(b1,b2,b3,b4)

                else:
                    with open('users.json','w') as fhand:
                        dictionary = []
                        for i in queries:
                            for j in e:
                                if i[0] in j.keys():
                                    for m in d:
                                        if i[0] == m['Roll no']:
                                            value = j[i[0]][0]
                                            dictionary.append({'Roll no':i[0].upper(),'Department':i[1].upper(),'Username':i[2],
                                            'Password':m['Password'],'Email':i[3],'Phno':i[4],'Address':i[5],'Cgpa':i[6],
                                            'profile_pic':value['profile_pic']})
                                    e.remove(j)
                        del queries
                        for i in d:
                            for j in dictionary:
                                if i['Roll no'] == j['Roll no']:
                                    d.remove(i)
                        
                        dictionary.extend(d)
                        
                        json.dump({'users':dictionary},fhand,indent=4)
                        del dictionary
                        with open('queries.json','w') as filehandler:
                            json.dump({'requests':e},filehandler,indent=4)
                            del e