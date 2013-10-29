
#Events that do not correspond to a modification of an attribute can be generated with a Button traits. 
#The callback is then called _foo_fired(). Here is an example of an interactive traitsUI application using a button:

from traits.api import *
from traitsui.api import View, Item, ButtonEditor

class CountMe(HasTraits):
    value =  Int()
    add_one = Button()

    def _add_one_fired(self):
        self.value +=1

    view = View('value', Item('add_one', show_label=False ))

CountMe().configure_traits()
