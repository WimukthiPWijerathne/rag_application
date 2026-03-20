import logging 
from fastapi import FastAPI
import inngest
import inngest.fastapi
from inngest.experimenatal import ai
from dotenv import load_dotenv
import uuid
import os
import datetime


load_dotenv()

