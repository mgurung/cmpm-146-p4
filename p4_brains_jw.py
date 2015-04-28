
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.have_resource = False


  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)

    #Movement command check
    if message == 'order' and type(details) == tuple:
      self.body.go_to(details)

    #Keyboard command check
    else:
      if details == 'i':
        self.state = 'idle'
        self.body.stop()
      elif details == 'a':
        self.state = 'attack'
        nearest_mantis = self.body.find_nearest('Mantis')
        self.body.follow(nearest_mantis)
        self.body.set_alarm(1)
      elif details == 'h':
        self.state = 'harvest'
        if self.have_resource:
          nearest_nest = self.body.find_nearest('Nest')
          self.body.go_to(nearest_nest)
        else:
          nearest_resource = self.body.find_nearest('Resource')
          self.body.go_to(nearest_resource)
        self.body.set_alarm(0.5)

      elif details == 'b':
        self.state = 'build'
        nearest_nest = self.body.find_nearest('Nest')
        self.body.go_to(nearest_nest)

    #Flee check
    if self.body.amount < 0.5:
      nearest_nest = self.body.find_nearest('Nest')
      self.body.go_to(nearest_nest)
      self.state = 'flee'
      self.body.set_alarm(1)

    #Timer check
    if message == 'timer' and details == None:
      if self.state == 'attack':
        nearest_mantis = self.body.find_nearest('Mantis')
        self.body.follow(nearest_mantis)
        self.body.set_alarm(1)

      if self.state == 'harvest':
        if self.have_resource:
          nearest_nest = self.body.find_nearest('Nest')
          self.body.go_to(nearest_nest)
        else:
          nearest_resource = self.body.find_nearest('Resource')
          self.body.go_to(nearest_resource)
        self.body.set_alarm(0.5)

      if self.state == 'flee':
        nearest_nest = self.body.find_nearest('Nest')
        self.body.go_to(nearest_nest)
        self.body.set_alarm(1)

    #Collision check
    if message == 'collide':
      if details['what'] == 'Mantis':
        mantis = details['who']
        if self.state == 'attack':
          mantis.amount -= 0.05

      if details['what'] == 'Resource':
        resource = details['who']
        if self.state == 'harvest' and not self.have_resource:
          resource.amount -= 0.25
          self.have_resource = True

      if details['what'] == 'Nest':
        nest = details['who']
        if self.state == 'build':
          nest.amount += 0.01
        if self.state == 'harvest':
          self.have_resource = False
        if self.state == 'flee':
          self.body.amount = 1.0
          self.state = 'attack'
          self.body.set_alarm(1)





world_specification = {
  'worldgen_seed': 13, # comment-out to randomize
  'nests': 5,#2,
  'obstacles': 0,#25,
  'resources': 10,#5,
  'slugs': 5,
  'mantises': 20,#5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
