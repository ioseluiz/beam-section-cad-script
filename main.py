from drawing import Drawing

def main():
    rebar_data = [
        {
            'id': 1,
            'rebar_id': '#5',
            'coor_x': 50,
            'coor_y': 50
        },
        {
            'id': 2,
            'rebar_id': '#5',
            'coor_x': 50,
            'coor_y': 650
        },
        {
            'id': 3,
            'rebar_id': '#5',
            'coor_x': 250,
            'coor_y': 650
        },
        {
            'id': 4,
            'rebar_id': '#5',
            'coor_x': 250,
            'coor_y': 50
        },
    ]
    beam = Drawing(300, 700, rebar_data, '#3')
    
    

if __name__  == '__main__':
    main()