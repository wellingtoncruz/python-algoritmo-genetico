import os, subprocess, sys, socket, time, struct, random, traci, random, datetime, copy
import guy, config

class Population:
	
	def __init__(self, brandnew=True):
		self.config = config.Config()	
		
		self.members = []
		self.nextgeneration = []
		self.generation = int(0)
	
		if(self.config.GENERATIONLOG):
			h = random.randrange(1000,9999)
			self.generationlogfile = open(self.config.GENERATIONLOGFILE+str(h), "w")
			self.generationmediafile = open("medias.txt"+str(h), "w")
				
		if(brandnew):
			for i in range(0, self.config.MAXPOPULATION):
				self.members.append(guy.Guy())
				
		self.orderYourGuys()
	
	def introduceYourGuys(self):
		for guy in self.members:
			guy.introduceYourself()
			
	def evaluateYourGuys(self, members):
		if(self.config.SPEEDLOG):
			speedlogfile = open(self.config.SPEEDLOGFILE, "w")
			print >> speedlogfile, "POPULATION EVALUATION STARTED AT %s" % (datetime.datetime.now())
		
		for i in range(0, len(members)):
			if(self.config.SPEEDLOG):
				print >> speedlogfile, "\tEVALUATION OF GUY NUM %d STATED AT %s" % (i, datetime.datetime.now())

			members[i].evaluateYourself()
			print " GUY %i SCORE: %f"%(i, members[i].getScore())
			
			if(self.config.SPEEDLOG):
				print >> speedlogfile, "\tEVALUATION OF GUY NUM %d FINISHED AT %s" % (i, datetime.datetime.now())
		
		if(self.config.SPEEDLOG):			
			print >> speedlogfile, "POPULATION EVALUATION FINISHED AT %s" % (datetime.datetime.now())
			
		return members
			
			
	def orderYourGuys(self):
		if(self.config.DEBUG):
			print "MEMBERS LIST BEFORE QUICKSORT"
			for guy in self.members:
				print guy.getScore()
			
		self.members = self._quicksort_(self.members)

		if(self.config.DEBUG):
			print "MEMBERS LIST AFTER QUICKSORT"
			for guy in self.members:
				print guy.getScore()
	
	def selectACouple(self):
		candidates = copy.copy(self.members)
		couple = []
		
		if(self.config.SELECTIONMETHOD==0):
			for x in [0,1]:
				roullete = selector = int(0)
				for i in range(1, len(candidates)):
					roullete += i*2
				
				rand = random.randrange(1, roullete)
				
				if(self.config.DEBUG):
					print "MAX VALUE FOR ROULLETE: %d"%(roullete)
					print "RANDOM VALUE FOR ROULLETE: %d"%(rand)

				for i in range(1, len(candidates)):
					selector += i*2
					if(rand > selector):
						continue
					else:
						if(self.config.DEBUG):
							print "\nSELECTED GUY IS: "
							print candidates[i].introduceYourself()
					
						couple.append(candidates.pop(i))
						break
						
		elif(self.config.SELECTIONMETHOD==1):
			for x in [0,1]:
				roullete = selector = float(0)
				for i in range(0, len(candidates)):
					roullete += candidates[i].getScore()
				
				rand = random.randrange(0, int(roullete))
				
				if(self.config.DEBUG):
					print "MAX VALUE FOR ROULLETE: %d"%(roullete)
					print "RANDOM VALUE FOR ROULLETE: %d"%(rand)

				for i in range(0, len(candidates)):
					selector += candidates[i].getScore()
					if(rand > selector):
						continue
					else:
						if(self.config.DEBUG):
							print "\nSELECTED GUY IS: "
							print candidates[i].introduceYourself()
					
						couple.append(candidates.pop(i))
						break						
		
		return couple
	
	def buildNextGeneration(self):

		if(self.config.GENERATIONLOG):
			print >> self.generationlogfile, "GENERATION %d SUMMARY:"%(self.generation)
			medium = 0.0
			for i in range(0, len(self.members)):
				#print >> self.generationlogfile, "GUY %i SCORE %f "%(i, self.members[i].getScore())
				medium += self.members[i].getScore()
				print >> self.generationlogfile, "%d&%f\\\\"%(i, self.members[i].getScore())
				print >> self.generationlogfile, "\hline"
			#print >> self.generationlogfile, "media: %f"%(medium/len(self.members))
			print >> self.generationmediafile, "%s"%(str(medium/len(self.members)).replace(".",","))
		self.generation += 1
		
		i = 0
		while(i < self.config.MAXPOPULATION):
			couple = self.selectACouple()
			son = guy.Guy(False, False, couple[0], couple[1])
			if(not(son.isEqual(couple[0])) and not(son.isEqual(couple[1]))):
				self.nextgeneration.append(son)
				i += 1
		
		self.nextgeneration = self.evaluateYourGuys(self.nextgeneration)
		self.members = self.members + self.nextgeneration
		self.nextgeneration = []
		
		self.orderYourGuys()
		
		self.members = self.members[self.config.MAXPOPULATION:]

		print "GENERATION %d SUMMARY"%(self.generation)
		for i in range(0, len(self.members)):
			g = self.members[i]
			print "i: %d s: %f"%(i, g.getScore())
		
	def letsGoDarwin(self):
		for i in range(0, self.config.MAXGENERATIONS):
			guy = self.getBestEvolutedGuy()
			if(guy.getScore() < self.config.VERYGOODGUY):
				self.buildNextGeneration()
			
	def getBestEvolutedGuy(self):
		return self.members[len(self.members)-1]

	def _quicksort_(self, members):
		
		if len(members) <= 1:
			return members
		
		less, equal, greater = [], [], []
		pivot = members[0]

		for guy in members:
			if(guy.getScore() < pivot.getScore()): 
				less.append(guy)
			elif(guy.getScore() == pivot.getScore()):
				equal.append(guy)
			else:
				greater.append(guy)
				
		return self._quicksort_(less) + equal + self._quicksort_(greater)
