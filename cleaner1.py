import time
import datetime
import copy

class Cleaner:
    def __init__(self, environment):
        self.environment = environment
        self.environmentSize = 2
        self.moveDirection = 1
        self.cleanedFloors = []
        self.actualScore = 0
        self.scores = []
        self.actionController()

    def addScore(self, scoreType):
        measures = {
            "analyze and clean": 3,
            "analyze and do nothing": 1,
            "shutdown": 2,
            "move": 1
        }
        self.actualScore += measures[scoreType]

    def resetScore(self):
        self.scores.append(self.actualScore)
        self.actualScore = 0
    
    def verifyDirty(self):
        actualPosition = self.environment.getPosition()
        actualDateTime = self.__actualDateTime()
        print("[{}] O robô está analisando o piso {}.".format(actualDateTime, actualPosition))
        actualPositionDirty = self.environment.getFloorState(actualPosition)
        if (actualPositionDirty == 0):
            print("Resultado da análise: Piso limpo.\n")
            self.addFloorToMemory(actualPosition)
            return False
        else:
            print("Resultado da análise: Piso sujo.\n")
            return True
        
    def __actualDateTime(self):
        actualDateTime = datetime.datetime.now()
        formattedDateTime = actualDateTime.strftime("%d-%m-%Y %H:%M:%S")
        return formattedDateTime

    def cleanFloor(self, position):
        actualScenario = self.environment.getActualScenario()
        floor = self.environment.scenarios[actualScenario][0]
        floor[position] = 0
        actualPosition = self.environment.getPosition()
        actualDateTime = self.__actualDateTime()
        self.addFloorToMemory(actualPosition)
        print("[{}] O robô limpou o piso {}.\nPisos limpos: {}.\n".format(actualDateTime, actualPosition, self.cleanedFloors))

    def verifyMoveDireciton(self):
        actualDateTime = self.__actualDateTime()
        actualPosition = self.environment.getPosition()
        if (actualPosition == 0):
            self.moveDirection = 1
        elif (actualPosition == self.environmentSize - 1):
            self.moveDirection = -1

    def moveCleaner(self):
        initialPosition = self.environment.getPosition()
        self.verifyMoveDireciton()
        self.environment.setPosition(self.environment.getPosition() + self.moveDirection)
        actualPosition = self.environment.getPosition()
        actualDateTime = self.__actualDateTime()
        print("[{}] O robô se moveu do piso {} para o piso {}.\n".format(actualDateTime, initialPosition, actualPosition))
        self.addScore("move")

    def checkBetterWay(self):
        actualDateTime = self.__actualDateTime()
        print("[{}] O robô está analisando qual o caminho mais curto para terminar o trajeto.".format(actualDateTime))
        if (self.environment.getPosition() < self.environmentSize/2):
            self.moveDirection = -1
            print("Conclusão: Inicialmente é mais favorável iniciar pela esquerda.\n")
        else:
            self.moveDirection = 1
            print("Conclusão: Inicialmente é mais favorável iniciar pela direita.\n")

    def addFloorToMemory(self, pos):
        if (pos not in self.cleanedFloors):
            self.cleanedFloors.append(pos)
    
    def checkJobFinished(self):
        if (len(self.cleanedFloors) == self.environmentSize):
            return True
        else:
            return False

    def actionController(self):
        self.checkBetterWay()
        while (not self.environment.getScenarioFinish()):
            isDirty = self.verifyDirty()
            actualPosition = self.environment.getPosition()
            if (isDirty):
                self.cleanFloor(actualPosition)
                self.addScore("analyze and clean")
            if (self.checkJobFinished()):
                self.cleanedFloors = []
                actualDateTime = self.__actualDateTime()
                print("[{}] O robô se desligou no piso {}\n".format(actualDateTime, actualPosition))
                self.addScore("shutdown")
                self.resetScore()
                self.environment.tradeScenario()
            else:
                self.addScore("analyze and do nothing")
                self.moveCleaner()
            time.sleep(2)
        self.finalResult()
    
    def finalResult(self):
        print("RESULTADOS FINAIS:")
        environments = self.environment.scenariosBackup
        totalScore = 0
        for i in range(len(self.scores)):
            totalScore += self.scores[i]
            print("Cenário {} | Ambiente: {} | Posição inicial: {} | Pontuação: {}.".format(i, environments[i][0], environments[i][1], self.scores[i]))
        print("Pontuação total: {}".format(totalScore/(i+1)))

        

class Environment:
    def __init__(self, scenarios):
        self.scenarios = scenarios
        self.scenariosBackup = copy.deepcopy(scenarios)
        self.actualSceneario = 0
        self.pos = self.scenarios[self.actualSceneario][1]
        self.printEnvCondition()

    def getPosition(self):
        return self.pos
    
    def setPosition(self):
        return self.pos
    
    def getActualScenario(self):
        return self.actualSceneario

    def tradeScenario(self):
        self.actualSceneario += 1
        if (self.actualSceneario < len(self.scenarios)):
            self.pos = self.scenarios[self.actualSceneario][1]
            self.printEnvCondition()

    def getScenarioFinish(self):
        finish = False
        if (self.actualSceneario > len(self.scenarios) -1):
            finish = True
        return finish
    
    def setPosition(self, pos):
        self.pos = pos

    def getFloorState(self, pos):
        return self.scenarios[self.actualSceneario][0][pos]
    
    def printEnvCondition(self):
        print("AMBIENTE:\nMapa: {}\nPosição inicial do robô: {}\n".format(self.scenarios[self.actualSceneario][0], self.pos))
    
def main():
    environment = Environment([([1,1], 0), ([1,1], 1), ([0,1], 0), ([0,1], 1), ([1,0], 0), ([1,0], 1), ([0,0], 0), ([0,0], 1)])
    cleaner = Cleaner(environment)

if __name__ == "__main__":
    main()