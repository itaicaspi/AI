'''Constants - details about the map.
accessible using "import ways.info'''




ROAD_TYPES = ('motorway', 'motorway_link',
              'trunk', 'trunk_link',
              'primary', 'primary_link',
              'secondary', 'secondary_link',
              'tertiary', 'tertiary_link',
              'residential', 'living_street', 
              'unclassified')

TYPE_INDICES = list(range(len(ROAD_TYPES)))


SPEED_RANGES = (
            (80, 110),  # 'motorway'
            (80, 100),  # 'motorway_link'
            (70, 110),  # 'trunk'
            (70, 90),  # 'trunk_link'
            (60, 90),  # 'primary'
            (60, 80),  # 'primary_link'
            (50, 80),  # 'secondary'
            (50, 70),  # 'secondary_link'
            (40, 80),  # 'tertiary'
            (40, 60),  # 'tertiary_link'
            (20, 50),  # 'residential'
            (5, 30),  # 'living_street'                
            (30, 90),  # 'unclassified'
            )

DEFAULT_MINIMUM_DISTANCE = 50

L_FACTOR = 10000

TRAFFIC_JAM_PARAM = 37

