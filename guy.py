import os, subprocess, sys, socket, time, struct, random, traci, random
import config, fitness

class Guy:
	
	def __init__(self, autoFitness=True, randomize=True, mother=False, father=False):
		self.config = config.Config()
		self.lights = [[],[]]
		
		for i in range(0, len(self.config.LIGHTSID)):
			if(randomize):
				self.lights[i].append(self.generateCromossome())
			else:
				self.lights[i].append(self.crossCromossome(mother.getCromossome(i), father.getCromossome(i)))
		
		mutate = (float(random.randrange(0, 100))/100)

		if(mutate <= self.config.MUTATIONRATE):
			self.mutateMyself()
		
		for i in range(0, len(self.config.LIGHTSID)):			
			self.lights[i].append(self.calculateTime(self.lights[i][0]))
			self.lights[i].append(self.config.CYCLE_TIME - self.lights[i][1])
			
		self.fitness = fitness.Fitness(self)
		self.score = 0.0
			
		if(autoFitness):
			self.evaluateYourself()
			self.lights.append(self.score)

	def getScore(self):
		return self.score
		
	def getCromossome(self, i):
		return self.lights[i][0]
		
	def generateCromossome(self):
		cromossome = str()
		max_green_time = self.config.CYCLE_TIME - (self.config.YELLOW_TIME * 2) - (self.config.MINFASETIME)
		total_fase_time = self.config.CYCLE_TIME - (self.config.YELLOW_TIME * 2)
		
		if(self.config.CREATIONMETHOD==0):		
			for i in range(0, max_green_time):
				rand1 = random.randrange(0, 100)
				rand2 = random.randrange(0, 100)
				if(rand2 < rand1):
					cromossome += str("1")
				else:
					cromossome += str("0")
					
		elif(self.config.CREATIONMETHOD==1):
			ones = random.randrange(0, max_green_time)
			positions = []
			for i in range(0, ones):
				pos = random.randrange(0, total_fase_time)
				while(pos in positions):
					pos = random.randrange(0, total_fase_time)
				positions.append(pos)
			
			for i in range(0, total_fase_time):
				if(i in positions):
					cromossome += str("1")
				else: 
					cromossome += str("0")
		
		return cromossome
		
	def crossCromossome(self, cromofather, cromomother):
		div = random.randrange(0, self.config.CYCLE_TIME)
		
		if(self.config.DEBUG):
			print "DIV %d"%(div)
			print "DAD: %s"%(cromofather)
			print "MON: %s"%(cromomother)
			print "SON: %s"%(cromofather[:div] + cromomother[div:])
		
		return cromofather[:div] + cromomother[div:]
	
	def mutateMyself(self):
		
		for x in range(0, len(self.config.LIGHTSID)):
			genesToMutate = random.randrange(0, int(len(self.lights[x][0]) * self.config.MUTATIONGENERATE))
			for i in range(0, genesToMutate):
				position = random.randrange(0, len(self.lights[x][0]))
				newgene = str((int(self.lights[x][0][position]) + 1) % 2)
				self.lights[x][0] = self.lights[x][0][:position] + newgene + self.lights[x][0][position+1:]
	
	def calculateTime(self, cromossome):
		greenTime = int(0)
		for c in cromossome:
			if(int(c) > 0):
				greenTime += 1
		return greenTime
		
	def isEqual(self, otherguy):
		if((self.lights[0][0] == otherguy.lights[0][0]) and (self.lights[1][0] == otherguy.lights[1][0])):
			return True

		
	def introduceYourself(self):
		guyfile = open("guy"+str(random.randrange(1000,9999))+".txt", "w")
		print "Hello, I'm a Guy"
		print "My Cromossome is for Light %s is %s."%(self.config.LIGHTSID[0], self.lights[0][0])
		print "My Cromossome is for Light %s is %s."%(self.config.LIGHTSID[1], self.lights[1][0])
		print "My Green Time for Light %s is %d."%(self.config.LIGHTSID[0], self.lights[0][1])
		print "My Green Time for Light %s is %d."%(self.config.LIGHTSID[1], self.lights[1][1])
		print "My Red Time for Light %s is %d."%(self.config.LIGHTSID[0], self.lights[0][2])
		print "My Red Time for Light %s is %d."%(self.config.LIGHTSID[1], self.lights[1][2])
		print "And my Score is %f.\n"%(self.score)
		
		print  >> guyfile, "\hline"
		print  >> guyfile, "Cromossomo 1: %s\\\\"%(self.lights[0][0])
		print  >> guyfile, "Tempo de Verde:  %ds\\\\"%(self.lights[0][1])
		print  >> guyfile, "Tempo de Vermelho:  %ds\\\\"%(self.lights[0][2])
		
		print  >> guyfile, "Cromossomo 2: %s\\\\"%(self.lights[1][0])
		print  >> guyfile, "Tempo de Verde:  %ds \\\\"%(self.lights[1][1])
		print  >> guyfile, "Tempo de Vermelho:  %ds \\\\"%(self.lights[1][2])
		print  >> guyfile, "Fitness %f \\\\"%(self.score)
		print  >> guyfile, "\hline"
	
	def evaluateYourself(self):
		self.score = self.fitness.evaluate()
		
	def showGUI(self):
		self.score = self.fitness.evaluate(True)
