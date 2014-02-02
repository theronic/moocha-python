import json
import os
import logging
logger = logging.getLogger(__name__)

def load_json(module_path, filename):
	module_realpath = os.path.realpath(module_path)
	module_dir = os.path.dirname(module_realpath)
	path = os.path.join(module_dir, filename)
	return json.load(open(path))

def dump_json(dict_, module_path, filename):
	logger.warn("Writing json to %s", filename)
	module_realpath = os.path.realpath(module_path)
	module_dir = os.path.dirname(module_realpath)
	path = os.path.join(module_dir, filename)
	return json.dump(dict_, open(path, 'w'))