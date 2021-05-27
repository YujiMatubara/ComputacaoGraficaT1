import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math as math

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(720, 600, "transformation", None, None)
glfw.make_context_current(window)

vertex_code = """
        attribute vec2 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,0.0,1.0);
        }
        """

fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

# Request a program and shader slots from GPU
program  = glCreateProgram()
vertex   = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

# Set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# Compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")

glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

# Attach shader objects to the program
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
# Make program the default program
glUseProgram(program)

# preparando espaço para 3 vértices usando 2 coordenadas (x,y)
vertices = np.zeros(36, [("position", np.float32, 2)])

# preenchendo as coordenadas de cada vértice
vertices[0] = [-0.2, -0.3]  #portao
vertices[1] = [-0.2, +1.0]
vertices[2] = [+0.2, -0.3]
vertices[3] = [+0.2, +1.0]

vertices[4] = [-0.2, +0.8]      #risco
vertices[5] = [-0.2, +0.75]
vertices[6] = [+0.2, +0.8]
vertices[7] = [+0.2, +0.75]

vertices[8] = [-0.2, +0.55]     #risco
vertices[9] = [-0.2, +0.50]
vertices[10] = [+0.2, +0.55]
vertices[11] = [+0.2, +0.50]

vertices[12] = [-0.2, +0.3]     #risco
vertices[13] = [-0.2, +0.25]
vertices[14] = [+0.2, +0.3]
vertices[15] = [+0.2, +0.25]

vertices[16] = [-0.2,  0.0]     #risco
vertices[17] = [-0.2, +0.05]
vertices[18] = [+0.2,  0.0]
vertices[19] = [+0.2, +0.05]

vertices[20] = [-0.08, +0.82]   #detalhe azul
vertices[21] = [-0.08, +0.73]
vertices[22] = [+0.08, +0.82]
vertices[23] = [+0.08, +0.73]

vertices[24] = [-0.08, +0.58]    #detalhe azul
vertices[25] = [-0.08, +0.47]
vertices[26] = [+0.08, +0.58]
vertices[27] = [+0.08, +0.47]

vertices[28] = [-0.08, +0.33]   #detalhe azul
vertices[29] = [-0.08, +0.22]
vertices[30] = [+0.08, +0.33]
vertices[31] = [+0.08, +0.22]

vertices[32] = [-0.08, -0.03]   #detalhe azul
vertices[33] = [-0.08, +0.08]
vertices[34] = [+0.08, -0.03]
vertices[35] = [+0.08, +0.08]

# Request a buffer slot from GPU
buffer = glGenBuffers(1)
# Make this buffer the default one
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Upload data
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Bind the position attribute
# --------------------------------------
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)

loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

loc_color = glGetUniformLocation(program, "color")
R = 1.0
G = 0.0
B = 0.0

# tamanho
s_x = 1.0
s_y = 1.0
s_z = 1.0

# rotacao
rad = 0.0
s = math.sin(rad)
c = math.cos(rad)

# translacao
t_x = 0.0
t_y = 0.0
t_z = 0.0
    

def mouse_event(window,button,action,mods):
    print('[mouse event] button =',button)
    print('[mouse event] action =',action)
    print('[mouse event] mods =',mods)
    print('-------')
    global s_x, s_y, s_z
    if button == 0:
        if action == 1:
            s_x += 0.05
            s_y += 0.05
    if button == 1:
        if action == 1:
            s_x -= 0.05
            s_y -= 0.05
    
glfw.set_mouse_button_callback(window,mouse_event)

def key_event(window,key,scancode,action,mods):
    global rad, s, c, t_x, t_y, t_z
    if key == 263:
        rad += 0.05
        if rad >= (2 * math.pi): rad = rad - (2 * math.pi)
        s = math.sin(rad)
        c = math.cos(rad)
    if key == 262:
        rad -= 0.05
        if rad < 0: rad = (2 * math.pi) + rad
        s = math.sin(rad)
        c = math.cos(rad)
    if key == 87: t_y += 0.05 #cima
    if key == 83: t_y -= 0.05 #baixo
    if key == 65: t_x -= 0.05 #esquerda
    if key == 68: t_x += 0.05 #direita
    
glfw.set_key_callback(window,key_event)

glfw.show_window(window)

while not glfw.window_should_close(window):

    glfw.poll_events() 

    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(1.0, 1.0, 1.0, 1.0)    
    
    #Draw Triangle
    mat_transformation = np.array([     s_x * c, -(s_x * s), 0.0, (s_x * c * t_x) - (s_x * s * t_y), 
                                        s_y * s, s_y * s_z, 0.0, (s_y * s * t_x) + (s_y * c * t_y), 
                                        0.0, 0.0, s_z, s_z * t_z, 
                                        0.0, 0.0, 0.0, 1.0], np.float32)
                                    
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transformation)
    
    glUniform4f(loc_color, 0.69, 0.572, 0.423, 1.0)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4) # portao

    glUniform4f(loc_color, 0.0, 0.0, 0.0, 1.0)
    glDrawArrays(GL_TRIANGLE_STRIP, 4, 4) # risco
    glDrawArrays(GL_TRIANGLE_STRIP, 8, 4) # risco
    glDrawArrays(GL_TRIANGLE_STRIP, 12, 4) # risco
    glDrawArrays(GL_TRIANGLE_STRIP, 16, 4) # risco

    glUniform4f(loc_color, 0.737, 0.925, 0.863, 1.0)
    glDrawArrays(GL_TRIANGLE_STRIP, 20, 4) # detalhe azul
    glDrawArrays(GL_TRIANGLE_STRIP, 24, 4) # detalhe azul
    glDrawArrays(GL_TRIANGLE_STRIP, 28, 4) # detalhe azul
    glDrawArrays(GL_TRIANGLE_STRIP, 32, 4) # detalhe azul

    glfw.swap_buffers(window)

glfw.terminate()