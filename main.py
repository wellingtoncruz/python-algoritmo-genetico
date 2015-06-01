import os, subprocess, sys, socket, time, struct, random, traci, random
import fitness, guy, population

#guy.introduceYourself()
#print guy.getScore()

population = population.Population()
population.letsGoDarwin()
guy = population.getBestEvolutedGuy()
#guy = guy.Guy()
guy.introduceYourself()
#guy.showGUI()
#print guy.getScore()
