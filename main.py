import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import theo_module as tm
import matplotlib.pyplot as plt


    

#data
col_1=[
    [sg.Text('解析するファイル')],
    [sg.FileBrowse('Browse', file_types=(('csv file', '*.csv'),)), sg.InputText(key='filepath')],
    [sg.Button('データのプロット', key='btn1')],
    [sg.Button('理論のプロット', key='btn2'), sg.Button('理論のプロットのクリア', key='btn3')]
]

col_2=[
    [sg.Canvas(size=(300, 300), key='-CANVAS_data-')]
]

col_3=[
    [sg.Text('I0'), sg.Slider(range=(-10, 10), default_value=0, size=(80, 10), resolution=0.0001, orientation='h', key='-SLIDER-I0-', enable_events=True)],
    [sg.Text('R'), sg.Slider(range=(1, 300), default_value=10, size=(80, 10), resolution=0.1, orientation='h', key='-SLIDER-R-', enable_events=True)],
    [sg.Text('sigma'), sg.Slider(range=(0.01, 100), default_value=0.01, size=(80, 10), resolution=0.01, orientation='h', key='-SLIDER-sigma-', enable_events=True)],
    [sg.Text('q_min'), sg.Slider(range=(-3, -0.5), default_value=-2, size=(80, 10), resolution=0.1, orientation='h', key='-SLIDER-q_min-', enable_events=True)],
    [sg.Text('q_max'), sg.Slider(range=(0, 1.5), default_value=0.5, size=(80, 10), resolution=0.01, orientation='h', key='-SLIDER-q_max-', enable_events=True)],
    [sg.Text('points'), sg.Slider(range=(1000, 100000), default_value=1000, size=(80, 10), resolution=100, orientation='h', key='-SLIDER-points-', enable_events=True)],
    [sg.Text('sigma_resol'), sg.Slider(range=(20, 100), default_value=20, size=(80, 10), resolution=1, orientation='h', key='-SLIDER-sigma_resol-', enable_events=True)],
    [sg.Button('エクスポート', key='btn_export')]
]

layout=[
    [col_1],
    [col_3],
    [col_2]
]


#sg.theme('Topanga')  
window=sg.Window(
    'Solid Sphere Analysis App version 1.0.0',
    layout,
    finalize=True,
    auto_size_text=True,
    location=(0,0),
    resizable=True
    )

#canvas

##plot code

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


fig = plt.figure(figsize=(3, 3))
ax = fig.add_subplot(111)

def setfig():
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$q$')
    ax.set_ylabel('I($q$)')
    ax.set_xlim(10**(-2), 10*1)
    ax.grid(lw=1, c='gray', ls='dotted')
    plt.tight_layout()

def dataplot():
    path=value['filepath']
    setfig()
    ax.scatter(tm.data(path)['q'], tm.data(path)['i'], s=2)
    fig_agg.draw()

def theoryplot():
    I0=10**float(value['-SLIDER-I0-'])
    R=float(value['-SLIDER-R-'])
    sigma=float(value['-SLIDER-sigma-'])
    q_min=float(value['-SLIDER-q_min-'])
    q_max=float(value['-SLIDER-q_max-'])
    points=int(value['-SLIDER-points-'])
    sigma_resol=int(value['-SLIDER-sigma_resol-'])
    ax.plot(tm.theory_sphere(I0, R, sigma, q_min, q_max, points, sigma_resol)[0], tm.theory_sphere(I0, R, sigma, q_min, q_max, points, sigma_resol)[1], lw=1, color='r')
    fig_agg.draw()     

def theorydata():
    I0=10**float(value['-SLIDER-I0-'])
    R=float(value['-SLIDER-R-'])
    sigma=float(value['-SLIDER-sigma-'])
    q_min=float(value['-SLIDER-q_min-'])
    q_max=float(value['-SLIDER-q_max-'])
    points=int(value['-SLIDER-points-'])
    sigma_resol=int(value['-SLIDER-sigma_resol-'])
    params={'I0':I0, 'R':R, 'sigma':sigma}
    return tm.theory_sphere(I0, R, sigma, q_min, q_max, points, sigma_resol), params


fig_agg = draw_figure(window['-CANVAS_data-'].TKCanvas, fig)

while True:
    event, value = window.read()
    if event == None:
        break
    if event=='btn1':
        dataplot()
    if event=='btn2':
        setfig()
        theoryplot()
    if event=='-SLIDER-I0-' or event=='-SLIDER-R-' or event=='-SLIDER-sigma-' or event=='-SLIDER-q_min-'or event=='-SLIDER-q_max-' or event=='-SLIDER-points-' or event=='-SLIDER-sigma_resol-':
        ax.cla()
        dataplot()
        theoryplot()
    if event=='btn3':
        ax.cla()
        setfig()
        sg.popup('データはリセットされました。\t新しいデータを読み込もプロットをしてください。', title='')
    if event=='btn_export':
        s_folder=sg.popup_get_folder('フォルダーを指定してください。')
        s_name=sg.popup_get_text('作成するファイル名を入力してください。')
        tm.export(theorydata()[0],theorydata()[1], s_folder+'/'+s_name)
        
        
window.close()

"""
created by Shin Takano
version 1.0.0 18/10/2022

"""