'''
Raymond Hettinger

super considered super

Linearisation:

MRO Method Resolution Order
super in Python does not call parents, 
but parents from the children
super means "next in line", starting from youngest child

!!!
-> children get called before their parents
-> parents get called in the order listed
-> parents stay in order
!!!
-> multiple inheritance: use keyword arguments
   (you can not know who you are calling)

'''


from collections import Counter, OrderedDict
import unittest


class DoughFactory:
    '''
    class DoughFactory
    '''

    def get_dough(self):
        return 'insecticide treated wheat dough'


class Pizza(DoughFactory):
    '''
    class Pizza
    '''

    def order_pizza(self, *toppings):
        print('Getting dough')
        dough = super().get_dough()
        print('Making pie with %s' % dough)
        for topping in toppings:
            print('Adding %s' % topping)


class OrganicDoughFactory(DoughFactory):
    '''
    class OrganicDoughFactory
    '''

    def get_dough(self):
        return 'pure untreated wheat dough'


class OrganicPizza(Pizza, OrganicDoughFactory):
    '''
    class OrganicPizza
    '''
    pass


if __name__ == '__main__':
    Pizza().order_pizza('Pepperoni', 'Pepper')
    print(help(Pizza))

    OrganicPizza().order_pizza('Sausage', 'Mushroom')
    print(help(OrganicPizza))


# --------------------------------------------------------------

class Robot:
    """
    Sophisticated class that moves a real robot 
    """
    # Don't wear down real robots by running tests!

    def fetch(self, tool):
        print('Physical Movement! Fetching')

    def move_forward(self, tool):
        print('Physical Movement! Moving forward')

    def move_backward(self, tool):
        print('Physical Movement! Moving backward')

    def replace(self, tool):
        print('Physical Movement! Replacing')


class CleaningRobot(Robot):  # CleaningRobot 'is a' Robot, not 'has a' Robot
    '''
    class CleaningRobot
    '''

    def clean(self, tool, times=10):
        super().fetch(tool)
        for i in range(times):
            super().move_forward(tool)
            super().move_backward(tool)
        super().replace(tool)


class MockBot(Robot):
    """
    Simulate a real robot by merely recording tasks
    """

    def __init__(self):
        self.tasks = []

    def fetch(self, tool):
        self.tasks.append('fetching %s' % tool)

    def move_forward(self, tool):
        self.tasks.append('forward %s' % tool)

    def move_backward(self, tool):
        self.tasks.append('backward %s' % tool)

    def replace(self, tool):
        self.tasks.append('replacing %s' % tool)


class MockedCleaningRobot(CleaningRobot, MockBot):
    """
    Injects a mock bot into the robot dependency
    """

# it checks Mockbot *before* Robot is checked


# import unittest
class TestCleaningRobot(unittest.TestCase):
    '''
    class TestCleaningRobot
    '''

    def test_clean(self):
        t = MockedCleaningRobot()
        t.clean('mop')
        expected = (['fetching mop'] +
                    ['forward mop', 'backward mop'] * 10 +
                    ['replacing mop'])
        self.assertEqual(t.tasks, expected)


if __name__ == '__main__':
    unittest.main()

# --------------------------------------------------------------


class OrderedCounter(Counter, OrderedDict):
    '''
    Counter that remembers the order elements are first seen
    '''

    def __repr__(self):
        return'%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)


oc = OrderedCounter('abracadabra')
print(oc)
