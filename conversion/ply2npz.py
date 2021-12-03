#
# P L Y 2 N P Z
#
from pyntcloud import PyntCloud
import argparse
import sys

parser = argparse.ArgumentParser("Transform a .ply file to a .npz")

parser.add_argument('-i', '--input', action="store", required=True, help="PLY file")
parser.add_argument('-o', '--output', action="store", required=True, help="Output file")
arguments = parser.parse_args()

cloud = PyntCloud.from_file(arguments.input)

try:
    cloud.to_file(arguments.output)
except ValueError:
    print("Supported file types: ['ASC', 'BIN', 'CSV', 'NPZ', 'OBJ', 'PLY', 'PTS', 'TXT', 'XYZ']")
    sys.exit(1)

sys.exit(0)