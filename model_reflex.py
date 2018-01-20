import numpy as np

class ModelAgent:
	def __init__(self):
		self.memory = [0,0,0]
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
    
	def update_state(state):
		# new_state: Dirty/BackHome/Straight/OneStep/NewR/FinalR/NewL/FinalL/RevertR
		if memory == [0,0,0] and state == "Free":
			new_state = "Straight"
		elif memory == [0,0,0] and state == "Blocked":
			new_state = "NewR"
		elif memory == [1,0,0] and state == "Free":
			new_state = "OneStep"
		if memory == [1,0,0] and state == "Blocked":
			new_state = "FinalR"
		elif memory == [1,1,0] and state == "Free":
			new_state = "FinalR"
		elif memory == [1,1,0] and state == "Blocked":
			new_state = "FinalR"
		elif memory == [1,1,1] and state == "Free":
			new_state = "Straight"
		elif memory == [1,1,1] and state == "Blocked":
			new_state = "NewL"
		elif memory == [0,1,1] and state == "Free":
			new_state = "OneStep"
		if memory == [0,1,1] and state == "Blocked":
			new_state = "RevertR"
		elif memory == [0,0,1] and state == "Free":
			new_state = "FinalL"
		elif memory == [0,0,1] and state == "Blocked":
			new_state = "FinalL"
		else:
			new_state = state
		
	# create condition-action rule sets (What action I should do now?)
	# background information (first rule that matches the given state description)
	def rule_match(self, state):   
		# new_state: Dirty/BackHome/Straight/OneStep/NewR/FinalR/NewL/FinalL/RevertR
		if state == "Dirty":
			action = "Clean"
		elif state == "Straight" or state == "OneStep":
			action = "GoHead"
		elif state == "NewR" or state == "FinalR" or state == "RevertR":   
			action = "TurnRight"     
		elif state == "NewL" or state == "FinalL": 
			action = "TurnLeft" 
		else: # BackHome
			action = "Off"
		return action
    
	def agent_program(self, percept):
		print("percept [W,D,H]:", percept)
		state = self.interpret_input(percept)
		print("state:", state)
		action = self.rule_match(state)		
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

