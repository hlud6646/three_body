# three_body
Model of three bodies under gravitational attraction.

This module stores the location and velocity of 3 point masses and updates them according to gravitational attraction.
They are equally massive and begin at rest in random locations. This is easy to modify in the init_state() function.

The module also contains a method for drawing the configuration on a numpy array, and a generator of frames, to be displayed/saved however you like.
