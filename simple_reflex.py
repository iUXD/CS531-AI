class SimpleDeterminAgent:
	def __init__(self):
		pass
        
	# build a general-purpose interpreter (What the world is like now?)
	# current internal state (abstract description of the current state from the percept)
	def interpret_input(self, percept): 
		# percept = wall/dirt/home
		if percept[1] == 1:
		    state = "Dirty"        
		elif percept[0] == 0:
		#elif percept[0:2] == [0, 0]:
		    state = "Free"
		elif percept[0] == 1 and percept[2] == 1:
		    state = "BackHome"
		#elif percept[0:2] == [1, 0]:
		#    state = "Blocked"        
		else: #"Blocked" 
		    state = "Blocked"
		return state
    
	# create condition-action rule sets (What action I should do now?)
	# background information (first rule that matches the given state description)
	def rule_match(self, state):      
		# state = Dirty, BackHome, Blocked, Free
		if state == "Dirty":
			action = "Clean"
		elif state == "Free":
			action = "GoHead"
		elif state == "Blocked":            
			action = "TurnRight"        
		else: # state = "BackHome"
			action = "Off"
		return action
    
	def agent_program(self, percept):
		print("percept:", percept)
		state = self.interpret_input(percept)
		print("state:", state)
		action = self.rule_match(state)
		print("action:", action)
		return action

	def update_position(self, action, location, direction):
	# action = GoHead, TurnRight, TurnLeft, Clean, Off
		if action == "GoHead":
			if direction == 0:
				location[0] += 1
			elif direction == 1:
				location[1] += 1
			elif direction == 2:
				location[0] -= 1
			else: # direction == 4
				location[1] -= 1            
		elif action == "TurnRight":            
			if direction == 3:
				direction = 0
			else:
				direction += 1        
		elif action == "TurnLeft":
			if direction == 0:
				direction = 3
			else:
				direction -= 1 
		else: # action = Clean, Off
			location = location 
		return location, direction
    
	def update(self, percept, location, direction):
		print("current position:", location, direction)
		# Decision Making
		action = self.agent_program(percept)
		# For visualization
		location, direction = self.update_position(action, location, direction)
		print("new position:", location, direction)  
		return location, direction,action

