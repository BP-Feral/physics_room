import sys
import pygame
import pymunk
import pymunk.pygame_util
import math

import random as rm

class Game:

    def __init__(self):
        self.WIDTH = 1200
        self.HEIGHT = 700

    def init_data(self):
        pygame.init()
        self.initial_force = 0
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 1 / self.fps
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.first_mass = 30
        self.second_mass = 20
        self.speed1 = 450000
        
    def init_colors(self):
        self.color_white = (255, 255, 255)
        self.color_red = (255, 0, 0)
        self.color_green = (0, 255, 0)
        self.color_blue = (0, 0, 255)
        self.color_black = (0, 0, 0)
        self.color_message = (60, 80, 82)

        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        
    def init_fonts(self):
        self.sans16_font = pygame.font.Font('freesansbold.ttf', 16)

    def create_ball(self, space, radius, mass, color, x, y):
        body = pymunk.Body()
        body.position = (x, y)
        shape = pymunk.Circle(body, radius)
        shape.mass = mass
        shape.color = color
        space.add(body, shape)
        return body, shape

    def create_boundaries(self, space, width, height):
        rects = [
            [(width/2, height -10), (width, 20)],
            [(width/2, 10), (width, 20)],
            [(10, height/2),(20 ,height)],
            [(width - 10, height/2), (20, height)]
        ]
        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.5
            space.add(body, shape)
    
    def draw(self, space, draw_options):
        self.window.fill(self.color_black)
        space.debug_draw(draw_options)
    
    def render_text(self, message, size, color, x, y):
        message_to_display = self.sans16_font.render(message, True, color)
        message_rect = message_to_display.get_rect()
        message_rect.bottomleft = (x, y)

        self.window.blit(message_to_display, message_rect)

    def menu(self):
        self.menu_loop = True
        
        # First input box
        mass1_input_box = pygame.Rect(650, 95, 60, 28)
        mass1_text = ''
        mass1_message = '1 - 300'
        mass1_active = False
        mass1_color = self.color_inactive
        
        mass2_input_box = pygame.Rect(1000, 95, 60, 28)
        mass2_text = ''
        mass2_message = '1 - 300'
        mass2_active = False
        mass2_color = self.color_inactive

        speed1_input_box = pygame.Rect(650, 155, 60, 28)
        speed1_text = ''
        speed1_message = '1 - 100'
        speed1_active = False
        speed1_color = self.color_inactive        
        
        next_level = pygame.Rect(480, 565, 250, 50)

        while self.menu_loop:
            self.window.fill(self.color_white)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_loop = False
                    pygame.quit()
                    sys.exit()
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mass1_input_box.collidepoint(event.pos):
                        mass1_active = True
                    else:
                        mass1_active = False
                    
                    mass1_color = self.color_active if mass1_active else self.color_inactive

                    if mass2_input_box.collidepoint(event.pos):
                        mass2_active = True
                    else:
                        mass2_active = False
                    
                    mass2_color = self.color_active if mass2_active else self.color_inactive
                    
                    if speed1_input_box.collidepoint(event.pos):
                        speed1_active = True
                    else:
                        speed1_active = False
                    
                    speed1_color = self.color_active if speed1_active else self.color_inactive
                    
                    
                    if next_level.collidepoint(event.pos):
                        self.menu_loop = False
                        self.level()
                
                if event.type == pygame.KEYDOWN:
                    if mass1_active:
                        if event.key == pygame.K_RETURN:
                            try:
                                if 0 < int(mass1_text) < 300:
                                    self.first_mass = mass1_text
                                    mass1_text = ''
                                    mass1_message = "Valoare setata!"
                                else:
                                    mass1_message = "Valoare prea mare"
                            except ValueError:
                                mass1_message = "Ceva nu a mers bine!"
                                pass
                        elif event.key == pygame.K_BACKSPACE:
                            mass1_text = mass1_text[:-1]
                        else:
                            mass1_text += event.unicode
                    
                    if mass2_active:
                        if event.key == pygame.K_RETURN:
                            try:
                                if 0 < int(mass2_text) < 300:
                                    self.second_mass = mass2_text
                                    mass2_text = ''
                                    mass2_message = "Valoare setata!"
                                else:
                                    mass2_message = "Valoare prea mare"
                            except ValueError:
                                mass2_message = "Ceva nu a mers bine!"
                                pass
                        elif event.key == pygame.K_BACKSPACE:
                            mass2_text = mass2_text[:-1]
                        else:
                            mass2_text += event.unicode

                    if speed1_active:
                        if event.key == pygame.K_RETURN:
                            try:
                                if 0 < int(speed1_text) < 100:
                                    self.speed1 = int(speed1_text) * 10000
                                    speed1_text = ''
                                    speed1_message = "Valoare setata!"
                                else:
                                    speed1_message = "Valoare prea mare"
                            except ValueError:
                                speed1_message = "Ceva nu a mers bine!"
                                pass
                        elif event.key == pygame.K_BACKSPACE:
                            speed1_text = speed1_text[:-1]
                        else:
                            speed1_text += event.unicode
                
            
            self.render_text("R: Reseteaza obiectele", 16, self.color_black, 100, 100)
            self.render_text("SPACE: Opreste miscarea obiectelor", 16, self.color_black, 100, 120)
            self.render_text("LMB: Click pentru a face bila rosie sa mearga spre mouse", 16, self.color_black, 100, 140)
            self.render_text(mass1_message, 16, self.color_message, 650, 150)
            self.render_text(mass2_message, 16, self.color_message, 950, 150)
            self.render_text(speed1_message, 16, self.color_message, 650, 210)
           
            txt_surface_mass1 = self.sans16_font.render(mass1_text, True, mass1_color)
            width = max(80, txt_surface_mass1.get_width()+10)
            mass1_input_box.w = width
            self.window.blit(txt_surface_mass1, (mass1_input_box.x+5, mass1_input_box.y+5))
            pygame.draw.rect(self.window, mass1_color, mass1_input_box, 2)
            
            txt_surface_mass2 = self.sans16_font.render(mass2_text, True, mass2_color)
            width = max(80, txt_surface_mass2.get_width()+10)
            mass2_input_box.w = width
            self.window.blit(txt_surface_mass2, (mass2_input_box.x+5, mass2_input_box.y+5))
            pygame.draw.rect(self.window, mass2_color, mass2_input_box, 2)
            
            txt_surface_speed1 = self.sans16_font.render(speed1_text, True, speed1_color)
            width = max(80, txt_surface_speed1.get_width()+10)
            speed1_input_box.w = width
            self.window.blit(txt_surface_speed1, (speed1_input_box.x+5, speed1_input_box.y+5))
            pygame.draw.rect(self.window, speed1_color, speed1_input_box, 2)
            
            pygame.draw.rect(self.window, self.color_black, next_level, 2)
            
            self.render_text("Prima bila", 16, self.color_red, 650, 80)
            self.render_text("Masa", 16, self.color_black, 600, 120)
            self.render_text("Viteza", 16, self.color_black, 600, 180)
            
            self.render_text("A doua bila", 16, self.color_green, 1000, 80)
            self.render_text("Masa", 16, self.color_black, 950, 120) 
            
            pygame.draw.line(self.window, self.color_black, (580, 550), (580, 20), 5)
            pygame.draw.line(self.window, self.color_black, (580, 550), (1150, 550), 5)
            pygame.draw.line(self.window, self.color_black, (1150, 550), (1150, 20), 5)
            pygame.draw.line(self.window, self.color_black, (580, 20), (1150, 20), 5)
            
            self.render_text("-- Click pentru a continua... --", 16, self.color_blue, 500, 600)
            
            pygame.display.update()
            self.clock.tick(self.fps)

    def level(self):
        
        self.level_loop = True

        space = pymunk.Space()
        space.gravity = 0, 0
        
        rand_x = rm.randint(50, 950)
        rand_y = rm.randint(50, 750)
        
        first_body, first_ball = self.create_ball(space, int(self.first_mass), 10, (255, 0, 0 ,100), self.WIDTH/2 - 200, self.HEIGHT/2)
        first_ball.elasticity = 0.50

        second_body, second_ball = self.create_ball(space, int(self.second_mass), 10, (0, 255, 0, 100), self.WIDTH/2 + 200, self.HEIGHT/2)
        second_ball.elasticity = 0.50
        
    
        
        self.create_boundaries(space, self.WIDTH, self.HEIGHT)
        draw_options = pymunk.pygame_util.DrawOptions(self.window) # type: ignore
        
        while self.level_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.level_loop = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.initial_force = 10
                    a = pygame.mouse.get_pos()
                    body_position = first_body._get_position()
                    distance_x = a[0] - body_position[0]
                    distance_y = a[1] - body_position[1]                 
                    
                    first_body.angle = math.atan2(distance_y, distance_x)
                    first_body.apply_force_at_local_point((int(self.speed1), 0), a)
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.initial_force = 0
                        first_body.velocity = (0, 0)
                        second_body.velocity = (0, 0)

                    if event.key == pygame.K_r:
                        self.level_loop = False
                        proc = Game()
                        proc.init_colors()
                        proc.init_data()
                        proc.init_fonts()                        
                        proc.menu()

            self.draw(space, draw_options)
            
            red_velocity = first_body._get_velocity()
            self.render_text(f"velocity: {abs(round(red_velocity.x, 2)), abs(round(red_velocity.y, 2))}", 16, self.color_red, 25, 40)

            green_velocity = second_body._get_velocity()        
            self.render_text(f"velocity: {abs(round(green_velocity.x, 2)), abs(round(green_velocity.y, 2))}", 16, self.color_green, 25, 60)
            
            dataX = first_ball.shapes_collide(second_ball)
            
            print(dataX)
            self.render_text("R: Reseteaza obiectele", 16, self.color_white, 100, 620)
            self.render_text("SPACE: Opreste miscarea obiectelor", 16, self.color_white, 100, 640)
            self.render_text("LMB: Click pentru a face bila rosie sa mearga spre mouse", 16, self.color_white, 100, 660)
            
            pygame.display.update()

            space.step(self.dt)
            self.clock.tick(self.fps)