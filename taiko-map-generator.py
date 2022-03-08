#mapData
"""
timing points = 240,1200,4,1,0,100,1,0
start point, bpm (1 / 1200 * 60.000), meter (4,1), sample set (0,1,2,3), volume, uninherited (0 or 1), effects (0-3 kiai)
x,y,1(1nocombo-5newcombo),hitsound,0:0:0:0:
0 = normal
4 = finish normal
8 = clap
12 = finish clap
240-1440 *1/1 = 1200+
240-840 * 1/2 = 600+
240-540 * 1/4 = 300+
"""

import re

map = "F:/osu!/Songs/NIMI - STAMINA PRACTICE/NIMI - STAMINA GOD (nakanotsu nimi) [tst].osu"
mapLines = []
pattern = 'ddkd'
bpm = 0

mapGeneral = { # osu file format v14
	# [General]
	'AudioFilename:':'',
	'AudioLeadIn:':'',
	'PreviewTime:':'',
	'Countdown:':'',
	'SampleSet:':'',
	'StackLeniency:':'',
	'Mode:':'',
	'LetterboxInBreaks:':'',
	'WidescreenStoryboard:':'',
	# [Editor]
	'DistanceSpacing:':'',
	'BeatDivisor:':'',
	'GridSize:':'',
	'TimelineZoom:':'',
	# [Metadata]
	'Title:':'',
	'TitleUnicode:':'',
	'Artist:':'',
	'ArtistUnicode:':'',
	'Creator:':'',
	'Version:':'',
	'Source:':'',
	'Tags:':'',
	'BeatmapID:':'',
	'BeatmapSetID:':'',
	# [Difficulty]
	'HPDrainRate:':'',
	'CircleSize:':'',
	'OverallDifficulty:':'',
	'ApproachRate:':'',
	'SliderMultiplier:':'',
	'SliderTickRate:':''
}
mapGroups = {
	# [Group]
	'Events':[],
	'TimingPoints':[],
	'HitObjects':[],
	'HitObjectsTiming':[],
	'NewHitObjects':[],
}

def getBpm():
	pass

def readOsu():
	global mapLines
	global mapGroups
	capture = False

	# openfile
	with open(map, 'r') as mapFile:
		mapLines = mapFile.readlines()
	
	# Get parameters from beatmap
	for line in mapLines:
		for key in mapGeneral:
			if key in line:
				mapGeneral[key] = line.split(":")[1].rstrip("\n").lstrip()
	
	# Read [Events]
	for line in mapLines:			
		if '[TimingPoints]' in line:
			capture = False
		if capture:
			mapGroups['Events'].append(line.rstrip("\n"))
		if '[Events]' in line:
			capture = True
	mapGroups['Events'] = [x for x in mapGroups['Events'] if x]
		
	# Read [Timing Points]
	for line in mapLines:		
		if '[HitObjects]' in line:
			capture = False
		if capture:			
			mapGroups['TimingPoints'].append(line.rstrip("\n"))
		if '[TimingPoints]' in line:
			capture = True
	mapGroups['TimingPoints'] = [x for x in mapGroups['TimingPoints'] if x]

	# Read [HitObjects]
	for line in mapLines:
		if capture:
			mapGroups['HitObjects'].append(line.rstrip("\n"))
		if '[HitObjects]' in line:
			capture = True
	capture = False
	mapGroups['HitObjects'] = [x for x in mapGroups['HitObjects'] if x]

	# Read hitObjects Timing
	for data in mapGroups['HitObjects']:
		mapGroups['HitObjectsTiming'].append(re.split("\d\d\d,\d\d\d,",data)[1].split(',')[0])	

def generatePattern():
	# OK
	global pattern
	global mapGroups
	global mapGeneral
	convertedPattern = []

	for t in pattern:
		if t == 'd': convertedPattern.append('0')
		else: convertedPattern.append('8')
	pos = 0

	for time in mapGroups['HitObjectsTiming']:
		mapGroups['NewHitObjects'].append("260,200,"+time+","+convertedPattern[pos]+",0,0:0:0:0:")
		if pos<len(convertedPattern)-1:
			pos += 1
		else:
			pos = 0

	mapGeneral['Version:'] = pattern

def writeMap():
	newMap = ['osu file format v14','','[General]']
	general = [
		'AudioFilename:',
		'AudioLeadIn:',
		'PreviewTime:',
		'Countdown:',
		'SampleSet:',
		'StackLeniency:',
		'Mode:',
		'LetterboxInBreaks:',
		'WidescreenStoryboard:'
		]
	editor = [
		'DistanceSpacing:',
		'BeatDivisor:',
		'GridSize:',
		'TimelineZoom:'
	]
	metadata = [
		'Title:',
		'TitleUnicode:',
		'Artist:',
		'ArtistUnicode:',
		'Creator:',
		'Version:',
		'Source:',
		'Tags:',
		'BeatmapID:',
		'BeatmapSetID:'
	]
	difficulty = [
		'HPDrainRate:',
		'CircleSize:',
		'OverallDifficulty:',
		'ApproachRate:',
		'SliderMultiplier:',
		'SliderTickRate:'
	]

	for v in general:
		newMap.append(str(v+mapGeneral[v]))
	newMap.append('')

	newMap.append('[Editor]')
	for v in editor:
		newMap.append(str(v+mapGeneral[v]))
	newMap.append('')

	newMap.append('[Metadata]')
	for v in metadata:
		newMap.append(str(v+mapGeneral[v]))
	newMap.append('')

	newMap.append('[Difficulty]')
	for v in difficulty:
		newMap.append(str(v+mapGeneral[v]))
	newMap.append('')

	newMap.append('[Events]')
	for v in mapGroups['Events']:
		newMap.append(v)
	newMap.append('')

	newMap.append('[TimingPoints]')
	for v in mapGroups['TimingPoints']:
		newMap.append(v)
	newMap.append('')

	newMap.append('[HitObjects]')
	for v in mapGroups['NewHitObjects']:
		newMap.append(v)
	newMap.append('')

	filename = mapGeneral['ArtistUnicode:'] + ' - ' + mapGeneral['TitleUnicode:'] + ' (' + mapGeneral['Creator:'] + ') ' + '[' + mapGeneral['Version:'] + '].osu'
	print(filename)

	with open(filename,'w') as f:
		for line in newMap:
			f.write(line+'\n')

readOsu()
generatePattern()
writeMap()