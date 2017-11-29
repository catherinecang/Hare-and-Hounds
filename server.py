import hug
import json
from hug.middleware import CORSMiddleware

from hare_and_hounds import *

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

@hug.get('/')
def next_best_move(pos: hug.types.delimited_list()):
    pos = [int(i) for i in pos]
    return solve_next_moves(compress(*pos))