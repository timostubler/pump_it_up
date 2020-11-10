import schemdraw
import schemdraw.elements as elm



def draw_branch():
    d = schemdraw.Drawing()
    res = d.add(elm.Dot(label='$U_{in}$'))
    d.add(elm.Line)
    d.add(elm.Resistor(label='$R_T$'))
    d.add(elm.Line)
    vel = d.add(elm.Resistor(label='$R_V$'))
    d.add(elm.Line)
    d.add(elm.Capacitor(label='$C_C$'))
    d.add(elm.Line)
    d.add(elm.Dot(label='$U_{Signal}$'))
    d.add(elm.Line(d='down', ls='--'))
    d.add(elm.Line(d='left',tox =vel.end, ls='--'))
    d.add(elm.SourceV(d='left', ls='--', label='$U_{Signal} - U_{in}$'))
    d.add(elm.Line(d='left',tox=res.start, ls='--'))
    d.add(elm.Line(d='up', ls='--'))
    d.draw()

    return d

def draw_circuit():
    d = schemdraw.Drawing()

    line_length = 1

    # Left Side:
    res_in = d.add(elm.Dot(label='$U_{in}$'))
    d.add(elm.Line, l=line_length)
    d.add(elm.Resistor(label='$R_{T_{in}}$'))
    vel_in = d.add(elm.Resistor(label='$R_{V_{in}}$'))
    d.add(elm.Line, l=line_length, label='$I_{in}$')
    center_dot_up = d.add(elm.Dot)
    print('d.here:', d.here)
    d.push()
    d.add(elm.Line,d='down', l=1, label='$I_{C}$')
    chamber = d.add(elm.Capacitor(d='down', label='$C_C$'))
    center_dot_down = d.add(elm.Dot, botlabel='$U_{Signal}$')
    d.add(elm.SourceV(d='left',tox=res_in.start, ls='--', label='$U_{Signal} - U_{in}$'))
    d.add(elm.Line(d='up',l=4, ls='--'))

    # Right Side:
    d.pop()
    d.add(elm.Line,d='right', l=line_length, label='$I_{out}$')
    vel_out = d.add(elm.Resistor(label='$R_{V_{out}}$'))
    d.add(elm.Resistor(label='$R_{T_{out}}$'))
    d.add(elm.Line, l=line_length)
    res_out = d.add(elm.Dot(label='$U_{out}$'))
    d.add(elm.Line(d='down',l=4, ls='--'))
    d.add(elm.SourceV(d='left', tox=chamber.end, ls='--',reverse=True, label='$U_{Signal} - U_{out}$'))
    d.draw()

    return d

def draw_circuit_second():
    d = schemdraw.Drawing()

    line_length = 1

    # Left Side:
    res_in = d.add(elm.Dot(label='$U_{in}$'))
    res_in_line = d.add(elm.Line, l=line_length)
    left_ind = d.add(elm.Inductor(label='$L_{T_{in}}$'))
    left_res = d.add(elm.Resistor(label='$R_{T_{in}}$'))
    d.add(elm.Line(l=1.5, d='down'))
    vel_cap_in = d.add(elm.Capacitor(d='right', botlabel='$C_{V_{in}}$'))
    d.add(elm.Line(l=1.5, d='up'))
    vel_in = d.add(elm.Resistor(d='right',label='$R_{V_{in}}$', at=left_res.end))
    d.add(elm.Line, l=line_length, label='$I_{in}$')
    center_dot_up = d.add(elm.Dot)
    push1 = d.push()
    d.add(elm.Line,d='down', l=line_length, label='$I_{C}$')
    chamber_res = d.add(elm.Resistor(label='$R_{C}$'))
    chamber = d.add(elm.Capacitor(d='down', label='$C_C$'))
    to_bottom_line = d.add(elm.Line, d='down', l=line_length)
    center_dot_down = d.add(elm.Dot, botlabel='$U_{Signal}$')
    left_source = d.add(elm.SourceV(d='left',tox=res_in.start, ls='--', label='$U_{Signal} - U_{in}$'))
    d.add(elm.Line(d='up',toy=res_in_line.start, ls='--'))

    # Right Side:
    pop1 = d.pop()
    center_top_line = d.add(elm.Line,d='right', l=line_length, label='$I_{out}$')
    d.add(elm.Line(l=1.5, d='down'))
    vel_cap_out = d.add(elm.Capacitor(d='right', botlabel='$C_{V_{out}}$'))
    d.add(elm.Line(l=1.5, d='up'))
    vel_out = d.add(elm.Resistor(d='right', label='$R_{V_{out}}$', at = center_top_line.end))
    right_res = d.add(elm.Resistor(label='$R_{T_{out}}$'))
    right_ind = d.add(elm.Inductor(label='$L_{T_{out}}$'))
    res_out_line = d.add(elm.Line, l=line_length)
    res_out = d.add(elm.Dot(label='$U_{out}$'))
    d.add(elm.Line(d='down',toy=to_bottom_line.end, ls='--'))
    right_source = d.add(elm.SourceV(d='left', ls='--',tox=to_bottom_line.end, reverse=True, label='$U_{Signal} - U_{out}$'))

    d.draw()

    return d

def save_drawing(d, filename):
    d.save(f'./circuits/{filename}.svg')


if __name__ == '__main__':
    # d_branch = draw_branch()
    d_circuit = draw_circuit()

    save_drawing(d_circuit, filename='first_order_circuit')