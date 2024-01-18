"""
bfs
"""
from collections import deque
"""
def is_seller(name):
    return name[-1] == 'm'

graph = {}
graph["you"] = {"alice","bob","claire"}
graph["bob"] = {"anuj","peggy"}
graph["alice"] = {"peggy"}
graph["claire"] = {"thom","jonny"}  
graph["anuj"] = {}
graph["peggy"] = {}
graph["thom"] = {}
graph["jonny"] = {}

def search(name):
    search_deque = deque()
    search_deque += graph[name]
    searched = []
    while search_deque:
        person = search_deque.popleft()
        if not person in searched:
            if is_seller(person):
                print(person + "  is mango seller")
                return True
            else:
                # search_deque.append(graph[person])
                search_deque += graph[person]
                searched.append(person)

    return False

search("you")
"""




# ##########leetcode 797 bfs##########
# # graph = [[4,3,1],[3,2,4],[3],[4],[]]
# graph = [[1,2],[3],[3],[]]

# all = []
# n = len(graph)
# search_deque = deque()
# for t in graph[0]:
#     search_deque.append([0,t])
# while search_deque:
#     soul = search_deque.popleft()
#     end_n = soul[-1]
#     if end_n == n-1:
#         all.append(soul)
#     else:
#         if len(graph[end_n]):
#             for t in graph[end_n]:
#                 search_deque.append(soul + [t])

# print(all)



# ###################leetcode 797  dfs################################
# graph = [[4,3,1],[3,2,4],[3],[4],[]]
# # graph = [[1,2],[3],[3],[]]
# n = len(graph)
# stack = [[0]]
# all = []
# while len(stack):
#     path = stack.pop()
#     if path[-1] == n-1:
#         all.append(path)
#     else:
#         for next_node in graph[path[-1]]:
#             stack.append(path + [next_node])

# print(all)


# #################leetcode 1134#################3
# n = 153
# ll = []
# tmp = n
# while True:
#     k = tmp // 10
#     ll.append(tmp %10)
#     if k != 0:
#         tmp = k
#         continue
#     break
# m = len(ll)
# if n == sum([a**m for a  in ll]):
#     print("True")
# else:
#     print("false")




###############leetcode 455#######################33
g = [1,2,7,10]
s = [1,3,5,9]
#output: 3

ng = 0
ns = 0
g.sort()
s.sort()
while (ng <= len(g) -1 and ns<=len(s)-1):
    if s[ns] >= g[ng]:
        ns +=1
        ng +=1

    else:
        ns +=1

print("res: ", ng)