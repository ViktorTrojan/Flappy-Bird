from Scrolling import Scrolling

class Ground(Scrolling):
    def isColliding(self, bird):
        if(bird.boundingBox[1] + bird.boundingBox[3] >= self.y):
            return True