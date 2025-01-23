extends Node

func parse_input(input: String):
	var input_string = input.strip_edges().to_lower()
	var task_type = get_task(input_string)
	
	if task_type == "creating scene":
		print("Create Scene Task Detected")
		var nodes_to_create = get_Node(input_string)
		return true
	
	return false
	
func get_task(input: String)-> String:
	var tasks = {
		"creating scene": ["scene", "create a scene", "build a scene", "make scene", "design", "scene creation"],
		"creating script": ["script", "write", "program", "code", "create script"],
		"explaining code": ["explain", "understand", "code", "describe"],
		"explaining error": ["error", "debug", "issue", "explain error"],
		"correcting error": ["fix", "correct", "debug", "resolve", "problem"]
	}
	
	for task in tasks.keys():
		for keyword in tasks[task]:
			if keyword in input:
				return task
	
	return "Unknown task"
	
func get_Node(input:String)-> Array[String]:
	var node_list: Array[String]= []
	for keyword in input:
		if is_valid_node_type(keyword):
			node_list.append(keyword)
			
	return node_list
		
func is_valid_node_type(word: String) -> bool:
	return ClassDB.class_exists(word)
