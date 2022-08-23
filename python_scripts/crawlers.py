from abc import ABC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from abc import abstractmethod, ABC


class Crawler(ABC):

    def __init__(self) -> None:
        super().__init__()

    