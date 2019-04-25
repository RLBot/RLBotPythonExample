import math
import time
from rlbot.agents.base_agent import  SimpleControllerState
from Util import *

'''
class defend:
	def __init__(self):

	def execute(self, agent):

		return dependableController(agent, target_location, target_speed)
'''
class collectBoost:
	def __init__(self):
		self.expired = False

	def execute(self, agent):
		closest_boost = -1
		closest_distance = 99999
		target_speed = 2300
		while closest_boost == -1:
			for i in range(1,len(boosts)):
				#if distance2D(boosts[i], agent.me) < closest_distance and (distance2D(boosts[i], agent.me) / target_speed) > agent.timers[i]:
				if distance2D(boosts[i], agent.me) < closest_distance and agent.activeBoosts[i] == True:
					closest_boost = i
					closest_distance = distance2D(boosts[i], agent.me)

		target_location = boosts[closest_boost]

		return dependableController(agent, target_location, target_speed)

class driveToBall:
	def __init__(self):
		self.expired = False

	def execute(self, agent):
		approachDistance = 30
		target_speed = 1600

		ballLocation = agent.ball.location
		goalCenter = Vector3([0 , 5100*-sign(agent.team), 200])
		ballGoalAngle = angle2(ballLocation, goalCenter)
		xlocation = approachDistance * sign(agent.team) * math.cos(ballGoalAngle)
		ylocation = approachDistance * sign(agent.team) * math.sin(ballGoalAngle)
		target_location = ballLocation - Vector3([xlocation, ylocation, 0])
		
		
		return dependableController(agent, target_location, target_speed)

'''
class takeShot:
	def __init__(self):
		self.expired = False

	def execute(self, agent):

		return dependableController(agent, target_location, target_speed)
'''
'''
class pushBall:
	def __init__(self):
		self.lostBall = False

	def execute(self, agent):

		return dependableController(agent, target_location, target_speed)
'''

def dependableController(agent, target_location, target_speed):
	controller_state = SimpleControllerState()

	location = toLocal(target_location,agent.me)
	angle = math.atan2(location.data[1],location.data[0])

	speed = velocity2D(agent.me)

	#steering
	controller_state.steer = steer(angle)

	#throttle
	if target_speed > speed:
		controller_state.throttle = 1.0
		if target_speed > 1400 and agent.start > 2.2 and speed < 2250:
			controller_state.boost = True
		else:
			controller_state.boost = False
	elif target_speed < speed:
		controller_state.throttle = 0
		controller_state.boost = False

	#dodging
	time_difference = time.time() - agent.start
	if time_difference > 2.2 and distance2D(target_location,agent.me) > (velocity2D(agent.me)*2.5) and abs(angle) < 1.3 and agent.me.location.data[2] < 100:
		agent.start = time.time()
	elif time_difference <= 0.1:
		controller_state.jump = True
		controller_state.pitch = -1
	elif time_difference >= 0.1 and time_difference <= 0.15:
		controller_state.jump = False
		controller_state.pitch = -1
	elif time_difference > 0.15 and time_difference < 1:
		controller_state.jump = True
		controller_state.yaw = controller_state.steer
		controller_state.pitch = -1

	return controller_state

