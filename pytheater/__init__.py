import logging
import sys

from pytheater.core.actor_system import ActorSystem


logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

