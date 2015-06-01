import os, subprocess, sys, socket, time, struct, random, traci, random, copy
import config

class Fitness:

	def __init__(self, guy):
		self.guy = guy
		self.config = config.Config()
		
	def evaluate(self, GUI=False):

		global_step = int(1)
		lights_config = self.guy.lights
		cycle= [[],[]]
		
		lights_id = self.config.LIGHTSID
		passed_cycles = [int(0),int(0)]
		detectors = self.config.DETECTORSID
		
		detectors_registry = [[],[]]
		detectors_jam = [[],[]]
		detectors_count = [[],[]]
		cycles_saturation = [[],[]]
		lane_saturation = [[],[]]
		medium_values = [[],[]]

		for x in range(0, len(self.config.LIGHTSID)):
			cycle[x] = dict([(lights_config[x][1] + lights_config[x][2] + self.config.YELLOW_TIME, self.config.YELLOW_PHASEA), (lights_config[x][1] + self.config.YELLOW_TIME, self.config.RED_PHASE), (lights_config[x][1], self.config.YELLOW_PHASEB), (0, self.config.GREEN_PHASE)])
		
		#cycle[0] = dict([(58, self.config.YELLOW_PHASEA), (40, self.config.RED_PHASE), (38, self.config.YELLOW_PHASEB), (0, self.config.GREEN_PHASE)])
		
		#cycle[1] = dict([(58, self.config.YELLOW_PHASEA), (43, self.config.RED_PHASE), (41, self.config.YELLOW_PHASEB), (0, self.config.GREEN_PHASE)])
				
		if(self.config.LOG):
			logfile = open(self.config.LOGFILE, "w")
		
		if(self.config.DEEPLOG):
			deeplogfile = open(self.config.DEEPLOGFILE, "w")
		
		for x in range(len(detectors)):
			for i in range(len(detectors[x])):
				detectors_registry[x].append([[],[]])
				detectors_count[x].append([0, 0])
				detectors_jam[x].append(0)
				medium_values[x].append(0)
				
		self.config.configSumo(GUI)
		
		traci.init(self.config.PORT)

		while(global_step <= self.config.SIMULATION_TIME):

			step_lights = [int(global_step % self.config.CYCLE_TIME), int((global_step + self.config.OFFSET) % self.config.CYCLE_TIME)]

			traci.simulationStep(global_step)
			
			for x in range(0, len(lights_id)):

				for time in sorted(cycle[x].keys(), reverse=True):
				
					if(step_lights[x] >= time):
						traci.trafficlights.setRedYellowGreenState(lights_id[x], cycle[x][time])
						break
						
				if(self.config.DEEPLOG):
					print >> deeplogfile, "\nGLOBAL STEP %d: LIGHT STEP %d LIGHT: %s" % (global_step, step_lights[x], lights_id[x])

				if(step_lights[x] == 0):
					new_cycle = True
					passed_cycles[x] += 1
				else:
					new_cycle = False

				if(self.config.LOG and new_cycle and (passed_cycles[x] > self.config.IGNORECYCLES)):
					print >> logfile, "CYCLE %d LIGHT: %s"%(passed_cycles[x], lights_id[x])

				for i in range(0, len(detectors[x])):
				
					'''
					print str(detectors[x][i]) + "_IN"
					print traci.inductionloop.getLastStepVehicleNumber(str(detectors[x][i]) + "_IN")
					print str(detectors[x][i]) + "_OUT"
					print traci.inductionloop.getLastStepVehicleNumber(str(detectors[x][i]) + "_OUT")
					print traci.inductionloop.getLastStepVehicleIDs(str(detectors[x][i]) + "_OUT")
					'''
					
					detecIn = traci.inductionloop.getLastStepVehicleIDs(str(detectors[x][i]) + "_IN")
					detecOut = traci.inductionloop.getLastStepVehicleIDs(str(detectors[x][i]) + "_OUT")
					
					for car in detecIn:
						if(not(car in detectors_registry[x][i][0])):
							detectors_count[x][i][0] += 1
							detectors_jam[x][i] = 0
							detectors_registry[x][i][0].append(car)
						else:
							detectors_jam[x][i] += 1

					for car in detecOut:
						if(not(car in detectors_registry[x][i][1])):
							detectors_count[x][i][1] += 1
							detectors_registry[x][i][1].append(car)
							
					if(detectors_jam[x][i] >= self.config.JAMDETECTION):
						if(self.config.DEBUG):
							print "JAM DETECTED ON LANE: %s"%(detectors[x][i])
						detectors_count[x][i][0] += 1 * self.config.JAMPENALTY

					if(self.config.DEBUG):
						print detectors_count[x]
						
					if(self.config.DEEPLOG):
						print >> deeplogfile, "LANE: %s COUNT IN: %d OUT: %d" % (detectors[x][i], detectors_count[x][i][0], detectors_count[x][i][1])
						
					if(new_cycle):
							
						if(passed_cycles[x] > self.config.IGNORECYCLES):

							if((detectors_count[x][i][0] > 0) and (detectors_count[x][i][1]) > 0):
								lane_saturation[x].append(float(detectors_count[x][i][1]) / float(detectors_count[x][i][0]))
							else:
								if(detectors_count[x][i][0] <= 0):
									lane_saturation[x].append(1)
								else:
									lane_saturation[x].append(0)
							
							if(self.config.DEBUG):
								print "LANE: %s OUT: %f IN: %f SAT: %f"%(detectors[x][i], float(detectors_count[x][i][1]), float(detectors_count[x][i][0]), lane_saturation[x][i])
								
							if(self.config.LOG):
								print >> logfile, "\tLANE %s\n\tIN: %d\n\tOUT:%d\n\tSATURATION %f\n" % (detectors[x][i], detectors_count[x][i][0], detectors_count[x][i][1], lane_saturation[x][i])

						detectors_count[x][i][0] -= detectors_count[x][i][1]
						detectors_count[x][i][1] = 0
						if(detectors_count[x][i][0] < 0):
							detectors_count[x][i][0] =0
				
				if(new_cycle and (passed_cycles[x] > self.config.IGNORECYCLES)):
					if(self.config.DEBUG):
						print "Saturacao x: %d i: %d"%(x,i)
						print lane_saturation[x]
					cycles_saturation[x].append(copy.deepcopy(lane_saturation[x]))
					lane_saturation[x] = []
					
			global_step += 1
	
		traci.close()
		
		cycles_logged = [int(0),int(0)]

		for light in range(0, len(cycles_saturation)):
			for cycle in range(0, len(cycles_saturation[light])):
				cycles_logged[light] += 1
				for lane in range(0, len(cycles_saturation[light][cycle])):
					medium_values[light][lane] += cycles_saturation[light][cycle][lane]
					if(self.config.DEBUG):
						print "L: %d C: %d L: %d V: %f \n"%(light, cycle, lane, cycles_saturation[light][cycle][lane])

		for light in range(0, len(medium_values)):
			for lane in range(0, len(medium_values[light])):
				medium_values[light][lane] = medium_values[light][lane] / cycles_logged[light]
				
		medium_values = copy.deepcopy(medium_values[0] + medium_values[1])
		score = 0.0
		
		for value in range(0, len(medium_values)):
			score += medium_values[value]
			
		return score
