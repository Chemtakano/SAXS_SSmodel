import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plot_module as pm
import matplotlib.pyplot as plt

##plot code

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
    

#data
col_1=[
    [sg.Text('解析するファイル')],
    [sg.FileBrowse('Browse'), sg.InputText(key='filepath')],
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
    [sg.Text('q_min'), sg.Slider(range=(-5, -2), default_value=-2, size=(80, 10), resolution=0.1, orientation='h', key='-SLIDER-q_min-', enable_events=True)],
    [sg.Text('q_max'), sg.Slider(range(1, 3), default_value=1, size=(80, 10), resolution=0.01, orientation='h', key='-SLIDER-q_max-', enable_events=True)],
    [sg.Text('points'), sg.Slider(range=(1000, 100000), default_value=1000, size=(80, 10), resolution=100, orientation='h', key='-SLIDER-points-', enable_events=True)],
    [sg.Text('sigma_resol'), sg.Slider(range=(10, 100), default_value=10, size=(80, 10), resolution=1, orientation='h', key='-SLIDER-sigma_resol-', enable_events=True)]
]

layout=[
    [col_1],
    [col_3],
    [col_2]
]


#sg.theme('Topanga')  
window=sg.Window(
    'SAXS app',
    layout,
    finalize=True,
    auto_size_text=True,
    location=(0,0),
    resizable=True
    )

#canvas
fig = plt.figure(figsize=(3, 3))
ax = fig.add_subplot(111)
def setfig():
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$q$')
    ax.set_ylabel('I($q$)')
    ax.grid(lw=1, c='gray', ls='dotted')
    plt.tight_layout()


fig_agg = draw_figure(window['-CANVAS_data-'].TKCanvas, fig)

while True:
    event, value = window.read()
    if event == None:
        break
    if event=='btn1':
        path=value['filepath']
        setfig()
        ax.scatter(pm.data(path)['q'], pm.data(path)['i'], s=3)
        fig_agg.draw()
    if event=='btn2':
    #event=='-SLIDER-I0-' or event=='-SLIDER-R-' or event=='-SLIDER-sigma-':
        I0=10**float(value['-SLIDER-I0-'])
        R=float(value['-SLIDER-R-'])
        sigma=float(value['-SLIDER-sigma-'])
        q_min=float(value['-SLIDER-q_min-'])
        q_max=float(value['-SLIDER-q_max-'])
        points=int(value['-SLIDER-points-'])
        sigma_resol=int(value['-SLIDER-sigma_resol-'])
        ax.plot(pm.theory_sphere(I0, R, sigma, q_min, q_max, points, sigma_resol)[0], pm.theory_sphere(I0, R, sigma, q_min, q_max, points, sigma_resol)[1], lw=1)
        fig_agg.draw()
    if event=='btn3':
        ax.cla()
        path=value['filepath']
        setfig()
        ax.scatter(pm.data(path)['q'], pm.data(path)['i'], s=3)
        fig_agg.draw()


window.close()