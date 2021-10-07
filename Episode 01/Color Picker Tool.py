import cv2
import numpy as np
import PySimpleGUI as sg
import math

sg.theme('DarkAmber')   # Add a touch of color

img=np.zeros([512, 512, 3], np.uint8)
for i in range(img.shape[1]):
	d = int(math.ceil(i/2))
	img[:,i,:] = np.array([d,d,d],np.uint8)

img = cv2.applyColorMap(img,cv2.COLORMAP_HSV)
imgbytes = cv2.imencode(".png", img)[1].tobytes()
resized = img
hsv_img = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)


ColumnA = [
[ sg.Input(enable_events=True, key="IMGBROWSE"), sg.FileBrowse('Search Image')],
[sg.Text('Upper Limit - [000,000,000]', key='up_Text')],
[sg.Text('    HUE      - '),sg.Slider(range=(0,180),size=(40, 15), default_value=180, key='up_hue', orientation='h',enable_events=True, disable_number_display=True)],
[sg.Text('Saturation  - '),sg.Slider(range=(0,255),size=(40, 15), default_value=255,  key='up_Sat', orientation='h',enable_events=True, disable_number_display=True)],
[sg.Text('Brightness - '),sg.Slider(range=(0,255),size=(40, 15), default_value=255,  key='up_Bright', orientation='h',enable_events=True, disable_number_display=True)],
[sg.Text('Lower Limit - [000,000,000]', key='lower_Text')],
[sg.Text('    HUE      - '),sg.Slider(range=(0,180),size=(40, 15), key='low_hue', orientation='h',enable_events=True, disable_number_display=True)],
[sg.Text('Saturation  - '),sg.Slider(range=(0,255),size=(40, 15), key='low_Sat', orientation='h',enable_events=True, disable_number_display=True)],
[sg.Text('Brightness - '),sg.Slider(range=(0,255),size=(40, 15), key='low_Bright', orientation='h',enable_events=True, disable_number_display=True)],
[sg.Button('PrintValues',  key='PrintValues')]
]

ColumnB = [
[sg.Image(data=imgbytes,key="IMAGE",size=(512,512))],
]

layout = [
    [
        sg.Column(ColumnA),
        sg.VSeperator(),
        sg.Column(ColumnB),
    ]
]

# Create the Window
window = sg.Window('Color Picker', layout)
# Event Loop to process "events" and get the "values" of the inputs
lower_limit = np.array([0, 0, 0]) 
upper_limit= np.array([180, 255, 255]) 


while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		break

	if event == 'up_hue':
		upper_limit[0] = values['up_hue']
	if event == 'up_Sat':
		upper_limit[1] = values['up_Sat']
	if event == 'up_Bright':
		upper_limit[2] = values['up_Bright']
	if event == 'low_hue':
		lower_limit[0] = values['low_hue']
	if event == 'low_Sat':
		lower_limit[1] = values['low_Sat']
	if event == 'low_Bright':
		lower_limit[2] = values['low_Bright']
	if event == 'PrintValues':
		print('Upper_Limit = np.', repr(upper_limit).replace(' ',''))
		print('Lower_Limit = np.', repr(lower_limit).replace(' ',''))
	if event == 'IMGBROWSE':
		img=cv2.imread(values['IMGBROWSE'])
		scale = 512/img.shape[0]
		print('scale - ',scale)
		width = int(img.shape[1] * scale)
		resized = cv2.resize(img,(width,512))
		hsv_img = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv_img, lower_limit, upper_limit)
	output = cv2.bitwise_and(resized, resized, mask = mask)
	imgbytes = cv2.imencode(".png", output)[1].tobytes()
	window["IMAGE"].update(data=imgbytes)
	window["up_Text"].update('Upper Limit - ['+str(upper_limit[0])+","+str(upper_limit[1])+","+str(upper_limit[2])+']')
	window["lower_Text"].update('Lower Limit - ['+str(lower_limit[0])+","+str(lower_limit[1])+","+str(lower_limit[2])+']')

window.close()



