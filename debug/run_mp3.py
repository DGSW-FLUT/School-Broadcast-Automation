import sys, pygame, time

pygame.mixer.init()
pygame.mixer_music.load(sys.argv[1])
print(f'Playing {sys.argv[1]}')
pygame.mixer_music.play()
while pygame.mixer_music.get_busy(): time.sleep(0.1)
print(f'Stoping {sys.argv[1]}')
pygame.mixer.quit()
