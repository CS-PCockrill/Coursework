from collections import defaultdict

task_list = [
	"task: taskA",
	"files: foobar.txt bar.txt",
	"deps: taskB taskC",
	"",
	"task: taskB",
	"files: tester.py",
	"deps: taskD taskC",
	"",
	"task: taskC",
	"files: potato.c",
	"deps: taskE",
	"",
	"task: taskD",
	"files: init.py",
	"deps: taskE",
	"",
	"task: taskE",
	"files: testing.c",
	"deps:",
	""
	]

def findRerunTasks(taskDependencyList, filesChanged):
	rerunTasks = []
	adjlist = defaultdict(list)
	changedNode = []

	for task in range(0, len(taskDependencyList), 4):
		taskName = taskDependencyList[task].split(": ")[1]
		deps = taskDependencyList[task+2].split(" ")[1:]
		files = taskDependencyList[task+1][7:]

		if files in filesChanged:
			changedNode.append(taskName)

		# structured as Task: <-depends on
		# in other words, list/value is all tasks that depend on key
		for dep in deps:
			adjlist[dep].append(taskName)

	print(adjlist)

	# Perform DFS on changed nodes to determine recompilation order (in reverse order)
	for node in changedNode:
		dfs(node, adjlist, rerunTasks)
	# Reverse list to get order tasks need to recompile in.
	return rerunTasks[::-1]

def dfs(task, graph, rerun):
	for dep in graph[task]:
		if dep not in rerun:
			dfs(dep, graph, rerun)

	rerun.append(task)
	return True

print(findRerunTasks(task_list, ["testing.c"]))

