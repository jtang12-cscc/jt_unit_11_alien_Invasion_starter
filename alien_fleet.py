import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):
        """

        This function sets up the appropriate height and width for the alien fleet.

        """
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)

        self._create_new_shape_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)
    
    # New Fleet Shape starts here

    def _create_new_shape_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):

        """

        This function makes sure that the shape of the fleet goes back to the previous one once the latter has no more ships left.

        """

        shape_x = fleet_w / 2
        shape_y = fleet_h / 2

        max_distance = min(fleet_w / 2, fleet_h / 2)
        
        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if abs(col - shape_x) + abs(row - shape_y) > max_distance:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """

        This function determines the offsets for the alien fleet.

        Args:
            alien_w (int): Determines the alien's width
            alien_h (int): Determines the alien's height
            screen_w (int): Determines the screen width
            fleet_w (int): Determines the fleet's width
            fleet_h (int): Determines the fleet's height

        Returns:
            int: This variable is used to print out the results of the offsets.
        """
        half_screen = self.settings.screen_h//2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h
        x_offset = int((screen_w-fleet_horizontal_space)//2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset


    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """

        This function calculates the fleet's overall size.

        Args:
            screen_h (int): Determines the screen height.

        Returns:
            int: This variable is used to print out the results of the fleet size.
        """
        fleet_w = ((screen_w)//alien_w)
        fleet_h = ((screen_h/2)//alien_h)
        
        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2
        
        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2
        
    
        return int(fleet_w), int(fleet_h)


    def _create_alien(self, current_x: int, current_y:int):
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break


    def _drop_alien_fleet(self):
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed


    def update_fleet(self):
        self._check_fleet_edges()
        self.fleet.update()


    def draw(self):
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()


    def check_collisions(self, other_group):
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)


    def check_fleet_bottom(self):
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
    
    def check_destroyed_status(self):
        return not self.fleet