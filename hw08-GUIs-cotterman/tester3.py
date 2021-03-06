#Interactions with objects generate events, and these events can be associated to callbacks, 
  #ie functions or methods processing the event. 
#In a GUI, callbacks created by user-generated events are place on an "event stack"
#The event loop process each call on the event queue one after the other, thus emptying the event queue. 
#The flow of the program is still sequential (two code blocks never run at the same time in an event loop), 
 #but the execution order is chosen by the user, and not by the developer.

from traits.api import *

class EchoBox(HasTraits):
    input =  Str()
    output = Str()
    #Defining callbacks for the modification of an attribute foo of a HasTraits object 
        #can be done be creating a method called _foo_changed(), as follows. 
    def _input_changed(self):
        self.output = self.input

EchoBox().configure_traits()
