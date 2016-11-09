import sys
from wearn.models.wear import Wear

predictions= Wear.search(sys.argv[1])

predictions_by_euclidean = sorted(predictions, key=lambda x: x[2])[:10]

print predictions_by_euclidean
