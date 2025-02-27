from django.http import HttpResponse
from .task import run_auto_check
import asyncio
# Basic view returning plain text
def check(request):
    asyncio.run(run_auto_check())
    return HttpResponse("Started....")


