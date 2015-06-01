import os, subprocess, sys, socket, time, struct, random, traci, random, datetime
class Config:

	def __init__(self):
		#TCP PORT for TRACI
		self.PORT = 8813
		
		#Application
		self.DEBUG = False
		self.LOG = True
		self.DEEPLOG = False
		self.SPEEDLOG = True
		self.GENERATIONLOG = True
		
		#Logfiles
		self.LOGFILE = "log.txt"
		self.DEEPLOGFILE = "deeplog.txt"
		self.SPEEDLOGFILE = "speed.txt"
		self.GENERATIONLOGFILE = "generations.txt"

		#Bussiness rules
		self.JAMDETECTION = 25
		self.JAMPENALTY = 2
		self.YELLOW_TIME = 2
		self.MINFASETIME = 2

		#Times
		self.SIMULATION_TIME = 720
		#self.SIMULATION_TIME = 360
		self.CYCLE_TIME = 60
		self.OFFSET = 10;
		self.IGNORECYCLES = 2
		
		#TRACI Lights Config
		self.LIGHTSID = ["A", "B"]
		#self.DETECTORSID = [["AT_A","A_AT","AB_A","A_AB", "AL_A","A_AL","B_A"],["BT_B","B_BT","BB_B","B_BB","BR_B","B_BR","A_B"]]
		self.DETECTORSID = [["AT_A","AB_A","AL_A","B_A"],["BT_B","BB_B","BR_B","A_B"]] #Vias de Entrada
		
		self.GREEN_PHASE = "GGrrGGrr"
		self.YELLOW_PHASEA = "rryyrryy"
		self.YELLOW_PHASEB = "yyrryyrr"
		self.RED_PHASE = "rrGGrrGG"
		
		#Sumo Config
		self.SUMOEXEGUI = "sumo-gui"
		#self.SUMOEXE = "sumo-gui"
		self.SUMOEXE = "sumo"
		self.SUMOCONFIG = "tgiv1.sumo.cfg"
		
		#Genetic Algorithms
		self.MAXPOPULATION = 20
		self.MAXGENERATIONS = 10
		self.MUTATIONRATE = 0.3
		self.MUTATIONGENERATE = 0.05
		self.CREATIONMETHOD = 1
		self.SELECTIONMETHOD = 0
		self.PERFECTRATE = 0.95
		self.VERYGOODGUY = (len(self.DETECTORSID[0]) + len(self.DETECTORSID[1])) * self.PERFECTRATE
		
	def configSumo(self, GUI):
		if "SUMO" in os.environ:
			self.SUMOEXE = os.path.join(os.environ["SUMO"], "sumo-gui")
		if(GUI):
			self.SUMOPROCESS = subprocess.Popen("%s -c %s" % (self.SUMOEXEGUI, self.SUMOCONFIG), shell=True, stdout=sys
			.stdout)
		else:
			self.SUMOPROCESS = subprocess.Popen("%s -c %s" % (self.SUMOEXE, self.SUMOCONFIG), shell=True, stdout=sys
			.stdout)