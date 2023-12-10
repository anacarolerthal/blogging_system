import unittest
import sys

#APPENDS SRC FOLDER TO PATH
sys.path.append('../src')
from event import Event

class ObserverPatternSystem(unittest.TestCase):

    def setUp(self):
        self.event = Event()

    def test_shouldSubscribeWithSucess(self):
        #Arrange
        event_type = "Teste unitario"
        fn = str.split

        #Act
        #subscribe(event_type, fn)
        self.event.subscribe(event_type, fn)

        #Assert
        #self.assertEquals(subscribers[event_type], fn)
        #self.assertEquals(self.event.subscribers[event_type], fn)
        self.assertEquals(self.event.subscribers[event_type][0], fn)

    

if __name__ == '__main__':
    unittest.main()


