import sys

import pygame as pg
from pygame.draw import circle, line, polygon
from math import sqrt, sin, cos, pi, exp, asin
from time import sleep
import numpy as np
import colour
"""
    requirements:
        pip install pygame
        pip install numpy
        pip install colour-science
"""
def thin_film_interference(wavelength, thickness, n_film):
    """
    Calculate the reflection intensity for thin film interference.
    Parameters:
    wavelength (float): Wavelength of incident light in nanometers
    thickness (float): Thickness of the film in nanometers
    n_film (float): Refractive index of the film
    Returns:
    float: Intensity of reflection (0 to 1)
    """

    # Calculate phase difference
    delta = (4 * np.pi * n_film * thickness) / wavelength

    # Calculate reflection coefficients
    r1 = (1 - n_film) / (1 + n_film)
    r2 = (n_film - 1) / (n_film + 1)

    # Calculate reflection intensity
    R = (r1 ** 2 + r2 ** 2 + 2*r1 * r2 * np.cos(delta)) / (1 + r1 **2 + r2 ** 2 + 2 * r1 * r2 * np.cos(delta))

    return R

def new_avg(intensities):
    wavelengths = np.array(WL)
    # Get the RGB values for each wavelength
    rgb_values = np.array([wl_rgb(w) for w in WL])
    cmfs = colour.colorimetry.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
    illuminant = colour.SDS_ILLUMINANTS['D65']

    # Calculate XYZ tristimulus values
    cmf_values = cmfs.values
    illuminant_values = illuminant.values

    def xyzsum(wavelengths, intensities, rgb_values, cmf_index):
        cmf_interp = np.interp(wavelengths, cmfs.wavelengths, cmf_values[:, cmf_index])
        illuminant_interp = np.interp(wavelengths, illuminant.wavelengths, illuminant_values)
        return np.sum(intensities * rgb_values * cmf_interp * illuminant_interp)

    X = xyzsum(wavelengths, intensities, rgb_values[:, 0], 0)
    Y = xyzsum(wavelengths, intensities, rgb_values[:, 1], 1)
    Z = xyzsum(wavelengths, intensities, rgb_values[:, 2], 2)

    # Normalize XYZ values
    total = np.sum([X, Y, Z])
    X, Y, Z = X / total, Y / total, Z / total

    # Convert XYZ to RGB
    RGB = colour.XYZ_to_sRGB([X, Y, Z])

    # Clip RGB values to [0, 1] range and gamma correct
    RGB = np.clip(RGB, 0, 1)
    RGB = colour.models.cctf_encoding(RGB)
    # RGB = colour.algebra.cctf_encoding(RGB)

    return RGB

def wl_rgb(l):
    """
    Convert wavelength to RGB color.
    :param l: wavelength in nm (400-700)
    :return: tuple of (r, g, b) values in range 0-1
    """
    r, g, b = 0.0, 0.0, 0.0

    if 400.0 <= l < 410.0:
        t = (l - 400.0) / (410.0 - 400.0)
        r = 0.33 * t - 0.20 * t * t
    elif 410.0 <= l < 475.0:
        t = (l - 410.0) / (475.0 - 410.0)
        r = 0.14 - 0.13 * t * t
    elif 545.0 <= l < 595.0:
        t = (l - 545.0) / (595.0 - 545.0)
        r = 1.98 * t - t * t
    elif 595.0 <= l < 650.0:
        t = (l - 595.0) / (650.0 - 595.0)
        r = 0.98 + 0.06 * t - 0.40 * t * t
    elif 650.0 <= l < 700.0:
        t = (l - 650.0) / (700.0 - 650.0)
        r = 0.65 - 0.84 * t + 0.20 * t * t

    if 415.0 <= l < 475.0:
        t = (l - 415.0) / (475.0 - 415.0)
        g = 0.80 * t * t
    elif 475.0 <= l < 590.0:
        t = (l - 475.0) / (590.0 - 475.0)
        g = 0.8 + 0.76 * t - 0.80 * t * t
    elif 585.0 <= l < 639.0:
        t = (l - 585.0) / (639.0 - 585.0)
        g = 0.84 - 0.84 * t

    if 400.0 <= l < 475.0:
        t = (l - 400.0) / (475.0 - 400.0)
        b = 2.20 * t - 1.50 * t * t
    elif 475.0 <= l < 560.0:
        t = (l - 475.0) / (560.0 - 475.0)
        b = 0.7 - t + 0.30 * t * t

    return int(250 * r), int(250 * g), int(250 * b)

def x_L(x):
    """
    x is the position of a ring of the bobble
    x=0 is the center of the bobble
    x=1 is the outer ring of the bobble
    alpha is the angle of incidence
    beta is the angle of refraction
    L is the length of the path the light travel inside the bobble film
    """
    alpha = (asin(min(x,1)))
    beta = asin(sin(alpha)/n)
    L = 2*d*n*cos(beta)
    return L

def rings():
    """
    returns array of rings to draw
    each ring is an array of intesities for each wavelength
    """
    L = [x_L(x) for x in X]
    rings_i = [[thin_film_interference(w,l,n) for w in WL] for l in L]

    return rings_i

def text(t,X,Y,c=(255,255,255),s=120):
    my_font = pg.font.SysFont('Cpmic Sans MS',s)
    text_surface = my_font.render(t,False,c)
    screen.blit(text_surface,(X,Y))

#display parameters
pg.font.init()
pg.init()
cx = 300
cy = 400
screen = pg.display.set_mode((2 * cx, 2 * cy))

#phisical parameters
d = 100  # nm
n = 1.33


#resolotion and setup
N = 96
X = [j / (N) for j in range(N)] #how far away
WL = [j for j in range(380, 760, 380 // N)]
dark_mode = True
while True:
    if pg.mouse.get_pressed()[0]:
        d = 2*cy-pg.mouse.get_pos()[1]
    if dark_mode:
        screen.fill(0)
        text(str(d) + "nm", cx - 120, 50, s=100)

    else:
        screen.fill((255,255,255))
        text(str(d) + "nm", cx - 120, 50, s=100, c=[0, 0, 0])
    rings_i = rings()

    v = [thin_film_interference(k, d, n) for k in WL]
    col = [wl_rgb(k) for k in WL]

    for k in range(N-1):
        line(screen, col[k], (k * 2 * cx / N, 2 * cy - 100),((k) * 2 * cx / N, 2 * cy - 100 - v[k] * 1000),15)
    for i in range(1*N):
        c = [int(q * 255) for q in new_avg(rings_i[i])]
        circle(screen, c, (cx, cy), i*2 , 3)

    # check the thin film
    # for i in range(1000):
    #     L2 = i + 1
    #     A = [thin_film_interference(w, L2, n) for w in WL]
    #     c = [int(q*180) for q in new_avg(A)]
    #
    #     if i % 100 == 0:
    #         c = (255, 255, 255)
    #     line(screen, c, (i, 2000), (i, 0), 1)

    pg.display.flip()
    sleep(0.05)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.dict["key"] == pg.K_SPACE:
                dark_mode = not dark_mode
                sleep(0.1)
            if event.dict["key"] == pg.K_q:
                pg.quit()
                sys.exit()