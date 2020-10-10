import os
import re
from random import randint
import time

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options

settings = Options()
settings.headless = True


def next_song(url):
    try:
        driver.get(url)
        time.sleep(3)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button")
        ))
        driver.find_element_by_css_selector("button.ytp-large-play-button.ytp-button").click()
        WebDriverWait(driver, 20).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "button.ytp-ad-skip-button.ytp-button")
        ))
        time.sleep(6)
        driver.find_element_by_css_selector("button.ytp-ad-skip-button.ytp-button").click()
    except:
        print("Skip or large play button not pressed")


def erase():
    if driver.current_url in songs:
        songs.remove(driver.current_url)
    next_song(songs[randint(0, len(songs) - 1)].strip())


def quit_radio():
    driver.close()
    with open('music_playlist.txt', 'w') as playlist:
        for song in songs:
            playlist.write(song + '\n')


def save():
    songs[len(songs) - 1] = driver.current_url


def load():
    next_song(songs[len(songs) - 1])


def print_options():
    print("Options:\nhelp - Displays descriptions of options\nnext - chooses another song\nerase - removes song from "
          "playlist, then chooses another song\nquit - stops program\nsave - saves song into memory (overwrites "
          "whatever is already there)\nload - plays song from memory")


def clear():
    del songs[0:len(songs)]


def search(start_url):
    clear()
    driver.get('https://www.youtube.com/results?search_query=' + '+'.join(start_url.split()))
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.CSS_SELECTOR, "a#video-title.yt-simple-endpoint.style-scope.ytd-video-renderer")
    ))
    first = driver.find_element_by_css_selector("a#video-title.yt-simple-endpoint.style-scope.ytd-video-renderer")
    songs.append(first.get_attribute("href"))
    first.click()
    for n in range(20):
        time.sleep(3)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.ytd-compact-video-renderer")
        ))
        recommended = driver.find_elements_by_css_selector(
            'a.yt-simple-endpoint.style-scope.ytd-compact-video-renderer')
        for element in recommended:
            next_url = element.get_attribute("href")
            if next_url not in songs:
                songs.append(next_url)
        recommended[0].click()
    print("Created new playlist!")


songs = []
driver = selenium.webdriver.Firefox(options=settings)

try:
    script_directory = __file__.split('/')
    script_directory.pop()
    with open('/'.join(script_directory) + '/music_playlist.txt', 'r') as playlist:
        for song in playlist.readlines():
            song.replace(" ", "")
            if song != "\n":
                songs.append(song)
except FileNotFoundError:
    print("No music playlist in script directory, please type what you'd like to listen to:\n")
    search(input())

command = ''
while command != 'quit':
    command = input()
    if command == 'next':
        next_song(songs[randint(0, len(songs) - 1)].strip())
    elif command == 'erase':
        erase()
    elif command == 'quit':
        quit_radio()
    elif command == 'save':
        save()
    elif command == 'load':
        load()
    elif command == 'help':
        print_options()
    elif re.match('search.*', command):
        search_start = command.split()
        search_start.pop(0)
        if not search_start:
            print("Search for what? Please retry.")
        else:
            search(' '.join(search_start))
    else:
        print("Invalid input, type 'help' for options")
