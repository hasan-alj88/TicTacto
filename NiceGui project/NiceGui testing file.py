from nicegui import ui, events
import datetime

# button example
ui.button('Select your character', color= 'turquoise',
          on_click=lambda : ui.link("https://www.youtube.com/"))

# toggle buttons example
ui.label('Are you a DM or not?')
label = ui.label('')
toggle_text = ui.toggle(['I am NOT a DM', 'I am the DM'],value= 'I am NOT a DM',
                        on_change= lambda  : label.set_text(f'You clicked {toggle_text.value}'))

# image variable
image = ui.image('https://static.wikia.nocookie.net/the-hanged-three/images/9/97/Nothic.jpg/revision/latest/scale-to-width-down/1000?cb=20170905150306, ').classes('w-64')

# toggle + image variable
toggle_image = ui.toggle(['Dwarf-File', 'Jameel-File'],
                         on_change= lambda : image.set_source(f'{toggle_image.value}.png'))

# toggled buttons checkmark (radio) element
questionnaire = ui.radio(['Human','Elf','Dwarf-File','Half-bred','Jameel-File'],
                         on_change= lambda: image.set_source(f'{questionnaire.value}.png'))

# select element
teams = ['Dwarf', 'Jameel']
select_teams = ui.select(teams)
image_object = ui.image('').classes('w-48')
select_button = ui.button('Confirm', on_click= lambda : image_object.set_source( f'{select_teams.value}-File.png'))

# checkbox element + console web communication
# also shows good structure for quick and easy feature implementation
# if you want to remove an image temporarily set image.set_visibility to false and true
ui.button('Save', on_click=lambda :sets())
def sets():
    x = 0
    print('This is MY code')
    if cb_Dwarf.value == True and cb_Jameel.value == True:
        cb_label.set_text('You cant BE BOTH, you must not be perfect')
        x = 1
    if cb_Dwarf.value == False and cb_Jameel.value == False:
        cb_label.set_text('You cant be nothing')
        x = 1
    if cb_Dwarf.value is True and x == 0:
        cb_label.set_text('You are SHORT')
    if cb_Jameel.value is True and x == 0:
        cb_label.set_text('YOU ARE BEAUTIFUL')
cb_Dwarf = ui.checkbox('Dwarf')
cb_Jameel = ui.checkbox('Jameel')
cb_label = ui.label('You are')

# switch elements
switch_dwarf = ui.switch('Dwarf', on_change=lambda: func())
switch_jameel = ui.switch('Jameel', on_change=lambda: func())
switch_image = ui.image('').classes('w-32')
switch_label = ui.label('')
def func():
    x = 1
    if switch_dwarf.value is True and switch_jameel.value is True:
        switch_label.set_text('You cant be perfect ive told u this')
        switch_image.set_source('')
        x = 0
    if switch_dwarf.value is False and switch_jameel.value is False:
        switch_label.set_text('you gotta pick one')
        switch_image.set_source('')
        x = 0
    if switch_dwarf.value is True and x == 1:
        switch_image.set_source('Dwarf-File.png')
    if switch_jameel.value is True and x == 1:
        switch_image.set_source('Jameel-file.png')

# slider
slider = ui.slider(min= 0, max  = 6, on_change= lambda : label_updater()).props('label-always')
label_obj = ui.label(f'slider is at number')
def label_updater():
    label_obj.set_text(f'slider is at number {slider.value}')

# joystick element

joystick = ui.joystick(color='grey', on_move=lambda e:joy_sticky(e), on_end=lambda  e:coordinates.set_text('0,0'))
coordinates = ui.label ('0,0')
def joy_sticky(e):
    coordinates.set_text(f'{e.x:.3f},{e.y:.3f}')
    if e.x > 0 and e.y > 0:
        image.set_source('Dwarf-File.png')
    if e.x < 0 < e.y:
        image.set_source('Jameel-File.png')

# input
file_input = ui.input(label= 'File Name',
                      placeholder= 'Enter a file name',)
button_input = ui.button('Confirm File Name', on_click= lambda : image_input.set_source(f'{file_input.value}.png'))
image_input = ui.image('').classes('w-32')
password_input = ui.input(label= 'Password',
                          placeholder='Enter your password',
                          password= True)

# chatbot
name_input = ui.input(label= 'Name', placeholder= 'write ur name here')
text_area = ui.textarea(label='Message', placeholder=' write ur message here')
button_text = ui.button('Send Message', on_click= lambda: send())
def send():
    ui.chat_message(f'{text_area.value}', name= f'{name_input.value}',
                    avatar= 'https://robohash.org/ui')
    name_input.value = ''
    text_area.value = ''

# calculator
first_num = ui.number('First Number', placeholder= 'place your first number here')
Second_num = ui.number('Second Number', placeholder= 'place your second number here')

add_button = ui.button('+', on_click= lambda: answer.set_text(f'The answer is {first_num.value + Second_num.value}' ))
multi_button = ui.button('X', on_click= lambda: answer.set_text(f'The answer is {first_num.value * Second_num.value}'))
division_button = ui.button('/',on_click= lambda: answer.set_text(f'The answer is {first_num.value / Second_num.value}'))
subtract_button = ui.button('-',on_click= lambda: answer.set_text(f'The answer is {(first_num.value - Second_num.value)}'))
answer = ui.label('')


# knob
knob = ui.knob(0,min= 0, max= 100,on_change= lambda : knob_value(),show_value= True, color= 'gray')


knob_input = ui.input('Knob number',value= '0', on_change= lambda: knob_selector())
def knob_value():
    knob.value = int(knob.value)
    knob_input.set_value(f'{knob.value}')

def knob_selector():
    knob.value = int(knob_input.value)

# color selector
label_color = ui.markdown('***Color Selector***')
color_input = ui.color_input(label= 'Color input', on_change= lambda : label_color.style(f'color:{color_input.value}'))

# date and time input
date = ui.date(value =f'{datetime.datetime.now}')
time = ui.time(value = f'{datetime.datetime.now}')
save_date = ui.label('')
date_button = ui.button('Schedule date', on_click=lambda : schedule())

def schedule():
    save_date.set_text(f'{date.value}, {time.value}')

# text file upload
def uploads(e:events.UploadEventArguments):
    text = e.content.read().decode("utf-8")
    markdown.set_content(text)
ui.upload(on_upload=uploads)
markdown = ui.markdown('Choose a Text file')

# ep 19



ui.run()
