import numpy as np

class SimpleDeterminAgent:
	def __init__(self, init_param):
		self.deterministic = init_param
		pass
        
	# build a general-purpose interpreter (What the world is like now?)
	# current internal state (abstract description of the current state from the percept)
	def interpret_input(self, percept): 
		# percept: Wall/Dirt/Home
		if percept[1] == 1:
		    state = "Dirty"        
		elif percept[0] == 0:
		    state = "Free"
		elif percept[0] == 1 and percept[2] == 1:
		    state = "BackHome"      
		else: # Blocked
		    state = "Blocked"
		return state
    
	# create condition-action rule sets (What action I should do now?)
	# background information (first rule that matches the given state description)
	def rule_match_deterministic(self, state):      
		# state: Dirty/BackHome/Blocked/Free
		if state == "Dirty":
			action = "Clean"
		elif state == "Free":
			action = "GoHead"
		elif state == "Blocked":   
			action = "TurnRight"        
		else: # BackHome
			action = "Off"
		return action

	def rule_match_stochastic(self, state):      
		# state: Dirty/BackHome/Blocked/Free
		if state == "Dirty":
			action = "Clean"
		elif state == "Free":
			action = np.random.choice(["GoHead", "TurnRigt", "TurnLeft"], 1, p=[0.34, 0.33, 0.33])
		elif state == "Blocked":  
			action = np.random.choice(["TurnRigt", "TurnLeft"], 1, p=[0.5, 0.5])        
		else: # BackHome
			action = "Off"
		return action
    
	def agent_program(self, percept):
		print("percept [W,D,H]:", percept)
		state = self.interpret_input(percept)
		print("state:", state)
		if self.deterministic == True:
			action = self.rule_match_deterministic(state)
		else: # stochastic
			action = self.rule_match_stochastic(state)
		print("action:", action)
		return action

	def update_position(self, action, location, direction):
		# action = GoHead/TurnRight/TurnLeft/Clean/Off
		if action == "GoHead":
			if direction == 0:
				location[1] += 1
			elif direction == 1:
				location[0] += 1
			elif direction == 2:
				location[1] -= 1
			else: # 3
				location[0] -= 1
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
		else: # Clean, Off
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

